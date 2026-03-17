import asyncio
from typing import List
from app.models.gateway_models import LLMRequest, LLMResponse
from app.services.providers.base import BaseLLMProvider
from app.services.router import ResilientRouter

class SimpleMockProvider(BaseLLMProvider):
    def __init__(self, name: str):
        self.name = name
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            id="test-id",
            text=f"Response from {self.name}", 
            model=request.model, 
            provider=self.name,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )
    
    def get_name(self) -> str:
        return self.name

async def test_round_robin():
    providers = [
        SimpleMockProvider("Provider-A"),
        SimpleMockProvider("Provider-B"),
        SimpleMockProvider("Provider-C")
    ]
    router = ResilientRouter(providers)
    request = LLMRequest(prompt="test", model="test-model")
    
    print("--- Starting Round Robin Test ---")
    for i in range(5):
        resp = await router.route_request_round_robin(request)
        print(f"Request {i+1}: Got {resp.provider}")

if __name__ == "__main__":
    asyncio.run(test_round_robin())
