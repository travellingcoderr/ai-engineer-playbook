import os
from typing import Any, Union
from langchain_core.embeddings import Embeddings
from packages.core.enums import VectorStoreProvider
from packages.core.config import (
    get_config,
    BaseVectorStoreConfig
)

class VectorStoreFactory:
    """
    Factory to instantiate vector stores based on configuration.
    """
    @staticmethod
    def create_vector_store(
        embeddings: Embeddings,
        config: Union[BaseVectorStoreConfig, dict, Any] = None,
        **kwargs: Any
    ):
        """
        Creates a vector store instance. 
        Args:
            embeddings: The embedding model to use.
            config: A configuration object (BaseVectorStoreConfig or subclass) or a dictionary.
            **kwargs: Fallback parameters for older implementations.
        """
        # 1. Resolve configuration from global settings if not provided
        if config is None:
            try:
                settings = get_config()
                # AppConfig holds VectorStoreConfiguration by default
                config = getattr(settings, "vector_store", None)
            except Exception:
                config = None

        # 2. Extract provider and collection name
        provider = None
        collection_name = None

        if isinstance(config, BaseVectorStoreConfig):
            provider = config.provider
            collection_name = config.collection_name
        elif isinstance(config, dict):
            provider = config.get("provider")
            collection_name = config.get("collection_name")
        elif config is not None:
            # Handle case where it's a legacy VectorStoreConfiguration object which might not inherit from BaseVectorStoreConfig
            provider = getattr(config, "provider", None)
            collection_name = getattr(config, "collection_name", None)

        # Fallback to kwargs or environment if still missing
        provider = provider or kwargs.get("provider") or os.getenv("VECTOR_STORE_PROVIDER", "chroma")
        collection_name = "knowledge"

        # Normalize provider
        if isinstance(provider, str):
            provider = provider.lower().strip()

        # 3. Instantiate based on provider
        if provider == VectorStoreProvider.PGVECTOR:
            from langchain_postgres import PGVector
            connection = kwargs.get("connection") or getattr(config, "connection_string", None) or os.getenv("DATABASE_URL")
            if not connection:
                raise ValueError("PGVector requires a connection string (connection_string or DATABASE_URL).")
            return PGVector(
                embeddings=embeddings,
                collection_name=collection_name,
                connection=connection,
                use_jsonb=True,
            )
            
        elif provider == VectorStoreProvider.PINECONE:
            from langchain_pinecone import PineconeVectorStore
            # Pinecone specific config fields
            api_key = kwargs.get("api_key") or getattr(config, "api_key", None)
            if api_key:
                os.environ["PINECONE_API_KEY"] = api_key
            return PineconeVectorStore(
                embedding=embeddings,
                index_name=collection_name
            )
            
        elif provider == VectorStoreProvider.QDRANT:
            from langchain_qdrant import QdrantVectorStore
            host = kwargs.get("host") or getattr(config, "host", "localhost")
            port = kwargs.get("port") or getattr(config, "port", 6333)
            return QdrantVectorStore.from_existing_collection(
                embedding=embeddings,
                collection_name=collection_name,
                url=f"http://{host}:{port}"
            )
            
        elif provider == VectorStoreProvider.CHROMA:
            from langchain_chroma import Chroma
            # Chroma usually handles its own client connection if passed a client, 
            # here we assume a basic setup for now.
            return Chroma(
                collection_name=collection_name,
                embedding_function=embeddings
            )
        else:
            raise ValueError(f"Unsupported Vector Store provider: {provider}")
