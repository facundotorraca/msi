variable "domain" {
  description = "The domain to use with Cloudflare"
  type        = string
}

variable "instance_public_ip" {
  description = "The public IP of the EC2 instance"
  type        = string
}
