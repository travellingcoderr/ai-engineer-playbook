# InsureDoc: AKS with Managed Mesh and Workload Identity
# ---------------------------------------------------------------------------------------
# VALUE: This is the 'Brain' of the platform. By using Managed Istio and 
# Workload Identity, we eliminate 'East-West' traffic sniffing and hardcoded secrets.
# ---------------------------------------------------------------------------------------

resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-insuredoc"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks-insuredoc"
  
  # IDENTITY: Workload Identity allows your pods (Orchestrator, Claim, Ingestion) 
  # to assume an Azure identity and authenticate to Key Vault/CosmosDB without 
  # storing passwords or API keys in code or K8s secrets.
  identity {
    type = "SystemAssigned"
  }
  
  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }

  # SERVICE MESH: Managed Istio ensures all pod-to-pod traffic is encrypted via 
  # Mutual TLS (mTLS). It provides zero-trust security 'out of the box' 
  # without adding any code to your Node.js apps.
  service_mesh_profile {
    mode                             = "Istio"
    internal_ingress_gateway_enabled = true
    external_ingress_gateway_enabled = false # Disabled to save Public IP quota
  }

  # CSI DRIVER: This mounts Azure Key Vault secrets directly into your pods 
  # as local files. If you update a secret in the vault, it rotates the pod 
  # file automatically without a restart.
  key_vault_secrets_provider {
    secret_rotation_enabled = true
  }

  workload_identity_enabled = true
  oidc_issuer_enabled       = true

  default_node_pool {
    name       = "default"
    node_count = 1 # Reduced from 2 to stay within 2-vCPU Free Trial limits
    vm_size    = "Standard_B2s" # Universally available burstable SKU for Trials
    vnet_subnet_id = azurerm_subnet.aks.id
  }
}
