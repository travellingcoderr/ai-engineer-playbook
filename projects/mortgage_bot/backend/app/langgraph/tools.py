from langchain_core.tools import tool
from packages.core.services.rag.rag_service import RAGService
import os

@tool
def search_knowledge(query: str):
    """Searches the mortgage knowledge base for relevant guidelines and documentation."""
    connection_string = os.getenv("DATABASE_URL")
    rag = RAGService(connection_string=connection_string)
    results = rag.search(query, k=3)
    return "\n\n".join([r.page_content for r in results])

@tool
def get_loan_details(loan_id: str):
    """Fetches details for a specific loan number to provide context-aware support."""
    # Mock data for demonstration
    return {
        "loan_id": loan_id,
        "borrower": "John Doe",
        "status": "In Processing",
        "milestone": "Appraisal",
        "last_updated": "2026-03-15"
    }
