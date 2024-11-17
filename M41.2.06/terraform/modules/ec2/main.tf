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
              set -e  # Exit on any error

              # Enable logging
              exec > >(tee /var/log/user-data.log|logger -t user-data) 2>&1

              echo "Starting user-data script..."

              # Wait for cloud-init to complete
              echo "Waiting for cloud-init to complete..."
              cloud-init status --wait || echo "Cloud-init wait failed"

              # Update and upgrade packages
              echo "Updating package list and upgrading packages..."
              apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y || echo "Failed to update/upgrade packages"

              # Install required packages
              echo "Installing required packages..."
              apt-get install -y \
                  apt-transport-https \
                  ca-certificates \
                  curl \
                  software-properties-common \
                  git || echo "Failed to install required packages"

              # Install Docker
              echo "Installing Docker..."
              curl -fsSL https://get.docker.com -o get-docker.sh || echo "Failed to download Docker installation script"
              sh get-docker.sh || echo "Failed to install Docker"

              # Add ubuntu user to docker group
              echo "Adding ubuntu user to Docker group..."
              usermod -aG docker ubuntu || echo "Failed to add ubuntu to docker group"

              # Install Docker Compose
              echo "Installing Docker Compose..."
              curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose || echo "Failed to download Docker Compose"
              chmod +x /usr/local/bin/docker-compose || echo "Failed to set permissions for Docker Compose"

              # Clone VAmPI repository
              echo "Cloning VAmPI repository..."
              git clone https://github.com/erev0s/VAmPI.git /opt/vampi || echo "Failed to clone VAmPI repository"

              # Set correct permissions
              echo "Setting permissions for VAmPI..."
              chown -R ubuntu:ubuntu /opt/vampi || echo "Failed to set permissions for VAmPI"

              # Update Docker Compose configuration
              echo "Updating Docker Compose configuration..."
              sed -i 's/5000:5000/80:5000/' /opt/vampi/docker-compose.yml || echo "Failed to update Docker Compose configuration"

              # Deploy VAmPI
              echo "Deploying VAmPI..."
              cd /opt/vampi || echo "Failed to change directory to /opt/vampi"
              docker-compose up -d || echo "Failed to start VAmPI with Docker Compose"

              echo "User-data script completed successfully."
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