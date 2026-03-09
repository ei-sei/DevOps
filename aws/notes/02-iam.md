# 2. Identity & Access Management (IAM)

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: What is IAM

What is IAM?
> 

What is the difference between authentication and authorisation?
> 

Is IAM a global service or a regional service?
> 

---

## Part 2: IAM Users

What is an IAM User?
> 

What are the two types of access an IAM User can have?
> 

When would you create an IAM User?
> 

---

## Part 3: IAM Groups

What is an IAM Group?
> 

Can a user belong to multiple groups?
> 

Can groups be nested (a group inside another group)?
> 

Why should you manage permissions through groups instead of attaching policies directly to users?
> 

---

## Part 4: IAM Policies

What is an IAM Policy?
> 

What format is a policy written in?
> 

What are the main parts of a policy document (Version, Statement, Effect, Action, Resource, Condition)?
> 

What does `"Effect": "Allow"` do?
> 

What does `"Effect": "Deny"` do?
> 

What happens when an explicit Allow and an explicit Deny conflict on the same action?
> 

What is the default behaviour if there is no explicit Allow or Deny? (implicit deny)
> 

What is the difference between an AWS managed policy and a customer managed policy?
> 

What is an inline policy? When would you use one?
> 

What does "least privilege" mean?
> 

Why is `"Resource": "*"` dangerous?
> 

---

## Part 5: IAM Roles

What is an IAM Role?
> 

How is a Role different from a User?
> 

When would you use a Role instead of a User?
> 

What is a trust policy?
> 

What is an instance profile?
> 

How does an EC2 instance get AWS permissions without access keys?
> 

What is the difference between the trust policy and the permissions policy on a role?
> 

---

## Part 6: Security Best Practices

What is MFA and why use it?
> 

What are Access Keys used for?
> 

Why should you never hardcode Access Keys in code or commit them to Git?
> 

How often should you rotate Access Keys?
> 

What is the IAM Credential Report? What does it show?
> 

What is IAM Access Analyzer?
> 

---

## Part 7: Cross-Account Access

How do you grant access to resources in another AWS account?
> 

What does `sts:AssumeRole` do?
> 

Walk through the flow: User in Account A needs to access S3 in Account B.
> 

---

## Part 8: Identity Federation

What is identity federation?
> 

Why would a company use federation instead of creating IAM Users for every employee?
> 

What is AWS IAM Identity Center (formerly SSO)?
> 

---

## Commands to Learn

```bash
# What does this do?
aws iam list-users
```
> 

```bash
# What does this do?
aws iam create-user --user-name devops-user
```
> 

```bash
# What does this do?
aws sts get-caller-identity
```
> 

```bash
# What does this do?
aws iam attach-user-policy --user-name devops-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```
> 

```bash
# What does this do?
aws iam list-attached-user-policies --user-name devops-user
```
> 

```bash
# What does this do?
aws iam list-roles
```
> 

```bash
# What does this do?
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name my-session
```
> 

---

## Hands-On Tasks

- Create an IAM User with console access, add them to an "Admins" group
- Write a custom JSON policy that allows read-only access to a specific S3 bucket
- Create an IAM Role for EC2 with S3 read access, launch an instance with it, verify access
- Enable MFA on your IAM admin user
- Use the IAM Policy Simulator to test a policy

---

## Quick Quiz

1. What is the difference between an IAM User, Group, and Role?
   > 

2. What happens when there is an explicit Deny and an explicit Allow on the same action?
   > 

3. How would you give an EC2 instance access to S3 without using access keys?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________