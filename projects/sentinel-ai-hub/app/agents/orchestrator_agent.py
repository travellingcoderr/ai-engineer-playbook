import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from openai.types.responses.response_input_param import FunctionCallOutput
from app.core.foundry_client import FoundryProjectManager
from app.agents.policy_expert_agent import PolicyExpertAgent, search_policies
from app.agents.responder_agent import ResponderAgent
from app.tools.mcp_bridge import MultiMCPManager
from app.core.safety_evaluator import SentinelSafetyEvaluator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentinelOrchestratorAgent:
    """
    [ORCHESTRATOR AGENT] - SDK v2.0.0 Hardened
    Main coordinator for Project Sentinel.
    Uses the OpenAI-compatible runtime for tool-driven response generation.
    """
    def __init__(self):
        self.project_manager = FoundryProjectManager()
        self.mcp_manager = MultiMCPManager()
        self.project_client = self.project_manager.client # For Registry Ops
        self.openai_client = self.project_manager.get_openai_client() # For Runtime Ops
        self.agents = {}
        self.safety_evaluator = SentinelSafetyEvaluator()

    async def setup(self):
        """Initialize Multi-MCP connectivity and synchronize agents in Foundry."""
        self.mcp_manager.register_server("mock", "python3", ["app/tools/mcp_server.py"])
        
        slack_token = os.getenv("SLACK_BOT_TOKEN")
        if slack_token and slack_token != "xoxb-...":
            self.mcp_manager.register_server("slack", "npx", ["-y", "@modelcontextprotocol/server-slack"], env={"SLACK_BOT_TOKEN": slack_token})

        await self.mcp_manager.connect_all()
        
        logger.info("Synchronizing Agent versions in Foundry...")
        # Registry operations are on the root project client
        self.agents[PolicyExpertAgent.NAME] = self.project_client.agents.create_version(
            agent_name=PolicyExpertAgent.NAME,
            definition=PolicyExpertAgent.get_definition()
        )
        self.agents[ResponderAgent.NAME] = self.project_client.agents.create_version(
            agent_name=ResponderAgent.NAME,
            definition=ResponderAgent.get_definition()
        )
        logger.info("All agents synchronized.")

    def _get_runtime_tools(self):
        return [
            tool.as_dict()
            for tool in (
                PolicyExpertAgent.get_definition().tools
                + ResponderAgent.get_definition().tools
            )
        ]

    def _get_runtime_instructions(self) -> str:
        return (
            "You are the Sentinel incident orchestrator. "
            "Use search_policies to ground any policy or SLA claim. "
            "Use available logistics and communication tools when they help produce an actionable response. "
            "Do not invent tool results. "
            "If a tool fails, continue with the remaining evidence and clearly note the limitation. "
            "Return a concise operational summary with policy impact, risk assessment, and next actions."
        )

    async def process_event(self, event_data: Dict[str, Any], conversation_id: Optional[str] = None) -> str:
        """
        Main orchestration loop using the Responses API with local tool handling.
        """
        logger.info(f"Processing event: {event_data['event_type']} in {event_data['city']}")

        # 1. Construct contextual prompt.
        prompt = (
            f"URGENT ALERT: {event_data['event_type']} in {event_data['city']}. "
            f"Severity: {event_data['severity']}/10. Details: {event_data['details']}. "
            "1. Search disaster protocols. 2. Check shipment risk via MCP. 3. Post summary to Slack."
        )

        # 2. Start the response loop.
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT", PolicyExpertAgent.MODEL)
        tools = self._get_runtime_tools()
        instructions = self._get_runtime_instructions()
        response = self.openai_client.responses.create(
            input=prompt,
            model=model,
            instructions=instructions,
            tools=tools,
        )

        # 3. Handle tool calls until the model produces a final message.
        while True:
            tool_outputs = []
            for item in response.output:
                if item.type != "function_call":
                    continue

                func_name = item.name
                args = json.loads(item.arguments)

                logger.info(f"Orchestrator invoking tool: {func_name}({args})")
                try:
                    if func_name == "search_policies":
                        output = search_policies(**args)
                        logger.info(f"Search Results retrieved: {str(output)[:500]}...") # Log a snippet
                    else:
                        output = await self.mcp_manager.execute_tool(func_name, args)
                        logger.info(f"Tool '{func_name}' output: {output}")
                except Exception as e:
                    logger.error(f"Tool execution failed: {e}")
                    output = f"Error: {e}"

                tool_outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=output,
                    )
                )

            if tool_outputs:
                response = self.openai_client.responses.create(
                    input=tool_outputs,
                    model=model,
                    instructions=instructions,
                    tools=tools,
                    previous_response_id=response.id,
                )
                await asyncio.sleep(0)
                continue

            final_response = response.output_text
            if not final_response:
                error_msg = f"Agent produced no final text (Status: {response.status})"
                logger.error(error_msg)
                return error_msg

            logger.info("--- AGENT RESPONSE PRODUCED ---")
            logger.info(f"Response Content: {final_response}")
            logger.info("--------------------------------")

            # Validation through local safety guardrails.
            logger.info("Applying Sentinel Safety Evaluator...")
            safety_report = await self.safety_evaluator.validate_response(
                query=prompt,
                response=final_response,
            )
            if safety_report.get("is_safe", True):
                return final_response

            return (
                "Response blocked by safety guardrails. "
                f"Details: {json.dumps(safety_report)}"
            )

    async def cleanup(self):
        await self.mcp_manager.disconnect_all()
        self.project_client.close()

if __name__ == "__main__":
    pass
