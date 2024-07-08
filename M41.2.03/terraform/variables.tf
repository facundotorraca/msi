variable "app_domain" {
  description = "Application domain"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
}

variable "cloudflare_token" {
  description = "API key for Cloudflare account"
  type        = string
}
