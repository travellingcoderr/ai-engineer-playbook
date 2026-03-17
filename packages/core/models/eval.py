from pydantic import BaseModel
from typing import Optional, Dict, Any
from packages.core.enums import AIModel

class CostEvalInput(BaseModel):
    model: AIModel
    input_tokens: int = 0
    output_tokens: int = 0
    provider_metadata: Dict[str, Any] = {}

class AccuracyEvalInput(BaseModel):
    query: str
    response: str
    reference: Optional[str] = None
    model: AIModel = AIModel.GPT_4O
