terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.35.0"
    }
  }
}

data "cloudflare_zone" "msi_domain_zone" {
  name = var.domain
}

resource "cloudflare_record" "vampi_dns" {
  zone_id = data.cloudflare_zone.msi_domain_zone.id
  name    = "vampi"
  value   = var.instance_public_ip
  type    = "A"
  ttl     = 1
  proxied = true
}