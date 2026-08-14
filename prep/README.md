# DevOps Interview Prep

Questions only - no answers. Work through each section from memory before checking your notes.

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
- What is the difference between an absolute path and a relative path?
- What does the `~` character represent, and where does it point?
- How do you find a file by name anywhere on the system?
- What is the difference between a hard link and a symbolic link?
- How do you view the size of a directory and its contents?

### Users, Groups & Permissions
- What do the three permission groups (owner, group, other) represent?
- What does `chmod 755` set, and what does each digit mean?
- What is the difference between `su` and `sudo`?
- How do you add an existing user to a group without removing them from others?
- What is `umask` and how does it affect file creation?
- How would you find all files owned by a specific user?

### Process Management & System Monitoring
- What is the difference between a process and a daemon?
- How do you send a signal to a process, and what is the difference between SIGTERM and SIGKILL?
- What does the load average shown in `top` or `uptime` represent?
- How do you run a process in the background and bring it back to the foreground?
- What command shows which process is listening on a specific port?

### Log Analysis & Text Processing
- What is the difference between `grep` and `awk`?
- How do you follow a log file in real time?
- How would you count the number of occurrences of an error string in a log file?
- What does `|` (pipe) do, and how does it differ from redirecting to a file with `>`?
- How do you extract a specific column from a space-delimited file?

### Networking
- What command shows your current IP address and network interfaces?
- What is the difference between `curl` and `wget`?
- How do you test if a remote port is open from the command line?
- What does `netstat` or `ss` show you?

### Package Management
- What is the difference between `apt install` and `apt-get install`?
- How do you list all installed packages?
- What happens if you run `apt upgrade` vs `apt full-upgrade`?

---

## 2. Git

- What is the difference between `git fetch` and `git pull`?
- What is the difference between `git merge` and `git rebase`, and when would you use each?
- What does a detached HEAD state mean, and how do you get out of it?
- How do you undo the last commit without losing the changes?
- What is the difference between `git reset`, `git revert`, and `git restore`?
- How do you squash multiple commits into one?
- What is a fast-forward merge, and when does it happen?
- How do you resolve a merge conflict?
- What does `git stash` do, and when would you use it over committing?
- What is the purpose of `.gitignore`, and what happens if you add a file that is already tracked?
- What does a force push (`git push --force`) do and why is it dangerous on a shared branch?
- How do you find which commit introduced a specific bug?
- What is the difference between `origin` and `upstream` in a forked repo?

---

## 3. Networking

- What is the OSI model? Name the layers and give one example per layer.
- What is the difference between TCP and UDP?
- What happens when you type a URL into a browser and press enter? Walk through every step.
- What is DNS, and what is the difference between an A record, CNAME, and MX record?
- What is the difference between a public IP and a private IP?
- What is NAT and why is it needed?
- What is a subnet mask and what does CIDR notation represent?
- What is the purpose of a load balancer, and what is the difference between Layer 4 and Layer 7 load balancing?
- What is the difference between HTTP and HTTPS?
- What is TLS, and what does the handshake process involve?
- What is Nginx, and what is the difference between using it as a web server vs a reverse proxy?
- What is the difference between a forward proxy and a reverse proxy?
- What does a 502 Bad Gateway error mean?

---

## 4. Docker

### Core Concepts
- What problem does Docker solve that running an app directly on a host does not?
- What is the difference between a Docker image and a container?
- What is a Docker layer, and why does layer caching matter for build times?
- What happens when you run `docker run` on an image that does not exist locally?
- What is the difference between `docker stop` and `docker kill`?

### Dockerfile
- What is the difference between `CMD` and `ENTRYPOINT`?
- What is the difference between `RUN`, `CMD`, and `ENTRYPOINT`?
- Why should you combine `RUN` commands with `&&` in a Dockerfile?
- What is a multi-stage build and why would you use one?
- Why should you use a non-root user in a Dockerfile?
- What does the `COPY` instruction do, and how does it differ from `ADD`?

### Networking
- What are the default Docker network drivers, and when would you use each?
- How do two containers on the same Docker network communicate?
- What is the difference between binding to `127.0.0.1` and `0.0.0.0` when publishing a port?

### Compose
- What problem does Docker Compose solve over running individual `docker run` commands?
- What is the difference between `depends_on` and a health check in Compose?
- What happens to volumes when you run `docker compose down` vs `docker compose down -v`?
- How do you scale a specific service in Compose?

### Volumes & Persistence
- What is the difference between a bind mount and a named volume?
- Where does Docker store named volumes on the host?
- Why should you not store persistent data inside a container's writable layer?

### Best Practices & Registry
- What is the principle of least privilege as it applies to containers?
- How do you scan a Docker image for vulnerabilities?
- What does it mean for a container to be stateless, and why does it matter?
- What is Docker Hub, and how does image tagging work?
- What is the difference between `latest` and a pinned version tag?

---

## 5. Bash Scripting

### Variables & Parameters
- How do you declare and reference a variable in bash?
- What is the difference between single quotes and double quotes in bash?
- What do `$0`, `$1`, `$#`, and `$@` represent?
- What is the difference between `$@` and `$*`?
- How do you set a default value for a variable if it is not set?

### Conditionals & Loops
- What is the difference between `[ ]` and `[[ ]]` in bash conditionals?
- How do you check if a file exists before reading it?
- What is the difference between `-eq` and `==` for comparisons?
- How do you loop over all files in a directory?
- What is a `while read` loop used for?

### Functions
- How do you define and call a function in bash?
- How do functions return values in bash?
- What is the scope of a variable declared inside a function?

### Piping & Redirection
- What is the difference between `>` and `>>`?
- What does `2>&1` do?
- What is the difference between `/dev/null` and `/dev/stdin`?
- How do you pass the output of one command as an argument (not stdin) to another?

### Error Handling
- What does `set -e` do, and when might it cause unexpected behaviour?
- What does `set -u` do?
- What does the exit code `0` mean vs a non-zero exit code?
- How do you check the exit code of the last command?
- What is a trap in bash and when would you use it?

### Production Standards
- What makes a script "production quality" vs a quick one-liner?
- How do you make a script executable?
- What should go at the top of every production bash script?

---

## 6. AWS

### Core & IAM
- What is the shared responsibility model in AWS?
- What is the difference between an IAM user, group, role, and policy?
- What is the principle of least privilege, and how do you apply it in IAM?
- What is the difference between an inline policy and a managed policy?
- How does an EC2 instance get permissions to call AWS services without storing credentials?
- What is the difference between authentication and authorisation in the context of IAM?

### Networking & VPC
- What is a VPC and why do you need one?
- What is the difference between a public subnet and a private subnet?
- What is an Internet Gateway and a NAT Gateway, and which direction does traffic flow through each?
- What is the difference between a Security Group and a Network ACL?
- What is VPC peering and what are its limitations?
- How do route tables control traffic in a VPC?

### EC2
- What is the difference between an On-Demand, Reserved, and Spot instance?
- What is an AMI and what does it contain?
- What is the difference between stopping and terminating an EC2 instance?
- What is instance metadata and how do you access it from within an instance?
- What is user data and when does it run?

### Security Groups
- What are the default inbound and outbound rules on a new security group?
- Security groups are stateful - what does that mean in practice?
- How do you allow an EC2 instance to accept HTTP traffic only from a load balancer, not from the internet directly?

### Load Balancing
- What is the difference between an Application Load Balancer (ALB) and a Network Load Balancer (NLB)?
- What is a target group?
- How does an ALB perform health checks, and what happens to an unhealthy target?
- What is sticky sessions and when would you use it?

### Storage
- What is the difference between S3, EBS, and EFS?
- What are S3 storage classes and when would you use Glacier over Standard?
- What is S3 versioning and what problem does it solve?
- What is the difference between an S3 bucket policy and an ACL?
- What is EBS and what happens to an EBS volume when an EC2 instance is terminated?

### Route 53
- What is the difference between an A record and an alias record in Route 53?
- What is a hosted zone?
- What routing policies does Route 53 support, and when would you use weighted vs latency-based?

### Containers on AWS
- What is the difference between ECS and EKS?
- What is the difference between EC2 launch type and Fargate in ECS?
- What is a task definition in ECS?
- What is ECR and how does it relate to Docker Hub?

### Serverless
- What is Lambda and what problem does it solve compared to running a server?
- What triggers can invoke a Lambda function?
- What are Lambda cold starts and how do you mitigate them?
- What is API Gateway and how does it work with Lambda?

### CloudFront
- What is CloudFront and what problem does it solve?
- What is the difference between a CloudFront origin and a distribution?
- What is a cache behaviour and what can you control with it?
- How do you invalidate the CloudFront cache?

### Databases
- What is the difference between RDS and DynamoDB?
- What is a Multi-AZ deployment in RDS and why would you use it?
- What is a read replica and when would you use one?
- What is DynamoDB's consistency model?

### Monitoring
- What is the difference between CloudWatch Metrics, Logs, and Alarms?
- What is CloudTrail and how does it differ from CloudWatch?
- What is an SNS topic and how does it relate to CloudWatch Alarms?

### Messaging
- What is the difference between SQS and SNS?
- What is the difference between a standard queue and a FIFO queue in SQS?
- What is a dead-letter queue?

### Security
- What is AWS KMS and what does it manage?
- What is AWS Secrets Manager and how is it different from Parameter Store?
- What is AWS Shield and what does it protect against?
- What is AWS WAF?

### Disaster Recovery & Well-Architected
- What are the four DR strategies (backup & restore, pilot light, warm standby, multi-site), and how do they differ in RTO/RPO?
- What are the five pillars of the AWS Well-Architected Framework?

---

## 7. GitHub Actions

- What is a workflow, a job, and a step? How do they relate to each other?
- What is the difference between `on: push` and `on: pull_request` triggers?
- What is a runner, and what is the difference between a GitHub-hosted runner and a self-hosted runner?
- How do you pass data between steps in the same job?
- How do you pass data between jobs?
- What are GitHub Actions secrets and how do you access them in a workflow?
- What is a matrix strategy and when would you use it?
- What is the difference between `uses` and `run` in a step?
- How do you cache dependencies in a workflow to speed up builds?
- What is a reusable workflow and when would you use it over a composite action?
- How do you prevent a workflow from running on certain branches?
- What does `needs` do in a job definition?
- How would you build and push a Docker image to a registry in a GitHub Actions workflow?

---

## 8. Terraform

- What problem does Terraform solve that writing cloud resources manually in the console does not?
- What is the difference between Terraform and CloudFormation?
- What is a provider in Terraform?
- What is the purpose of `terraform init`?
- What is the difference between `terraform plan` and `terraform apply`?
- What is the Terraform state file and why is it important?
- What are the risks of storing the state file locally?
- What is a remote backend and why should you use one?
- What is the difference between a `resource` and a `data` block?
- What is a Terraform module and why would you use one?
- What is the difference between `count` and `for_each`?
- How do you handle sensitive values like passwords in Terraform?
- What happens when you run `terraform destroy`?
- What is `terraform import` used for?
- What does `terraform fmt` do and why does it matter in a team?

---

## 9. Kubernetes

### Basics & Architecture
- What problem does Kubernetes solve that plain Docker does not?
- What are the two broad categories of nodes in a Kubernetes cluster, and what runs on each?
- What is the API server's role?
- What is etcd and what happens if it goes down?
- What is the scheduler's job?
- What is the kubelet?
- What is kube-proxy?
- What is a namespace and why would you use one?
- What is a Pod? Can a Pod have more than one container, and if so, how do they communicate?

### Running & Managing Workloads
- What is the difference between a Pod and a Deployment?
- What is a ReplicaSet and how does it relate to a Deployment?
- How does a rolling update work in a Deployment?
- What is the difference between `RollingUpdate` and `Recreate` as a Deployment strategy?
- What is a DaemonSet and when would you use one?
- What is a StatefulSet and how does it differ from a Deployment?
- What is a Job and a CronJob in Kubernetes?
- What does it mean for a Pod to be in a `CrashLoopBackOff` state?
- How do liveness and readiness probes differ, and what happens when each fails?

### Exposing Applications
- What are the four Service types in Kubernetes and when would you use each?
- What is the difference between a ClusterIP and a NodePort?
- What is a LoadBalancer service and what does it provision?
- What is an Ingress, and how does it differ from a Service?
- What is an Ingress controller?

### Storage
- What is the difference between a PersistentVolume (PV) and a PersistentVolumeClaim (PVC)?
- What is a StorageClass?
- What does the `accessMode` on a PVC control?
- What is the difference between `Retain`, `Delete`, and `Recycle` reclaim policies?
- What is a StatefulSet's relationship to persistent storage?

### Config & Secrets
- What is the difference between a ConfigMap and a Secret?
- How can you mount a ConfigMap or Secret into a Pod?
- How are Secrets stored in etcd, and what does that mean for security?
- What is the risk of passing secrets as environment variables vs mounting them as files?

### Networking
- How does Pod-to-Pod communication work within a cluster?
- What is a CNI plugin and what does it do?
- What is DNS resolution inside a cluster? How do you reach a Service in another namespace?
- What is a NetworkPolicy and what does it control?
- What is the default network behaviour if no NetworkPolicy exists?

### Ingress & External Access
- What annotations are commonly used on Ingress resources?
- How does TLS termination work at the Ingress level?
- What is the difference between path-based and host-based routing in Ingress?

### Security
- What is RBAC in Kubernetes?
- What is the difference between a Role and a ClusterRole?
- What is a ServiceAccount and why should Pods use dedicated ones?
- What is a PodSecurityContext?
- What does `runAsNonRoot: true` enforce?
- What is the principle of least privilege as it applies to Kubernetes workloads?

### Scheduling & Node Management
- How does the Kubernetes scheduler decide which node to place a Pod on?
- What is the difference between node selectors, node affinity, and taints/tolerations?
- What is a taint and what does it do?
- What is a toleration?
- What is the difference between `NoSchedule`, `PreferNoSchedule`, and `NoExecute` taint effects?
- What are resource requests and limits, and what happens when a container exceeds its memory limit?

### Observability
- What is the difference between logs, metrics, and traces?
- How do you stream logs from a running Pod?
- How do you get logs from a crashed Pod?
- What is the Kubernetes metrics server used for?
- What is `kubectl top` and what does it show?

---

## 10. Monitoring & Observability

### Foundations
- What is the difference between monitoring and observability?
- What are the three pillars of observability?
- What is the difference between a metric, a log, and a trace?
- What is the difference between push-based and pull-based metric collection?
- What is the RED method, and what does each letter stand for?
- What is the USE method?

### Prometheus
- What is Prometheus and how does it collect metrics?
- What is a scrape target and how does Prometheus discover them?
- What are the four Prometheus metric types?
- What is the difference between a Counter and a Gauge?
- What is PromQL? Write a query that gives you the per-second rate of a counter over the last 5 minutes.
- What is the Alertmanager and how does it relate to Prometheus?
- What is a recording rule and why would you create one?
- What is the Pushgateway used for?

### Grafana
- What is Grafana and what problem does it solve on its own?
- What is a data source in Grafana?
- What is the difference between a dashboard panel and a row?
- What are Grafana variables and how do they make dashboards reusable?
- What is a Grafana alert, and how does it differ from a Prometheus alert?

### Alertmanager
- What is the role of Alertmanager relative to Prometheus?
- What is alert grouping and why is it useful?
- What is alert silencing vs alert inhibition?
- What is a receiver in Alertmanager?

### Loki
- What is Loki and how does it differ from Elasticsearch for log storage?
- What is a label in Loki and why should you keep the label cardinality low?
- What is LogQL? Give an example of filtering logs by label and then by content.
- What is Promtail?
- What is the difference between Loki's index and the log chunks?

### Full Stack
- How do Prometheus, Grafana, Alertmanager, and Loki work together as a monitoring stack?
- What is the first thing you would check when you receive an alert that a service is down?
- How would you design alerting to minimise alert fatigue?
- What is the difference between a symptom-based alert and a cause-based alert? Which is preferred?

---

## 11. General DevOps

- What is DevOps and what problem does it solve in a software organisation?
- What is the difference between CI and CD?
- What is the difference between continuous delivery and continuous deployment?
- What is a deployment pipeline and what stages does it typically have?
- What is infrastructure as code (IaC) and why does it matter?
- What is the difference between mutable and immutable infrastructure?
- What is a blue-green deployment?
- What is a canary deployment?
- What is the difference between horizontal scaling and vertical scaling?
- What is a single point of failure and how do you eliminate one?
- What is an SLA, SLO, and SLI? How do they relate to each other?
- What is toil in SRE, and why does it matter?
- What is the four golden signals of monitoring?
- What is the difference between mean time to detect (MTTD) and mean time to recover (MTTR)?
- What is shift-left security?
- If a production deployment goes wrong, what is your first action?
- How would you roll back a bad deployment with zero downtime?
- What is the 12-factor app methodology?
- What does "idempotent" mean in the context of infrastructure or scripts?
