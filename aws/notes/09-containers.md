# 7. Container Services

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Why Containers on AWS

You can already run Docker on EC2 manually. What problems does that create at scale?
> Running Docker on EC2 manually at scale means you must handle instance provisioning, container placement across hosts, restart logic for failed containers, rolling deployments, and load balancer registration yourself.

What does a container orchestration service solve?
> A **container orchestration service** (what this means: a system that automaticaly places, starts, stops, scales, and replaces containers across a fleet of machines) removes that operational burden from you.

What container orchestration services does AWS offer?
> AWS offers **ECS** (what this means Elastic Container Service, AWS's own orchestration service) and EKS (what this means: Elastic Kubernetes Service, managed Kubernetes on AWS).

---

## Part 2: ECS Core Concepts

What is ECS (Elastic Container Service)?
> AWS's manages service for running and scaling Docker containers. Handles scheduling, placement, and lifecycle of your containers.

What is a cluster in ECS?
> A **cluster** (what this means: a logical grouping of compute resource where ECS runs your containers) is the boundary within which your tasks and services operate.

What is a task definition?
> A **task definition** (what this means: a JSON blueprint that describes how one or more containers should run - the image, CPU, memory, ports, environment varibales, and IAM roles) is like a template for your containers.

What is a task?
> A **task** (what this means: a running instance of a task definition - the actual containers or containers executing on your cluster) is the live version of your blueprint.

What is a service?
> A **service** (what this means: an ECS construct that ensures a specified number of tasks are always running and replaces any that stop or fail) keeps your application continuously available.

What is the relationship between task definition, task, and service?
> - task definition is the template.
> - task is the instantiatioin of that template
> - a service manages how many tasks run and keep that count healthy.

How does an ECS service differ from just running a standalone task?
> An ECS service continuously monitors running tasks and automatically replaces failed ones to maintain your desired count, whereas a standalone task runs once and stops when finished.

---

## Part 3: Task Definitions in Detail

What format is a task definition written in?
> written in JSON and registered with ECS.

What is a container definition within a task definition?
> a container definition (what this means: the section of a task definition that describes a single container - its image, resources, ports, and configuration) is the per-container specification within the broader task definition.

What do you specify in a container definition? Name at least 5 things.
> In a container definition you specify: Docker image URI, CPU units, memory limit, port mappings, environment variables, log configuration, command override, and health check command.

How do you set CPU and memory limits on a task?
> You set CPU and memory at both the task level (hard limits for the whole task) and optionally at the container level; Fargate requires task-level CPU and memory values from a fixed list of valid combinations.

How do you pass environment variables to a container in ECS?
> You pass enviroment variables to containers either as plaintext key-value pairs in the container definition, or as references to SSM Parameter Store or Secrets Manager (what this means: AWS services that store configuration and secrets securely, keeping sensitive values out of your task definitions).

Can you have multiple containers in a single task definition? When would you?
> Yes, a single task definition can include muiltiple containers; you do this when containers are tightly coupled and must run together, such as an application container paired with a logging agent.

What is the sidecar pattern?
> The sidecar pattern ( what this means: running a helper container alongside your main application container in the same task to handle cross-cutting concerns like logging, metrics collectioin, or proxy functions) keeps auxiliary logic separate from your application code.

---

## Part 4: Task Role vs Execution Role

What is a task role?
> A task role (what this means: an IAM role that your running container assumes to call other AWS services, like reading from S3 or writing to DynamoDB) gives your application code its AWS permissions.

What is a task execution role?
> A task execution role (what this means: an IAM role used by the ECS agent itself to perform infrastructure tasks like pulling yourb container image from ECR and sending logs to CloudWatch) gives ECS permission to set up your container.

What is the difference between them?
> - task role is for your application code
> - execution role is for ECS's own setup operations.

Give an example of when each is used:
> - task role is used when your application code calls `s3.getObject()` or `dynamodb.putItem()`
> - execution role is used when ECS pulls the image from ECR and writes container startup logs to CloudWatch

---

## Part 5: Fargate vs EC2 Launch Type

What is the EC2 launch type? What are you responsible for managing?
> EC2 launch type (what this means: an ECS mode where you provision and manage the EC2 instances in your cluster yourself) means your are responsible for instance sizing, patching, scaling the underlying hosts, and cluster capacity.

What is Fargate? What does AWS manage for you?
> Fargate (what this means: a severless computer engine for ECS where AWS provisions and manages the underlying infrastructure and you only define your task's CPU and memory) removes all host mananagement from you.

What is the key difference between them from an operations perspective?
> With Fargate you define what your container needs and AWS runs it; with EC2 launch type you manage the host machines that run your containers.

When would you choose Fargate over EC2 launch type?
> Choose Fargate when you want to avoid managing servers, have variable or unpredicatable workloads, or want to get started quickly without capacity planning.

When would you choose EC2 launch type over Fargate?
> Choose EC2 lanch type when you need specific instance types (GPU, high memory), want to use Spot Instances for cost savings, or have workloads dense enough that EC2 is significantly cheaper

How does pricing differ between them?
> Fargate pricing is per vCPU and GB of memory per second of task runtime; EC2 launch type pricing is the cost of the underlying EC2 instances regardless of how pack they are with tasks.

---

## Part 6: ECR (Elastic Container Registry)

What is ECR?
> **ECR** (what this means: Elastic Container Registry, AWS's fully managed Docker container image registry) stores and serves your container images within AWS. 

What is a repository in ECR?
> A **repository** (what this means: a named storage location within ECR for all versions of a single container image) is where you push and pull a specific image.

How do you authenticate Docker to ECR?
> To authenticate Docker to ECR, run `aws ecr get-login-password` piped into `docker login` using the registry URL.

Walk through the steps to build and push an image to ECR:
> 1. Create the ECR repository
> 2. Authenticate Docker to ECR with `aws ecr get-login-password ... | docker login ...`
> 3. Build your image with `docker build -t my-app .`
> 4. Tag it with the ECR URI: `docker tag my-app:latest <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest`
> 5. Push with `docker push <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest`

How long does the ECR authentication token last?
> 12 hours

What is a lifecycle policy in ECR? Why use one?
> **lifecycle policy** (what this means: a rule that automatically expires and deletes old images from your ECR repository based on age or count) keeps storage costs down by removing images you no longer need.

What is image scanning in ECR?
> **Image scanning** (what this means: an ECR feature that checks your container images fro knwn operating system and package vulnerabilities using a CVE database) helps you find security issues before deploying.

---

## Part 7: EKS Overview

What is EKS (Elastic Kubernetes Service)?
> **EKS** (what this means: Elastic Kubernetes Service, AWS's managed service that runs a Kubernetes control plane for you) lets you use Kubernetes without operating the control plane yourself.

What does "managed control plane" mean in EKS?
> AWS runs, patches, scales, and backs up the **Kubernetes control plane** (what this means: the set of components - API server, etcd, scheduler, controller manager - that manage the cluster) so you only manage worker nodes.


What are the worker node options in EKS?
> Your worker node options in EKS are self-managed EC2 nodes, **managed node groups** (what this means: EC2 nodes where AWS handles provisioning and lifecycle), and Fargate for serverless pods.

When would you choose EKS over ECS?
> Choose EKS when your team already uses Kubernetes, you need portability across cloud providers, or you require Kubernetes-specific features and ecosystem tools.

When would ECS be the simpler choice?
> Choose ECS when you want a simpler AWS-native solution with less operational overhead and no Kubernetes expertise required.

---

## Part 8: Container Networking

What is awsvpc networking mode?
> **awsvpc networking mode** (what this means: an ECS networking mode that gives each task its own elastic network interface and a private IP address within your VPC, just like an EC2 instance) is required for Fargate and recommended for EC2 launch type.

In awsvpc mode, what does each task get?
> In awsvpc mode, each task gets its own **ENI** (what this means: Elastic Network Interface, a virtual network card) and a dedicated private IP address in your VPC subnet.

How does an ALB route traffic to ECS containers?
> An ALB routes traffic to ECS containers using **dynamic port mapping** with the bridge networking mode, or directly to the task's IP and container port with awsvpc mode via **IP target type** (what this means: an ALB target group setting that routes to IP addresses directly rather than instance IDs).

How do containers in the same task communicate with each other?
> Containers within the same task in awsvpc mode share a network namespace and communicate over `localhost`.

What is service discovery in ECS? What AWS service powers it?
> **Service discovery** (what this means: a mechanism that lets services find each other by name rather than by hardcoded IP) in ECS is powered by **AWS Cloud Map** (what this means: AWS's managed service registry that maintains a list of healthy task IPs mapped to a DNS name).


---

## Part 9: Container Logging

How do you view container logs in ECS?
> You view ECS container logs in **CloudWatch Logs** when the `awslogs` log driver is configured in your task definition.

What is the awslogs log driver?
> The **awslogs log driver** (what this means: a Docker log driver that streams container stdout and stderr directly to CloudWatch Logs) is the standard way to collect ECS container logs.

What are log groups and log streams?
> A **log group** (what this means: a named container in CloudWatch Logs that holds all related log streams) organizes logs by application or environment; a **log stream** (what this means: the sequence of log events from a single container instance) holds the output from one task.


What is Container Insights?
> **Container Insights** (what this means: a CloudWatch feature that collects CPU, memory, network, and disk metrics from your ECS clusters and tasks) gives you performance monitoring without any custom instrumentation.


---

## Commands to Learn

```bash
# Create an ECR repository
aws ecr create-repository --repository-name my-app
```

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region eu-west-2 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.eu-west-2.amazonaws.com
```

```bash
# List images in an ECR repository
aws ecr list-images --repository-name my-app
```

```bash
# Create an ECS cluster
aws ecs create-cluster --cluster-name my-cluster
```

```bash
# List ECS clusters
aws ecs list-clusters
```

```bash
# Register a task definition from a JSON file
aws ecs register-task-definition --cli-input-json file://task-def.json
```

```bash
# List services in a cluster
aws ecs list-services --cluster my-cluster
```

```bash
# Describe a service
aws ecs describe-services --cluster my-cluster --services my-service
```

```bash
# Update a service to use a new task definition version
aws ecs update-service --cluster my-cluster --service my-service \
  --task-definition my-task:2
```
