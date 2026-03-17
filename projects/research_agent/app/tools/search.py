from langchain_core.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults

from app.tools.base import BaseAgentTool

class TavilySearchTool(BaseAgentTool):
    """
    A concrete implementation of a web search tool using Tavily.
    Tavily is an AI-native search engine optimized for autonomous agents.
    It returns clean, parsed content rather than just HTML links.
    """
    def __init__(self, max_results: int = 5):
        # The API key is automatically picked up from TAVILY_API_KEY env var
        self._tool = TavilySearchResults(max_results=max_results)

    def get_tool(self) -> BaseTool:
        return self._tool
