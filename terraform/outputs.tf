output "ec2_instance_id" {
  description = "BWapp EC2 Instance ID"
  value       = module.bwapp_ec2.instance_id
}

output "ec2_public_ip" {
  description = "BWapp EC2 Instance Public IP"
  value       = module.bwapp_ec2.public_ip
}

output "ec2_public_dns" {
  description = "BWapp EC2 Instance Public DNS"
  value       = module.bwapp_ec2.public_dns
}

output "cloudflare_record" {
  description = "Cloudflare record for the BWAPP instance"
  value       = module.bwapp_cloudflare.record
}
