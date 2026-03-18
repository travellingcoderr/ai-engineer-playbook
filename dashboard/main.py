from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import os

app = FastAPI(title="Command Center Dashboard")

# Mount the projects directory to serve documentation
repo_root = os.path.dirname(os.path.dirname(__file__))
app.mount("/projects", StaticFiles(directory=os.path.join(repo_root, "projects")), name="projects")

# Read the HTML file once on startup
HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    # Centralized port configuration matching the Makefile
    config = {
        "RAG_PORT": 8000,
        "GATEWAY_PORT": 8001,
        "OBS_PORT": 8002,
        "RESEARCH_PORT": 8003,
        "MULTI_AGENT_PORT": 8004,
        "GUARD_PORT": 8005,
        "RESILIENT_GATEWAY_PORT": 8006,
        "N8N_PORT": 5678,
        "PERF_EVAL_PORT": 8007,
        "QDRANT_PORT": 6333,
        "MONGO_PORT": 27017,
        "REDIS_PORT": 6379,
        "MORTGAGE_BOT_API_PORT": 8008,
        "MORTGAGE_BOT_FRONTEND_PORT": 3000,
    }
    
    with open(HTML_FILE_PATH, "r") as f:
        html_content = f.read()
        # Simple string replacement for dynamic ports
        for key, value in config.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
        return html_content

@app.post("/api/stop/{service_name}")
async def stop_service(service_name: str):
    """
    Executes the appropriate terminal commands to stop a service.
    """
    allowed_services = {
        "rag": {"cmd": "make stop-docker-rag", "fallback": "make kill-rag"},
        "mcp": {"cmd": "make stop-docker-gateway", "fallback": "make kill-gateway"},
        "observe": {"cmd": "make kill-observe", "fallback": None},
        "research": {"cmd": "make stop-docker-research", "fallback": "make kill-research"},
        "guardrails": {"cmd": "make stop-docker-guardrails", "fallback": "make kill-guardrails"},
        "resilient": {"cmd": "make stop-docker-resilient-gateway", "fallback": "make kill-resilient-gateway"},
        "n8n": {"cmd": "make stop-n8n", "fallback": None},
        "perf": {"cmd": "make stop-docker-perf-eval", "fallback": "make kill-perf-eval"},
        "infra": {"cmd": "make stop-infra", "fallback": "make kill-infra"}
    }
    
    if service_name not in allowed_services:
        raise HTTPException(status_code=400, detail="Unknown service")
        
    config = allowed_services[service_name]
    
    try:
        # We run this from the parent directory of the dashboard (the repo root)
        repo_root = os.path.dirname(os.path.dirname(__file__))
        
        # Try primary stop command (Docker)
        subprocess.run(
            config["cmd"], 
            shell=True, 
            cwd=repo_root, 
            capture_output=True, 
            text=True
        )
        
        # If it failed or there is a fallback to kill the baremetal port just to be safe
        if config["fallback"]:
            subprocess.run(
                config["fallback"], 
                shell=True, 
                cwd=repo_root, 
                capture_output=True,
                text=True
            )
            
        return {"status": "success", "message": f"{service_name} stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
