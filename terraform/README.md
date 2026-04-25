# Terraform

Provisioning and managing AWS infrastructure using Terraform. Covers core concepts, modular design, and real deployments.

## Contents

- [notes/](notes/) - Core concepts, variables, modules, data sources
- [tutorial/](tutorial/) - Step-by-step Terraform tutorial
- [lab/](lab/) - Hands-on labs deploying real AWS infrastructure

## Labs

### [Lab 01 - WordPress](lab/01-wordpress/)

Deploy a WordPress stack on AWS - custom VPC, EC2, security groups, user data. Refactored into reusable modules.

![architecture](assets/lab01/architecture.png)

---

### [Lab 02 - Cloud-Init EC2](lab/02-cloud-init-ec2-deployment/)

EC2 deployment using cloud-init for automated instance configuration with NGINX.

![architecture](assets/lab02/architecture.png)

## Topics Covered

- Providers, resources, variables, outputs, data sources
- Modules - writing and calling reusable module structures
- Remote state and tfvars
- AWS - VPC, IGW, subnets, route tables, security groups, EC2
- Data sources for dynamic AMI lookup
- User data vs cloud-init for instance bootstrapping
