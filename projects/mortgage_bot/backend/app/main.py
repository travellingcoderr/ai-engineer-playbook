from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import tickets, knowledge, loans, crew
from .database import init_db

from fastapi.middleware.cors import CORSMiddleware
from packages.core.services.observability import ObservabilityClient
from packages.core.enums.observability import LogLevel
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
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
    response = await call_next(request)
    duration = time.time() - start_time
    
    obs_client.log(
        message=f"{request.method} {request.url.path} - {response.status_code} ({duration:.4f}s)",
        level=LogLevel.INFO if response.status_code < 400 else LogLevel.ERROR
    )
    return response

app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(loans.router, prefix="/api/loans", tags=["Loans"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(crew.router, prefix="/api/crew", tags=["CrewAI"])

@app.get("/health")
async def health():
    return {"status": "healthy"}
