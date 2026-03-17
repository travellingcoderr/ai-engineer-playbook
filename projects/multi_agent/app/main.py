from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from packages.core.config import get_config
from packages.core.services import ObservabilityClient
import time
import uuid
import logging

logger = logging.getLogger(__name__)
obs_client = ObservabilityClient(service_name="multi_agent")

@asynccontextmanager
async def lifespan(app: FastAPI):
    obs_client.log("Multi-Agent Service started")
    yield

# Create the standard FastAPI app
app = FastAPI(
    title="Multi-Agent Orchestrator API",
    description="A LangGraph supervisor system managing a specialized Researcher and Coder team.",
    version="1.0.0",
    lifespan=lifespan
)

# Shared config integration check, matching the RAG system pattern
try:
    settings = get_config()
except Exception:
    logger.exception("FAILED TO LOAD SHARED APP CONFIG")

class TaskRequest(BaseModel):
    task: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "multi-agent"}

@app.post("/team/run")
async def run_team(request: TaskRequest):
    """
    Kicks off the autonomous multi-agent LangGraph workflow.
    """
    from .agent.graph import agent_team
    
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    
    obs_client.log(f"Starting multi-agent task: {request.task}", trace_id=trace_id)
    
    try:
        logger.info("Starting /team/run task")
        # LangGraph inputs require a 'messages' list for state
        result = agent_team.invoke(
            {"messages": [("user", request.task)]},
            {"configurable": {"thread_id": "1"}} 
        )
        
        end_time = time.time()
        from packages.core.enums import MetricUnit, LogLevel
        obs_client.metric("team_execution_latency", (end_time - start_time), unit=MetricUnit.SECONDS)
        obs_client.metric("team_task_count", 1, unit=MetricUnit.COUNT)
        obs_client.trace("multi_agent_coordination", start_time, end_time, trace_id, span_id)
        
        # Last message in the state typically holds the finalized answer
        final_message = result["messages"][-1].content if result.get("messages") else ""
        
        return {
            "status": "success", 
            "task": request.task,
            "final_response": final_message,
            "full_state": str(result)
        }
    except Exception as e:
        from packages.core.enums import LogLevel
        obs_client.log(f"Team execution failed: {str(e)}", level=LogLevel.ERROR, trace_id=trace_id)
        logger.exception("Multi-agent team execution failed")
        raise HTTPException(status_code=500, detail=str(e))
