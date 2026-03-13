
from fastapi import FastAPI

app = FastAPI()

docs = [
    "AI systems rely on embeddings and vector search.",
    "RAG combines retrieval with generation."
]

@app.get("/ask")
def ask(q: str):
    return {"answer": docs[0]}
