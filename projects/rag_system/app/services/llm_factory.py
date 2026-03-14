import os
from langchain_core.language_models.chat_models import BaseChatModel

# We will import these conditionally to avoid crashing if a package isn't installed
# but the user isn't using that provider anyway.

class LLMFactory:
    """
    Factory class to instantiate the correct LLM based on configuration.
    """
    
    @staticmethod
    def create_llm(provider: str, model_name: str, **kwargs) -> BaseChatModel:
        """
        Creates and returns a LangChain BaseChatModel instance.
        
        Args:
            provider: The name of the LLM provider ('openai', 'gemini', 'anthropic', etc.)
            model_name: The specific model to use (e.g., 'gpt-4o', 'gemini-1.5-pro')
            **kwargs: Extra arguments like api_keys passed from the configuration.
        """
        provider = provider.lower().strip()
        
        if provider == "openai":
            return LLMFactory._create_openai(model_name, kwargs.get("openai_api_key"))
            
        elif provider == "gemini":
            return LLMFactory._create_gemini(model_name, kwargs.get("gemini_api_key"))
            
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def _create_openai(model_name: str, api_key: str | None) -> BaseChatModel:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("Please install langchain-openai to use the OpenAI provider.")
            
        # Fallback to env var if not in config explicitly
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key is missing. Set it in .env or config.")
            
        return ChatOpenAI(model=model_name, api_key=key, temperature=0.0)

    @staticmethod
    def _create_gemini(model_name: str, api_key: str | None) -> BaseChatModel:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise ImportError("Please install langchain-google-genai to use the Gemini provider.")
            
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("Gemini API key is missing. Set it in .env or config.")
            
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=key, temperature=0.0)
