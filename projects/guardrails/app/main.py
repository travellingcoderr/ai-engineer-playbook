import time
import json
from fastapi import FastAPI, Request, HTTPException
from packages.core.models.guardrails import GuardRequest, GuardResponse
from .services.factory import GuardrailFactory
from packages.core.services import ObservabilityClient
import uuid

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
async def validate_text(request: GuardRequest):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    obs_client.log(f"Validating text: {request.text[:50]}...", trace_id=trace_id)
    
    try:
        engine = GuardrailFactory.get_engine("simple")
        response = engine.validate(request.text, request.checks)
        latency = (time.time() - start_time)
        response.latency_ms = latency * 1000
        
        from packages.core.enums import MetricUnit, LogLevel
        obs_client.metric("validation_latency", latency, unit=MetricUnit.SECONDS)
        if response.safe:
            obs_client.log("Text passed guardrails", trace_id=trace_id)
        else:
            from packages.core.enums import LogLevel
            obs_client.log(f"Guardrail violation: {response.explanation}", level=LogLevel.WARNING, trace_id=trace_id)
            
        return response
    except Exception as e:
        from packages.core.enums import LogLevel
        obs_client.log(f"Validation error: {str(e)}", level=LogLevel.ERROR, trace_id=trace_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
