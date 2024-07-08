output "record" {
  description = "Cloudflare record for the BWAPP instance"
  value       = cloudflare_record.bwapp_dns.name
}
