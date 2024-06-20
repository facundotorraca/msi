variable "domain" {
  description = "Application domain"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to create resources in"
  default     = "us-east-1"
}

variable "cloudflare_token" {
  description = "API key for Cloudflare account"
  type        = string
}
