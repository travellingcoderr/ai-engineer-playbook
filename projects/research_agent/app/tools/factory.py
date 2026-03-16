from typing import List
from langchain_core.tools import BaseTool

from app.tools.search import TavilySearchTool
from app.tools.scrape import ScrapeTool
from app.core.config import get_research_config

class ToolFactory:
    """
    A centralized Factory responsible for instantiating and configuring
    the AI Agent's toolkit based on the project configuration.
    """
    
    @staticmethod
    def create_tools() -> List[BaseTool]:
        """
        Dynamically loads the tools requested in the configuration file.
        Returns a list of LangChain BaseTools ready for the agent to use.
        """
        config = get_research_config()
        tools: List[BaseTool] = []
        
        for tool_name in config.tools.enabled_tools:
            if tool_name == "search":
                if config.tools.search_provider == "tavily":
                    search_impl = TavilySearchTool()
                    tools.append(search_impl.get_tool())
                else:
                    raise ValueError(f"Unknown search provider: {config.tools.search_provider}")
                
            elif tool_name == "scrape":
                scrape_impl = ScrapeTool()
                tools.append(scrape_impl.get_tool())
            else:
                raise ValueError(f"Unknown tool requested in config: {tool_name}")
                
        return tools
