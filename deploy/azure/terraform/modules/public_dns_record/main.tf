# use this module only if your DNS zone is hosted in Azure DNS

resource "azurerm_dns_a_record" "this" {
  name                = var.record_name
  zone_name           = var.dns_zone_name
  resource_group_name = var.dns_resource_group_name
  ttl                 = var.ttl
  records             = [var.ipv4_address]
}
