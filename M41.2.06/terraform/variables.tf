variable "root_domain" {
  description = "Application root domain"
  type        = string
  default     = "msi-domain.xyz"
}

variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
  default     = "us-east-1"
}