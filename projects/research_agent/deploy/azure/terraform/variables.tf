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
  default     = "Standard_B2s"
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
