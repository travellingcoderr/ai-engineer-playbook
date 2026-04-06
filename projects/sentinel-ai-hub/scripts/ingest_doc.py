import os
import json
import logging
import uuid
from dotenv import load_dotenv
from app.core.document_intel import DocumentIntelManager
from app.core.search_client import SentinelSearchClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_document(file_path: str):
    load_dotenv()
    
    # 1. Extract Markdown (Preserves structure)
    doc_intel = DocumentIntelManager()
    markdown_content = doc_intel.extract_markdown(file_path)
    logger.info(f"Extracted {len(markdown_content)} characters of Markdown.")

    # 2. Simple Chunking (In production, use Sematic Chunking or LangChain)
    # Here we just treat the whole doc as one chunk for the demo or split by #
    chunks = markdown_content.split("\n#")
    
    search_client = SentinelSearchClient()
    upload_batch = []
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip(): continue
        
        doc_id = str(uuid.uuid4())
        upload_batch.append({
            "id": doc_id,
            "title": os.path.basename(file_path),
            "content": "# " + chunk if i > 0 else chunk,
            "content_vector": search_client.get_embedding(chunk),
            "metadata": json.dumps({"source": file_path, "chunk": i})
        })

    # 3. Upload to Azure Search
    logger.info(f"Uploading {len(upload_batch)} chunks to search index...")
    search_client.client.upload_documents(upload_batch)
    logger.info("Ingestion complete.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ingest_document(sys.argv[1])
    else:
        print("Usage: python ingest_doc.py <path_to_pdf>")
