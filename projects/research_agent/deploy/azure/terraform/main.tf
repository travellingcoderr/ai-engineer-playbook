# This Terraform configuration creates the following Azure resources:
# 1. Resource Group: To manage related resources
# 2. Container Registry (ACR): To store and manage Docker images
# 3. Kubernetes Cluster (AKS): To run containerized applications
# 4. Key Vault: To securely store secrets, keys, and certificates
# 5. Role Assignments:
#    - AcrPull: Allows AKS to pull images from ACR
#    - Key Vault Secrets User: Allows AKS to read secrets from Key Vault (if enabled)
#    - Key Vault Certificate User: Allows AKS to read certificates from Key Vault (if enabled)

data "azurerm_client_config" "current" {}

locals {
  common_tags = {
    Scope = "Beta"
  }
}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_container_registry" "this" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = local.common_tags
}

resource "azurerm_kubernetes_cluster" "this" {
  name                = var.aks_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  dns_prefix          = "${var.aks_name}-dns"

  default_node_pool {
    name       = "system"
    node_count = var.aks_node_count
    vm_size    = var.aks_vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  dynamic "key_vault_secrets_provider" {
    for_each = var.enable_keyvault_csi ? [1] : []
    content {
      secret_rotation_enabled = true
    }
  }

  dynamic "web_app_routing" {
    for_each = var.enable_app_routing ? [1] : []
    content {
      dns_zone_ids = []
    }
  }

  tags = local.common_tags
}

resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.this.id
  skip_service_principal_aad_check = true
}

resource "azurerm_key_vault" "this" {
  name                       = var.key_vault_name
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  rbac_authorization_enabled = true
  tags                       = local.common_tags
}

resource "azurerm_role_assignment" "aks_keyvault_secrets_user" {
  count                = var.enable_keyvault_csi ? 1 : 0
  principal_id         = azurerm_kubernetes_cluster.this.key_vault_secrets_provider[0].secret_identity[0].object_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.this.id
}

resource "azurerm_role_assignment" "aks_keyvault_certificate_user" {
  count                = var.enable_keyvault_csi ? 1 : 0
  principal_id         = azurerm_kubernetes_cluster.this.key_vault_secrets_provider[0].secret_identity[0].object_id
  role_definition_name = "Key Vault Certificate User"
  scope                = azurerm_key_vault.this.id
}
