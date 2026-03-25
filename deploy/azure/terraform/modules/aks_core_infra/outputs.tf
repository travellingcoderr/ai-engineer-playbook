output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "resource_group_id" {
  value = azurerm_resource_group.this.id
}

output "acr_login_server" {
  value = azurerm_container_registry.this.login_server
}

output "acr_id" {
  value = azurerm_container_registry.this.id
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "aks_namespace" {
  value = var.aks_namespace
}

output "aks_kubelet_object_id" {
  value = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
}

output "aks_keyvault_csi_object_id" {
  value = var.enable_keyvault_csi ? azurerm_kubernetes_cluster.this.key_vault_secrets_provider[0].secret_identity[0].object_id : null
}

output "aks_keyvault_csi_client_id" {
  value = var.enable_keyvault_csi ? azurerm_kubernetes_cluster.this.key_vault_secrets_provider[0].secret_identity[0].client_id : null
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}

output "key_vault_id" {
  value = azurerm_key_vault.this.id
}
