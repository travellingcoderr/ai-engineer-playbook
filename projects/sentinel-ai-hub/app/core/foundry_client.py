import os
import logging
from typing import Optional
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoundryProjectManager:
    """
    Central manager for Azure AI Foundry Project interactions.
    Handles authentication and provides access to Project-level sub-clients 
    using the SDK v2.0.0+ endpoint-based pattern.
    """
    def __init__(self, endpoint: Optional[str] = None):
        load_dotenv()
        # Loading from new AZURE_AI_PROJECT_ENDPOINT
        self.endpoint = endpoint or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        
        if not self.endpoint:
            logger.error("FAILED to load AZURE_AI_PROJECT_ENDPOINT from .env")
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT not found in environment.")

        # Verification log
        masked_endpoint = f"{self.endpoint[:15]}...{self.endpoint[-15:]}"
        logger.info(f"Connecting to Foundry Project at: {masked_endpoint}")
        
        self.credential = DefaultAzureCredential()
        
        # v2.0.0 Unified Client Initialization
        self.client = AIProjectClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        logger.info("AIProjectClient (v2.0.0) initialized successfully.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_agents_client(self):
        """Returns the unified Agents operations client."""
        return self.client.agents

    def get_openai_client(self):
        """
        Returns an authenticated OpenAI client for runtime inference.

        Prefer the direct Azure OpenAI endpoint when configured because it is the
        most stable path for model inference. Fall back to the project-scoped
        Foundry runtime only when no direct endpoint is available.
        """
        legacy_api_version = os.getenv("AZURE_AI_AGENTS_API_VERSION")
        if legacy_api_version:
            logger.warning(
                "Ignoring deprecated AZURE_AI_AGENTS_API_VERSION=%s. "
                "azure-ai-projects now manages the runtime API surface.",
                legacy_api_version,
            )

        aoai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if aoai_endpoint:
            logger.info("Using direct Azure OpenAI runtime endpoint for inference.")
            return OpenAI(
                base_url=f"{aoai_endpoint.rstrip('/')}/openai/v1/",
                api_key=get_bearer_token_provider(
                    self.credential,
                    "https://cognitiveservices.azure.com/.default",
                ),
            )

        return self.client.get_openai_client()

    def get_search_connection(self):
        """
        Retrieves the connection details for the Azure AI Search service 
        linked to this project.
        """
        connections = self.client.connections.list()
        for conn in connections:
            if conn.connection_type == "CognitiveSearch":
                return conn
        return None

if __name__ == "__main__":
    # Quick test
    try:
        with FoundryProjectManager() as manager:
            print("Foundry Project Manager (v2.0.0) is ready.")
    except Exception as e:
        print(f"Error: {e}")
