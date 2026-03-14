from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import os
from contextlib import asynccontextmanager

from app.services.rag import RAGService

# Create a global instance to hold our service
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_service
    # Initialize the RAG service when the app starts
    rag_service = RAGService()
    yield
    # Cleanup on shutdown if necessary
    rag_service = None

app = FastAPI(lifespan=lifespan)

@app.post("/ingest")
def ingest_document(file_path: str):
    """
    Ingests a document from a local file path or URL into the vector database.
    """
    if not rag_service:
        raise HTTPException(status_code=500, detail="RAG Service not initialized")
    
    try:
        chunks = rag_service.ingest_document(file_path)
        return {"status": "success", "chunks_ingested": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask")
def ask(q: str):
    """
    Queries the RAG system using the configured LLM and Vector Store.
    """
    if not rag_service:
        raise HTTPException(status_code=500, detail="RAG Service not initialized")
        
    try:
        answer = rag_service.ask_question(q)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
