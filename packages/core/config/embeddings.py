from pydantic import Field, BaseModel
from packages.core.enums import EmbeddingProvider

class EmbeddingConfiguration(BaseModel):
    provider: EmbeddingProvider = Field(default=EmbeddingProvider.OPENAI, description="The embedding provider (e.g., openai, huggingface)")
    model: str = Field(default="text-embedding-3-small", description="The specific embedding model name")
