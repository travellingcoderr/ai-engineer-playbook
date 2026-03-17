import time
import uuid
import random
from .base import BaseLLMProvider
from packages.core.models.ai import LLMRequest, LLMResponse

class MockAzureProvider(BaseLLMProvider):
    """
    A provider that simulates Azure OpenAI behavior including 
    regional identifiers and occasional rate limiting.
    """
    
    def __init__(self, region: str = "eastus", failure_rate: float = 0.0):
        self.region = region
        self.failure_rate = failure_rate

    def get_name(self) -> str:
        return f"mock-azure-{self.region}"

    async def complete(self, request: LLMRequest) -> LLMResponse:
        # Simulate network latency
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate regional failures for testing resiliency
        if random.random() < self.failure_rate:
            raise Exception(f"Simulated Azure Region Failure: {self.region} is overloaded (429)")

        return LLMResponse(
            id=f"mock-res-{uuid.uuid4().hex[:8]}",
            text=f"[Simulated response from Azure {self.region}] You asked: {request.prompt}",
            model=request.model,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            provider="Azure (Mock)",
            region=self.region,
            cached=False
        )
