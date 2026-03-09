# 7. Container Services

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Why Containers on AWS

You can already run Docker on EC2 manually. What problems does that create at scale?
> 

What does a container orchestration service solve?
> 

What container orchestration services does AWS offer?
> 

---

## Part 2: ECS Core Concepts

What is ECS (Elastic Container Service)?
> 

What is a cluster in ECS?
> 

What is a task definition?
> 

What is a task?
> 

What is a service?
> 

What is the relationship between task definition, task, and service?
> 

How does an ECS service differ from just running a standalone task?
> 

---

## Part 3: Task Definitions in Detail

What format is a task definition written in?
> 

What is a container definition within a task definition?
> 

What do you specify in a container definition? Name at least 5 things.
> 

How do you set CPU and memory limits on a task?
> 

How do you pass environment variables to a container in ECS?
> 

Can you have multiple containers in a single task definition? When would you?
> 

What is the sidecar pattern?
> 

---

## Part 4: Task Role vs Execution Role

What is a task role?
> 

What is a task execution role?
> 

What is the difference between them?
> 

Give an example of when each is used:
> 

---

## Part 5: Fargate vs EC2 Launch Type

What is the EC2 launch type? What are you responsible for managing?
> 

What is Fargate? What does AWS manage for you?
> 

What is the key difference between them from an operations perspective?
> 

When would you choose Fargate over EC2 launch type?
> 

When would you choose EC2 launch type over Fargate?
> 

How does pricing differ between them?
> 

---

## Part 6: ECR (Elastic Container Registry)

What is ECR?
> 

What is a repository in ECR?
> 

How do you authenticate Docker to ECR?
> 

Walk through the steps to build and push an image to ECR:
> 

How long does the ECR authentication token last?
> 

What is a lifecycle policy in ECR? Why use one?
> 

What is image scanning in ECR?
> 

---

## Part 7: EKS Overview

What is EKS (Elastic Kubernetes Service)?
> 

What does "managed control plane" mean in EKS?
> 

What are the worker node options in EKS?
> 

When would you choose EKS over ECS?
> 

When would ECS be the simpler choice?
> 

---

## Part 8: Container Networking

What is awsvpc networking mode?
> 

In awsvpc mode, what does each task get?
> 

How does an ALB route traffic to ECS containers?
> 

How do containers in the same task communicate with each other?
> 

What is service discovery in ECS? What AWS service powers it?
> 

---

## Part 9: Container Logging

How do you view container logs in ECS?
> 

What is the awslogs log driver?
> 

What are log groups and log streams?
> 

What is Container Insights?
> 

---

## Commands to Learn

```bash
# What does this do?
aws ecr create-repository --repository-name my-app
```
> 

```bash
# What does this do?
aws ecr get-login-password --region eu-west-2 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.eu-west-2.amazonaws.com
```
> 

```bash
# What does this do?
aws ecr list-images --repository-name my-app
```
> 

```bash
# What does this do?
aws ecs create-cluster --cluster-name my-cluster
```
> 

```bash
# What does this do?
aws ecs list-clusters
```
> 

```bash
# What does this do?
aws ecs register-task-definition --cli-input-json file://task-def.json
```
> 

```bash
# What does this do?
aws ecs list-services --cluster my-cluster
```
> 

```bash
# What does this do?
aws ecs describe-services --cluster my-cluster --services my-service
```
> 

```bash
# What does this do?
aws ecs update-service --cluster my-cluster --service my-service \
  --task-definition my-task:2
```
> 

---

## Hands-On Tasks

- Create an ECR repository and push a Docker image to it
- Write a task definition for a simple web app (nginx or your own)
- Create an ECS Fargate cluster and run a standalone task
- Create an ECS service with ALB integration and verify it serves traffic
- Update the task definition with a new image version and deploy a rolling update
- View container logs in CloudWatch
- Set up an ECR lifecycle policy to keep only the last 10 images

---

## Quick Quiz

1. What is the difference between a task definition, a task, and a service?
   > 

2. What is the difference between a task role and an execution role?
   > 

3. How would you deploy a new container version to ECS with zero downtime?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________