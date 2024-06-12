provider "aws" {
  region = var.aws_region
}

module "bwapp_ec2_instance" {
  source = "./modules/ec2"
}

