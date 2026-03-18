from typing import List
import os
import uuid
from datetime import datetime
from packages.core.services.rag.rag_service import RAGService
from langchain_core.documents import Document
from sqlmodel import Session, select
from app.database import engine
from app.models.knowledge import KnowledgeDocument
from packages.core.services.observability import ObservabilityClient
from packages.core.enums.observability import LogLevel

obs_client = ObservabilityClient(service_name="mortgage_bot_worker")

def process_document(doc_id: str, blob_uri: str, metadata: dict):
    """
    Background task to process an uploaded document and store it in pgvector.
    """
    obs_client.log(f"Starting ingestion for document {doc_id}", level=LogLevel.INFO)
    try:
        # 1. Acquire document content
        if not os.path.exists(blob_uri):
            raise FileNotFoundError(f"File not found at {blob_uri}")
        
        documents = []
        if blob_uri.lower().endswith(".pdf"):
            obs_client.log(f"Loading PDF from {blob_uri}", level=LogLevel.DEBUG)
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(blob_uri)
            # Load and set metadata for each page
            for i, page in enumerate(loader.load()):
                page.metadata.update({**metadata, "doc_id": doc_id, "page_index": i})
                documents.append(page)
            obs_client.log(f"Extracted {len(documents)} pages from PDF", level=LogLevel.INFO)
        else:
            obs_client.log(f"Loading text file from {blob_uri}", level=LogLevel.DEBUG)
            # Fallback for plain text
            with open(blob_uri, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Simple split by paragraphs for now
            chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
            for i, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={**metadata, "doc_id": doc_id, "chunk_index": i}
                    )
                )
            obs_client.log(f"Extracted {len(documents)} chunks from text file", level=LogLevel.INFO)
        
        # 3. Add to vector store
        if documents:
            obs_client.log(f"Storing {len(documents)} documents in vector store", level=LogLevel.DEBUG)
            connection_string = os.getenv("DATABASE_URL")
            rag_service = RAGService(connection_string=connection_string, collection_name="knowledge")
            rag_service.add_documents(documents)
        
        # 4. Update status in Postgres
        with Session(engine) as session:
            db_doc = session.exec(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id)).one_or_none()
            if db_doc:
                db_doc.status = "published"
                session.add(db_doc)
                session.commit()
                obs_client.log(f"Document {doc_id} status updated to 'published'", level=LogLevel.INFO)

    except Exception as e:
        obs_client.log(f"Error processing document {doc_id}: {str(e)}", level=LogLevel.ERROR)
        # Update status to error
        with Session(engine) as session:
            db_doc = session.exec(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id)).one_or_none()
            if db_doc:
                db_doc.status = "error"
                session.add(db_doc)
                session.commit()
        raise e
