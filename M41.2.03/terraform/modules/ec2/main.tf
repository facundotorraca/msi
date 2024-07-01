terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}

resource "aws_instance" "bwapp" {
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
              docker pull raesene/bwapp
              docker run -d -p 80:80 raesene/bwapp
              EOF

  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.bwapp_sg.id]
  tags = { Name = "msi-bwapp", project = "msi" }
}

resource "aws_security_group" "bwapp_sg" {
  name        = "msi-bwapp-sg"
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

  tags = { Name = "msi-bwapp-sg", project = "msi" }
}
