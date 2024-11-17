variable "root_domain" {
  description = "Application root domain"
  type        = string
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  default     = "ami-08c40ec9ead489470"  # Ubuntu Server 20.04 LTS AMI
  type        = string
}

variable "key_name" {
  description = "The name of the key pair to use for the instance."
  default     = "msi-keypair"
  type        = string
}

variable "instance_type" {
  description = "The instance type for the EC2 instance."
  default     = "t2.micro"
  type        = string 
}
