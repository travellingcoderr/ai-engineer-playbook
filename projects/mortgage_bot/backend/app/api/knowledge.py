from fastapi import APIRouter, UploadFile, File, Depends
from functools import lru_cache
import re
from sqlalchemy import or_
from sqlmodel import Session, select
from langchain_core.messages import AIMessage, HumanMessage
from ..database import engine, get_session
from ..data.worker_job_repository import WorkerJobRepository
from ..langgraph.agent import create_mortgage_bot_agent
from ..models.knowledge import KnowledgeDocument
from ..models.ticket import Ticket
from packages.core.services.rag.rag_service import RAGService
import uuid
from redis import Redis
from rq import Queue
import os
from packages.core.services.observability import ObservabilityClient
from packages.core.services import reset_llm_instrumentation_context, set_llm_instrumentation_context
from packages.core.enums.observability import LogLevel

router = APIRouter()
redis_conn = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
q = Queue(connection=redis_conn)
obs_client = ObservabilityClient(service_name="mortgage_bot_backend")


@lru_cache(maxsize=1)
def get_mortgage_bot_agent():
    return create_mortgage_bot_agent()


def _build_search_results(query: str, session: Session) -> list[dict]:
    obs_client.log(
        f"Building search results for query='{query}'",
        level=LogLevel.INFO,
    )
    connection_string = os.getenv("DATABASE_URL")
    context_token = set_llm_instrumentation_context(
        feature="knowledge_search",
        workflow_type="rag_search",
        step_name="embedding_lookup",
    )
    try:
        rag_service = RAGService(connection_string=connection_string, collection_name="knowledge")
        knowledge_results = rag_service.search(query, k=5)
    finally:
        reset_llm_instrumentation_context(context_token)

    ticket_pattern = f"%{query.strip()}%"
    ticket_statement = (
        select(Ticket)
        .where(
            or_(
                Ticket.subject.ilike(ticket_pattern),
                Ticket.description.ilike(ticket_pattern),
                Ticket.category.ilike(ticket_pattern),
                Ticket.user_name.ilike(ticket_pattern),
                Ticket.loan_id.ilike(ticket_pattern),
            )
        )
        .order_by(Ticket.created_at.desc())
        .limit(5)
    )
    ticket_results = session.exec(ticket_statement).all()

    obs_client.log(
        f"Search query='{query}' returned {len(knowledge_results)} knowledge matches and {len(ticket_results)} ticket matches",
        level=LogLevel.INFO,
    )

    return [
        {
            "type": "knowledge",
            "title": r.metadata.get("title") or r.metadata.get("document_title") or "Knowledge Document",
            "content": r.page_content,
            "metadata": r.metadata,
        }
        for r in knowledge_results
    ] + [
        {
            "type": "ticket",
            "title": ticket.subject,
            "content": ticket.description,
            "metadata": {
                "ticket_id": str(ticket.id),
                "status": ticket.status,
                "severity": ticket.severity,
                "category": ticket.category,
                "user_name": ticket.user_name,
                "loan_id": ticket.loan_id,
            },
        }
        for ticket in ticket_results
    ]


def _build_help_message(results: list[dict]) -> str:
    if not results:
        return "No close matches were found. Create a support ticket so the team can investigate the issue directly."

    top_result = results[0]
    if top_result["type"] == "knowledge":
        return (
            f"The best match is the document '{top_result['title']}'. "
            "Review it first because it looks like the closest guidance for this issue."
        )

    return (
        f"The closest existing issue is '{top_result['title']}'. "
        "Review the similar ticket details first before creating a new support request."
    )


def _extract_loan_id(query: str) -> str:
    loan_match = re.search(r"\bLN-\d+\b", query, re.IGNORECASE)
    return loan_match.group(0).upper() if loan_match else ""


def _run_agent_query(query: str) -> dict:
    agent = get_mortgage_bot_agent()
    loan_id = _extract_loan_id(query)
    context_token = set_llm_instrumentation_context(
        feature="knowledge_search",
        workflow_type="langgraph",
        step_name="agent_reasoning",
    )
    try:
        agent_result = agent.invoke(
            {
                "messages": [HumanMessage(content=query)],
                "loan_id": loan_id,
                "context": {},
            }
        )
    finally:
        reset_llm_instrumentation_context(context_token)
    messages = agent_result.get("messages", [])
    ai_messages = [message for message in messages if isinstance(message, AIMessage)]
    final_answer = ""
    used_tools: list[str] = []

    for message in ai_messages:
        if getattr(message, "tool_calls", None):
            used_tools.extend(
                tool_call.get("name", "unknown_tool")
                for tool_call in message.tool_calls
            )
        if isinstance(message.content, str) and message.content.strip():
            final_answer = message.content

    with Session(engine) as session:
        related_results = _build_search_results(query, session)[:3]

    return {
        "query": query,
        "answer": final_answer,
        "used_tools": used_tools,
        "loan_id": loan_id or None,
        "related_results": related_results,
    }

@router.post("/upload")
async def upload_document(
    title: str,
    description: str = None,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1. Save file to shared volume
    file_path = f"/app/uploads/{file.filename}"
    import shutil
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    obs_client.log(f"File saved to {file_path}", level=LogLevel.INFO)

    # 2. Create document record in Postgres
    doc_id = uuid.uuid4()
    doc = KnowledgeDocument(
        id=doc_id,
        title=title,
        description=description,
        source_type="upload",
        blob_uri=file_path,
        mime_type=file.content_type,
        hash=str(uuid.uuid4()), # Placeholder for actual file hash
        status="processing"
    )
    session.add(doc)
    session.commit()
    
    # 3. Enqueue background task
    job = q.enqueue(
        "tasks.ingestion.process_document",
        doc_id=str(doc_id),
        blob_uri=file_path,
        metadata={"title": title}
    )
    WorkerJobRepository(session).create_job(
        job_id=job.id,
        queue_name=q.name,
        task_name="tasks.ingestion.process_document",
        document_id=str(doc_id),
        payload={"blob_uri": file_path, "metadata": {"title": title}},
    )
    
    obs_client.log(f"Document {doc_id} queued for processing as job {job.id}", level=LogLevel.INFO)
    
    return {"doc_id": str(doc_id), "status": "queued", "job_id": job.id}

@router.get("/search")
async def search_knowledge(query: str, session: Session = Depends(get_session)):
    obs_client.log(
        f"/api/knowledge/search called with query='{query}'",
        level=LogLevel.INFO,
    )
    results = _build_search_results(query, session)

    return {
        "query": query,
        "results": results,
    }


@router.get("/assist")
async def assist_with_issue(
    issue: str,
    subject: str | None = None,
    category: str | None = None,
    loan_id: str | None = None,
    session: Session = Depends(get_session),
):
    query_parts = [subject, issue, category, loan_id]
    enriched_query = " ".join(part.strip() for part in query_parts if part and part.strip())
    obs_client.log(
        f"/api/knowledge/assist called with enriched_query='{enriched_query}'",
        level=LogLevel.INFO,
    )
    results = _build_search_results(enriched_query, session)

    return {
        "query": enriched_query,
        "message": _build_help_message(results),
        "recommended_result": results[0] if results else None,
        "related_results": results[:3],
        "has_match": bool(results),
    }


@router.get("/agent-assist")
async def agent_assist_with_issue(
    issue: str,
    subject: str | None = None,
    category: str | None = None,
    loan_id: str | None = None,
):
    query_parts = [subject, issue, category, loan_id]
    enriched_query = " ".join(part.strip() for part in query_parts if part and part.strip())
    obs_client.log(
        f"/api/knowledge/agent-assist called with enriched_query='{enriched_query}'",
        level=LogLevel.INFO,
    )
    agent_output = _run_agent_query(enriched_query)

    return {
        "query": enriched_query,
        "message": agent_output["answer"]
        or "No close matches were found. Create a support ticket so the team can investigate the issue directly.",
        "recommended_result": agent_output["related_results"][0] if agent_output["related_results"] else None,
        "related_results": agent_output["related_results"],
        "used_tools": agent_output["used_tools"],
        "has_match": bool(agent_output["answer"] or agent_output["related_results"]),
    }


@router.get("/agent-search")
async def agent_search(query: str):
    obs_client.log(
        f"/api/knowledge/agent-search called with query='{query}'",
        level=LogLevel.INFO,
    )

    return _run_agent_query(query)
