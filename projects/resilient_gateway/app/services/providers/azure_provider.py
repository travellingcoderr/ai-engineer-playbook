import logging
from typing import Optional
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from app.models.gateway_models import LLMRequest, LLMResponse
from app.services.providers.base import BaseLLMProvider

logger = logging.getLogger("azure-provider")

class AzureOpenAIProvider(BaseLLMProvider):
    """
    Production Azure OpenAI provider implementation using LangChain (LCEL).
    """
    
    def __init__(
        self, 
        name: str,
        api_key: str,
        azure_endpoint: str,
        api_version: str = "2024-02-15-preview",
        deployment_name: Optional[str] = None
    ):
        self.name = name
        self.deployment_name = deployment_name
        
        self.llm = AzureChatOpenAI(
            azure_deployment=deployment_name,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            validate_base_url=False
        )

    async def complete(self, request: LLMRequest) -> LLMResponse:
        try:
            # Simple LCEL-style invocation via ainvoke
            # Since we're wrapping it in our standard interface, we don't build a complex chain here
            # but the underlying provider is now fully LangChain compatible.
            
            response = await self.llm.ainvoke(
                [HumanMessage(content=request.prompt)],
                config={
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                    "stop": request.stop
                }
            )
            
            # Extract usage metadata if available
            metadata = response.response_metadata
            usage = metadata.get("token_usage", {})
            
            return LLMResponse(
                id=str(metadata.get("id", "langchain-id")),
                text=response.content,
                model=response.response_metadata.get("model_name", request.model),
                usage={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                },
                provider=self.name,
                region=self.name.split("-")[-1] if "-" in self.name else None
            )
            
        except Exception as e:
            logger.error(f"Azure LCEL Provider {self.name} failure: {str(e)}")
            raise e

    def get_name(self) -> str:
        return self.name
