from fastapi import Depends, FastAPI, HTTPException

from app.auth import get_role_from_auth_header
from app.models import ToolRequest, ToolResponse
from app.tools import invoke_tool

app = FastAPI(title="Sample MCP-Style Gateway", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tools/invoke", response_model=ToolResponse)
def call_tool(request: ToolRequest, role: str = Depends(get_role_from_auth_header)) -> ToolResponse:
    try:
        result = invoke_tool(role=role, tool_name=request.tool_name, arguments=request.arguments)
        return ToolResponse(ok=True, tool_name=request.tool_name, result=result)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
