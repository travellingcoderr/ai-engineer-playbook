from fastapi import APIRouter, HTTPException

from ..crewai import run_mortgage_issue_triage_crew
from packages.core.enums.observability import LogLevel
from packages.core.services.observability import ObservabilityClient

router = APIRouter()
obs_client = ObservabilityClient(service_name="mortgage_bot_backend")


@router.get("/triage")
async def run_crew_triage(query: str):
    try:
        result = run_mortgage_issue_triage_crew(query)
        obs_client.log(
            f"/api/crew/triage completed for query='{query}'",
            level=LogLevel.INFO,
        )
        return result
    except ImportError as exc:
        obs_client.log(
            "CrewAI dependency is missing while calling /api/crew/triage",
            level=LogLevel.ERROR,
        )
        raise HTTPException(
            status_code=500,
            detail="CrewAI is not installed in the backend environment.",
        ) from exc
    except Exception as exc:
        obs_client.log(
            f"/api/crew/triage failed with {exc.__class__.__name__}",
            level=LogLevel.ERROR,
        )
        raise HTTPException(
            status_code=500,
            detail="CrewAI triage failed.",
        ) from exc
