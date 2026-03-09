# 15. Security and Encryption

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Encryption Fundamentals

What is encryption at rest?
>

What is encryption in transit?
>

What is the difference between symmetric and asymmetric encryption?
>

What is an encryption key?
>

---

## Part 2: KMS (Key Management Service)

What is AWS KMS?
>

What is a Customer Master Key (CMK)?
>

What is the difference between AWS managed keys and customer managed keys?
>

What services integrate with KMS?
>

What is key rotation? Is it automatic?
>

What is envelope encryption?
>

Can you use KMS keys across Regions?
>

What are KMS multi-Region keys?
>

---

## Part 3: SSM Parameter Store

What is SSM Parameter Store?
>

What types of parameters can you store?
>

What is the difference between Standard and Advanced parameters?
>

What is a SecureString parameter? How is it encrypted?
>

How do you reference Parameter Store values in your application?
>

Can you organise parameters in a hierarchy?
>

---

## Part 4: AWS Secrets Manager

What is AWS Secrets Manager?
>

How is Secrets Manager different from SSM Parameter Store?
>

What is automatic rotation? Which service supports it?
>

When would you use Secrets Manager instead of Parameter Store?
>

---

## Part 5: AWS Certificate Manager (ACM)

What is ACM?
>

What does ACM provide for free?
>

How do you validate a certificate in ACM (DNS vs email)?
>

Which validation method is preferred and why?
>

Can ACM certificates be used with ALB? With CloudFront?
>

Why must CloudFront certificates be in us-east-1?
>

---

## Part 6: CloudHSM

What is AWS CloudHSM?
>

How is CloudHSM different from KMS?
>

When would you need CloudHSM instead of KMS?
>

---

## Part 7: WAF (Web Application Firewall)

What is AWS WAF?
>

What does WAF protect against?
>

What resources can WAF be attached to?
>

What is a Web ACL?
>

What are WAF rules? Give examples of common rules.
>

What is a rate-based rule? What does it help prevent?
>

---

## Part 8: AWS Shield

What is AWS Shield?
>

What is the difference between Shield Standard and Shield Advanced?
>

Is Shield Standard free?
>

What does Shield Advanced add?
>

---

## Part 9: AWS Firewall Manager

What is AWS Firewall Manager?
>

How does it relate to WAF and Shield?
>

When would you use Firewall Manager?
>

---

## Part 10: GuardDuty

What is Amazon GuardDuty?
>

What data sources does GuardDuty analyse?
>

What types of threats does it detect?
>

How is GuardDuty different from WAF?
>

---

## Part 11: Amazon Inspector

What is Amazon Inspector?
>

What does it scan?
>

What is the difference between GuardDuty and Inspector?
>

---

## Part 12: Amazon Macie

What is Amazon Macie?
>

What does it scan for?
>

What service does Macie work with?
>

When would you use Macie?
>

---

## Part 13: Choosing the Right Security Service

Fill in this comparison:

| Service | What it does | Protects against |
|---------|-------------|-----------------|
| WAF | | |
| Shield | | |
| GuardDuty | | |
| Inspector | | |
| Macie | | |

---

## Commands to Learn

```bash
# What does this do?
aws kms list-keys
```
>

```bash
# What does this do?
aws kms create-key --description "My encryption key"
```
>

```bash
# What does this do?
aws ssm put-parameter --name "/app/db-password" \
  --value "secret123" --type SecureString
```
>

```bash
# What does this do?
aws ssm get-parameter --name "/app/db-password" --with-decryption
```
>

```bash
# What does this do?
aws secretsmanager create-secret --name my-db-secret \
  --secret-string '{"username":"admin","password":"secret123"}'
```
>

```bash
# What does this do?
aws secretsmanager get-secret-value --secret-id my-db-secret
```
>

---

## Hands-On Tasks

- Create a KMS key and use it to encrypt an S3 bucket
- Store a database password in SSM Parameter Store as a SecureString
- Store a secret in Secrets Manager and retrieve it from a Lambda function
- Request a public certificate from ACM and attach it to an ALB
- Enable GuardDuty and review any findings
- Create a WAF Web ACL with a rate-based rule

---

## Quick Quiz

1. What is the difference between SSM Parameter Store and Secrets Manager?
   >

2. How would you encrypt data at rest and in transit for a web application?
   >

3. What is the difference between WAF, Shield, and GuardDuty?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
