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
              
              # Wait for cloud-init to complete
              cloud-init status --wait

              # Update package list and upgrade packages
              apt-get update
              DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

              # Install required packages
              apt-get install -y \
                  apt-transport-https \
                  ca-certificates \
                  curl \
                  software-properties-common \
                  git

              # Install Docker
              curl -fsSL https://get.docker.com -o get-docker.sh
              sh get-docker.sh

              # Add ubuntu user to docker group
              usermod -aG docker ubuntu

              # Install Docker Compose
              curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose

              # Clone VAmPI repository
              git clone https://github.com/erev0s/VAmPI.git /opt/vampi

              # Set correct permissions
              chown -R ubuntu:ubuntu /opt/vampi

              # Update Docker Compose configuration
              sed -i 's/5000:5000/80:5000/' /opt/vampi/docker-compose.yml

              # Deploy VAmPI
              cd /opt/vampi
              docker-compose up -d
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