# InsureDoc: Key Vault with Private Link Architecture
# ---------------------------------------------------------------------------------------
# VALUE: This is the 'Root of Trust' for the entire platform. 
# It holds TLS certificates for Emissary Ingress and secrets for the AI services.
# ---------------------------------------------------------------------------------------

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                        = "kv-insuredoc-${var.suffix}"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "premium" # Required for Private Link support
  enable_rbac_authorization   = true      # Modern approach: use Azure Roles instead of old Access Policies
  
  # SECURITY: The 'Deny' firewall ensures that no one can reach your secrets via 
  # the public internet, even if they have the password. Access is VNet-only.
  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }
}

# PRIVATE LINK: This creates a virtual network interface (NIC) for the Key Vault 
# inside your VNet. Your AKS pods talk to this private IP, keeping traffic 
# off the Microsoft backbone and the public web.
resource "azurerm_private_endpoint" "kv" {
  name                = "pe-kv-insuredoc"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.endpoints.id

  private_service_connection {
    name                           = "kv-connection"
    private_connection_resource_id = azurerm_key_vault.main.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  # DNS: Critical for translating 'kv-insuredoc.vaultcore.azure.net' to 
  # the private IP address of the endpoint inside the VNet.
  private_dns_zone_group {
    name                 = "kv-dns-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.vault.id]
  }
}
