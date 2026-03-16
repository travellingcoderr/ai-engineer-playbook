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

from fastapi import UploadFile, File
import tempfile

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingests an uploaded document into the vector database.
    """
    if not rag_service:
        raise HTTPException(status_code=500, detail="RAG Service not initialized")
    
    try:
        # Create a temporary file to save the uploaded content
        # LangChain loaders typically require physical file paths
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process the temporary file path just like a local file
            chunks = rag_service.ingest_document(temp_file_path)
            return {"status": "success", "chunks_ingested": len(chunks), "file": file.filename}
        finally:
            # Clean up the temporary file after ingestion
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

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
