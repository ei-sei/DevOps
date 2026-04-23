variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
}

variable "instance_type" {
  type = string
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to attach the security group to"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID to place the EC2 instance in"
}

variable "user_data" {
  type        = string
  description = "Cloud-init config to run on boot"
  default     = null
}