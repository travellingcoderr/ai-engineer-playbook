variable "azure_subscription_id" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "acr_name" {
  type = string
}

variable "aks_name" {
  type = string
}

variable "aks_node_count" {
  type    = number
  default = 1
}

variable "aks_vm_size" {
  type    = string
  default = "Standard_DC2as_v5"
}

variable "aks_node_pool_max_surge" {
  type    = string
  default = "0"
}

variable "aks_namespace" {
  type    = string
  default = "rag-system-dev"
}

variable "key_vault_name" {
  type = string
}

variable "enable_rbac_role_assignments" {
  type    = bool
  default = true
}

variable "enable_app_routing" {
  type    = bool
  default = true
}

variable "enable_keyvault_csi" {
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

variable "enable_github_actions_subscription_role_assignments" {
  type    = bool
  default = true
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
