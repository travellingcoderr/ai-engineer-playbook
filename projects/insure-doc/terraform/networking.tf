# InsureDoc: Networking & Private DNS Architecture
# ---------------------------------------------------------------------------------------
# VALUE: This is the 'Foundation'. We use a segmented VNet to separate 
# public-facing AKS traffic from backend data storage traffic.
# ---------------------------------------------------------------------------------------

resource "azurerm_virtual_network" "main" {
  name                = "vnet-insuredoc"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}

# AKS SUBNET: Dedicated for the K8s cluster and its Managed Istio sidecars. 
# Isolated from the data-storage subnets.
resource "azurerm_subnet" "aks" {
  name                 = "snet-aks"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# ENDPOINT SUBNET: A 'Private Subnet' where all internal IP addresses 
# for databases (Cosmos/KeyVault) are located.
resource "azurerm_subnet" "endpoints" {
  name                 = "snet-endpoints"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

# PRIVATE DNS ZONES: This is the internal 'Phonebook'. It tells 
# your AKS pods that 'cosmos-insuredoc.mongo.cosmos.azure.com' 
# should resolve to the private VNet IP, not the public web.
resource "azurerm_private_dns_zone" "vault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone" "cosmos" {
  name                = "privatelink.mongo.cosmos.azure.com"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone" "search" {
  name                = "privatelink.search.windows.net"
  resource_group_name = azurerm_resource_group.main.name
}

# DNS LINK: This 'plugs' the DNS phonebook into your VNet.
resource "azurerm_private_dns_zone_virtual_network_link" "vault" {
  name                  = "link-vault"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.vault.name
  virtual_network_id    = azurerm_virtual_network.main.id
}
