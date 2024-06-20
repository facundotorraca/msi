terraform {
  required_providers {
    cloudflare = {
      source = "cloudflare/cloudflare"
      version = "4.35.0"
    }
  }
}

data "cloudflare_zones" "my_zone" {
  filter {
    name = var.domain
  }
}

resource "cloudflare_record" "bwapp" {
  zone_id = data.cloudflare_zones.my_zone.id
  name    = var.domain
  value   = var.instance_public_ip
  type    = "A"
  ttl     = 1
  proxied = true
}
