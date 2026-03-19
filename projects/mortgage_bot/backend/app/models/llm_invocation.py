from datetime import datetime
import uuid

from sqlmodel import Field, SQLModel


class LLMInvocationBase(SQLModel):
    trace_id: str
    request_id: str
    feature: str
    workflow_type: str
    step_name: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    success: bool = True


class LLMInvocation(LLMInvocationBase, table=True):
    __tablename__ = "llm_invocations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
