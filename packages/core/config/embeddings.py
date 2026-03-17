from pydantic import Field, BaseModel
from packages.core.enums import EmbeddingProvider, EmbeddingModel

class EmbeddingConfiguration(BaseModel):
    provider: EmbeddingProvider = Field(default=EmbeddingProvider.OPENAI, description="The embedding provider (e.g., openai, huggingface)")
    model: EmbeddingModel = Field(default=EmbeddingModel.TEXT_EMBEDDING_3_SMALL, description="The specific embedding model name")
