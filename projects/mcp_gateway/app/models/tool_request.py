from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    tool_name: str = Field(..., description="Tool to invoke")
    arguments: dict = Field(default_factory=dict, description="Tool arguments")
