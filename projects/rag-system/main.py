
from fastapi import FastAPI
app = FastAPI()

docs = [
    "AI is transforming software development",
    "Vector databases enable semantic search"
]

@app.get("/ask")
def ask(q: str):
    return {"answer": docs[0]}
