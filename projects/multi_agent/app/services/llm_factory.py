from packages.core.config import get_config
from langchain_openai import ChatOpenAI

class LLMFactory:
    """
    Standardizes the instantiation of the main LLM across the entire Multi-Agent project.
    By depending on the `packages.core.config`, we avoid duplicating environment parsers.
    """
    
    @staticmethod
    def create_llm():
        settings = get_config()
        
        # Standard configuration pattern identical to the RAG system
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
            temperature=0  # For coding/research orchestration, temperature 0 is best
        )
