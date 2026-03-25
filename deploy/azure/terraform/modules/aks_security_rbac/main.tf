data "azuread_service_principal" "github_actions" {
  count     = var.enable_github_actions_role_assignments ? 1 : 0
  client_id = var.github_actions_client_id
}

resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = var.aks_kubelet_object_id
  role_definition_name             = "AcrPull"
  scope                            = var.acr_id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "aks_keyvault_secrets_user" {
  count                = var.enable_keyvault_csi ? 1 : 0
  principal_id         = var.aks_keyvault_csi_object_id
  role_definition_name = "Key Vault Secrets User"
  scope                = var.key_vault_id
}

resource "azurerm_role_assignment" "aks_keyvault_certificate_user" {
  count                = var.enable_keyvault_csi ? 1 : 0
  principal_id         = var.aks_keyvault_csi_object_id
  role_definition_name = "Key Vault Certificate User"
  scope                = var.key_vault_id
}

resource "azurerm_role_assignment" "key_vault_secrets_officer" {
  for_each             = toset(var.key_vault_secrets_officer_object_ids)
  principal_id         = each.value
  role_definition_name = "Key Vault Secrets Officer"
  scope                = var.key_vault_id
}

resource "azurerm_role_assignment" "github_actions_reader_subscription" {
  count                = var.enable_github_actions_role_assignments && !var.enable_github_actions_subscription_contributor ? 1 : 0
  principal_id         = data.azuread_service_principal.github_actions[0].object_id
  role_definition_name = "Reader"
  scope                = "/subscriptions/${var.azure_subscription_id}"
}

resource "azurerm_role_assignment" "github_actions_contributor_subscription" {
  count                = var.enable_github_actions_role_assignments && var.enable_github_actions_subscription_contributor ? 1 : 0
  principal_id         = data.azuread_service_principal.github_actions[0].object_id
  role_definition_name = "Contributor"
  scope                = "/subscriptions/${var.azure_subscription_id}"
}

resource "azurerm_role_assignment" "github_actions_contributor_rg" {
  count                = var.enable_github_actions_role_assignments ? 1 : 0
  principal_id         = data.azuread_service_principal.github_actions[0].object_id
  role_definition_name = "Contributor"
  scope                = var.resource_group_id
}

resource "azurerm_role_assignment" "github_actions_acr_push" {
  count                = var.enable_github_actions_role_assignments ? 1 : 0
  principal_id         = data.azuread_service_principal.github_actions[0].object_id
  role_definition_name = "AcrPush"
  scope                = var.acr_id
}

resource "azurerm_role_assignment" "github_actions_acr_pull" {
  count                = var.enable_github_actions_role_assignments ? 1 : 0
  principal_id         = data.azuread_service_principal.github_actions[0].object_id
  role_definition_name = "AcrPull"
  scope                = var.acr_id
}
