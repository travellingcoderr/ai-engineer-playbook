from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import subprocess
import os

app = FastAPI(title="Command Center Dashboard")

# Read the HTML file once on startup
HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open(HTML_FILE_PATH, "r") as f:
        return f.read()

@app.post("/api/stop/{service_name}")
async def stop_service(service_name: str):
    """
    Executes the appropriate terminal commands to stop a service.
    """
    allowed_services = {
        "rag": {"cmd": "make stop-docker-rag", "fallback": "make kill-rag"},
        "mcp": {"cmd": "make kill-gateway", "fallback": None},
        "observe": {"cmd": "make kill-observe", "fallback": None},
        "research": {"cmd": "make stop-docker-research", "fallback": "make kill-research"}
    }
    
    if service_name not in allowed_services:
        raise HTTPException(status_code=400, detail="Unknown service")
        
    config = allowed_services[service_name]
    
    try:
        # We run this from the parent directory of the dashboard (the repo root)
        repo_root = os.path.dirname(os.path.dirname(__file__))
        
        # Try primary stop command (Docker)
        result = subprocess.run(
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
