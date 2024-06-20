terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.54.1"
    }
    cloudflare = {
      source = "cloudflare/cloudflare"
      version = "4.35.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "cloudflare" {
  api_token = var.cloudflare_token
}


module "bwapp_ec2_instance" {
  source = "./modules/ec2"
}

module "bwapp_cloudflare_record" {
  source             = "./modules/cloudflare"
  domain             = var.domain
  instance_public_ip = module.bwapp_ec2_instance.public_ip 
}
