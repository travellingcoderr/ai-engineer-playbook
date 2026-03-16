from pydantic import BaseModel
from typing import List, Optional

class GuardRequest(BaseModel):
    text: str
    checks: List[str] = ["pii", "injection", "secrets", "toxicity"]

class GuardResponse(BaseModel):
    safe: bool
    action: str  # e.g., "allowed", "redacted", "blocked"
    filtered_text: str
    findings: List[str]
    latency_ms: Optional[float] = None
