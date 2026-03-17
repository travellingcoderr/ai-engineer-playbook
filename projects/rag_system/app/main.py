from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import tempfile
from contextlib import asynccontextmanager
import time
import uuid

from app.services.rag import RAGService
from packages.core.observability import ObservabilityClient

# Create a global instances to hold our services
rag_service = None
obs_client = ObservabilityClient(service_name="rag_system")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_service
    # Initialize the RAG service when the app starts
    rag_service = RAGService()
    obs_client.log("RAG System Service started")
    yield
    # Cleanup on shutdown if necessary
    rag_service = None



app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

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
        
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    
    obs_client.log(f"Received question: {q}", trace_id=trace_id)
    
    try:
        answer = rag_service.ask_question(q)
        
        end_time = time.time()
        obs_client.metric("query_latency", (end_time - start_time), unit="seconds")
        obs_client.metric("query_count", 1, unit="count")
        obs_client.trace("rag_query", start_time, end_time, trace_id, span_id)
        
        return {"answer": answer}
    except Exception as e:
        obs_client.log(f"Error processing question: {str(e)}", level="ERROR", trace_id=trace_id)
        raise HTTPException(status_code=500, detail=str(e))
