# 9. Container Services

---

## Part 1: Why Containers on AWS

You can already run Docker on EC2 manually. What problems does that create at scale?
> Running Docker on EC2 manually at scale means you must handle instance provisioning, container placement across hosts, restart logic for failed containers, rolling deployments, and load balancer registration yourself.

What does a container orchestration service solve?
> A **container orchestration service** automatically places, starts, stops, scales, and replaces containers across a fleet of machines, removing that operational burden from you.

What container orchestration services does AWS offer?
> AWS offers **ECS** (Elastic Container Service), AWS's own orchestration tool, and **EKS** (Elastic Kubernetes Service), which runs managed Kubernetes on AWS.

---

## Part 2: ECS Core Concepts

What is ECS (Elastic Container Service)?
> AWS's managed service for running and scaling Docker containers. Handles scheduling, placement, and lifecycle of your containers.

What is a cluster in ECS?
> A **cluster** is a logical grouping of compute resources where ECS runs your containers - it's the boundary within which your tasks and services operate.

What is a task definition?
> A **task definition** is a JSON blueprint that describes how one or more containers should run - the image, CPU, memory, ports, environment variables, and IAM roles.

What is a task?
> A **task** is a running instance of a task definition - the actual containers executing on your cluster.

What is a service?
> A **service** is an ECS construct that ensures a specified number of tasks are always running and replaces any that stop or fail, keeping your application continuously available.

What is the relationship between task definition, task, and service?
> - task definition is the template.
> - task is the instantiation of that template.
> - a service manages how many tasks run and keeps that count healthy.

How does an ECS service differ from just running a standalone task?
> An ECS service continuously monitors running tasks and automatically replaces failed ones to maintain your desired count, whereas a standalone task runs once and stops when finished.

---

## Part 3: ECR (Elastic Container Registry)

What is ECR?
> **ECR** (Elastic Container Registry) is AWS's fully managed Docker container image registry - it stores and serves your container images within AWS.

What is a repository in ECR?
> A **repository** is a named storage location within ECR for all versions of a single container image - it's where you push and pull a specific image.

How do you authenticate Docker to ECR?
> Run `aws ecr get-login-password` piped into `docker login` using the registry URL.

Walk through the steps to build and push an image to ECR:
> 1. Create the ECR repository.
> 2. Authenticate Docker to ECR with `aws ecr get-login-password ... | docker login ...`
> 3. Build your image with `docker build -t my-app .`
> 4. Tag it with the ECR URI: `docker tag my-app:latest <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest`
> 5. Push with `docker push <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest`

How long does the ECR authentication token last?
> 12 hours.

What is a lifecycle policy in ECR? Why use one?
> A **lifecycle policy** is a rule that automatically expires and deletes old images from your ECR repository based on age or count, keeping storage costs down by removing images you no longer need.

What is image scanning in ECR?
> **Image scanning** checks your container images for known OS and package vulnerabilities using a CVE database, helping you catch security issues before deploying.

---

## Part 4: IAM Roles

What is a task role?
> A **task role** is an IAM role that your running container assumes to call other AWS services, like reading from S3 or writing to DynamoDB. It gives your application code its AWS permissions.

What is a task execution role?
> A **task execution role** is an IAM role used by the ECS agent to perform infrastructure tasks like pulling your container image from ECR and sending logs to CloudWatch.

What is the difference between them?
> - task role is for your application code.
> - execution role is for ECS's own setup operations.

Give an example of when each is used:
> - task role is used when your application code calls `s3.getObject()` or `dynamodb.putItem()`.
> - execution role is used when ECS pulls the image from ECR and writes container startup logs to CloudWatch.

---

## Part 5: Task Definitions

What format is a task definition written in?
> Written in JSON and registered with ECS.

What is a container definition within a task definition?
> A **container definition** is the section of a task definition that describes a single container - its image, resources, ports, and configuration.

What do you specify in a container definition? Name at least 5 things.
> In a container definition you specify: Docker image URI, CPU units, memory limit, port mappings, environment variables, log configuration, command override, and health check command.

How do you set CPU and memory limits on a task?
> You set CPU and memory at both the task level (hard limits for the whole task) and optionally at the container level. Fargate requires task-level CPU and memory values from a fixed list of valid combinations.

How do you pass environment variables to a container in ECS?
> You pass environment variables to containers either as plaintext key-value pairs in the container definition, or as references to SSM Parameter Store or Secrets Manager - AWS services that store configuration and secrets securely, keeping sensitive values out of your task definitions.

Can you have multiple containers in a single task definition? When would you?
> Yes, a single task definition can include multiple containers. You do this when containers are tightly coupled and must run together, such as an application container paired with a logging agent.

What is the sidecar pattern?
> The **sidecar pattern** means running a helper container alongside your main application container in the same task to handle cross-cutting concerns like logging, metrics collection, or proxy functions - keeping auxiliary logic separate from your application code.

---

## Part 6: Cluster

What is a cluster and what does creating one actually provision?
> A **cluster** is the logical boundary where your ECS tasks and services run. Creating a Fargate cluster provisions nothing - there are no servers to manage. Creating an EC2 cluster requires you to register EC2 instances into it as container hosts.

What are the two launch type options when creating a cluster?
> Fargate, where AWS manages the underlying infrastructure, and EC2, where you manage the host instances yourself.

Can a single cluster run both Fargate and EC2 tasks?
> Yes, a cluster supports mixed launch types. You can run some services on Fargate and others on EC2 within the same cluster.

What is cluster capacity in the EC2 launch type?
> **Cluster capacity** is the total CPU and memory available across all registered EC2 instances. ECS schedules tasks onto instances that have enough remaining capacity. If the cluster is full, new tasks will fail to place until capacity is added.

What is a Capacity Provider?
> A **Capacity Provider** links a cluster to an Auto Scaling Group so ECS can automatically add or remove EC2 instances based on task demand, keeping cluster capacity in sync with your workload.

---

## Part 7: Service

What do you configure when creating a service?
> When creating a service you specify: the task definition to use, the desired task count, the launch type (Fargate or EC2), the VPC subnets and security groups for the tasks, and optionally a load balancer target group to attach to.

What is desired count?
> **Desired count** is the number of tasks ECS will keep running at all times. If a task stops or fails, the service scheduler launches a replacement to maintain this count.

How does a service attach to an ALB?
> You specify a **target group** and the container name and port in the service configuration. ECS automatically registers and deregisters task IPs with the target group as tasks start and stop.

What is a rolling deployment in ECS?
> A **rolling deployment** replaces running tasks with new ones gradually. ECS starts new tasks with the updated task definition, waits for them to pass health checks, then stops the old ones - keeping the service available throughout.

What controls rolling deployment behaviour?
> Two settings: **minimum healthy percent** (the floor - how many old tasks must stay up during the update) and **maximum percent** (the ceiling - how many total tasks can run at once during the update).

How do you deploy a new version of your container?
> Push the new image to ECR, register a new task definition revision pointing to it, then update the service to use the new revision. ECS performs a rolling deployment automatically.

What is auto-scaling in ECS?
> **Auto-scaling** adjusts the service's desired count up or down based on CloudWatch metrics like CPU utilisation or request count, so your service scales with load without manual intervention.

---

## Part 8: Fargate vs EC2 Launch Type

What is the EC2 launch type? What are you responsible for managing?
> The **EC2 launch type** is an ECS mode where you provision and manage the EC2 instances in your cluster yourself. You are responsible for instance sizing, patching, scaling the underlying hosts, and cluster capacity.

What is Fargate? What does AWS manage for you?
> **Fargate** is a serverless compute engine for ECS where AWS provisions and manages the underlying infrastructure. You only define your task's CPU and memory requirements.

What is the key difference between them from an operations perspective?
> With Fargate you define what your container needs and AWS runs it. With EC2 launch type you manage the host machines that run your containers.

When would you choose Fargate over EC2 launch type?
> Choose Fargate when you want to avoid managing servers, have variable or unpredictable workloads, or want to get started quickly without capacity planning.

When would you choose EC2 launch type over Fargate?
> Choose EC2 launch type when you need specific instance types (GPU, high memory), want to use Spot Instances for cost savings, or have workloads dense enough that EC2 is significantly cheaper.

How does pricing differ between them?
> Fargate pricing is per vCPU and GB of memory per second of task runtime. EC2 launch type pricing is the cost of the underlying EC2 instances regardless of how packed they are with tasks.

---

## Part 9: Container Networking

What is awsvpc networking mode?
> **awsvpc networking mode** gives each task its own elastic network interface and a private IP address within your VPC, just like an EC2 instance. It is required for Fargate and recommended for EC2 launch type.

In awsvpc mode, what does each task get?
> Each task gets its own **ENI** (Elastic Network Interface) - a virtual network card - and a dedicated private IP address in your VPC subnet.

How does an ALB route traffic to ECS containers?
> An ALB routes traffic to ECS containers using **dynamic port mapping** with bridge networking mode, or directly to the task's IP and container port with awsvpc mode via **IP target type** - an ALB target group setting that routes to IP addresses directly rather than instance IDs.

How do containers in the same task communicate with each other?
> Containers within the same task in awsvpc mode share a network namespace and communicate over `localhost`.

What is service discovery in ECS? What AWS service powers it?
> **Service discovery** lets services find each other by DNS name rather than by hardcoded IP. In ECS it's powered by **AWS Cloud Map**, AWS's managed service registry that maps DNS names to healthy task IPs.

---

## Part 10: Container Logging

How do you view container logs in ECS?
> You view ECS container logs in **CloudWatch Logs** when the `awslogs` log driver is configured in your task definition.

What is the awslogs log driver?
> The **awslogs log driver** streams container stdout and stderr directly to CloudWatch Logs and is the standard way to collect ECS container logs.

What are log groups and log streams?
> A **log group** is a named container in CloudWatch Logs that holds all related log streams, typically organized by application or environment. A **log stream** holds the sequence of log events from a single container instance.

What is Container Insights?
> **Container Insights** is a CloudWatch feature that collects CPU, memory, network, and disk metrics from your ECS clusters and tasks, giving you performance monitoring without any custom instrumentation.

---

## Part 11: EKS Overview

What is EKS (Elastic Kubernetes Service)?
> **EKS** (Elastic Kubernetes Service) is AWS's managed service that runs a Kubernetes control plane for you, so you can use Kubernetes without operating the control plane yourself.

What does "managed control plane" mean in EKS?
> AWS runs, patches, scales, and backs up the **Kubernetes control plane** - the set of components (API server, etcd, scheduler, controller manager) that manage the cluster - so you only manage worker nodes.

What are the worker node options in EKS?
> Self-managed EC2 nodes, **managed node groups** (EC2 nodes where AWS handles provisioning and lifecycle), and Fargate for serverless pods.

When would you choose EKS over ECS?
> Choose EKS when your team already uses Kubernetes, you need portability across cloud providers, or you require Kubernetes-specific features and ecosystem tools.

When would ECS be the simpler choice?
> Choose ECS when you want a simpler AWS-native solution with less operational overhead and no Kubernetes expertise required.

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
# List task definition revisions
aws ecs list-task-definitions --family-prefix my-task
```

```bash
# Create a Fargate service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-service \
  --task-definition my-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc],securityGroups=[sg-abc],assignPublicIp=ENABLED}"
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

```bash
# Force a new deployment (redeploy with same task definition)
aws ecs update-service --cluster my-cluster --service my-service \
  --force-new-deployment
```
