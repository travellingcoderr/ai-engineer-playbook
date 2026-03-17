from abc import ABC, abstractmethod
from langchain_core.tools import BaseTool

class BaseAgentTool(ABC):
    """
    Abstract interface for all tools in the multi-agent system.
    Enforces a standard way to retrieve a LangChain compatible BaseTool.
    """
    
    @abstractmethod
    def get_tool(self) -> BaseTool:
        """Returns the LangChain compatible tool instance."""
        pass
