# DevOps

A collection of DevOps labs, notes, and projects. Each branch is a self-contained topic.

## Repository Structure

This repository uses a branch-based organisation instead of subdirectories. Each branch contains a complete, self-contained project.

## Technologies

- **Cloud:** AWS (EC2, ECS, VPC, ALB, S3, CloudFront, Lambda, API Gateway, DynamoDB, IAM)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Containers:** Docker
- **Scripting:** Bash, Python
- **DNS:** Cloudflare, Route53
- **Version Control:** Git

  
## Branches

| Branch                                        | Category         | Description                                                                                                         |
| --------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| [`linux`](../../tree/linux)                   | Foundations      | Linux administration notes, commands, and lab exercises                                                             |
| [`git`](../../tree/git)                       | Foundations      | Operational runbook and troubleshooting guides                                                                      |
| [`scripts`](../../tree/automation-scripts)    | Foundations      | Shell scripts and automation utilities                                                                              |
| [`networking`](../../tree/networking)         | Foundations      | Networking fundamentals, DNS lab, and Nginx on EC2 with Cloudflare DNS                                              |
| [`docker`](../../tree/docker)                 | Containerisation | Docker fundamentals, Dockerfiles, and compose examples                                                              |
| [`aws`](../../tree/aws)                       | Cloud            | AWS fundamentals and labs covering VPC, ALB, S3, CloudFront, Route53, Lambda, API Gateway, DynamoDB, and IAM        |
| [`terraform`](../../tree/terraform)           | IaC              | Terraform fundamentals and labs, deploying AWS resources as code                                                    |
| [`github-actions`](../../tree/github-actions) | CI/CD            | GitHub Actions workflows covering CI/CD pipelines, Docker image builds, testing, linting, and automated deployments |

## Projects

| Project                                                              | Description                                                                                                                     | Stack                                                             |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [threat-composer-ecs](https://github.com/ei-sei/threat-composer-ecs) | Containerised deployment of the AWS open-source Threat Composer app on ECS Fargate, behind an ALB with HTTPS on a custom domain | ECS Fargate, ALB, ECR, ACM, Terraform, GitHub Actions, Cloudflare |