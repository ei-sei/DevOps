# Terraform Command Cheatsheet

---

## Core Workflow

| Command | What it does |
|---|---|
| `terraform init` | Initializes the project and downloads providers |
| `terraform init -upgrade` | Re-downloads providers, updating to latest allowed version |
| `terraform validate` | Checks config is syntactically valid without touching infrastructure |
| `terraform plan` | Previews what will be created, changed, or destroyed |
| `terraform plan -out=tfplan` | Saves the plan to a file for later use |
| `terraform apply` | Applies changes to real infrastructure |
| `terraform apply tfplan` | Applies a previously saved plan file |
| `terraform apply -auto-approve` | Applies without prompting for confirmation |
| `terraform destroy` | Destroys all managed infrastructure |
| `terraform destroy -auto-approve` | Destroys without prompting for confirmation |

---

## State

| Command | What it does |
|---|---|
| `terraform show` | Prints the current state in a readable format |
| `terraform state list` | Lists all resources tracked in state |
| `terraform state show <resource>` | Shows details of a specific resource in state |
| `terraform state rm <resource>` | Removes a resource from state without destroying it |
| `terraform refresh` | Updates state to match real-world infrastructure |

---

## Import

| Command | What it does |
|---|---|
| `terraform import <resource> <id>` | Imports an existing resource into state |

Example:
```bash
terraform import aws_s3_bucket.my_bucket my-bucket-name
```

---

## Variables

| Command | What it does |
|---|---|
| `terraform apply -var="key=value"` | Pass a variable value directly on the CLI |
| `terraform apply -var-file="prod.tfvars"` | Use a specific tfvars file |

---

## Workspace

| Command | What it does |
|---|---|
| `terraform workspace list` | List all workspaces |
| `terraform workspace new <name>` | Create a new workspace |
| `terraform workspace select <name>` | Switch to a workspace |

---

## Targeting

| Command | What it does |
|---|---|
| `terraform plan -target=<resource>` | Plan only a specific resource |
| `terraform apply -target=<resource>` | Apply only a specific resource |
| `terraform destroy -target=<resource>` | Destroy only a specific resource |

Example:
```bash
terraform apply -target=aws_instance.my_ec2
```

---

## Formatting

| Command | What it does |
|---|---|
| `terraform fmt` | Auto-formats all `.tf` files to standard style |
| `terraform fmt -check` | Checks formatting without making changes |
