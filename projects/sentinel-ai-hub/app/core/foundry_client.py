import os
import logging
from typing import Optional
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoundryProjectManager:
    """
    Central manager for Azure AI Foundry Project interactions.
    Handles authentication and provides access to Project-level sub-clients.
    """
    def __init__(self, connection_string: Optional[str] = None):
        load_dotenv()
        self.connection_string = connection_string or os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
        
        if not self.connection_string:
            raise ValueError("AZURE_AI_PROJECT_CONNECTION_STRING not found in environment.")

        # DefaultAzureCredential works best with 'az login' locally
        self.credential = DefaultAzureCredential()
        
        self.client = AIProjectClient.from_connection_string(
            connection_string=self.connection_string,
            credential=self.credential
        )
        logger.info("AIProjectClient initialized successfully.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_agents_client(self):
        """Returns the sub-client for Agent operations."""
        return self.client.agents

    def get_search_connection(self):
        """
        Retrieves the connection details for the Azure AI Search service 
        linked to this project.
        """
        # This is useful if we want to dynamically find the search endpoint
        connections = self.client.connections.list()
        for conn in connections:
            if conn.connection_type == "CognitiveSearch":
                return conn
        return None

if __name__ == "__main__":
    # Quick test
    try:
        with FoundryProjectManager() as manager:
            print("Foundry Project Manager is ready.")
    except Exception as e:
        print(f"Error: {e}")
