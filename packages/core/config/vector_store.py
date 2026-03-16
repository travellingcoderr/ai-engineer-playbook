from pydantic_settings import BaseSettings
from pydantic import Field

class VectorStoreConfiguration(BaseSettings):
    provider: str = Field(default="chroma", description="The vector store provider (e.g., chroma, qdrant)")
    collection_name: str = Field(default="rag_collection", description="Collection/Index name in the DB")
    host: str = Field(default="localhost", description="Host address of the vector database")
    port: int = Field(default=8000, description="Port number of the vector database")
