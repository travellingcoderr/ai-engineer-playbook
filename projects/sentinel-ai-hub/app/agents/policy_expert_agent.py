import json
import logging
from typing import List, Dict, Any, Optional
from azure.ai.projects.models import FunctionTool
from app.core.search_client import SentinelSearchClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_policies(query: str) -> str:
    """
    Search through the internal Insurance Policy and SLA database to find 
    relevant clauses, terms, and conditions.
    
    :param query: The specific topic or clause to search for, e.g. 'hurricane coverage'
    :return: A string containing the most relevant excerpts from the policies.
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
    [POLICY EXPERT AGENT]
    Represents the Policy Expert Agent.
    Provides the tool definition and system instructions.
    """
    AGENT_ROLE = "policy_expert"
    AGENT_TYPE = "researcher"

    NAME = "policy-expert"
    INSTRUCTIONS = (
        "You are an Insurance Policy and Compliance Expert. "
        "Your goal is to accurately interpret complex contract language. "
        "ALWAYS use the 'search_policies' tool to find factual information before answering. "
        "If you cannot find a specific clause, state that clearly. "
        "Present your findings in a structured, professional manner."
    )

    @staticmethod
    def get_tool() -> FunctionTool:
        """Returns the FunctionTool for Azure AI Foundry Agents."""
        return FunctionTool(functions=[search_policies])

if __name__ == "__main__":
    pass
