
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

docs = [
    "AI systems rely on embeddings and vector search.",
    "RAG combines retrieval with generation."
]

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/ask")
def ask(q: str):
    return {"answer": docs[0]}
