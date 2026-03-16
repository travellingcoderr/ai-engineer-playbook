from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from packages.core.config import get_config
import logging

logger = logging.getLogger(__name__)

# Create the standard FastAPI app
app = FastAPI(
    title="Multi-Agent Orchestrator API",
    description="A LangGraph supervisor system managing a specialized Researcher and Coder team.",
    version="1.0.0"
)

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
    
    try:
        logger.info("Starting /team/run task")
        # LangGraph inputs require a 'messages' list for state
        # The thread config allows us to track state iteratively if we added checkpointer memory
        result = agent_team.invoke(
            {"messages": [("user", request.task)]},
            {"configurable": {"thread_id": "1"}} 
        )
        
        # Last message in the state typically holds the finalized answer
        final_message = result["messages"][-1].content if result.get("messages") else ""
        
        return {
            "status": "success", 
            "task": request.task,
            "final_response": final_message,
            "full_state": str(result)
        }
    except Exception as e:
        logger.exception("Multi-agent team execution failed")
        raise HTTPException(status_code=500, detail=str(e))
