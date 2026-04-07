import logging
import os
from typing import List, Dict, Any
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponderAgent:
    """
    [RESPONDER AGENT] - SDK v2.0.0 Patterns
    It uses MCP tools (Mock, Slack, Google Maps) for real-time actions.
    """
    NAME = "responder"
    MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    INSTRUCTIONS = (
        "You are a Logistics and Dispatch Specialist. "
        "Your goal is to mitigate business disruptions. "
        "SAFETY FIRST: Always ensure your responses omit sensitive PII or warehouse security codes. "
        "Only suggest actions that are safe for personnel. "
        "Always follow these steps:\n"
        "1. **Analyze**: Assess risk using 'calculate_risk_index'.\n"
        "2. **Research**: Verify inventory and shipment status.\n"
        "3. **Reflect**: Review your gathered data against the SLA. Are your proposed actions compliant with the penalty clauses? Critique your own plan before posting.\n"
        "4. **Execute**: Use Maps to check for proximity and post the final plan to Slack."
    )

    @staticmethod
    def get_definition() -> PromptAgentDefinition:
        """Returns the PromptAgentDefinition for SDK v2.0.0+."""
        return PromptAgentDefinition(
            model=ResponderAgent.MODEL,
            instructions=ResponderAgent.INSTRUCTIONS,
            tools=ResponderAgent.get_tools()
        )

    @staticmethod
    def get_tools() -> List[FunctionTool]:
        """
        Returns a list of FunctionTool objects for the Responder Agent.
        """
        return [
            # --- Mock Supply Chain Tools ---
            FunctionTool(
                name="get_shipment_status",
                description="Get the real-time status of a shipment by its ID.",
                parameters={
                    "type": "object",
                    "properties": {
                        "shipment_id": {"type": "string", "description": "The shipment ID"}
                    },
                    "required": ["shipment_id"]
                }
            ),
            FunctionTool(
                name="calculate_risk_index",
                description="Calculate a disruption risk index (0.0 to 1.0) based on severity.",
                parameters={
                    "type": "object",
                    "properties": {
                        "event_type": {"type": "string"},
                        "city": {"type": "string"},
                        "severity": {"type": "integer"}
                    },
                    "required": ["event_type", "city", "severity"]
                }
            ),
            
            # --- Slack Tools (MCP Server) ---
            FunctionTool(
                name="slack_post_message",
                description="Post a message to a Slack channel.",
                parameters={
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "description": "The channel ID or name"},
                        "text": {"type": "string", "description": "The message text"}
                    },
                    "required": ["channel", "text"]
                }
            ),
            FunctionTool(
                name="slack_list_channels",
                description="List all public Slack channels in the workspace.",
                parameters={"type": "object", "properties": {}}
            ),

            # --- Google Maps Tools (MCP Server) ---
            FunctionTool(
                name="google_maps_geocoding",
                description="Convert an address into geographic coordinates (lat/long).",
                parameters={
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "The address to geocode"}
                    },
                    "required": ["address"]
                }
            ),
            FunctionTool(
                name="google_maps_directions",
                description="Get directions and estimated travel time between two locations.",
                parameters={
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string", "description": "Origin address or lat/long"},
                        "destination": {"type": "string", "description": "Destination address or lat/long"},
                        "mode": {"type": "string", "enum": ["driving", "walking", "bicycling", "transit"]}
                    },
                    "required": ["origin", "destination"]
                }
            )
        ]

if __name__ == "__main__":
    pass
