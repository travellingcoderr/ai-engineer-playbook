import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from dotenv import load_dotenv

class LLMConfiguration(BaseSettings):
    provider: str = Field(default="openai", description="The LLM provider (e.g., openai, gemini, anthropic)")
    model: str = Field(default="gpt-4o", description="The specific model name for the provider", alias="OPENAI_MODEL")
    openai_api_key: str | None = Field(default=None, description="OpenAI API Key", alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API Key")

class EmbeddingConfiguration(BaseSettings):
    provider: str = Field(default="openai", description="The embedding provider (e.g., openai, huggingface)")
    model: str = Field(default="text-embedding-3-small", description="The specific embedding model name")

class VectorStoreConfiguration(BaseSettings):
    provider: str = Field(default="chroma", description="The vector store provider (e.g., chroma, qdrant)")
    collection_name: str = Field(default="rag_collection", description="Collection/Index name in the DB")
    host: str = Field(default="localhost", description="Host address of the vector database")
    port: int = Field(default=8000, description="Port number of the vector database")

class LoaderConfiguration(BaseSettings):
    strategy: str = Field(default="auto", description="How to load documents (e.g., auto, pdf, markdown)")

class SplitterConfiguration(BaseSettings):
    strategy: str = Field(default="recursive_character", description="How to split documents (e.g., recursive_character, semantic)")
    chunk_size: int = Field(default=1000, description="Size of each chunk")
    chunk_overlap: int = Field(default=200, description="Overlap between consecutive chunks")

class AppConfig(BaseSettings):
    """
    Main application configuration grouping all the sub-configurations.
    Loads variables from the environment or a .env file.
    """
    llm: LLMConfiguration = LLMConfiguration()
    embeddings: EmbeddingConfiguration = EmbeddingConfiguration()
    vector_store: VectorStoreConfiguration = VectorStoreConfiguration()
    loader: LoaderConfiguration = LoaderConfiguration()
    splitter: SplitterConfiguration = SplitterConfiguration()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="_",
        extra="ignore"
    )

@lru_cache()
def get_config() -> AppConfig:
    """Returns a cached instance of the application configuration."""
    load_dotenv() # Force load the root .env file
    
    config = AppConfig()
    
    # Manually patch keys that pydantic-settings might miss due to nesting discrepancies
    if os.getenv("OPENAI_API_KEY"):
        config.llm.openai_api_key = os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_MODEL"):
        config.llm.model = os.getenv("OPENAI_MODEL")
        
    return config
