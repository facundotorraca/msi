terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}

data "aws_route53_zone" "root_domain_zone" {
  name = var.root_domain
  private_zone = false
}

resource "aws_instance" "vampi" {
  ami           = var.ami_id
  instance_type = var.instance_type

  user_data = <<-EOF
              #!/bin/bash
              # Update the package repository
              apt-get update -y
              apt-get upgrade -y

              # Install Docker
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker

              # Pull and run the BWAPP Docker image
              docker pull erev0s/vampi
              docker run -d -p 5000:5000 erev0s/vampi
              EOF

  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.vampi_sg.id]
  tags = { Name = "msi-vampi", project = "msi" }
}

resource "aws_security_group" "vampi_sg" {
  name        = "msi-vamnpi-sg"
  description = "Allow HTTP and SSH traffic into BWapp"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "msi-vampi-sg", project = "msi" }
}

resource "aws_route53_record" "vampi_dns" {
  zone_id = data.aws_route53_zone.root_domain_zone.id
  name    = "vampi.${var.root_domain}"             
  type    = "A"                                    
  ttl     = 300                                    
  records = [aws_instance.vampi.public_ip]
}