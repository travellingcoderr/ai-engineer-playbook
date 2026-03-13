
from fastapi import FastAPI

app = FastAPI()

@app.get("/tool")
def tool(name: str):
    return {"tool": name, "status": "executed"}
