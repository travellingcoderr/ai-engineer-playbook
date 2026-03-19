import re

from ..mcp.get_loan_details import get_loan_details
from ..mcp.get_milestone_history import get_milestone_history
from ..mcp.list_loan_conditions import list_loan_conditions
from ..mcp.search_knowledge import search_knowledge
from packages.core.enums.observability import LogLevel
from packages.core.services import reset_llm_instrumentation_context, set_llm_instrumentation_context
from packages.core.services.observability import ObservabilityClient
from .agents import create_mortgage_triage_agents
from .tasks import create_mortgage_triage_tasks

obs_client = ObservabilityClient(service_name="mortgage_bot_backend")


def extract_loan_id(query: str) -> str | None:
    loan_match = re.search(r"\bLN-\d+\b", query, re.IGNORECASE)
    return loan_match.group(0).upper() if loan_match else None


def gather_mortgage_context(query: str) -> dict:
    loan_id = extract_loan_id(query)

    context_bundle = {
        "loan_id": loan_id,
        "loan_details": None,
        "loan_conditions": None,
        "milestone_history": None,
        "knowledge_context": search_knowledge.invoke({"query": query}),
    }

    if loan_id:
        context_bundle["loan_details"] = get_loan_details.invoke({"loan_id": loan_id})
        context_bundle["loan_conditions"] = list_loan_conditions.invoke({"loan_id": loan_id})
        context_bundle["milestone_history"] = get_milestone_history.invoke({"loan_id": loan_id})

    return context_bundle


def run_mortgage_issue_triage_crew(query: str) -> dict:
    from crewai import Crew, Process

    obs_client.log(
        f"CrewAI triage started for query='{query}'",
        level=LogLevel.INFO,
    )

    context_bundle = gather_mortgage_context(query)
    agents = create_mortgage_triage_agents()
    tasks = create_mortgage_triage_tasks(agents, query, context_bundle)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    context_token = set_llm_instrumentation_context(
        feature="knowledge_search",
        workflow_type="crewai",
        step_name="crew_kickoff",
    )
    try:
        result = crew.kickoff()
    finally:
        reset_llm_instrumentation_context(context_token)

    obs_client.log(
        f"CrewAI triage completed for query='{query}'",
        level=LogLevel.INFO,
    )
    return {
        "query": query,
        "loan_id": context_bundle["loan_id"],
        "context_bundle": context_bundle,
        "crew_result": str(result),
    }
