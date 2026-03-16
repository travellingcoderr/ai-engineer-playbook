import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv

from .llm import LLMConfiguration
from .embeddings import EmbeddingConfiguration
from .vector_store import VectorStoreConfiguration
from .loader import LoaderConfiguration
from .splitter import SplitterConfiguration
from .tools import ToolConfiguration

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
    tools: ToolConfiguration = ToolConfiguration()

    # The config doesn't hardcode the path here; pydantic will search the current directory.
    # We will enforce finding the root .env in get_config()
    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        extra="ignore"
    )

@lru_cache()
def get_config() -> AppConfig:
    """Returns a cached instance of the application configuration."""
    # Find the .env file in the project root by walking up from the current working directory
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        # Fallback manual relative path just in case
        load_dotenv("../../.env")
    
    config = AppConfig()
    
    # Manually patch keys that pydantic-settings might miss due to nesting discrepancies
    if os.getenv("OPENAI_API_KEY"):
        config.llm.openai_api_key = os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_MODEL"):
        config.llm.model = os.getenv("OPENAI_MODEL")
        
    return config
