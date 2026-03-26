module "core_infra" {
  source = "../aks_core_infra"

  resource_group_name = var.resource_group_name
  location            = var.location
  acr_name            = var.acr_name
  aks_name            = var.aks_name
  aks_node_count      = var.aks_node_count
  aks_vm_size         = var.aks_vm_size
  aks_node_pool_max_surge = var.aks_node_pool_max_surge
  aks_namespace       = var.aks_namespace
  key_vault_name      = var.key_vault_name
  enable_app_routing  = var.enable_app_routing
  enable_keyvault_csi = var.enable_keyvault_csi
  tags                = var.tags
}

module "security_rbac" {
  source = "../aks_security_rbac"

  azure_subscription_id                  = var.azure_subscription_id
  resource_group_id                      = module.core_infra.resource_group_id
  acr_id                                 = module.core_infra.acr_id
  key_vault_id                           = module.core_infra.key_vault_id
  aks_kubelet_object_id                  = module.core_infra.aks_kubelet_object_id
  aks_keyvault_csi_object_id             = module.core_infra.aks_keyvault_csi_object_id
  enable_keyvault_csi                    = var.enable_keyvault_csi
  enable_rbac_role_assignments           = var.enable_rbac_role_assignments
  github_actions_client_id               = var.github_actions_client_id
  enable_github_actions_role_assignments = var.enable_github_actions_role_assignments
  enable_github_actions_subscription_role_assignments = var.enable_github_actions_subscription_role_assignments
  enable_github_actions_subscription_contributor = var.enable_github_actions_subscription_contributor
  enable_github_actions_user_access_administrator = var.enable_github_actions_user_access_administrator
  key_vault_secrets_officer_object_ids   = var.key_vault_secrets_officer_object_ids
}
