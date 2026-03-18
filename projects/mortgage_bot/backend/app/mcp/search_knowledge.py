from langchain_core.tools import tool

from .tool_helpers import get_rag_service, log_tool_call


@tool
def search_knowledge(query: str):
    """Searches the mortgage knowledge base for relevant guidelines and documentation."""
    log_tool_call("search_knowledge", f"called with query='{query}'")
    rag = get_rag_service()
    results = rag.search(query, k=3)
    log_tool_call("search_knowledge", f"returned {len(results)} results")
    return "\n\n".join(result.page_content for result in results)
