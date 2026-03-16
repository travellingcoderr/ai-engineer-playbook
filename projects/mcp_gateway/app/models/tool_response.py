from pydantic import BaseModel


class ToolResponse(BaseModel):
    ok: bool
    tool_name: str
    result: dict
