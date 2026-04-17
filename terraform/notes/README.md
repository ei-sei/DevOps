# [Terraform](https://developer.hashicorp.com/terraform/docs) Concepts

## Contents

- [Terraform Concepts](#terraform-concepts)
  - [Contents](#contents)
  - [Core Concepts](#core-concepts)
  - [Terraform Workflow](#terraform-workflow)
  - [Resources](#resources)
    - [Resource Syntax](#resource-syntax)
    - [Resource Meta-Arguments](#resource-meta-arguments)
    - [Referencing Resources](#referencing-resources)
  - [Variables](#variables)
    - [Input Variables](#input-variables)
    - [Local Variables](#local-variables)
    - [Output Variables](#output-variables)
    - [Variable Hierarchy](#variable-hierarchy)
    - [Variable Types](#variable-types)
  - [Data Sources](#data-sources)

---

## Core Concepts

**Deploying Infrastructure** - Using code to automatically create and configure cloud resources (servers, networks, databases) instead of clicking through a web console.

**Terraform State File** - Terraform's memory - a file that tracks which real-world resources it created so it knows what to update or delete later. Never delete or manually edit this file.

**Resource Block** - The unit of code that defines one specific piece of infrastructure you want Terraform to create, like a single server or database.

**[Providers](https://developer.hashicorp.com/terraform/language/providers)** - Plugins that give Terraform the ability to talk to a specific platform (AWS, Azure, GCP).

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
  region = "us-east-1" # all resources will be created in this AWS region
}
```

**[Registry](https://registry.terraform.io/providers/hashicorp/aws/latest)** - A public library of pre-built providers and modules you can pull into your project instead of writing everything from scratch.

**[Import](https://developer.hashicorp.com/terraform/language/import)** - Brings a manually created resource under Terraform's management without recreating it - it only updates the state file, so you still have to write the matching resource block yourself.

---

## Terraform Workflow

| Stage | Details |
|---|---|
| `init` | Initializes the working directory and downloads providers. Always the first command to run after writing a new config. |
| `validate` | Checks that config files are syntactically valid and internally consistent. Never touches real infrastructure. |
| `plan` | Performs a refresh and creates an execution plan - shows a diff of what will change without making any changes. |
| `apply` | Scans the current directory and applies all changes to make infrastructure match your config. |
| `destroy` | Tears down all Terraform-managed infrastructure. Asks for confirmation before proceeding. |

---

## [Resources](https://developer.hashicorp.com/terraform/language/resources)

### Resource Syntax

```hcl
resource "<provider>_<type>" "<local_name>" {
  argument = value
}
```

Example - [S3 Bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket):

```hcl
resource "aws_s3_bucket" "my_bucket" {  # aws_s3_bucket = type, my_bucket = local name
  bucket = "my-bucket-name"             # bucket = argument (actual name in AWS)
}
```

Example - [EC2 Instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance):

```hcl
resource "aws_instance" "my_ec2" {
  ami           = "resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
  instance_type = "t3.micro"

  tags = {
    Name        = "my-ec2"
    Environment = "dev"
  }
}
```

### Resource Meta-Arguments

Meta-arguments change how Terraform handles a resource, regardless of type:

| Meta-Argument | Purpose |
|---|---|
| `count` | Create multiple copies of a resource using an index |
| `for_each` | Create multiple copies using a map or set of strings |
| `depends_on` | Explicitly tell Terraform to create this resource after another |
| `lifecycle` | Control how Terraform handles create, update, and destroy |

```hcl
resource "aws_s3_bucket" "buckets" {
  count  = 3
  bucket = "my-bucket-${count.index}"  # creates my-bucket-0, my-bucket-1, my-bucket-2
}
```

### Referencing Resources

Use `<type>.<local_name>.<attribute>` to pass values between resources without hardcoding:

```hcl
output "bucket_arn" {
  value = aws_s3_bucket.my_bucket.arn
}
```

---

## [Variables](https://developer.hashicorp.com/terraform/language/values/variables)

### Input Variables

Values passed in from outside, defined with a `variable` block:

```hcl
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

Set actual values in `terraform.tfvars` - loaded automatically:

```hcl
instance_type = "t3.medium"
region        = "us-east-1"
```

### Local Variables

Named values inside your config to avoid repeating the same expression:

```hcl
locals {
  env    = "dev"
  prefix = "myapp-${local.env}"
}
```

### Output Variables

Values Terraform prints after `apply` to expose resource info:

```hcl
output "bucket_name" {
  value = aws_s3_bucket.my_bucket.id
}
```

### Variable Hierarchy

| Priority | Source |
|---|---|
| 1 (highest) | `-var` flag on the CLI |
| 2 | `-var-file` flag on the CLI |
| 3 | `*.auto.tfvars` files |
| 4 | `terraform.tfvars` file |
| 5 (lowest) | `default` in the variable block |

### Variable Types

| Type | Description | Example |
|---|---|---|
| `string` | Plain text | `"us-east-1"` |
| `number` | Numeric value | `3` |
| `bool` | True or false | `true` |
| `list` | Ordered collection of values | `["a", "b", "c"]` |
| `map` | Key-value pairs | `{ env = "dev" }` |
| `object` | Structured set of named attributes | `{ name = string, port = number }` |

---

## [Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)

A data source reads existing infrastructure Terraform didn't create, so you can reference it without managing it.

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

Reference with `data.<type>.<local_name>.<attribute>`:

```hcl
resource "aws_instance" "my_ec2" {
  ami           = data.aws_ami.amazon_linux.id  # looks up AMI per region automatically
  instance_type = "t3.micro"
}
```
