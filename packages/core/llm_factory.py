import os
from typing import List
from langchain_core.language_models.chat_models import BaseChatModel
from .config import get_config

class LLMFactory:
    """
    Global Factory class to instantiate the correct LLM based on configuration.
    """
    @staticmethod
    def create_llm(provider: str = None, model_name: str = None, **kwargs) -> BaseChatModel:
        """
        Creates and returns a LangChain BaseChatModel instance using the global config settings.
        Fallback arguments ensure backwards compatibility with older legacy projects.
        """
        try:
            settings = get_config()
        except:
            settings = None
            
        provider = provider or (settings.llm_provider if settings else "openai")
        provider = provider.lower().strip() if provider else "openai"
        
        model_name = model_name or (settings.openai_model if settings else "gpt-4o")
        
        if provider == "openai":
            key = kwargs.get("openai_api_key") or (settings.openai_api_key if settings else None)
            base_url = kwargs.get("openai_api_base") or (settings.openai_api_base if settings else None)
            return LLMFactory._create_openai(model_name, key, base_url)
        elif provider == "gemini":
            key = kwargs.get("gemini_api_key") or (settings.gemini_api_key if settings else None)
            return LLMFactory._create_gemini(model_name, key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def _create_openai(model_name: str, api_key: str | None, base_url: str | None = None) -> BaseChatModel:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("Please install langchain-openai to use the OpenAI provider.")
            
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key is missing. Set it in .env or config.")
            
        return ChatOpenAI(model=model_name, api_key=key, base_url=base_url, temperature=0.0)

    @staticmethod
    def _create_gemini(model_name: str, api_key: str | None) -> BaseChatModel:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise ImportError("Please install langchain-google-genai to use the Gemini provider.")
            
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("Gemini API key is missing.")
            
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=key, temperature=0.0)
