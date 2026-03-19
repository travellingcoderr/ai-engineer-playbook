from fastapi import FastAPI
from contextlib import asynccontextmanager
import uuid

from .api import tickets, knowledge, loans, crew, instrumentation, jobs
from .database import init_db
from .services.llm_invocation_service import record_llm_invocation

from fastapi.middleware.cors import CORSMiddleware
from packages.core.services.observability import ObservabilityClient
from packages.core.services import (
    reset_llm_instrumentation_context,
    set_llm_instrumentation_context,
    set_llm_record_sink,
)
from packages.core.enums.observability import LogLevel
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    set_llm_record_sink(record_llm_invocation)
    yield

app = FastAPI(title="mortgage-bot API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, restrict to frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

obs_client = ObservabilityClient(service_name="mortgage_bot_backend")

@app.middleware("http")
async def observability_middleware(request, call_next):
    start_time = time.time()
    trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    context_token = set_llm_instrumentation_context(
        trace_id=trace_id,
        request_id=request_id,
        feature=request.url.path,
        workflow_type="http_request",
    )
    try:
        response = await call_next(request)
    finally:
        reset_llm_instrumentation_context(context_token)
    duration = time.time() - start_time
    
    obs_client.log(
        message=f"{request.method} {request.url.path} - {response.status_code} ({duration:.4f}s)",
        level=LogLevel.INFO if response.status_code < 400 else LogLevel.ERROR
    )
    response.headers["x-trace-id"] = trace_id
    response.headers["x-request-id"] = request_id
    return response

app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(loans.router, prefix="/api/loans", tags=["Loans"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(crew.router, prefix="/api/crew", tags=["CrewAI"])
app.include_router(instrumentation.router, prefix="/api/instrumentation", tags=["Instrumentation"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])

@app.get("/health")
async def health():
    return {"status": "healthy"}
