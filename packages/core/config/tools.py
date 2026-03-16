from pydantic_settings import BaseSettings
from pydantic import Field


class ToolConfiguration(BaseSettings):
    search_provider: str = Field(
        default="tavily",
        description="The search engine provider to use (e.g., tavily, duckduckgo)",
        alias="SEARCH_PROVIDER",
    )
