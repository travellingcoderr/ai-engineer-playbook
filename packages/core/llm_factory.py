import os
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
        except Exception:
            settings = None

        llm_settings = getattr(settings, "llm", None) if settings else None

        # Support both the current nested config schema and older flat attributes.
        provider = provider or (
            getattr(llm_settings, "provider", None)
            or getattr(settings, "llm_provider", None)
            or "openai"
        )
        provider = provider.lower().strip() if provider else "openai"

        model_name = model_name or (
            getattr(llm_settings, "model", None)
            or getattr(settings, "openai_model", None)
            or "gpt-4o"
        )
        
        if provider == "openai":
            key = kwargs.get("openai_api_key") or (
                getattr(llm_settings, "openai_api_key", None)
                or getattr(settings, "openai_api_key", None)
            )
            base_url = kwargs.get("openai_api_base") or (
                getattr(llm_settings, "openai_api_base", None)
                or getattr(settings, "openai_api_base", None)
            )
            return LLMFactory._create_openai(model_name, key, base_url)
        elif provider == "gemini":
            key = kwargs.get("gemini_api_key") or (
                getattr(llm_settings, "gemini_api_key", None)
                or getattr(settings, "gemini_api_key", None)
            )
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
