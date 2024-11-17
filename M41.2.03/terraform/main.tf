terraform {
  backend "s3" {
    bucket         = "ft-msi-terraform"
    key            = "M41.2.03/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
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


module "bwapp_ec2" {
  source = "./modules/ec2"
}

module "bwapp_cloudflare" {
  source             = "./modules/cloudflare"
  domain             = var.root_domain
  instance_public_ip = module.bwapp_ec2.public_ip 
}
