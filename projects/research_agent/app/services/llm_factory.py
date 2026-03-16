import os
from langchain_core.language_models.chat_models import BaseChatModel

class LLMFactory:
    """
    Factory class to instantiate the correct LLM based on configuration.
    Currently hardcoded for the Research Agent to use OpenAI, but easily extensible.
    """
    
    @staticmethod
    def create_llm(provider: str, model_name: str, **kwargs) -> BaseChatModel:
        provider = provider.lower().strip()
        
        if provider == "openai":
            return LLMFactory._create_openai(model_name, kwargs.get("openai_api_key"))
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def _create_openai(model_name: str, api_key: str | None) -> BaseChatModel:
        from langchain_openai import ChatOpenAI
            
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key is missing. Set it in .env or config.")
            
        return ChatOpenAI(model=model_name, api_key=key, temperature=0.0)
