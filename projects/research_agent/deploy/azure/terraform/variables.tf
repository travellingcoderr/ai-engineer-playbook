variable "azure_subscription_id" {
  type        = string
  description = "Azure subscription id"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group for research agent resources"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "acr_name" {
  type        = string
  description = "Azure Container Registry name"
}

variable "aks_name" {
  type        = string
  description = "AKS cluster name"
}

variable "aks_node_count" {
  type        = number
  description = "AKS node count"
  default     = 1
}

variable "aks_vm_size" {
  type        = string
  description = "AKS node VM size"
  default     = "Standard_DC2as_v5"
}

variable "aks_node_pool_max_surge" {
  type        = string
  description = "AKS node pool max surge used during upgrades"
  default     = "1"
}

variable "aks_namespace" {
  type        = string
  description = "Kubernetes namespace for the app"
  default     = "research-agent"
}

variable "key_vault_name" {
  type        = string
  description = "Azure Key Vault name"
}

variable "enable_app_routing" {
  type        = bool
  description = "Enable AKS web app routing add-on"
  default     = true
}

variable "enable_keyvault_csi" {
  type        = bool
  description = "Enable AKS Azure Key Vault CSI add-on"
  default     = true
}

variable "enable_rbac_role_assignments" {
  type        = bool
  description = "Whether Terraform should create Azure RBAC role assignments"
  default     = true
}

variable "github_actions_client_id" {
  type        = string
  description = "Client ID of the GitHub Actions Entra application used by azure/login"
  default     = ""
}

variable "enable_github_actions_role_assignments" {
  type        = bool
  description = "Whether to assign Azure RBAC roles to the GitHub Actions Entra application"
  default     = false
}

variable "enable_github_actions_subscription_role_assignments" {
  type        = bool
  description = "Whether Terraform should manage subscription-level Azure RBAC roles for the GitHub Actions Entra application"
  default     = true
}

variable "enable_github_actions_subscription_contributor" {
  type        = bool
  description = "Whether to assign subscription-level Contributor to the GitHub Actions Entra application"
  default     = false
}

variable "enable_github_actions_user_access_administrator" {
  type        = bool
  description = "Whether to assign subscription-level User Access Administrator to the GitHub Actions Entra application"
  default     = true
}

variable "key_vault_secrets_officer_object_ids" {
  type        = list(string)
  description = "Object IDs that should be allowed to create and manage secrets in the project Key Vault"
  default     = []
}
