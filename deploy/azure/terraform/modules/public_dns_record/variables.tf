variable "dns_zone_name" {
  type        = string
  description = "Azure DNS zone name, for example purpletechllc.com"
}

variable "dns_resource_group_name" {
  type        = string
  description = "Resource group that contains the Azure DNS zone"
}

variable "record_name" {
  type        = string
  description = "Relative DNS record name, for example research"
}

variable "ipv4_address" {
  type        = string
  description = "Public IPv4 address to point the DNS A record at"
}

variable "ttl" {
  type        = number
  description = "DNS TTL in seconds"
  default     = 300
}
