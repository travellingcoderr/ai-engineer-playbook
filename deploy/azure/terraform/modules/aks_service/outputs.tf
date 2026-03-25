output "resource_group_name" {
  value = module.core_infra.resource_group_name
}

output "acr_login_server" {
  value = module.core_infra.acr_login_server
}

output "aks_name" {
  value = module.core_infra.aks_name
}

output "aks_namespace" {
  value = module.core_infra.aks_namespace
}

output "aks_keyvault_csi_client_id" {
  value = module.core_infra.aks_keyvault_csi_client_id
}

output "key_vault_name" {
  value = module.core_infra.key_vault_name
}

output "github_actions_role_assignment_enabled" {
  value = module.security_rbac.github_actions_role_assignment_enabled
}
