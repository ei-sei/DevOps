variable "aws_region" {
  type        = string
  description = "AWS region to deploy into"
}

variable "instance_type" {
    type = string
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
}