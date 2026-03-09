# 17. Well-Architected Framework, CloudFormation, and Beanstalk

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Well-Architected Framework

What is the AWS Well-Architected Framework?
>

What are the six pillars? Name all of them.
>

---

## Part 2: The Six Pillars

What is the Operational Excellence pillar about?
>

What is the Security pillar about?
>

What is the Reliability pillar about?
>

What is the Performance Efficiency pillar about?
>

What is the Cost Optimisation pillar about?
>

What is the Sustainability pillar about?
>

---

## Part 3: Well-Architected Tool

What is the AWS Well-Architected Tool?
>

How do you use it?
>

What does it produce?
>

---

## Part 4: AWS Trusted Advisor

What is AWS Trusted Advisor?
>

What five categories does Trusted Advisor check?
>

Which checks are free and available to all accounts?
>

Which checks require a Business or Enterprise support plan?
>

Give an example of a Trusted Advisor recommendation.
>

---

## Part 5: CloudFormation Basics

What is AWS CloudFormation?
>

What is Infrastructure as Code (IaC)?
>

What format are CloudFormation templates written in?
>

What is a stack?
>

What happens when you delete a stack?
>

What is the difference between CloudFormation and Terraform?
>

---

## Part 6: CloudFormation Concepts

What are the main sections of a CloudFormation template (Resources, Parameters, Outputs, Mappings)?
>

What is the only required section?
>

What is a stack update? What happens to existing resources?
>

What is drift detection?
>

What is a nested stack? When would you use one?
>

What is a changeset?
>

---

## Part 7: Elastic Beanstalk

What is AWS Elastic Beanstalk?
>

How is Beanstalk different from deploying manually on EC2?
>

What does Beanstalk manage for you?
>

What components make up a Beanstalk environment (ALB, ASG, EC2, RDS)?
>

What is the difference between a web server environment and a worker environment?
>

What deployment strategies does Beanstalk support (all at once, rolling, immutable)?
>

When would you use Beanstalk?
>

---

## Commands to Learn

```bash
# What does this do?
aws cloudformation create-stack --stack-name my-stack \
  --template-body file://template.yaml
```
>

```bash
# What does this do?
aws cloudformation describe-stacks --stack-name my-stack
```
>

```bash
# What does this do?
aws cloudformation delete-stack --stack-name my-stack
```
>

```bash
# What does this do?
aws cloudformation detect-stack-drift --stack-name my-stack
```
>

---

## Hands-On Tasks

- Deploy a simple EC2 instance using a CloudFormation template
- Update the stack to change the instance type and observe the changeset
- Deploy a web application using Elastic Beanstalk
- Run the Well-Architected Tool review on your workload
- Review Trusted Advisor recommendations on your account

---

## Quick Quiz

1. What are the six pillars of the Well-Architected Framework?
   >

2. What is CloudFormation and how does it differ from manually creating resources?
   >

3. When would you use Elastic Beanstalk over deploying with CloudFormation directly?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
