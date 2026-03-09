# 4. Security Groups & NACLs

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: What is a Security Group

What is a Security Group?
> 

What is a Security Group attached to? (hint: not directly to an instance)
> 

Is a Security Group stateful or stateless?
> 

What does "stateful" mean in this context?
> 

---

## Part 2: Security Group Rules

What is the default inbound rule for a new Security Group?
> 

What is the default outbound rule for a new Security Group?
> 

Can you create a DENY rule in a Security Group?
> 

What happens if you attach multiple Security Groups to one instance?
> 

When do Security Group changes take effect?
> 

---

## Part 3: Configuring Rules

What three things do you specify in a Security Group rule?
> 

What does `0.0.0.0/0` mean as a source?
> 

Why is opening port 22 to 0.0.0.0/0 dangerous?
> 

What should you set as the source for SSH access instead?
> 

---

## Part 4: Security Group Chaining

What does it mean to reference another Security Group as a source?
> 

Give an example of a 3-tier security group chain (web, app, database):
> 

Why is referencing a Security Group better than hardcoding IP addresses?
> 

How does chaining help with Auto Scaling?
> 

---

## Part 5: Network ACLs

What is a Network ACL (NACL)?
> 

What level does a NACL operate at?
> 

Is a NACL stateful or stateless?
> 

What does "stateless" mean practically?
> 

Can you create DENY rules in a NACL?
> 

---

## Part 6: NACL Rule Evaluation

How does rule evaluation order work in NACLs?
> 

What does the default NACL allow?
> 

What does a custom (newly created) NACL allow by default?
> 

What are ephemeral ports?
> 

Why do ephemeral ports matter for NACLs but not for Security Groups?
> 

---

## Part 7: Security Groups vs NACLs

Fill in this comparison:

| Feature | Security Group | NACL |
|---------|---------------|------|
| Operates at | | |
| Stateful or Stateless | | |
| Rule types (Allow/Deny) | | |
| How rules are evaluated | | |
| Default behaviour | | |

When would you use a NACL in addition to Security Groups?
> 

---

## Part 8: Troubleshooting

You cannot SSH to your EC2 instance. What do you check, in order?
> 

You cannot reach your web app on port 443. Walk through your troubleshooting steps:
> 

What are VPC Flow Logs?
> 

What information do VPC Flow Logs capture?
> 

What is the VPC Reachability Analyzer?
> 

---

## Commands to Learn

```bash
# What does this do?
aws ec2 create-security-group --group-name web-sg \
  --description "Web server SG" --vpc-id vpc-xxxxx
```
> 

```bash
# What does this do?
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 22 --cidr 203.0.113.0/32
```
> 

```bash
# What does this do?
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```
> 

```bash
# What does this do?
aws ec2 authorize-security-group-ingress --group-id sg-db \
  --protocol tcp --port 3306 --source-group sg-app
```
> 

```bash
# What does this do?
aws ec2 describe-security-groups --group-ids sg-xxxxx
```
> 

```bash
# What does this do?
aws ec2 revoke-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```
> 

```bash
# What does this do?
aws ec2 describe-network-acls --filters "Name=vpc-id,Values=vpc-xxxxx"
```
> 

---

## Hands-On Tasks

- Launch an EC2 instance with SSH allowed only from your IP, verify it works
- Add HTTP (port 80), install nginx, verify web access
- Create a second instance that only accepts traffic from the first instance's Security Group
- Create a custom NACL that blocks a specific IP and attach it to a subnet
- Deliberately misconfigure a rule and troubleshoot the connectivity issue
- Enable VPC Flow Logs and review the traffic

---

## Quick Quiz

1. What is the key difference between a Security Group and a NACL?
   > 

2. An EC2 instance cannot be reached on port 443. Walk through your troubleshooting steps.
   > 

3. Why do NACLs require you to think about ephemeral ports but Security Groups do not?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________