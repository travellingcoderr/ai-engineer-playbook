from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from packages.core.enums import GatewayMode, RoutingStrategy
from packages.core.models.ai import LLMRequest, LLMResponse

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
