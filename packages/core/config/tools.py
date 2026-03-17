from pydantic import Field, BaseModel


class ToolConfiguration(BaseModel):
    search_provider: str = Field(
        default="tavily",
        description="The search engine provider to use (e.g., tavily, duckduckgo)",
        alias="SEARCH_PROVIDER",
    )
