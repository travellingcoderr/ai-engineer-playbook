from pydantic import BaseModel
from typing import List, Optional
from packages.core.enums import GuardAction, GuardCheckType

class GuardRequest(BaseModel):
    text: str
    checks: List[GuardCheckType] = [
        GuardCheckType.PII, 
        GuardCheckType.INJECTION, 
        GuardCheckType.SECRETS, 
        GuardCheckType.TOXICITY
    ]

class GuardResponse(BaseModel):
    safe: bool
    action: GuardAction
    filtered_text: str
    findings: List[str]
    latency_ms: Optional[float] = None
