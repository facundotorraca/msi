output "ec2_instance_id" {
  description = "VAmPI EC2 Instance ID"
  value       = module.vampi_ec2.instance_id
}

output "ec2_public_ip" {
  description = "VAmPI EC2 Instance Public IP"
  value       = module.vampi_ec2.public_ip
}

output "ec2_public_dns" {
  description = "VAmPI EC2 Instance Public DNS"
  value       = module.vampi_ec2.public_dns
}

output "cloudflare_record" {
  description = "Cloudflare record for the VAmPI instance"
  value       = module.vampi_cloudflare.record
}