from pydantic_settings import BaseSettings
from pydantic import Field

class EmbeddingConfiguration(BaseSettings):
    provider: str = Field(default="openai", description="The embedding provider (e.g., openai, huggingface)")
    model: str = Field(default="text-embedding-3-small", description="The specific embedding model name")
