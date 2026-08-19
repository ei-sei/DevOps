# DevOps

A collection of DevOps labs, notes, and projects. Each folder is a self-contained topic.

## Repository Structure

This repository uses a monorepo layout - each topic lives in its own top-level folder, self-contained with its own notes, labs, and README.

## Technologies

- **DNS:** Cloudflare, Route53
- **Version Control:** Git
- **Scripting:** Bash, Python
- **Containers:** Docker
- **Cloud:** AWS (EC2, ECS, VPC, ALB, S3, CloudFront, Lambda, API Gateway, DynamoDB, IAM)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions

## Topics

| Folder                                    | Category         | Description                                                                                                          |
| -------------------------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| [`linux`](linux/)                         | Foundations      | Linux administration notes, commands, and lab exercises                                                              |
| [`networking`](networking/)               | Foundations      | Networking fundamentals, DNS lab, and Nginx on EC2 with Cloudflare DNS                                               |
| [`git`](git/)                             | Foundations      | Operational runbook and troubleshooting guides                                                                       |
| [`scripts`](scripts/)                     | Foundations      | Shell scripts and automation utilities                                                                               |
| [`docker`](docker/)                       | Containerisation | Docker fundamentals, Dockerfiles, and compose examples                                                               |
| [`aws`](aws/)                             | Cloud            | AWS fundamentals and labs covering VPC, ALB, S3, CloudFront, Route53, Lambda, API Gateway, DynamoDB, and IAM         |
| [`terraform`](terraform/)                 | IaC              | Terraform fundamentals and labs, deploying AWS resources as code                                                     |
| [`github-actions`](github-actions/)       | CI/CD            | GitHub Actions workflows covering CI/CD pipelines, Docker image builds, testing, linting, and automated deployments |
| [`agentic-workflows`](agentic-workflows/) | AI               | AI/agentic engineering learning track: 14-topic curriculum, framework studies, project roadmap, and a CLI learning agent |
| [`monitoring-stack`](monitoring-stack/)   | Observability    | (In progress) Setting up observability with Prometheus, Grafana, and alerting configurations                        |
| [`kubernetes`](kubernetes/)               | Containerisation | (In progress) Local Kubernetes setup and learning exercises using minikube and kind                                 |

## Projects

| Project                                                              | Description                                                                                                                     | Stack                                                             |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [threat-composer-ecs](https://github.com/ei-sei/threat-composer-ecs) | Containerised deployment of the AWS open-source Threat Composer app on ECS Fargate, behind an ALB with HTTPS on a custom domain | ECS Fargate, ALB, ECR, ACM, Terraform, GitHub Actions, Cloudflare |
| [headscale-ecs](https://github.com/ei-sei/headscale-ecs)             | Self-hosted Headscale, the open-source Tailscale control plane, deployed on AWS ECS Fargate behind an NLB                      | ECS Fargate, NLB, Docker, Terraform, AWS                          |
