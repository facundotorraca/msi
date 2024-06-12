output "instance_id" {
  description = "BWapp EC2 Instance ID"
  value       = aws_instance.bwapp.id
}

output "public_ip" {
  description = "BWapp EC2 Instance Public IP"
  value       = aws_instance.bwapp.public_ip
}

output "public_dns" {
  description = "BWapp EC2 Instance Public DNS"
  value       = aws_instance.bwapp.public_dns
}