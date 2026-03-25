output "fqdn" {
  value = azurerm_dns_a_record.this.fqdn
}

output "record_name" {
  value = azurerm_dns_a_record.this.name
}
