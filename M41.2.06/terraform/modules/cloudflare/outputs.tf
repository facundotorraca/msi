output "record" {
  description = "Cloudflare record for the VAmPI instance"
  value       = cloudflare_record.vampi_dns.name
}
