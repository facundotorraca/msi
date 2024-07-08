terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.35.0"
    }
  }
}

data "cloudflare_zone" "bwapp_domain_zone" {
  name = var.domain
}

resource "cloudflare_record" "bwapp_dns" {
  zone_id = data.cloudflare_zone.bwapp_domain_zone.id
  name    = var.domain
  value   = var.instance_public_ip
  type    = "A"
  ttl     = 1
  proxied = true
}

resource "cloudflare_ruleset" "bwapp_waf_ruleset" {
  zone_id     = data.cloudflare_zone.bwapp_domain_zone.id
  name        = "msi-bwapp-waf"
  description = "MSI BWAPP WAF Ruleset"
  kind        = "zone"
  phase       = "http_request_firewall_custom"

  rules {
    action      = "block"
    enabled     = true
    description = "sql-injections"
    expression  = "(http.request.method eq \"GET\" and (http.request.uri.query contains \"select\" or http.request.uri.query contains \"insert\" or http.request.uri.query contains \"drop\" or http.request.uri.query contains \"union\" or http.request.uri.query contains \"update\" or http.request.uri.query contains \"exec\" or http.request.uri.query contains \"delete\"))"
  }

  rules {
    action      = "block"
    enabled     = true
    description = "xss-injections"
    expression  = "(http.request.method eq \"GET\" and (http.request.uri.query contains \"<script>\" or http.request.uri.query contains \"%3Cscript%3E\"))"
  }

  rules {
    action      = "block"
    enabled     = true
    description = "command-injections"
    expression  = "(http.request.method eq \"GET\" and (http.request.full_uri contains \"&&\" or http.request.full_uri contains \"|\"))"
  }

  rules {
    action      = "block"
    enabled     = true
    description = "path-traversal"
    expression  = "(http.request.method eq \"GET\" and (http.request.uri.path contains \"../\" or http.request.uri.path contains \"..%2f\"))"
  }

  rules {
    action      = "block"
    enabled     = true
    description = "suspicous-user-agent"
    expression  = "(http.request.headers[\"user-agent\"][0] contains \"sqlmap\")"
  }
}