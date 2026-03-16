from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

# We import the run function from the agent module
from projects.research_agent.agent import run
from packages.core.config import get_config

app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API to trigger an autonomous LangGraph agent that researches the web and writes comprehensive reports.",
    version="1.0.0"
)

# Force the environment/config to load on startup so it fails fast if keys are missing
@app.on_event("startup")
async def startup_event():
    get_config()

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The broad subject or specific question you want researched.", example="What are the top 3 biggest AI news stories from March 2026?")

class ResearchResponse(BaseModel):
    topic: str
    report_markdown: str

@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """
    Triggers the autonomous research agent.
    This endpoint is synchronous under the hood, so it will block until the research
    loop is complete (which could take a minute or more).
    """
    try:
        # Our run() function calls the LangGraph synchronously for now.
        # In a massive production system, you'd use Celery/Redis for background tasks.
        final_report = run(request.topic)
        return ResearchResponse(
            topic=request.topic,
            report_markdown=final_report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("projects.research_agent.app.main:app", host="0.0.0.0", port=8001, reload=True)
