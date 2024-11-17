output "instance_id" {
  description = "VAmPI EC2 Instance ID"
  value       = aws_instance.vampi.id
}

output "public_ip" {
  description = "VAmPI EC2 Instance Public IP"
  value       = aws_instance.vampi.public_ip
}

output "public_dns" {
  description = "VAmPI EC2 Instance Public DNS"
  value       = aws_instance.vampi.public_dns
}