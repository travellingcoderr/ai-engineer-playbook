from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from packages.core.enums import GatewayMode, RoutingStrategy

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000
    stop: Optional[List[str]] = None

class LLMResponse(BaseModel):
    id: str
    text: str
    model: str
    usage: Dict[str, int]
    provider: str
    region: Optional[str] = None
    cached: bool = False

class ProviderConfig(BaseModel):
    name: str
    priority: int = 1
    weight: int = 100
    enabled: bool = True
    settings: Dict[str, Any] = {}

class GatewayConfig(BaseModel):
    mode: GatewayMode = GatewayMode.SIMULATION # simulation or production
    strategy: RoutingStrategy = RoutingStrategy.PRIORITY # priority, random, weighted
    providers: List[ProviderConfig] = []
