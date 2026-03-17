from typing import List, Optional
from packages.core.models.ai import LLMRequest, LLMResponse
from app.services.providers.base import BaseLLMProvider
from packages.core.enums import RoutingStrategy

class ResilientRouter:
    """
    Routes LLM requests across multiple providers with failover and 
    resiliency logic.
    """
    
    def __init__(self, providers: List[BaseLLMProvider], strategy: RoutingStrategy = RoutingStrategy.PRIORITY):
        self.providers = providers
        self.strategy = strategy
        self._current_index = 0

    async def route_request(self, request: LLMRequest) -> LLMResponse:
        """Dispatches to the configured routing strategy."""
        if self.strategy == RoutingStrategy.ROUND_ROBIN:
            return await self.route_request_round_robin(request)
        
        # Default to Priority
        return await self.route_request_priority(request)

    async def route_request_priority(self, request: LLMRequest) -> LLMResponse:
        """Priority-based failover (Always starts with the first provider)."""
        last_exception = None
        
        for provider in self.providers:
            try:
                print(f"DEBUG: Attempting priority request with provider: {provider.get_name()}")
                return await provider.complete(request)
            except Exception as e:
                print(f"WARNING: Provider {provider.get_name()} failed: {str(e)}")
                last_exception = e
                continue
        
        raise Exception(f"All providers failed in Priority mode. Last error: {str(last_exception)}")

    async def route_request_round_robin(self, request: LLMRequest) -> LLMResponse:
        """Round-robin routing with failover support."""
        if not self.providers:
            raise Exception("No providers configured")

        last_exception = None
        num_providers = len(self.providers)
        
        # Determine starting point based on current index
        start_idx = self._current_index
        # Increment index for the next request
        self._current_index = (self._current_index + 1) % num_providers
        
        # Try all providers starting from start_idx
        for i in range(num_providers):
            current_provider_idx = (start_idx + i) % num_providers
            provider = self.providers[current_provider_idx]
            
            try:
                print(f"DEBUG [RR]: Attempting request with provider: {provider.get_name()}")
                return await provider.complete(request)
            except Exception as e:
                print(f"WARNING [RR]: Provider {provider.get_name()} failed: {str(e)}")
                last_exception = e
                continue
                
        raise Exception(f"All providers failed in Round Robin. Last error: {str(last_exception)}")
