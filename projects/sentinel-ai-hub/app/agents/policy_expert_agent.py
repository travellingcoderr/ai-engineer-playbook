import logging
import os
from typing import List, Dict, Any
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from app.core.search_client import SentinelSearchClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_policies(query: str) -> str:
    """
    Search through the internal Insurance Policy and SLA database to find 
    relevant clauses, terms, and conditions.
    """
    logger.info(f"Policy Expert Tool: Searching for '{query}'...")
    searcher = SentinelSearchClient()
    results = searcher.search_hybrid(query, top=3)
    
    if not results:
        return "No relevant policy clauses found."

    combined_results = []
    for res in results:
        combined_results.append(f"Source: {res['title']}\nContent: {res['content']}\n---")
    
    return "\n\n".join(combined_results)

class PolicyExpertAgent:
    """
    [POLICY EXPERT AGENT] - SDK v2.0.0 Patterns
    """
    NAME = "policy-expert"
    MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    
    INSTRUCTIONS = (
        "You are an Insurance Policy and Compliance Expert. "
        "Your goal is to accurately interpret complex contract language. "
        "CRITICAL SAFETY RULE: You must ONLY answer based on the search results found via 'search_policies'. "
        "If the search result is missing or doesn't answer the query, state 'I cannot find a relevant clause in our database'. "
        "Do not hallucinate or discuss non-business disruption topics. "
        "Present your findings in a structured, professional manner."
    )

    @staticmethod
    def get_definition() -> PromptAgentDefinition:
        """Returns the PromptAgentDefinition with explicit tool schemas for SDK v2.0.0+."""
        
        # Explicit Schema Definition (The "Azure Way" for v2.0)
        search_tool = FunctionTool(
            name="search_policies",
            description="Search through internal policies and SLAs to find relevant clauses.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The specific topic or clause to search for, e.g. 'hurricane coverage'"
                    }
                },
                "required": ["query"]
            }
        )

        return PromptAgentDefinition(
            model=PolicyExpertAgent.MODEL,
            instructions=PolicyExpertAgent.INSTRUCTIONS,
            tools=[search_tool]
        )

if __name__ == "__main__":
    pass
