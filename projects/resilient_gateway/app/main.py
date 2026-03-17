import time
import uvicorn
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.models.gateway_models import LLMRequest, GatewayConfig
from app.services.factory import ProviderFactory
from app.services.router import ResilientRouter
from app.services.webhook_service import WebhookService
from packages.core.observability import ObservabilityClient

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resilient-gateway")

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Simple Audit Log
        logger.info(
            f"AUDIT: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        return response

app = FastAPI(title="Resilient AI Gateway")
app.add_middleware(AuditLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Observability
obs = ObservabilityClient("resilient_gateway")

# Initialize Webhook Service
webhook = WebhookService()

# Global router instance (initialized with simulation by default)
default_config = GatewayConfig(mode="simulation")
providers = ProviderFactory.create_providers(default_config)
router = ResilientRouter(providers)

@app.get("/health")
async def health():
    return {"status": "healthy", "mode": default_config.mode}

@app.post("/v1/complete")
async def complete(request: LLMRequest):
    obs.log(f"Handling completion request for model: {request.model}")
    
    # Trigger n8n Webhook for enrichment
    # We await the response which might contain CRM context
    enrichment_data = await webhook.fire_event("request_received", {
        "prompt": request.prompt,
        "model": request.model
    })

    obs.log(f"Enrichment data: {enrichment_data}")
    
    # If n8n returned enrichment data, inject it into the prompt
    if enrichment_data:
        ctx = ""
        if "customer_status" in enrichment_data:
            ctx += f"\nCustomer Status: {enrichment_data['customer_status']}"
        if "last_purchase" in enrichment_data:
            ctx += f"\nLast Purchase: {enrichment_data['last_purchase']}"
        
        if ctx:
            request.prompt = f"Context:{ctx}\n\nUser Question: {request.prompt}"
            logger.info("Prompt enriched by n8n workflow")
    
    start_time = time.time()
    
    try:
        response = await router.route_request(request)
        
        duration = time.time() - start_time
        obs.metric("completion_latency", duration, unit="seconds")
        
        return response
    except Exception as e:
        logger.error(f"Gateway Error: {str(e)}")
        obs.log(f"Routing failure: {str(e)}", level="ERROR")
        raise HTTPException(status_code=503, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("projects.resilient_gateway.app.main:app", host="0.0.0.0", port=8006, reload=True)
