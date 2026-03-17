import os
from langchain_core.embeddings import Embeddings
from packages.core.enums import EmbeddingProvider

class EmbeddingFactory:
    """
    Factory class to instantiate the correct Embedding model based on configuration.
    """
    
    @staticmethod
    def create_embeddings(provider: EmbeddingProvider, model_name: str, **kwargs) -> Embeddings:
        """
        Creates and returns a LangChain Embeddings instance.
        
        Args:
            provider: The name of the embedding provider ('openai', 'huggingface')
            model_name: The specific model to use (e.g., 'text-embedding-3-small')
            **kwargs: Extra arguments like api_keys.
        """
        if provider == EmbeddingProvider.OPENAI:
            return EmbeddingFactory._create_openai(model_name, kwargs.get("openai_api_key"))
            
        elif provider == EmbeddingProvider.HUGGINGFACE:
            return EmbeddingFactory._create_huggingface(model_name)
            
        else:
            raise ValueError(f"Unsupported Embedding provider: {provider}")

    @staticmethod
    def _create_openai(model_name: str, api_key: str | None) -> Embeddings:
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            raise ImportError("Please install langchain-openai to use the OpenAI provider.")
            
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API key is missing. Set it in .env or config.")
            
        return OpenAIEmbeddings(model=model_name, api_key=key)

    @staticmethod
    def _create_huggingface(model_name: str) -> Embeddings:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
        except ImportError:
            raise ImportError("Please install langchain-community and sentence-transformers for HuggingFace embeddings.")
            
        return HuggingFaceEmbeddings(model_name=model_name)
