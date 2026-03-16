import os

class ToolFactory:
    """
    Global Factory Pattern for instantiating standard tools across agents.
    """
    @staticmethod
    def create_tools() -> list:
        """Alias for backwards compatibility with research_agent."""
        return ToolFactory.create_research_tools()
        
    @staticmethod
    def create_research_tools() -> list:
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langchain_community.tools.duckduckgo_search import DuckDuckGoSearchRun
        
        tools = []
        if os.getenv("TAVILY_API_KEY"):
            tools.append(TavilySearchResults(max_results=3))
        else:
            tools.append(DuckDuckGoSearchRun())
            
        return tools
