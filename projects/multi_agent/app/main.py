from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from packages.core.config import get_config
from packages.core.observability import ObservabilityClient
import time
import uuid
import logging

logger = logging.getLogger(__name__)
obs_client = ObservabilityClient(service_name="multi_agent")

# Create the standard FastAPI app
app = FastAPI(
    title="Multi-Agent Orchestrator API",
    description="A LangGraph supervisor system managing a specialized Researcher and Coder team.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    obs_client.log("Multi-Agent Service started")

# Shared config integration check, matching the RAG system pattern
try:
    settings = get_config()
except Exception as e:
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
        obs_client.metric("team_execution_latency", (end_time - start_time), unit="seconds")
        obs_client.metric("team_task_count", 1, unit="count")
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
        obs_client.log(f"Team execution failed: {str(e)}", level="ERROR", trace_id=trace_id)
        logger.exception("Multi-agent team execution failed")
        raise HTTPException(status_code=500, detail=str(e))
