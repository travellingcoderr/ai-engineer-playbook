from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import uvicorn

# We import the run function from the agent module
from projects.research_agent.agent import run
from packages.core.config import get_config
from packages.core.services import ObservabilityClient
import time
import uuid

obs_client = ObservabilityClient(service_name="research_agent")

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_config()
    obs_client.log("Research Agent Service started")
    yield

app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API to trigger an autonomous LangGraph agent that researches the web and writes comprehensive reports.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The broad subject or specific question you want researched.", example="What are the top 3 biggest AI news stories from March 2026?")

class ResearchResponse(BaseModel):
    topic: str
    report_markdown: str

@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """
    Triggers the autonomous research agent.
    """
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    
    obs_client.log(f"Starting research on: {request.topic}", trace_id=trace_id)
    
    try:
        # Our run() function calls the LangGraph synchronously for now.
        final_report = run(request.topic)
        
        end_time = time.time()
        from packages.core.enums import MetricUnit, LogLevel
        obs_client.metric("research_latency", (end_time - start_time), unit=MetricUnit.SECONDS)
        obs_client.metric("research_count", 1, unit=MetricUnit.COUNT)
        obs_client.trace("autonomous_research", start_time, end_time, trace_id, span_id)
        
        return ResearchResponse(
            topic=request.topic,
            report_markdown=final_report
        )
    except Exception as e:
        from packages.core.enums import LogLevel
        obs_client.log(f"Research failed: {str(e)}", level=LogLevel.ERROR, trace_id=trace_id)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("projects.research_agent.app.main:app", host="0.0.0.0", port=8001, reload=True)
