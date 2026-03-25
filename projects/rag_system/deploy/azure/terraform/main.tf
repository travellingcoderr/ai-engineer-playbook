module "aks_service" {
  source = "../../../../../deploy/azure/terraform/modules/aks_service"

  azure_subscription_id                  = var.azure_subscription_id
  resource_group_name                    = var.resource_group_name
  location                               = var.location
  acr_name                               = var.acr_name
  aks_name                               = var.aks_name
  aks_node_count                         = var.aks_node_count
  aks_vm_size                            = var.aks_vm_size
  aks_namespace                          = var.aks_namespace
  key_vault_name                         = var.key_vault_name
  enable_app_routing                     = var.enable_app_routing
  enable_keyvault_csi                    = var.enable_keyvault_csi
  github_actions_client_id               = var.github_actions_client_id
  enable_github_actions_role_assignments = var.enable_github_actions_role_assignments
  key_vault_secrets_officer_object_ids   = var.key_vault_secrets_officer_object_ids
}
