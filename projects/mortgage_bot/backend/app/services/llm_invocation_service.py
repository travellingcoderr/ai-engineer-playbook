from sqlmodel import Session

from ..data.llm_invocation_repository import LLMInvocationRepository
from ..database import engine


def record_llm_invocation(payload: dict) -> None:
    with Session(engine) as session:
        repository = LLMInvocationRepository(session)
        repository.create(payload)
