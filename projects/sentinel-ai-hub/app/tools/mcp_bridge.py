import os
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from azure.ai.projects.models import FunctionTool

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiMCPManager:
    """
    Manages multiple MCP server connections simultaneously.
    Supports Python, Node.js (npx), and other stdio-based servers.
    """
    def __init__(self):
        self.servers: Dict[str, Dict[str, Any]] = {}
        self.tool_to_server: Dict[str, str] = {}
        self._exit_stacks: Dict[str, asyncio.ExitStack] = {}

    def register_server(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        """Register a server configuration without connecting yet."""
        # Merge provided env with current process env
        full_env = os.environ.copy()
        if env:
            full_env.update(env)
            
        self.servers[name] = {
            "params": StdioServerParameters(
                command=command,
                args=args,
                env=full_env
            ),
            "session": None,
            "tools": []
        }
        logger.info(f"Registered MCP server: {name}")

    async def connect_all(self):
        """Connect to all registered servers and fetch their tool metadata."""
        for name, config in self.servers.items():
            try:
                logger.info(f"Connecting to MCP server: {name}...")
                exit_stack = asyncio.ExitStack()
                self._exit_stacks[name] = exit_stack
                
                read, write = await exit_stack.enter_async_context(stdio_client(config["params"]))
                session = await exit_stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                
                # List tools
                tools_list = await session.list_tools()
                config["session"] = session
                config["tools"] = tools_list.tools
                
                # Map tools to this server
                for tool in tools_list.tools:
                    self.tool_to_server[tool.name] = name
                    
                logger.info(f"Connected to {name}. Found {len(tools_list.tools)} tools.")
            except Exception as e:
                logger.error(f"Failed to connect to MCP server {name}: {e}")

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by finding the responsible server."""
        server_name = self.tool_to_server.get(name)
        if not server_name:
            raise ValueError(f"Tool {name} not found in any registered MCP server.")
            
        session = self.servers[server_name]["session"]
        logger.info(f"Executing tool '{name}' on server '{server_name}'...")
        
        result = await session.call_tool(name, arguments)
        return json.dumps(result.content)

    async def disconnect_all(self):
        """Safely disconnect all server sessions."""
        for name, stack in self._exit_stacks.items():
            try:
                await stack.aclose()
                logger.info(f"Disconnected from {name}.")
            except Exception as e:
                logger.error(f"Error disconnecting from {name}: {e}")

    def get_all_tool_metadata(self) -> List[Any]:
        """Get combined tool metadata from all connected servers."""
        all_tools = []
        for config in self.servers.values():
            all_tools.extend(config["tools"])
        return all_tools

if __name__ == "__main__":
    # Example usage:
    # manager = MultiMCPManager()
    # manager.register_server("mock", "python", ["app/tools/mcp_server.py"])
    # manager.register_server("slack", "npx", ["-y", "@modelcontextprotocol/server-slack"], env={"SLACK_BOT_TOKEN": "..."})
    # asyncio.run(manager.connect_all())
    pass
