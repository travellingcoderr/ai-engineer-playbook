from typing import Optional, Literal
from pydantic import Field, BaseModel
from packages.core.enums import VectorStoreProvider

class BaseVectorStoreConfig(BaseModel):
    """Base configuration for any vector store provider."""
    provider: VectorStoreProvider
    collection_name: str

class PGVectorConfig(BaseVectorStoreConfig):
    provider: Literal[VectorStoreProvider.PGVECTOR] = VectorStoreProvider.PGVECTOR
    connection_string: Optional[str] = None

class PineconeConfig(BaseVectorStoreConfig):
    provider: Literal[VectorStoreProvider.PINECONE] = VectorStoreProvider.PINECONE
    api_key: Optional[str] = None
    environment: Optional[str] = None

class QdrantConfig(BaseVectorStoreConfig):
    provider: Literal[VectorStoreProvider.QDRANT] = VectorStoreProvider.QDRANT
    host: str = "localhost"
    port: int = 6333 # Default Qdrant port

class ChromaConfig(BaseVectorStoreConfig):
    provider: Literal[VectorStoreProvider.CHROMA] = VectorStoreProvider.CHROMA
    host: str = "localhost"
    port: int = 8000 # Default Chroma port

class VectorStoreConfiguration(BaseModel):
    """A unified configuration model for backward compatibility and easy env loading."""
    provider: VectorStoreProvider = Field(default=VectorStoreProvider.CHROMA)
    collection_name: str = Field(default="rag_collection")
    connection_string: Optional[str] = None
    api_key: Optional[str] = None
    environment: Optional[str] = None
    host: str = "localhost"
    port: int = 8000
