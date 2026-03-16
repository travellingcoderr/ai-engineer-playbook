import time
import json
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth import get_role_from_auth_header, create_access_token
from app.models import ToolRequest, ToolResponse
from app.tools import invoke_tool

app = FastAPI(title="Sample MCP-Style Gateway", version="0.2.0")

class LoginRequest(BaseModel):
    username: str

@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Only log tool invocations for now
    if request.url.path == "/tools/invoke":
        log_data = {
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration": f"{duration:.4f}s",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        print(f"AUDIT_LOG: {json.dumps(log_data)}")
        
    return response

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Stub login: map any username to a role for demo
    role_map = {"admin": "admin", "analyst": "analyst", "engineer": "engineer"}
    role = role_map.get(form_data.username, "analyst")
    
    access_token = create_access_token(data={"sub": form_data.username, "role": role})
    return {"access_token": access_token, "token_type": "bearer"}


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
