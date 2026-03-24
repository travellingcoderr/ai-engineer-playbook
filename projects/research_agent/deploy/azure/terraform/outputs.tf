output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "acr_login_server" {
  value = azurerm_container_registry.this.login_server
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "aks_namespace" {
  value = var.aks_namespace
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}
