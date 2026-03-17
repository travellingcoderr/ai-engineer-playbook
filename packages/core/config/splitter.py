from pydantic import Field, BaseModel
from packages.core.enums import SplitterStrategy

class SplitterConfiguration(BaseModel):
    strategy: SplitterStrategy = Field(default=SplitterStrategy.RECURSIVE, description="How to split documents (e.g., recursive_character, semantic)")
    chunk_size: int = Field(default=1000, description="Size of each chunk")
    chunk_overlap: int = Field(default=200, description="Overlap between consecutive chunks")
