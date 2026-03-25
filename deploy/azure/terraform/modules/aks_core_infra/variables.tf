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

variable "aks_namespace" {
  type = string
}

variable "key_vault_name" {
  type = string
}

variable "enable_app_routing" {
  type    = bool
  default = true
}

variable "enable_keyvault_csi" {
  type    = bool
  default = true
}

variable "tags" {
  type    = map(string)
  default = {}
}
