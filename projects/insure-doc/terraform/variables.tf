# InsureDoc: Terraform Global Variables
# ---------------------------------------------------------------------------------------
# VALUE: This is the 'Control Panel'. It allows you to duplicate the 
# environment (e.g., prod vs staging) by just changing these values.
# ---------------------------------------------------------------------------------------

variable "resource_group" {
  description = "The logical container for all InsureDoc app resources."
  type        = string
  default     = "rg-insuredoc-final"
}

variable "location" {
  description = "The Azure region to deploy into. South Central US is a massive hub with great Trial availability."
  type        = string
  default     = "southcentralus"
}

variable "tenant_id" {
  description = "The Azure Active Directory Tenant ID (found in the Azure Portal)."
  type        = string
}

variable "suffix" {
  description = "A short unique string to prevent resource name collisions (e.g., kv-insuredoc-scus01)."
  type        = string
  default     = "scus01"
}
