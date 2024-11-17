terraform {
  backend "s3" {
    bucket         = "ft-msi-terraform"
    key            = "M41.2.06/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vampi_ec2" {
  source = "./modules/ec2"
}