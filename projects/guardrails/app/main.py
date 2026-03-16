import time
import json
from fastapi import FastAPI, Request, HTTPException
from .models.guard_models import GuardRequest, GuardResponse
from .services.factory import GuardrailFactory

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
    
    try:
        engine = GuardrailFactory.get_engine("simple")
        response = engine.validate(request.text, request.checks)
        response.latency_ms = (time.time() - start_time) * 1000
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
