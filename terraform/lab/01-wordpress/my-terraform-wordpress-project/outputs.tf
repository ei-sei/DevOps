output "public_ip" {
  description = "Public IP of the WordPress instance"
  value       = aws_instance.my_ec2.public_ip
}

output "public_dns" {
  description = "Public DNS name of the WordPress instance"
  value       = aws_instance.my_ec2.public_dns
}

output "wordpress_url" {
  description = "URL to open in your browser to finish WordPress setup"
  value       = "http://${aws_instance.my_ec2.public_ip}"
}