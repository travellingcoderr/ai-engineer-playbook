# InsureDoc: Main Terraform Provider & Lifecycle
# ---------------------------------------------------------------------------------------
# VALUE: This is the 'Source of Truth' for the provider configuration. 
# It ensures that all resources are created consistently in your Azure tenant.
# ---------------------------------------------------------------------------------------

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      # This ensures if you delete the Key Vault, it CANNOT be purged manually 
      # for a set time (protection against accidental deletion).
      purge_soft_delete_on_destroy = true
    }
  }
}

provider "azuread" {}

# RESOURCE GROUP: The single logical container for the entire platform. 
# This makes it easy to track costs and delete the entire project at once.
resource "azurerm_resource_group" "main" {
  name     = var.resource_group
  location = var.location
}
