output "public_ip" {
  description = "Public IP of the WordPress instance"
  value       = module.compute.public_ip
}

output "public_dns" {
  description = "Public DNS name of the WordPress instance"
  value       = module.compute.public_dns
}

output "wordpress_url" {
  description = "URL to open in your browser to finish WordPress setup"
  value       = "http://${module.compute.public_ip}"
}