variable "azure_subscription_id" {
  type = string
}

variable "resource_group_id" {
  type = string
}

variable "acr_id" {
  type = string
}

variable "key_vault_id" {
  type = string
}

variable "aks_kubelet_object_id" {
  type = string
}

variable "aks_keyvault_csi_object_id" {
  type    = string
  default = null
}

variable "enable_keyvault_csi" {
  type    = bool
  default = true
}

variable "enable_rbac_role_assignments" {
  type    = bool
  default = true
}

variable "github_actions_client_id" {
  type    = string
  default = ""
}

variable "enable_github_actions_role_assignments" {
  type    = bool
  default = false
}

variable "enable_github_actions_subscription_contributor" {
  type    = bool
  default = false
}

variable "enable_github_actions_user_access_administrator" {
  type    = bool
  default = true
}

variable "key_vault_secrets_officer_object_ids" {
  type    = list(string)
  default = []
}
