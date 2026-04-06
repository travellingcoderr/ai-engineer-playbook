import os
import json
import asyncio
import logging
from typing import List, Dict, Any, Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from app.core.foundry_client import FoundryProjectManager
from app.agents.policy_expert_agent import PolicyExpertAgent, search_policies
from app.agents.responder_agent import ResponderAgent
from app.tools.mcp_bridge import MultiMCPManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentinelOrchestratorAgent:
    """
    [ORCHESTRATOR AGENT]
    Main coordinator for Project Sentinel.
    - Manages the lifecycle of multiple AI Foundry Agents.
    - Handles persistent conversation threads across requests.
    - Routes tool output requirements from agents to the appropriate MCP bridges.
    """
    AGENT_ROLE = "orchestrator"
    AGENT_TYPE = "manager"

    def __init__(self):
        self.project_manager = FoundryProjectManager()
        self.mcp_manager = MultiMCPManager()
        self.agents_client = self.project_manager.get_agents_client()
        self.agents = {}

    async def setup(self):
        """Initialize Multi-MCP connectivity and ensure agents exist in Foundry."""
        
        # 1. Register MCP Servers
        # Mock Supply Chain (Python)
        self.mcp_manager.register_server(
            "mock", "python", ["app/tools/mcp_server.py"]
        )

        # Slack (Node.js/npx)
        slack_token = os.getenv("SLACK_BOT_TOKEN")
        if slack_token and slack_token != "xoxb-...":
            self.mcp_manager.register_server(
                "slack", "npx", ["-y", "@modelcontextprotocol/server-slack"],
                env={"SLACK_BOT_TOKEN": slack_token}
            )
        else:
            logger.warning("SLACK_BOT_TOKEN missing. Slack tools will be unavailable.")

        # Google Maps (Node.js/npx)
        maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if maps_key and maps_key != "...":
            self.mcp_manager.register_server(
                "google-maps", "npx", ["-y", "@modelcontextprotocol/server-google-maps"],
                env={"GOOGLE_MAPS_API_KEY": maps_key}
            )
        else:
            logger.warning("GOOGLE_MAPS_API_KEY missing. Google Maps tools will be unavailable.")

        # Connect all
        await self.mcp_manager.connect_all()
        
        # 2. Setup Policy Expert
        logger.info("Setting up Policy Expert Agent...")
        policy_agent = self.agents_client.create_agent(
            model="gpt-4o",
            name=PolicyExpertAgent.NAME,
            instructions=PolicyExpertAgent.INSTRUCTIONS,
            tools=[PolicyExpertAgent.get_tool()]
        )
        self.agents[PolicyExpertAgent.NAME] = policy_agent

        # 3. Setup Responder Agent (with expanded tools)
        logger.info("Setting up Responder Agent...")
        responder_agent = self.agents_client.create_agent(
            model="gpt-4o",
            name=ResponderAgent.NAME,
            instructions=ResponderAgent.INSTRUCTIONS,
            tools=ResponderAgent.get_tool_definitions()
        )
        self.agents[ResponderAgent.NAME] = responder_agent

    async def process_event(self, event_data: Dict[str, Any]):
        """
        Process a disruption event using Multi-Agent coordination and Multi-MCP tools.
        """
        logger.info(f"Processing event: {event_data['event_type']} in {event_data['city']}")
        
        # Create Thread
        thread = self.agents_client.create_thread()
        logger.info(f"Created Thread: {thread.id}")

        # Initial Prompt
        prompt = (
            f"URGENT ALERT: {event_data['event_type']} in {event_data['city']}. "
            f"Severity: {event_data['severity']}/10. details: {event_data['details']}. "
            "Task 1: Search policies for disaster protocols. "
            "Task 2: Check shipment/inventory risk via MCP. "
            "Task 3: Post a mitigation summary to Slack."
        )
        self.agents_client.create_message(
            thread_id=thread.id, role="user", content=prompt
        )

        # Start Run
        run = self.agents_client.create_run(
            thread_id=thread.id, 
            assistant_id=self.agents[PolicyExpertAgent.NAME].id
        )

        # Polling Loop
        while True:
            run = self.agents_client.get_run(thread_id=thread.id, run_id=run.id)
            logger.info(f"Run status: {run.status}")

            if run.status in ["queued", "in_progress"]:
                await asyncio.sleep(2)
                continue
            
            elif run.status == "requires_action":
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    output = ""
                    try:
                        # Route: Search or Multi-MCP
                        if func_name == "search_policies":
                            output = search_policies(**args)
                        else:
                            # Multi-MCP Routing (Mock, Slack, Maps)
                            output = await self.mcp_manager.execute_tool(func_name, args)
                    except Exception as e:
                        output = f"Error executing {func_name}: {e}"

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output
                    })

                self.agents_client.submit_tool_outputs_to_run(
                    thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                )
                continue
            
            elif run.status == "completed":
                messages = self.agents_client.list_messages(thread_id=thread.id)
                last_msg = messages.data[0]
                print(f"\n--- SENTINEL REPORT ---\n{last_msg.content[0].text.value}\n------------------------\n")
                break
            else:
                logger.error(f"Run failed/cancelled: {run.status}")
                break

    async def cleanup(self):
        await self.mcp_manager.disconnect_all()

if __name__ == "__main__":
    pass
