data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_container_registry" "this" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = var.tags
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

    upgrade_settings {
      max_surge       = var.aks_node_pool_max_surge
      max_unavailable = "1"
    }
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

  tags = var.tags
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
  tags                       = var.tags
}
