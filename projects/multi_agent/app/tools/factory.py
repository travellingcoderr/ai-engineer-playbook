import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.duckduckgo_search import DuckDuckGoSearchRun

class ToolFactory:
    """
    Standardized Factory Pattern for instantiating the tools our Worker agents will use.
    The Supervisor decides WHICH worker to use, the Worker knows WHICH tool to use.
    """
    
    @staticmethod
    def create_research_tools():
        """Returns the search tools required by the Researcher node."""
        tools = []
        
        # We check if TAVILY is present, otherwise fallback to DuckDuckGo (Free)
        if os.getenv("TAVILY_API_KEY"):
            tools.append(TavilySearchResults(max_results=3))
        else:
            tools.append(DuckDuckGoSearchRun())
            
        return tools
