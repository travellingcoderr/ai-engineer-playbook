output "resource_group_name" { value = module.aks_service.resource_group_name }
output "acr_login_server" { value = module.aks_service.acr_login_server }
output "aks_name" { value = module.aks_service.aks_name }
output "aks_namespace" { value = module.aks_service.aks_namespace }
output "aks_keyvault_csi_client_id" { value = module.aks_service.aks_keyvault_csi_client_id }
output "key_vault_name" { value = module.aks_service.key_vault_name }
