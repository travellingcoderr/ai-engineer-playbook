# InsureDoc: Terraform Backend Configuration
# ---------------------------------------------------------
# INSTRUCTIONS: 
# 1. Run 'bash scripts/setup-backend.sh'
# 2. Paste the output block below.
# ---------------------------------------------------------

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-insuredoc-tfstate"
    storage_account_name = "stinsu1775183400"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
