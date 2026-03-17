import os
from ..config import get_config

class ToolFactory:
    """
    Global Factory Pattern for instantiating standard tools across agents.
    """
    @staticmethod
    def create_tools() -> list:
        """Alias for backwards compatibility with research_agent."""
        return ToolFactory.create_research_tools()
        
    @staticmethod
    def create_research_tools(search_provider: str | None = None) -> list:
        provider = search_provider or ToolFactory._get_search_provider()

        if provider == "tavily":
            from langchain_community.tools.tavily_search import TavilySearchResults

            if not os.getenv("TAVILY_API_KEY"):
                raise ValueError("TAVILY_API_KEY is missing. Tavily search requires this key.")
            return [TavilySearchResults(max_results=3)]

        if provider == "duckduckgo":
            try:
                from langchain_community.tools.duckduckgo_search import DuckDuckGoSearchRun
            except ImportError as exc:
                raise ImportError(
                    "DuckDuckGo search is configured, but langchain_community DuckDuckGo support is unavailable."
                ) from exc
            return [DuckDuckGoSearchRun()]

        raise ValueError(f"Unsupported search provider: {provider}")

    @staticmethod
    def _get_search_provider() -> str:
        try:
            settings = get_config()
        except Exception:
            settings = None

        provider = (
            getattr(getattr(settings, "tools", None), "search_provider", None)
            or os.getenv("SEARCH_PROVIDER")
            or "tavily"
        )
        return provider.strip().lower()
