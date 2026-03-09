# 1. AWS Introduction

## Part 1: What is Cloud Computing

What is cloud computing in simple terms?
> 

What does "on-demand" mean in cloud computing?
> 

What does "pay-as-you-go" mean?
> 

What are the three cloud service models?
>

Give an AWS example of IaaS:
>

Give an AWS example of PaaS:
>

Give an AWS example of SaaS:
> 

What is the difference between public cloud, private cloud, and hybrid cloud?

>

---

## Part 2: Shared Responsibility Model

What is the shared responsibility model?
>

What is AWS responsible for?
>

What are YOU responsible for?
>

Give an example of something that is your responsibility, not AWS's:
>
---

## Part 3: AWS Global Infrastructure

What is an AWS Region?
>

What is an Availability Zone (AZ)?
> 

How are Regions and AZs related?
> 

How many AZs does a typical Region have?
> 

Why would you choose one Region over another? Name at least 3 factors:
> 

What is an Edge Location?
> 

What services use Edge Locations?
> 

---

## Part 4: AWS Free Tier

What is the AWS Free Tier?
> 

What are the three types of Free Tier offers?
> 

What EC2 instance type is Free Tier eligible?
> 

What happens when you exceed Free Tier limits?
> 

What services commonly cause surprise charges that catch people out?
> 

How do you check your Free Tier usage?
> 

---

## Part 5: Account Security

Why should you NOT use the root account for daily tasks?
> 

What is the first thing you should do after creating an AWS account?
> 

What is MFA?
> 

Why should you enable MFA on the root account immediately?
> 

What is the difference between the root account and an IAM admin user?
> 

---

## Part 6: Billing and Cost Management

How do you set up a billing alarm?
> 

What is AWS Budgets?
> 

What is Cost Explorer?
> 

How do tags help with cost management?
> 

What is the quickest way to find out what is costing you money right now?
> 

---

## Part 7: AWS Console and CLI

How do you navigate to a service in the AWS Management Console?
> 

What is AWS CloudShell?
> 

How do you install AWS CLI v2?
> 

What does `aws configure` do?
> 

What four things does `aws configure` ask you for?
> 

What is a named profile? When would you use one?
> 

What output formats are available in the CLI?
> 

---

## Commands to Learn

```bash
# What does this do?
aws configure
```
> 

```bash
# What does this do?
aws sts get-caller-identity
```
> 

```bash
# What does this do?
aws configure --profile dev
```
> 

```bash
# What does this do?
aws ec2 describe-regions --output table
```
> 

```bash
# What does this do?
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
   > 

2. Name three things that can cause surprise charges on a new AWS account.
   > 

3. Why is the root account dangerous to use day-to-day?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________