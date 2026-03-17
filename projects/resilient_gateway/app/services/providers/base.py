from abc import ABC, abstractmethod
from packages.core.models.ai import LLMRequest, LLMResponse

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers (Azure, OpenAI, Mock, etc.)"""
    
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
