from app.services.providers.mock_provider import MockAzureProvider
from app.models.gateway_models import GatewayConfig

class ProviderFactory:
    """
    Factory to create provider instances based on configuration.
    """
    
    @staticmethod
    def create_providers(config: GatewayConfig):
        providers = []
        
        if config.mode == "simulation":
            # In simulation mode, we create multiple mock regions to test failover
            providers.append(MockAzureProvider(region="eastus", failure_rate=0.4)) # High fail rate to trigger failover
            providers.append(MockAzureProvider(region="westeurope", failure_rate=0.0))
            providers.append(MockAzureProvider(region="japaneast", failure_rate=0.0))
        else:
            # Production mode logic would go here
            # for p in config.providers: ...
            pass
            
        return providers
