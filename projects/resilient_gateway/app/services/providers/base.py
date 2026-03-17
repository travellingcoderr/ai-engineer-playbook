from abc import ABC, abstractmethod
from app.models.gateway_models import LLMRequest, LLMResponse

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers (Azure, OpenAI, Mock, etc.)"""
    
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
