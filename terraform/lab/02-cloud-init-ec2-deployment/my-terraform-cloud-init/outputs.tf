output "public_ip" {
  description = "Public IP of the instance"
  value       = module.compute.public_ip
}

output "url" {
  description = "URL to verify the instance is running"
  value       = "http://${module.compute.public_ip}"
}