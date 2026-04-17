# Terraform Tutorial

A step-by-step guide to provisioning AWS infrastructure with Terraform.

---

## Prerequisites

- [Terraform installed](https://developer.hashicorp.com/terraform/install)
- AWS CLI installed and configured (`aws configure`)
- An AWS account

---

## Project Structure

Split your config across files - Terraform reads all `.tf` files in the folder together:

```
my-terraform-project/
  providers.tf      # terraform block and provider config
  variables.tf      # input variable definitions
  terraform.tfvars  # actual variable values (add to .gitignore if sensitive)
  main.tf           # resources and data sources
  outputs.tf        # output definitions
```

---

## Step 1 - Create a Project Folder

```bash
mkdir my-terraform-project
cd my-terraform-project
```

---

## Step 2 - providers.tf

```hcl
terraform {
  # Meta-configuration for Terraform itself (not what you're building)
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"  # Allow 6.x only - prevents breaking changes from 7.0+
    }
  }
}

provider "aws" {        # tells Terraform which provider to configure
  region = var.aws_region
}
```

---

## Step 3 - variables.tf

No defaults - forces values to be explicitly set in `terraform.tfvars`:

```hcl
variable "aws_region" {
  type        = string
  description = "AWS region to deploy into"
}

variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
}
```

---

## Step 4 - terraform.tfvars

```hcl
aws_region  = "eu-west-2"
bucket_name = "<your-unique-bucket-name>"
environment = "dev"
```

> S3 bucket names are globally unique across all AWS accounts. Use your username as a prefix to avoid clashes, e.g. `mruniquename-dev-bucket-2026`.

---

## Step 5 - main.tf

```hcl
# S3 Bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
  }
}

# Extra buckets using count
resource "aws_s3_bucket" "extra_buckets" {
  count  = 2
  bucket = "${var.bucket_name}-extra-${count.index}"

  tags = {
    Environment = var.environment
  }
}

# EC2 Instance - uses data source to get AMI automatically
resource "aws_instance" "my_ec2" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  tags = {
    Name        = "my-ec2"
    Environment = var.environment
  }
}

# Data source - looks up latest Amazon Linux 2 AMI for the current region
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

---

## Step 6 - outputs.tf

```hcl
output "bucket_name" {
  value = aws_s3_bucket.my_bucket.id
}

output "extra_bucket_names" {
  value = aws_s3_bucket.extra_buckets[*].id
}

output "ec2_instance_id" {
  value = aws_instance.my_ec2.id
}

output "ec2_public_ip" {
  value = aws_instance.my_ec2.public_ip
}
```

---

## Step 7 - terraform init

```bash
terraform init
```

If you update the provider version later, run `terraform init -upgrade` to update the lock file.

---

## Step 8 - terraform validate

```bash
terraform validate
```

Checks your config is valid before touching any real infrastructure.

---

## Step 9 - terraform plan

```bash
terraform plan
```

You should see `4 to add` - the S3 bucket, 2 extra buckets, and the EC2 instance.

---

## Step 10 - terraform apply

```bash
terraform apply
```

Type `yes` to confirm. After it completes, Terraform prints your outputs:

```
Outputs:

bucket_name        = "your-bucket-name"
extra_bucket_names = ["your-bucket-name-extra-0", "your-bucket-name-extra-1"]
ec2_instance_id    = "i-0abc123..."
ec2_public_ip      = "18.x.x.x"
```

Check the AWS console to verify all resources exist.

---

## Step 11 - Inspect the State File

```bash
cat terraform.tfstate
```

Terraform tracks every resource and its attributes here. Never delete or manually edit this file.

---

## Step 12 - terraform destroy

```bash
terraform destroy
```

Type `yes` to confirm. All resources Terraform created will be deleted.

---

## Summary

| Command | What it does |
|---|---|
| `terraform init` | Downloads providers |
| `terraform init -upgrade` | Updates provider versions in lock file |
| `terraform validate` | Checks config is valid |
| `terraform plan` | Previews changes |
| `terraform apply` | Applies changes |
| `terraform destroy` | Deletes everything |

---