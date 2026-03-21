# 1. AWS Introduction

## Part 1: What is Cloud Computing

What is cloud computing in simple terms?
> Renting computing resources (servers, storage, databases, networking) over the internet instead of owning physical hardware. You use what you need, when you need it, and pay accordingly.

What does "on-demand" mean in cloud computing?
> Resources are available instantly whenever you need them, and you stop paying when you stop using them. No need to pre-purchase hardware or wait weeks for provisioning.

What does "pay-as-you-go" mean?
> There is no fixed price. You only pay as much as you use.

What are the three cloud service models?

> - IaaS (Infrastructure as a Service) - raw infrastructure, you manage the OS and above e.g. EC2 (you get a virtual server, you install what you want)
> - PaaS (Platform as a Service) - platform to run your code, AWS manages the infrastructure e.g. Elastic Beanstalk (deploy your app, AWS handles the server)
> - SaaS (Software as a Service) - ready to use software, e.g. Amazon Workmail (just use it, no setup)

Give an AWS example of IaaS:
> EC2, S3, VPC

Give an AWS example of PaaS:
> Elastic Beanstalk, Lambda (Serverless)

Give an AWS example of SaaS:
> WorkMail

What is the difference between public cloud, private cloud, and hybrid cloud?

> - Public - shared infrastructure owned by AWS, available to anyone (what you use by default)
> - Private - cloud infrastructure dedicated to a single organisations, hosted on-premise or by a provider
> - Hybrid - mix of both, on-premise system connected to public cloud (common in enterprises that can't move everything to cloud)

---

## Part 2: Shared Responsibility Model

What is the shared responsibility model?
> AWS is responsible for the security of the cloud (physical infrastructure, hardware, hypervisor) whilst customers are responsible for security in the cloud (data, application code, IAM).

What is AWS responsible for?
> Physical infrastructure, hardware, hypervisor, networking infrastructure, managed services patching, AZ/Region infrastructure.

What are YOU responsible for?
> Data, application code, IAM, OS patching on EC2, Network/security group configuration, Encryption, Firewall configuration

Give an example of something that is your responsibility, not AWS's:
> IAM - ensuring users have only the necessary permission ([least privilege](/notes/02-iam.md#part-4-iam-policies))

---

## Part 3: AWS Global Infrastructure

What is an AWS Region?
> A physical location in the world, where AWS has clusters of data centres e.g. `eu-west-2` (london), `us-east-1` (N.Virginia). Each region is completely independent - data does not leave a region unless you explicitly move it.

What is an Availability Zone (AZ)?
> One or more physical data centres within a region, each with independent power, cooling and networking. They are isolated from each other so that failure in one doesn't affect another (this is to ensure high availability). They are connected via high bandwidth, low-latency, fully redundant private fibre optics network.

![AWS Region](/assets/notes/aws-region-az.png)

How are Regions and AZs related?
> Regions are a geographical location and AZs are data centres within that region, multiple AZs can belong to a single region.

How many AZs does a typical Region have?
> Typically 3 or more.

Why would you choose one Region over another? Name at least 3 factors:
> Latency, local laws (GDPR), service availability

What is an Edge Location?
> A specialised, geographically distributed data centre aimed to bring content and cloud services closer to users for low-latency and improving speeds.

What services use Edge Locations?
> CloudFront, Route53, Shield, WAF (Web Application Firewall)

---

## Part 4: AWS Free Tier

What is the AWS Free Tier?
> 12-month free trials for new accounts (e.g., EC2, S3), "Always Free" services for everyone with monthly limits

What are the three types of Free Tier offers?

> - 12-Month Free Tier (New Customers Only) - 750 hours per month of Amazon EC2 (t2.micro/t3.micro), 5 GB of Amazon S3 storage, and 750 hours of Amazon RDS
> - Always Free (All Customers) - 1 million AWS Lambda requests per month, 25 GB of DynamoDB storage, and 10 custom CloudWatch metrics.
> - Short-Term Trials - Amazon Redshift (2 months), Amazon SageMaker (2 months), and Amazon Inspector (15 days).
> - New 6-Month Offer (As of July 2025) - Provides $100-$200 in credits for new customers to use over 6 months, requiring tasks to be completed to unlock full credit amounts.

What EC2 instance type is Free Tier eligible?
> T3.micro, T3.small, T4g.micro, T4g.small, C7i-flex.large, M7i-flex.large

What happens when you exceed Free Tier limits?
> You are charged standard on-demand rates for any usage beyond the free tier limits.

What services commonly cause surprise charges that catch people out?
> EC2 Instance running 24/7, elastic IP (You get charged when an Elastic IP is not associated with a running instance at all), NAT Gateway, EBS snapshots, data transfer.

How do you check your Free Tier usage?
> Billing and Cost Management - Free Tier

---

## Part 5: Account Security

Why should you NOT use the root account for daily tasks?
> To prevent a single user from having unrestricted access to everything. A root account can do things that cannot be restricted by IAM policies - like closing the account or changing the support plan. If root was compromised this could lead to system abuse and skyrocket AWS bill. The concept of least privilege should be implemented so users only have access to what they need.

What is the first thing you should do after creating an AWS account?
> Set up MFA on root, create IAM admin user, set up billing alerts.

What is MFA?
> [Multi-Factor Authentication](/notes/02-iam.md#part-6-security-best-practices) - require a second form of verification beyond a password (e.g. code from an authenticator app)

Why should you enable MFA on the root account immediately?
> To add another layer of security, protecting the root account should be priority as this has unrestricted access and can't be limited by IAM policies.

What is the difference between the root account and an IAM admin user?
> root has unrestricted access, IAM admin user may have administrator privilege but still comes with limitation such as can not close aws account, change account email or support plan. Admin permissions can be revoked by root.

---

## Part 6: Billing and Cost Management

How do you set up a billing alarm?
> [CloudWatch](/notes/13-monitoring.md#part-3-cloudwatch-alarms) alarms with billing metrics and or Billing and Cost Management - Budgets

What is AWS Budgets?
> You can setup budgets that alert you within a specified threshold. This has the ability to automate actions when thresholds are hit (e.g. stop an EC2 instance)

What is Cost Explorer?
> A free AWS tool used to visualise, analyse and manage AWS spending and usage over time.

How do tags help with cost management?
> Help with cost management by acting as key-value pair labels for cloud resources, enabling detailed categorisation, tracking, and analysis of spending (e.g. You can tag a website with `Project: website`, then in cost explorer you can filter by tag)

What is the quickest way to find out what is costing you money right now?
> Billing and Cost Management - Cost Explorer

---

## Part 7: AWS Console and CLI

How do you navigate to a service in the AWS Management Console?
> Search bar on the top

What is AWS CloudShell?
> Browser based, pre-authenticated command line environment, no setup required. Can be accessed through the terminal icon in the management console navbar

How do you install AWS CLI v2?
```bash
#Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

What does `aws configure` do?
> configures your CLI with your AWS credentials and stores config within `.aws` inside your home directory.

What four things does `aws configure` ask you for?
> - AWS Access Key ID: The public key for your IAM user.
> - AWS Secret Access Key: The private key for your IAM user.
> - Default region name: The AWS region (e.g., us-east-1) you want to use by default.
> - Default output format: The format for CLI output (e.g., json, text, or table). 

What is a named profile? When would you use one?
> Used by AWS to maintain more than one set of active credentials for you to use with AWS-CLI, SDK, or other third-party tools. Named profiles are stored in ~/.aws/credentials file in the ini file format. Useful if you have a personal AWS account and a work account.

What output formats are available in the CLI?
> JSON, text, table, or YAML

---

## Commands to Learn

```bash
# Configure AWS CLI
aws configure
```
> 

```bash
# Return information about the IAM identity used to authenticate request, useful for verifying your CLI is configured correctly
aws sts get-caller-identity
```
> 

```bash
# Configure a named profile for dev
aws configure --profile dev
```
> 

```bash
# Describe regions enabled for your account
aws ec2 describe-regions --output table
```
> 

```bash
# Return current region
aws configure get region
```
> 

---

## Hands-On Tasks

- Create an AWS account, enable MFA on root, and create an IAM admin user
- Set up a billing alarm for £5
- Install AWS CLI, run `aws configure`, and verify with `aws sts get-caller-identity`
- Open CloudShell and run a command
- Switch between two Regions in the console and notice the difference

---

## Quick Quiz

1. What is the difference between a Region and an Availability Zone?


2. Name three things that can cause surprise charges on a new AWS account.


3. Why is the root account dangerous to use day-to-day?


---

## Confidence: 🟢

**Date completed:** 09/03/26