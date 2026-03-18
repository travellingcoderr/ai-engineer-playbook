from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from packages.core.enums import AIModel, LLMProvider

class LLMRequest(BaseModel):
    prompt: str
    model: AIModel = AIModel.GPT_4O
    temperature: float = 0.7
    max_tokens: int = 1000
    stop: Optional[List[str]] = None

class LLMResponse(BaseModel):
    id: str
    text: str
    model: AIModel
    usage: Dict[str, int]
    provider: LLMProvider
    region: Optional[str] = None
    cached: bool = False
