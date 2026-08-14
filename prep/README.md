# DevOps Interview Prep

A question bank covering every topic studied in this repo - Linux, Git, Networking, Docker, Bash, AWS, GitHub Actions, Terraform, Kubernetes, and Monitoring. Use it to self-test before interviews or assessments.

---

## Contents

1. [Linux](#1-linux)
2. [Git](#2-git)
3. [Networking](#3-networking)
4. [Docker](#4-docker)
5. [Bash Scripting](#5-bash-scripting)
6. [AWS](#6-aws)
7. [GitHub Actions](#7-github-actions)
8. [Terraform](#8-terraform)
9. [Kubernetes](#9-kubernetes)
10. [Monitoring & Observability](#10-monitoring--observability)
11. [General DevOps](#11-general-devops)

---

## 1. Linux

### File System & Navigation

<details>
<summary>What is the difference between an absolute path and a relative path?</summary><br><b>

</b>
</details>

<details>
<summary>What does the <code>~</code> character represent, and where does it point?</summary><br><b>

</b>
</details>

<details>
<summary>How do you find a file by name anywhere on the system?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a hard link and a symbolic link?</summary><br><b>

</b>
</details>

<details>
<summary>How do you view the size of a directory and its contents?</summary><br><b>

</b>
</details>

### Users, Groups & Permissions

<details>
<summary>What do the three permission groups (owner, group, other) represent?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>chmod 755</code> set, and what does each digit mean?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>su</code> and <code>sudo</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you add an existing user to a group without removing them from others?</summary><br><b>

</b>
</details>

<details>
<summary>What is <code>umask</code> and how does it affect file creation?</summary><br><b>

</b>
</details>

<details>
<summary>How would you find all files owned by a specific user?</summary><br><b>

</b>
</details>

### Process Management & System Monitoring

<details>
<summary>What is the difference between a process and a daemon?</summary><br><b>

</b>
</details>

<details>
<summary>How do you send a signal to a process, and what is the difference between SIGTERM and SIGKILL?</summary><br><b>

</b>
</details>

<details>
<summary>What does the load average shown in <code>top</code> or <code>uptime</code> represent?</summary><br><b>

</b>
</details>

<details>
<summary>How do you run a process in the background and bring it back to the foreground?</summary><br><b>

</b>
</details>

<details>
<summary>What command shows which process is listening on a specific port?</summary><br><b>

</b>
</details>

### Log Analysis & Text Processing

<details>
<summary>What is the difference between <code>grep</code> and <code>awk</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you follow a log file in real time?</summary><br><b>

</b>
</details>

<details>
<summary>How would you count the number of occurrences of an error string in a log file?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>|</code> (pipe) do, and how does it differ from redirecting to a file with <code>></code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you extract a specific column from a space-delimited file?</summary><br><b>

</b>
</details>

### Networking

<details>
<summary>What command shows your current IP address and network interfaces?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>curl</code> and <code>wget</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you test if a remote port is open from the command line?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>netstat</code> or <code>ss</code> show you?</summary><br><b>

</b>
</details>

### Package Management

<details>
<summary>What is the difference between <code>apt install</code> and <code>apt-get install</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you list all installed packages?</summary><br><b>

</b>
</details>

<details>
<summary>What happens if you run <code>apt upgrade</code> vs <code>apt full-upgrade</code>?</summary><br><b>

</b>
</details>

---

## 2. Git

### Basics

<details>
<summary>What is the difference between <code>git fetch</code> and <code>git pull</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What does a detached HEAD state mean, and how do you get out of it?</summary><br><b>

</b>
</details>

<details>
<summary>How do you undo the last commit without losing the changes?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>git reset</code>, <code>git revert</code>, and <code>git restore</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>git stash</code> do, and when would you use it over committing?</summary><br><b>

</b>
</details>

<details>
<summary>What is the purpose of <code>.gitignore</code>, and what happens if you add a file that is already tracked?</summary><br><b>

</b>
</details>

<details>
<summary>What does a force push (<code>git push --force</code>) do and why is it dangerous on a shared branch?</summary><br><b>

</b>
</details>

<details>
<summary>How do you find which commit introduced a specific bug?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>origin</code> and <code>upstream</code> in a forked repo?</summary><br><b>

</b>
</details>

### Merge & Rebase

<details>
<summary>What is the difference between <code>git merge</code> and <code>git rebase</code>, and when would you use each?</summary><br><b>

</b>
</details>

<details>
<summary>What is a fast-forward merge, and when does it happen?</summary><br><b>

</b>
</details>

<details>
<summary>How do you resolve a merge conflict?</summary><br><b>

</b>
</details>

<details>
<summary>How do you squash multiple commits into one?</summary><br><b>

</b>
</details>

---

## 3. Networking

### Fundamentals

<details>
<summary>What is the OSI model? Name the layers and give one example per layer.</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between TCP and UDP?</summary><br><b>

</b>
</details>

<details>
<summary>What happens when you type a URL into a browser and press enter? Walk through every step.</summary><br><b>

</b>
</details>

<details>
<summary>What is DNS, and what is the difference between an A record, CNAME, and MX record?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a public IP and a private IP?</summary><br><b>

</b>
</details>

<details>
<summary>What is NAT and why is it needed?</summary><br><b>

</b>
</details>

<details>
<summary>What is a subnet mask and what does CIDR notation represent?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between HTTP and HTTPS?</summary><br><b>

</b>
</details>

<details>
<summary>What is TLS, and what does the handshake process involve?</summary><br><b>

</b>
</details>

### Load Balancing & Proxies

<details>
<summary>What is the purpose of a load balancer, and what is the difference between Layer 4 and Layer 7 load balancing?</summary><br><b>

</b>
</details>

<details>
<summary>What is Nginx, and what is the difference between using it as a web server vs a reverse proxy?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a forward proxy and a reverse proxy?</summary><br><b>

</b>
</details>

<details>
<summary>What does a 502 Bad Gateway error mean?</summary><br><b>

</b>
</details>

---

## 4. Docker

### Core Concepts

<details>
<summary>What problem does Docker solve that running an app directly on a host does not?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a Docker image and a container?</summary><br><b>

</b>
</details>

<details>
<summary>What is a Docker layer, and why does layer caching matter for build times?</summary><br><b>

</b>
</details>

<details>
<summary>What happens when you run <code>docker run</code> on an image that does not exist locally?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>docker stop</code> and <code>docker kill</code>?</summary><br><b>

</b>
</details>

### Dockerfile

<details>
<summary>What is the difference between <code>CMD</code> and <code>ENTRYPOINT</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>RUN</code>, <code>CMD</code>, and <code>ENTRYPOINT</code>?</summary><br><b>

</b>
</details>

<details>
<summary>Why should you combine <code>RUN</code> commands with <code>&&</code> in a Dockerfile?</summary><br><b>

</b>
</details>

<details>
<summary>What is a multi-stage build and why would you use one?</summary><br><b>

</b>
</details>

<details>
<summary>Why should you use a non-root user in a Dockerfile?</summary><br><b>

</b>
</details>

<details>
<summary>What does the <code>COPY</code> instruction do, and how does it differ from <code>ADD</code>?</summary><br><b>

</b>
</details>

### Networking

<details>
<summary>What are the default Docker network drivers, and when would you use each?</summary><br><b>

</b>
</details>

<details>
<summary>How do two containers on the same Docker network communicate?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between binding to <code>127.0.0.1</code> and <code>0.0.0.0</code> when publishing a port?</summary><br><b>

</b>
</details>

### Compose

<details>
<summary>What problem does Docker Compose solve over running individual <code>docker run</code> commands?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>depends_on</code> and a health check in Compose?</summary><br><b>

</b>
</details>

<details>
<summary>What happens to volumes when you run <code>docker compose down</code> vs <code>docker compose down -v</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you scale a specific service in Compose?</summary><br><b>

</b>
</details>

### Volumes & Persistence

<details>
<summary>What is the difference between a bind mount and a named volume?</summary><br><b>

</b>
</details>

<details>
<summary>Where does Docker store named volumes on the host?</summary><br><b>

</b>
</details>

<details>
<summary>Why should you not store persistent data inside a container's writable layer?</summary><br><b>

</b>
</details>

### Best Practices & Registry

<details>
<summary>What is the principle of least privilege as it applies to containers?</summary><br><b>

</b>
</details>

<details>
<summary>How do you scan a Docker image for vulnerabilities?</summary><br><b>

</b>
</details>

<details>
<summary>What does it mean for a container to be stateless, and why does it matter?</summary><br><b>

</b>
</details>

<details>
<summary>What is Docker Hub, and how does image tagging work?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>latest</code> and a pinned version tag?</summary><br><b>

</b>
</details>

---

## 5. Bash Scripting

### Variables & Parameters

<details>
<summary>How do you declare and reference a variable in bash?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between single quotes and double quotes in bash?</summary><br><b>

</b>
</details>

<details>
<summary>What do <code>$0</code>, <code>$1</code>, <code>$#</code>, and <code>$@</code> represent?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>$@</code> and <code>$*</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you set a default value for a variable if it is not set?</summary><br><b>

</b>
</details>

### Conditionals & Loops

<details>
<summary>What is the difference between <code>[ ]</code> and <code>[[ ]]</code> in bash conditionals?</summary><br><b>

</b>
</details>

<details>
<summary>How do you check if a file exists before reading it?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>-eq</code> and <code>==</code> for comparisons?</summary><br><b>

</b>
</details>

<details>
<summary>How do you loop over all files in a directory?</summary><br><b>

</b>
</details>

<details>
<summary>What is a <code>while read</code> loop used for?</summary><br><b>

</b>
</details>

### Functions

<details>
<summary>How do you define and call a function in bash?</summary><br><b>

</b>
</details>

<details>
<summary>How do functions return values in bash?</summary><br><b>

</b>
</details>

<details>
<summary>What is the scope of a variable declared inside a function?</summary><br><b>

</b>
</details>

### Piping & Redirection

<details>
<summary>What is the difference between <code>></code> and <code>>></code>?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>2>&1</code> do?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>/dev/null</code> and <code>/dev/stdin</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you pass the output of one command as an argument (not stdin) to another?</summary><br><b>

</b>
</details>

### Error Handling

<details>
<summary>What does <code>set -e</code> do, and when might it cause unexpected behaviour?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>set -u</code> do?</summary><br><b>

</b>
</details>

<details>
<summary>What does the exit code <code>0</code> mean vs a non-zero exit code?</summary><br><b>

</b>
</details>

<details>
<summary>How do you check the exit code of the last command?</summary><br><b>

</b>
</details>

<details>
<summary>What is a trap in bash and when would you use it?</summary><br><b>

</b>
</details>

### Production Standards

<details>
<summary>What makes a script "production quality" vs a quick one-liner?</summary><br><b>

</b>
</details>

<details>
<summary>How do you make a script executable?</summary><br><b>

</b>
</details>

<details>
<summary>What should go at the top of every production bash script?</summary><br><b>

</b>
</details>

---

## 6. AWS

### Core & IAM

<details>
<summary>What is the shared responsibility model in AWS?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between an IAM user, group, role, and policy?</summary><br><b>

</b>
</details>

<details>
<summary>What is the principle of least privilege, and how do you apply it in IAM?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between an inline policy and a managed policy?</summary><br><b>

</b>
</details>

<details>
<summary>How does an EC2 instance get permissions to call AWS services without storing credentials?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between authentication and authorisation in the context of IAM?</summary><br><b>

</b>
</details>

### Networking & VPC

<details>
<summary>What is a VPC and why do you need one?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a public subnet and a private subnet?</summary><br><b>

</b>
</details>

<details>
<summary>What is an Internet Gateway and a NAT Gateway, and which direction does traffic flow through each?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a Security Group and a Network ACL?</summary><br><b>

</b>
</details>

<details>
<summary>What is VPC peering and what are its limitations?</summary><br><b>

</b>
</details>

<details>
<summary>How do route tables control traffic in a VPC?</summary><br><b>

</b>
</details>

### EC2

<details>
<summary>What is the difference between an On-Demand, Reserved, and Spot instance?</summary><br><b>

</b>
</details>

<details>
<summary>What is an AMI and what does it contain?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between stopping and terminating an EC2 instance?</summary><br><b>

</b>
</details>

<details>
<summary>What is instance metadata and how do you access it from within an instance?</summary><br><b>

</b>
</details>

<details>
<summary>What is user data and when does it run?</summary><br><b>

</b>
</details>

### Security Groups

<details>
<summary>What are the default inbound and outbound rules on a new security group?</summary><br><b>

</b>
</details>

<details>
<summary>Security groups are stateful - what does that mean in practice?</summary><br><b>

</b>
</details>

<details>
<summary>How do you allow an EC2 instance to accept HTTP traffic only from a load balancer, not from the internet directly?</summary><br><b>

</b>
</details>

### Load Balancing

<details>
<summary>What is the difference between an Application Load Balancer (ALB) and a Network Load Balancer (NLB)?</summary><br><b>

</b>
</details>

<details>
<summary>What is a target group?</summary><br><b>

</b>
</details>

<details>
<summary>How does an ALB perform health checks, and what happens to an unhealthy target?</summary><br><b>

</b>
</details>

<details>
<summary>What is sticky sessions and when would you use it?</summary><br><b>

</b>
</details>

### Storage

<details>
<summary>What is the difference between S3, EBS, and EFS?</summary><br><b>

</b>
</details>

<details>
<summary>What are S3 storage classes and when would you use Glacier over Standard?</summary><br><b>

</b>
</details>

<details>
<summary>What is S3 versioning and what problem does it solve?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between an S3 bucket policy and an ACL?</summary><br><b>

</b>
</details>

<details>
<summary>What is EBS and what happens to an EBS volume when an EC2 instance is terminated?</summary><br><b>

</b>
</details>

### Route 53

<details>
<summary>What is the difference between an A record and an alias record in Route 53?</summary><br><b>

</b>
</details>

<details>
<summary>What is a hosted zone?</summary><br><b>

</b>
</details>

<details>
<summary>What routing policies does Route 53 support, and when would you use weighted vs latency-based?</summary><br><b>

</b>
</details>

### Containers on AWS

<details>
<summary>What is the difference between ECS and EKS?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between EC2 launch type and Fargate in ECS?</summary><br><b>

</b>
</details>

<details>
<summary>What is a task definition in ECS?</summary><br><b>

</b>
</details>

<details>
<summary>What is ECR and how does it relate to Docker Hub?</summary><br><b>

</b>
</details>

### Serverless

<details>
<summary>What is Lambda and what problem does it solve compared to running a server?</summary><br><b>

</b>
</details>

<details>
<summary>What triggers can invoke a Lambda function?</summary><br><b>

</b>
</details>

<details>
<summary>What are Lambda cold starts and how do you mitigate them?</summary><br><b>

</b>
</details>

<details>
<summary>What is API Gateway and how does it work with Lambda?</summary><br><b>

</b>
</details>

### CloudFront

<details>
<summary>What is CloudFront and what problem does it solve?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a CloudFront origin and a distribution?</summary><br><b>

</b>
</details>

<details>
<summary>What is a cache behaviour and what can you control with it?</summary><br><b>

</b>
</details>

<details>
<summary>How do you invalidate the CloudFront cache?</summary><br><b>

</b>
</details>

### Databases

<details>
<summary>What is the difference between RDS and DynamoDB?</summary><br><b>

</b>
</details>

<details>
<summary>What is a Multi-AZ deployment in RDS and why would you use it?</summary><br><b>

</b>
</details>

<details>
<summary>What is a read replica and when would you use one?</summary><br><b>

</b>
</details>

<details>
<summary>What is DynamoDB's consistency model?</summary><br><b>

</b>
</details>

### Monitoring

<details>
<summary>What is the difference between CloudWatch Metrics, Logs, and Alarms?</summary><br><b>

</b>
</details>

<details>
<summary>What is CloudTrail and how does it differ from CloudWatch?</summary><br><b>

</b>
</details>

<details>
<summary>What is an SNS topic and how does it relate to CloudWatch Alarms?</summary><br><b>

</b>
</details>

### Messaging

<details>
<summary>What is the difference between SQS and SNS?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a standard queue and a FIFO queue in SQS?</summary><br><b>

</b>
</details>

<details>
<summary>What is a dead-letter queue?</summary><br><b>

</b>
</details>

### Security

<details>
<summary>What is AWS KMS and what does it manage?</summary><br><b>

</b>
</details>

<details>
<summary>What is AWS Secrets Manager and how is it different from Parameter Store?</summary><br><b>

</b>
</details>

<details>
<summary>What is AWS Shield and what does it protect against?</summary><br><b>

</b>
</details>

<details>
<summary>What is AWS WAF?</summary><br><b>

</b>
</details>

### Disaster Recovery & Well-Architected

<details>
<summary>What are the four DR strategies (backup & restore, pilot light, warm standby, multi-site), and how do they differ in RTO/RPO?</summary><br><b>

</b>
</details>

<details>
<summary>What are the five pillars of the AWS Well-Architected Framework?</summary><br><b>

</b>
</details>

---

## 7. GitHub Actions

### Concepts

<details>
<summary>What is a workflow, a job, and a step? How do they relate to each other?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>on: push</code> and <code>on: pull_request</code> triggers?</summary><br><b>

</b>
</details>

<details>
<summary>What is a runner, and what is the difference between a GitHub-hosted runner and a self-hosted runner?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>uses</code> and <code>run</code> in a step?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>needs</code> do in a job definition?</summary><br><b>

</b>
</details>

<details>
<summary>How do you prevent a workflow from running on certain branches?</summary><br><b>

</b>
</details>

### Data & Secrets

<details>
<summary>How do you pass data between steps in the same job?</summary><br><b>

</b>
</details>

<details>
<summary>How do you pass data between jobs?</summary><br><b>

</b>
</details>

<details>
<summary>What are GitHub Actions secrets and how do you access them in a workflow?</summary><br><b>

</b>
</details>

### Advanced

<details>
<summary>What is a matrix strategy and when would you use it?</summary><br><b>

</b>
</details>

<details>
<summary>How do you cache dependencies in a workflow to speed up builds?</summary><br><b>

</b>
</details>

<details>
<summary>What is a reusable workflow and when would you use it over a composite action?</summary><br><b>

</b>
</details>

<details>
<summary>How would you build and push a Docker image to a registry in a GitHub Actions workflow?</summary><br><b>

</b>
</details>

---

## 8. Terraform

### Core Concepts

<details>
<summary>What problem does Terraform solve that writing cloud resources manually in the console does not?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between Terraform and CloudFormation?</summary><br><b>

</b>
</details>

<details>
<summary>What is a provider in Terraform?</summary><br><b>

</b>
</details>

<details>
<summary>What is the purpose of <code>terraform init</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>terraform plan</code> and <code>terraform apply</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a <code>resource</code> and a <code>data</code> block?</summary><br><b>

</b>
</details>

### State

<details>
<summary>What is the Terraform state file and why is it important?</summary><br><b>

</b>
</details>

<details>
<summary>What are the risks of storing the state file locally?</summary><br><b>

</b>
</details>

<details>
<summary>What is a remote backend and why should you use one?</summary><br><b>

</b>
</details>

### Reusability & Operations

<details>
<summary>What is a Terraform module and why would you use one?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>count</code> and <code>for_each</code>?</summary><br><b>

</b>
</details>

<details>
<summary>How do you handle sensitive values like passwords in Terraform?</summary><br><b>

</b>
</details>

<details>
<summary>What happens when you run <code>terraform destroy</code>?</summary><br><b>

</b>
</details>

<details>
<summary>What is <code>terraform import</code> used for?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>terraform fmt</code> do and why does it matter in a team?</summary><br><b>

</b>
</details>

---

## 9. Kubernetes

### Basics & Architecture

<details>
<summary>What problem does Kubernetes solve that plain Docker does not?</summary><br><b>

</b>
</details>

<details>
<summary>What are the two broad categories of nodes in a Kubernetes cluster, and what runs on each?</summary><br><b>

</b>
</details>

<details>
<summary>What is the API server's role?</summary><br><b>

</b>
</details>

<details>
<summary>What is etcd and what happens if it goes down?</summary><br><b>

</b>
</details>

<details>
<summary>What is the scheduler's job?</summary><br><b>

</b>
</details>

<details>
<summary>What is the kubelet?</summary><br><b>

</b>
</details>

<details>
<summary>What is kube-proxy?</summary><br><b>

</b>
</details>

<details>
<summary>What is a namespace and why would you use one?</summary><br><b>

</b>
</details>

<details>
<summary>What is a Pod? Can a Pod have more than one container, and if so, how do they communicate?</summary><br><b>

</b>
</details>

### Running & Managing Workloads

<details>
<summary>What is the difference between a Pod and a Deployment?</summary><br><b>

</b>
</details>

<details>
<summary>What is a ReplicaSet and how does it relate to a Deployment?</summary><br><b>

</b>
</details>

<details>
<summary>How does a rolling update work in a Deployment?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>RollingUpdate</code> and <code>Recreate</code> as a Deployment strategy?</summary><br><b>

</b>
</details>

<details>
<summary>What is a DaemonSet and when would you use one?</summary><br><b>

</b>
</details>

<details>
<summary>What is a StatefulSet and how does it differ from a Deployment?</summary><br><b>

</b>
</details>

<details>
<summary>What is a Job and a CronJob in Kubernetes?</summary><br><b>

</b>
</details>

<details>
<summary>What does it mean for a Pod to be in a <code>CrashLoopBackOff</code> state?</summary><br><b>

</b>
</details>

<details>
<summary>How do liveness and readiness probes differ, and what happens when each fails?</summary><br><b>

</b>
</details>

### Exposing Applications

<details>
<summary>What are the four Service types in Kubernetes and when would you use each?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a ClusterIP and a NodePort?</summary><br><b>

</b>
</details>

<details>
<summary>What is a LoadBalancer service and what does it provision?</summary><br><b>

</b>
</details>

<details>
<summary>What is an Ingress, and how does it differ from a Service?</summary><br><b>

</b>
</details>

<details>
<summary>What is an Ingress controller?</summary><br><b>

</b>
</details>

### Storage

<details>
<summary>What is the difference between a PersistentVolume (PV) and a PersistentVolumeClaim (PVC)?</summary><br><b>

</b>
</details>

<details>
<summary>What is a StorageClass?</summary><br><b>

</b>
</details>

<details>
<summary>What does the <code>accessMode</code> on a PVC control?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>Retain</code>, <code>Delete</code>, and <code>Recycle</code> reclaim policies?</summary><br><b>

</b>
</details>

<details>
<summary>What is a StatefulSet's relationship to persistent storage?</summary><br><b>

</b>
</details>

### Config & Secrets

<details>
<summary>What is the difference between a ConfigMap and a Secret?</summary><br><b>

</b>
</details>

<details>
<summary>How can you mount a ConfigMap or Secret into a Pod?</summary><br><b>

</b>
</details>

<details>
<summary>How are Secrets stored in etcd, and what does that mean for security?</summary><br><b>

</b>
</details>

<details>
<summary>What is the risk of passing secrets as environment variables vs mounting them as files?</summary><br><b>

</b>
</details>

### Networking

<details>
<summary>How does Pod-to-Pod communication work within a cluster?</summary><br><b>

</b>
</details>

<details>
<summary>What is a CNI plugin and what does it do?</summary><br><b>

</b>
</details>

<details>
<summary>What is DNS resolution inside a cluster? How do you reach a Service in another namespace?</summary><br><b>

</b>
</details>

<details>
<summary>What is a NetworkPolicy and what does it control?</summary><br><b>

</b>
</details>

<details>
<summary>What is the default network behaviour if no NetworkPolicy exists?</summary><br><b>

</b>
</details>

### Ingress & External Access

<details>
<summary>What annotations are commonly used on Ingress resources?</summary><br><b>

</b>
</details>

<details>
<summary>How does TLS termination work at the Ingress level?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between path-based and host-based routing in Ingress?</summary><br><b>

</b>
</details>

### Security

<details>
<summary>What is RBAC in Kubernetes?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a Role and a ClusterRole?</summary><br><b>

</b>
</details>

<details>
<summary>What is a ServiceAccount and why should Pods use dedicated ones?</summary><br><b>

</b>
</details>

<details>
<summary>What is a PodSecurityContext?</summary><br><b>

</b>
</details>

<details>
<summary>What does <code>runAsNonRoot: true</code> enforce?</summary><br><b>

</b>
</details>

<details>
<summary>What is the principle of least privilege as it applies to Kubernetes workloads?</summary><br><b>

</b>
</details>

### Scheduling & Node Management

<details>
<summary>How does the Kubernetes scheduler decide which node to place a Pod on?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between node selectors, node affinity, and taints/tolerations?</summary><br><b>

</b>
</details>

<details>
<summary>What is a taint and what does it do?</summary><br><b>

</b>
</details>

<details>
<summary>What is a toleration?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between <code>NoSchedule</code>, <code>PreferNoSchedule</code>, and <code>NoExecute</code> taint effects?</summary><br><b>

</b>
</details>

<details>
<summary>What are resource requests and limits, and what happens when a container exceeds its memory limit?</summary><br><b>

</b>
</details>

### Observability

<details>
<summary>What is the difference between logs, metrics, and traces?</summary><br><b>

</b>
</details>

<details>
<summary>How do you stream logs from a running Pod?</summary><br><b>

</b>
</details>

<details>
<summary>How do you get logs from a crashed Pod?</summary><br><b>

</b>
</details>

<details>
<summary>What is the Kubernetes metrics server used for?</summary><br><b>

</b>
</details>

<details>
<summary>What is <code>kubectl top</code> and what does it show?</summary><br><b>

</b>
</details>

---

## 10. Monitoring & Observability

### Foundations

<details>
<summary>What is the difference between monitoring and observability?</summary><br><b>

</b>
</details>

<details>
<summary>What are the three pillars of observability?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a metric, a log, and a trace?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between push-based and pull-based metric collection?</summary><br><b>

</b>
</details>

<details>
<summary>What is the RED method, and what does each letter stand for?</summary><br><b>

</b>
</details>

<details>
<summary>What is the USE method?</summary><br><b>

</b>
</details>

### Prometheus

<details>
<summary>What is Prometheus and how does it collect metrics?</summary><br><b>

</b>
</details>

<details>
<summary>What is a scrape target and how does Prometheus discover them?</summary><br><b>

</b>
</details>

<details>
<summary>What are the four Prometheus metric types?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a Counter and a Gauge?</summary><br><b>

</b>
</details>

<details>
<summary>What is PromQL? Write a query that gives you the per-second rate of a counter over the last 5 minutes.</summary><br><b>

</b>
</details>

<details>
<summary>What is the Alertmanager and how does it relate to Prometheus?</summary><br><b>

</b>
</details>

<details>
<summary>What is a recording rule and why would you create one?</summary><br><b>

</b>
</details>

<details>
<summary>What is the Pushgateway used for?</summary><br><b>

</b>
</details>

### Grafana

<details>
<summary>What is Grafana and what problem does it solve on its own?</summary><br><b>

</b>
</details>

<details>
<summary>What is a data source in Grafana?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a dashboard panel and a row?</summary><br><b>

</b>
</details>

<details>
<summary>What are Grafana variables and how do they make dashboards reusable?</summary><br><b>

</b>
</details>

<details>
<summary>What is a Grafana alert, and how does it differ from a Prometheus alert?</summary><br><b>

</b>
</details>

### Alertmanager

<details>
<summary>What is the role of Alertmanager relative to Prometheus?</summary><br><b>

</b>
</details>

<details>
<summary>What is alert grouping and why is it useful?</summary><br><b>

</b>
</details>

<details>
<summary>What is alert silencing vs alert inhibition?</summary><br><b>

</b>
</details>

<details>
<summary>What is a receiver in Alertmanager?</summary><br><b>

</b>
</details>

### Loki

<details>
<summary>What is Loki and how does it differ from Elasticsearch for log storage?</summary><br><b>

</b>
</details>

<details>
<summary>What is a label in Loki and why should you keep the label cardinality low?</summary><br><b>

</b>
</details>

<details>
<summary>What is LogQL? Give an example of filtering logs by label and then by content.</summary><br><b>

</b>
</details>

<details>
<summary>What is Promtail?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between Loki's index and the log chunks?</summary><br><b>

</b>
</details>

### Full Stack

<details>
<summary>How do Prometheus, Grafana, Alertmanager, and Loki work together as a monitoring stack?</summary><br><b>

</b>
</details>

<details>
<summary>What is the first thing you would check when you receive an alert that a service is down?</summary><br><b>

</b>
</details>

<details>
<summary>How would you design alerting to minimise alert fatigue?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between a symptom-based alert and a cause-based alert? Which is preferred?</summary><br><b>

</b>
</details>

---

## 11. General DevOps

### Culture & Practices

<details>
<summary>What is DevOps and what problem does it solve in a software organisation?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between CI and CD?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between continuous delivery and continuous deployment?</summary><br><b>

</b>
</details>

<details>
<summary>What is a deployment pipeline and what stages does it typically have?</summary><br><b>

</b>
</details>

<details>
<summary>What is infrastructure as code (IaC) and why does it matter?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between mutable and immutable infrastructure?</summary><br><b>

</b>
</details>

<details>
<summary>What does "idempotent" mean in the context of infrastructure or scripts?</summary><br><b>

</b>
</details>

### Deployment Strategies

<details>
<summary>What is a blue-green deployment?</summary><br><b>

</b>
</details>

<details>
<summary>What is a canary deployment?</summary><br><b>

</b>
</details>

<details>
<summary>If a production deployment goes wrong, what is your first action?</summary><br><b>

</b>
</details>

<details>
<summary>How would you roll back a bad deployment with zero downtime?</summary><br><b>

</b>
</details>

### Reliability & SRE

<details>
<summary>What is the difference between horizontal scaling and vertical scaling?</summary><br><b>

</b>
</details>

<details>
<summary>What is a single point of failure and how do you eliminate one?</summary><br><b>

</b>
</details>

<details>
<summary>What is an SLA, SLO, and SLI? How do they relate to each other?</summary><br><b>

</b>
</details>

<details>
<summary>What is toil in SRE, and why does it matter?</summary><br><b>

</b>
</details>

<details>
<summary>What are the four golden signals of monitoring?</summary><br><b>

</b>
</details>

<details>
<summary>What is the difference between mean time to detect (MTTD) and mean time to recover (MTTR)?</summary><br><b>

</b>
</details>

<details>
<summary>What is shift-left security?</summary><br><b>

</b>
</details>

<details>
<summary>What is the 12-factor app methodology?</summary><br><b>

</b>
</details>
