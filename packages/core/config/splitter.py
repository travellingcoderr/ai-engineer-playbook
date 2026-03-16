from pydantic_settings import BaseSettings
from pydantic import Field

class SplitterConfiguration(BaseSettings):
    strategy: str = Field(default="recursive_character", description="How to split documents (e.g., recursive_character, semantic)")
    chunk_size: int = Field(default=1000, description="Size of each chunk")
    chunk_overlap: int = Field(default=200, description="Overlap between consecutive chunks")
