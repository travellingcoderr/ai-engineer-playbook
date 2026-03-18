from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from ..database import get_session
from ..models.knowledge import KnowledgeDocument
from packages.core.services.rag.rag_service import RAGService
import uuid
from redis import Redis
from rq import Queue
import os
from packages.core.services.observability import ObservabilityClient
from packages.core.enums.observability import LogLevel

router = APIRouter()
redis_conn = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
q = Queue(connection=redis_conn)
obs_client = ObservabilityClient(service_name="mortgage_bot_backend")

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
    q.enqueue(
        "tasks.ingestion.process_document",
        doc_id=str(doc_id),
        blob_uri=file_path,
        metadata={"title": title}
    )
    
    obs_client.log(f"Document {doc_id} queued for processing", level=LogLevel.INFO)
    
    return {"doc_id": str(doc_id), "status": "queued"}

@router.get("/search")
async def search_knowledge(query: str):
    connection_string = os.getenv("DATABASE_URL")
    rag_service = RAGService(connection_string=connection_string, collection_name="knowledge")
    
    results = rag_service.search(query, k=5)
    
    return {
        "query": query, 
        "results": [
            {"content": r.page_content, "metadata": r.metadata} 
            for r in results
        ]
    }
