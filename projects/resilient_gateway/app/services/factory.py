from typing import List
from app.services.providers.mock_provider import MockAzureProvider
from app.services.providers.azure_provider import AzureOpenAIProvider
from app.services.providers.base import BaseLLMProvider
from app.models.gateway_models import GatewayConfig

class ProviderFactory:
    """
    Factory to create provider instances based on configuration.
    """
    
    @staticmethod
    def create_providers(config: GatewayConfig) -> List[BaseLLMProvider]:
        providers = []
        
        if config.mode == "simulation":
            # In simulation mode, we create multiple mock regions to test failover
            providers.append(MockAzureProvider(region="eastus", failure_rate=0.4))
            providers.append(MockAzureProvider(region="westeurope", failure_rate=0.0))
            providers.append(MockAzureProvider(region="japaneast", failure_rate=0.0))
        else:
            # Production mode: Instantiate providers based on provided config
            for p_config in config.providers:
                if not p_config.enabled:
                    continue
                
                # We assume "azure" in name or type if we had a type field
                # For now, we use a simple check or assume all are Azure for this mission
                if "azure" in p_config.name.lower():
                    providers.append(AzureOpenAIProvider(
                        name=p_config.name,
                        api_key=p_config.settings.get("api_key", ""),
                        azure_endpoint=p_config.settings.get("azure_endpoint", ""),
                        api_version=p_config.settings.get("api_version", "2024-02-15-preview"),
                        deployment_name=p_config.settings.get("deployment_name")
                    ))
            
        return providers
