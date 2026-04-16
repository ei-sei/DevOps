# 2. Identity & Access Management (IAM)

---

## Part 1: What is IAM

What is IAM?
> Identity and Access Management - A way to manage users and permissions, so who can access what resource and how.

What is the difference between authentication and authorisation?
> Authentication verifies who you are using credentials such as passwords. Authorisation determines users permissions (what you can access)

Is IAM a global service or a regional service?
> Global - IAM users/roles/policies work across all regions

---

## Part 2: IAM Users

What is an IAM User?
> Long term identity created within the cloud service representing a specific person or application

What are the two types of access an IAM User can have?
> console access (password), programmatic access (access keys)

When would you create an IAM User?
> when a person needs their own credentials to interact with AWS, or when an application needs long-term credentials (though for applications, roles are usually preferred now)

---

## Part 3: IAM Groups

What is an IAM Group?
> A group with defined permission sets - only users can be added to the group to inherit the permissions.

Can a user belong to multiple groups?
> Yes - they will also inherit the permissions from both groups

Can groups be nested (a group inside another group)?
> No

Why should you manage permissions through groups instead of attaching policies directly to users?
> Easier to manage at scale - attach a policy once to a group instead of individually to each user. Also ensures consistency, e.g. 10 developers all get the exact same permissions rather than risking one being configured differently.

---

## Part 4: IAM Policies

What is an IAM Policy?
> A JSON document that defines what actions are allowed or denied on which AWS resources.

What format is a policy written in?
> JSON

What are the main parts of a policy document (Version, Statement, Effect, Action, Resource, Condition)?
> - Version - policy language version (always "2012-10-17")
> - Statement - the container for one or more permission blocks
> - Effect - allow or deny
> - Action - what API calls (e.g. s3:GetObject)
> - Resource - which AWS resource (ARN)
> - Condition - optional, when the rule applies (e.g. only from a specific IP)

What does `"Effect": "Allow"` do?
> Allow: permits the specified actions on the specified resources

What does `"Effect": "Deny"` do?
> Deny: blocks the specified actions on the specified resources

What happens when an explicit Allow and an explicit Deny conflict on the same action?
> The deny action will always take priority

What is the default behaviour if there is no explicit Allow or Deny? (implicit deny)
> Deny

What is the difference between an AWS managed policy and a customer managed policy?
> AWS managed policies are maintained and updated by AWS (e.g. when new services launch), while customer managed policies give you full control but you're responsible for maintaining them. Examples: `AmazonS3ReadOnlyAccess` is AWS managed; a policy you write for your specific S3 bucket is customer managed.

What is an inline policy? When would you use one?
> Inline policies are embedded directly into a single entity, resulting in a strict 1:1 relationship where the policy is deleted when the entity is removed. In practice you will use managed policies for almost everything as they're easier to manage. You will use inline policy when you want a permission that is strictly tied to one specific user or role and should never accidentally end up attached to anything else.

What does "least privilege" mean?
> Least privilege means giving users, services, or systems only the minimum permissions required to perform their specific job - nothing more, nothing less. The principle exists to limit the blast radius of a breach or misconfiguration: if an IAM role, EC2 instance, or Lambda function is compromised, the attacker can only do what that entity was permitted to do. In AWS, this means avoiding wildcard permissions like `s3:*` or `AdministratorAccess` unless absolutely necessary, and instead scoping policies to exact actions on exact resources.

Why is `"Resource": "*"` dangerous?
> Applies the action to all AWS resources, which violates least privilege. The real danger is combining `"Action": "*"` with `"Resource": "*"` - this gives unrestricted access to everything in the account.

---

## Part 5: IAM Roles

What is an IAM Role?
> entity that provides temporary security credentials with specific permissions that defines allowed actions for authorized users, applications, or services

How is a Role different from a User?
> A user has a fixed identity, a role can be assumed by anyone/anything the trust policy allows.

When would you use a Role instead of a User?
> When you need temporary short term permissions for services (like EC2, Lambda) or cross-account access.

What is a trust policy?
> Trust policy specifies which trusted account members are allowed to assume roles.

What is an instance profile?
> A container for an IAM role which passes information to an EC2 instance

How does an EC2 instance get AWS permissions without access keys?
> Instance profile, by attaching an IAM role via an instance profile, the EC2 instance receives temporary credentials automatically.

What is the difference between the trust policy and the permissions policy on a role?
> Permission policy determines whether the request is allowed or denied. Trust policy determines who can assume an IAM role.

---

## Part 6: Security Best Practices

What is MFA and why use it?
> Multi-Factor Authentication (MFA) - is a security mechanism that requires users to verify their identity using two or more independent factors before gaining access to a system. These factors fall into three categories: something you know (a password or PIN), something you have (a phone, hardware token, or authenticator app), and something you are (a fingerprint or face scan). The idea is that even if an attacker steals your password, they still can't log in without the second factor - significantly reducing the risk of unauthorized access. Common examples include entering a password and then a time-based one-time code (TOTP) from an app like Google Authenticator, or receiving an SMS code after logging in.

What are Access Keys used for?
> programmatic access - CLI, SDKs, and direct API calls.

How to create an access key?
> Go to the AWS Console, click your account name in the top right, select Security credentials, scroll to Access keys, and click Create access key.)

Why should you never hardcode Access Keys in code or commit them to Git?
> Exposes your keys to the public, this compromises your account as other people with this key can access your aws. Even in private repos, keys can leak through history, forks, or accidental public switches. Use roles or environment variables instead.

How often should you rotate Access Keys?
> AWS recommends rotating regularly (every 90 days is common guidance). Avoid long term keys entirely and use roles instead.

What is the IAM Credential Report? What does it show?
> account-level report that lists all IAM users and the status of their credentials (passwords, access keys, MFA). It shows when they were last used, last rotated, and whether MFA is enabled.

What is IAM Access Analyser?
> a security service that analyses resource-based policies to help you identify, monitor, and manage unintended public or cross-account access to your AWS resources

---

## Part 7: Cross-Account Access

How do you grant access to resources in another AWS account?
> Create a role in the target account with a trust policy and permissions policy

What does `sts:AssumeRole` do?
> Returns a set of temporary security credentials for a specific role.

Walk through the flow: User in Account A needs to access S3 in Account B.
> Account B creates a role with a trust policy allowing Account A and a permissions policy granting S3 access. Account A's user then calls `sts:AssumeRole` to assume that role and receives temporary credentials.

---

## Part 8: Identity Federation

What is identity federation?
> A security framework that enables users to securely access multiple applications, systems, or organisations using a single set of credentials (username/password). These external credentials get mapped to IAM roles, so users get temporary AWS access without needing an IAM user

Why would a company use federation instead of creating IAM Users for every employee?
> To centralise identity management, strengthen security and reduce operational overhead. If organisations already have corporate credentials (e.g. Active Directory, Google Workspace), why create a second set of credentials to manage.

What is AWS IAM Identity Center (formerly SSO)?
> An AWS service that provides a central place to manage SSO access across multiple AWS accounts and business applications, with built-in integration with identity providers like Active Directory.
---

## Commands to Learn

```bash
# List IAM users
aws iam list-users
```
> 

```bash
# Create an IAM user with name devops-user
aws iam create-user --user-name devops-user
```
> 

```bash
# returns information about the IAM identity making the call (account ID, user ARN, user ID)
aws sts get-caller-identity
```
> 

```bash
# Attach S3 read only policy to user
aws iam attach-user-policy --user-name devops-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```
> 

```bash
# Return the policies attached to specified user
aws iam list-attached-user-policies --user-name devops-user
```
> 

```bash
# List all IAM roles in the account
aws iam list-roles
```
> 

```bash
# assumes the specified role and returns temporary security credentials for that role
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
   > User is an individual entity with long-term credentials. Group is a collection of users that share the same permissions. Role provides temporary security credentials that can be assumed by users, application, or AWS services.

2. What happens when there is an explicit Deny and an explicit Allow on the same action?
   > Deny will take priority

3. How would you give an EC2 instance access to S3 without using access keys?
   > Instance profile

---

## Confidence: 🟢

**Date completed:** 10/03/26
