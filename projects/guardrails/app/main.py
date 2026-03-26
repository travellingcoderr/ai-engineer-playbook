import time
import json
from fastapi import FastAPI, Request, HTTPException
from packages.core.models.guardrails import GuardRequest, GuardResponse
from .services.factory import GuardrailFactory
from packages.core.services import ObservabilityClient
import uuid

from fastapi.security import APIKeyHeader
from fastapi import Security, Depends

API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == "top-secret-ai-token":  # In production, use env vars or DB
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

obs_client = ObservabilityClient(service_name="guardrails")

app = FastAPI(title="LLM Guardrails Service", version="0.1.0")

@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    if request.url.path == "/validate":
        log_entry = {
            "path": request.url.path,
            "status_code": response.status_code,
            "latency": f"{duration:.4f}s",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"GUARDRAIL_AUDIT: {json.dumps(log_entry)}")
    
    return response

@app.post("/validate", response_model=GuardResponse)
async def validate_text(request: GuardRequest, api_key: str = Depends(get_api_key)):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    obs_client.log(f"Validating text: {request.text[:50]}...", trace_id=trace_id)
    
    try:
        engine = GuardrailFactory.get_engine("advanced")
        response = engine.validate(request.text, request.checks)
        latency = (time.time() - start_time)
        response.latency_ms = latency * 1000
        
        from packages.core.enums import MetricUnit
        obs_client.metric("validation_latency", latency, unit=MetricUnit.SECONDS)
        
        if response.safe:
            obs_client.log(f"Validation passed ({len(response.findings)} minor notes)", trace_id=trace_id)
        else:
            from packages.core.enums import LogLevel
            # Log each finding as a separate warning for better dashboard visibility
            for finding in response.findings:
                obs_client.log(f"Guardrail violation: {finding}", level=LogLevel.WARNING, trace_id=trace_id)
            
        return response
    except Exception as e:
        from packages.core.enums import LogLevel
        obs_client.log(f"Validation error: {str(e)}", level=LogLevel.ERROR, trace_id=trace_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
