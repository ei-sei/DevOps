# DevOps Portfolio

A comprehensive collection of DevOps projects, labs, and infrastructure-as-code examples. Each project is organised as a separate branch for clean navigation and focused development.

## Repository Structure

This repository uses a **branch-based organisation** instead of subdirectories. Each branch contains a complete, self-contained project.

## Projects

### Foundations

| Branch | Description |
|--------|-------------|
| [`linux-lab-notebook`](../../tree/linux-lab-notebook) | Linux administration notes, commands, and lab exercises |
| [`git-runbook`](../../tree/git-runbook) | Operational runbooks and troubleshooting guides |
| [`automation-scripts`](../../tree/automation-scripts) | Shell scripts and automation utilities |
| [`networking`](../../tree/networking) | Networking fundamentals, DNS lab, and Nginx on EC2 with Cloudflare DNS |

### Cloud & Serverless

| Branch | Description |
|--------|-------------|
| [`aws`](../../tree/aws) | AWS fundamentals|
| [`aws-web-server`](../../tree/aws-web-server) | AWS EC2 web server deployment and configuration |
| [`serverless-url-shortener`](../../tree/serverless-url-shortener) | Serverless URL shortener using AWS Lambda, API Gateway, and DynamoDB |

### Containerisation

| Branch | Description |
|--------|-------------|
| [`docker-lab`](../../tree/docker-lab) | Docker fundamentals, Dockerfiles, and compose examples |
| [`aws-container-deployment`](../../tree/aws-container-deployment) | Deploying containers on AWS (ECS/Fargate) |

### Infrastructure as Code

| Branch | Description |
|--------|-------------|
| [`terraform-aws-infrastructure`](../../tree/terraform-aws-infrastructure) | Terraform modules for AWS infrastructure provisioning |
| [`ci-cd-pipeline`](../../tree/ci-cd-pipeline) | CI/CD pipeline configurations (GitHub Actions, Jenkins) |

### Kubernetes

| Branch | Description |
|--------|-------------|
| [`kubernetes-local-lab`](../../tree/kubernetes-local-lab) | Local Kubernetes setup with minikube/kind and learning exercises |
| [`eks-production-cluster`](../../tree/eks-production-cluster) | Production-grade EKS cluster configuration |

### Observability

| Branch | Description |
|--------|-------------|
| [`monitoring-stack`](../../tree/monitoring-stack) | Prometheus, Grafana, and alerting configurations |

### Capstone

| Branch | Description |
|--------|-------------|
| [`capstone-project`](../../tree/capstone-project) | End-to-end DevOps project combining all skills |


## Branch Workflow

```
main (this README)
 ├── linux-lab-notebook
 ├── git-runbook
 ├── automation-scripts
 ├── networking
 ├── aws
 ├── aws-web-server
 ├── serverless-url-shortener
 ├── docker-lab
 ├── aws-container-deployment
 ├── terraform-aws-infrastructure
 ├── ci-cd-pipeline
 ├── kubernetes-local-lab
 ├── eks-production-cluster
 ├── monitoring-stack
 └── capstone-project
```

## Technologies

- **Cloud:** AWS (EC2, Lambda, ECS, EKS, S3, DynamoDB)
- **Containers:** Docker, Kubernetes
- **IaC:** Terraform, CloudFormation
- **CI/CD:** GitHub Actions, Jenkins
- **Monitoring:** Prometheus, Grafana
- **Scripting:** Bash, Python

