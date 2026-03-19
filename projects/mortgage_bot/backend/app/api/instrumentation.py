from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..data.llm_invocation_repository import LLMInvocationRepository
from ..database import get_session

router = APIRouter()


def get_llm_invocation_repository(
    session: Session = Depends(get_session),
) -> LLMInvocationRepository:
    return LLMInvocationRepository(session)


@router.get("/summary")
async def get_instrumentation_summary(
    repository: LLMInvocationRepository = Depends(get_llm_invocation_repository),
):
    return repository.summary()


@router.get("/events")
async def get_instrumentation_events(
    limit: int = 100,
    repository: LLMInvocationRepository = Depends(get_llm_invocation_repository),
):
    return repository.list_recent(limit=limit)
