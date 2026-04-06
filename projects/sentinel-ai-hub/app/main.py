import asyncio
import json
import logging
import os
from dotenv import load_dotenv
from azure.eventhub.aio import EventHubConsumerClient
from app.agents.orchestrator_agent import SentinelOrchestratorAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_event(partition_context, event):
    """
    Callback for when a new event is received from Event Hub.
    """
    logger.info(f"Received event from partition: {partition_context.partition_id}")
    
    try:
        event_data = json.loads(event.body_as_str())
        # The orchestrator is passed via partition_context or global (for simple demo)
        # Here we use a global reference set in main()
        await orchestrator.process_event(event_data)
        
        # Checkpoint is optional for demo but good practice
        # await partition_context.update_checkpoint(event)
    except Exception as e:
        logger.error(f"Error processing event: {e}")

async def main():
    load_dotenv()
    
    global orchestrator
    orchestrator = SentinelOrchestratorAgent()
    
    # 1. Initialize Orchestrator (MCP, Agents)
    logger.info("Initializing Sentinel Orchestrator...")
    await orchestrator.setup()
    
    # 2. Setup Event Hub Consumer
    connection_str = os.getenv("EVENTHUB_CONNECTION_STR")
    eventhub_name = os.getenv("EVENTHUB_NAME")
    consumer_group = "$Default"

    if not connection_str or not eventhub_name:
        logger.warning("Event Hub configuration missing. Switching to SIMULATION MODE.")
        # Simulation mode: trigger a sample event manually
        sample_event = {
            "event_type": "Hurricane Alert",
            "city": "Miami",
            "severity": 8,
            "details": "Major hurricane approaching the coast. Potential impact on Warehouse A."
        }
        await orchestrator.process_event(sample_event)
        await orchestrator.cleanup()
        return

    client = EventHubConsumerClient.from_connection_string(
        conn_str=connection_str,
        consumer_group=consumer_group,
        eventhub_name=eventhub_name
    )

    logger.info(f"Listening for events on Event Hub: {eventhub_name}...")
    async with client:
        await client.receive(on_event=on_event, starting_position="-1")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Sentinel shutting down.")
