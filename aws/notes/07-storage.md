# 5. AWS Storage Services

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Storage Types Overview

What is block storage?
> 

What is object storage?
> 

What is file storage?
> 

Which AWS service provides each type?
> 

---

## Part 2: EBS Basics

What is EBS (Elastic Block Store)?
> 

What is an EBS volume?
> 

Is an EBS volume tied to a specific AZ?
> 

Can you attach an EBS volume to instances in different AZs?
> 

What is a root volume?
> 

What happens to the root volume when you terminate an instance? (default behaviour)
> 

What is the "Delete on Termination" setting?
> 

---

## Part 3: EBS Volume Types

What is gp2? What is it used for?
> 

What is gp3? How does it differ from gp2?
> 

Why should you use gp3 over gp2 for most workloads?
> 

What is io1/io2? When would you use it?
> 

What is st1? What is it optimised for?
> 

What is sc1? When would you use it?
> 

What is the difference between IOPS and throughput?
> 

---

## Part 4: EBS Snapshots

What is an EBS snapshot?
> 

Where are snapshots stored?
> 

Are snapshots full or incremental? What does that mean for cost?
> 

How do you use a snapshot to create a volume in a different AZ?
> 

How do you copy a snapshot to a different Region? Why would you do this?
> 

What is the relationship between snapshots and AMIs?
> 

What are snapshot lifecycle policies?
> 

---

## Part 5: EBS Encryption

How does EBS encryption work?
> 

What service manages the encryption keys?
> 

How do you encrypt an existing unencrypted volume?
> 

Are snapshots of encrypted volumes also encrypted?
> 

Does encryption have a noticeable performance impact?
> 

---

## Part 6: S3 Basics

What is S3 (Simple Storage Service)?
> 

What is the difference between object storage and block storage?
> 

What is a bucket?
> 

Why must bucket names be globally unique?
> 

What is an object? What does it consist of?
> 

What is the maximum size of a single object?
> 

What does "11 nines of durability" mean practically?
> 

What is the difference between durability and availability?
> 

---

## Part 7: S3 Storage Classes

What is S3 Standard?
> 

What is S3 Standard-IA? What is the trade-off?
> 

What is S3 One Zone-IA? What is the risk?
> 

What is S3 Glacier Instant Retrieval?
> 

What is S3 Glacier Flexible Retrieval? How long does retrieval take?
> 

What is S3 Glacier Deep Archive? How long does retrieval take?
> 

What is S3 Intelligent-Tiering? How does it work?
> 

When would you use each storage class?
> 

---

## Part 8: S3 Security

What is a bucket policy? What format is it written in?
> 

What is the difference between a bucket policy and an IAM policy for controlling S3 access?
> 

What are ACLs? Should you use them?
> 

What is "Block Public Access"?
> 

What is server-side encryption? What are the options (SSE-S3, SSE-KMS, SSE-C)?
> 

---

## Part 9: S3 Features

What is versioning? Why should you enable it?
> 

What is a lifecycle policy? What can it do?
> 

Give an example lifecycle rule:
> 

What is a pre-signed URL? When would you use one?
> 

How do you host a static website on S3?
> 

What are S3 Event Notifications? What can they trigger?
> 

What is cross-region replication (CRR)? When would you use it?
> 

---

## Part 10: EFS

What is EFS (Elastic File System)?
> 

What protocol does EFS use?
> 

Can EFS be shared across multiple instances?
> 

Can EFS be shared across multiple AZs?
> 

How is EFS different from EBS?
> 

When would you use EFS?
> 

What are EFS storage classes (Standard, IA)?
> 

---

## Part 11: Choosing the Right Storage

Fill in this comparison:

| Feature | EBS | S3 | EFS |
|---------|-----|-----|-----|
| Storage type | | | |
| Attached to | | | |
| Shared across instances? | | | |
| AZ-specific? | | | |
| Best for | | | |

When would you use EBS?
> 

When would you use S3?
> 

When would you use EFS?
> 

When would you use instance store?
> 

---

## Part 12: S3 Advanced Features

What is S3 CORS? When do you need it?
>

What is S3 Transfer Acceleration? How does it work?
>

What is multipart upload? When should you use it?
>

What is S3 MFA Delete? Why would you enable it?
>

What are S3 Access Logs? Where are they stored?
>

What is S3 Object Lock? What are the two retention modes (governance and compliance)?
>

What is Glacier Vault Lock? How is it different from S3 Object Lock?
>

What is an S3 Access Point? What problem does it solve?
>

What is S3 Object Lambda?
>

---

## Part 13: EBS Advanced

What is EBS Multi-Attach?
>

Which EBS volume type supports Multi-Attach?
>

What are the limitations of Multi-Attach?
>

---

## Part 14: Amazon FSx

What is Amazon FSx?
>

What is FSx for Windows File Server? When would you use it?
>

What is FSx for Lustre? When would you use it?
>

What is the difference between EFS and FSx for Windows?
>

---

## Part 15: AWS Storage Gateway

What is AWS Storage Gateway?
>

What problem does it solve?
>

What are the three types of Storage Gateway (File, Volume, Tape)?
>

When would you use Storage Gateway?
>

---

## Part 16: Snow Family

What is the AWS Snow Family?
>

What is Snowcone?
>

What is Snowball Edge?
>

What is Snowmobile?
>

When would you use Snow Family instead of transferring data over the internet?
>

How does data get from a Snow device into S3?
>

---

## Part 17: DataSync and Transfer Family

What is AWS DataSync?
>

What is DataSync used for?
>

What is AWS Transfer Family?
>

What protocols does Transfer Family support?
>

When would you use Transfer Family?
>

---

## Commands to Learn

```bash
# What does this do?
aws s3 ls
```
> 

```bash
# What does this do?
aws s3 mb s3://my-unique-bucket-name
```
> 

```bash
# What does this do?
aws s3 cp myfile.txt s3://my-bucket/
```
> 

```bash
# What does this do?
aws s3 sync ./local-dir s3://my-bucket/remote-dir
```
> 

```bash
# What does this do?
aws s3 presign s3://my-bucket/myfile.txt --expires-in 3600
```
> 

```bash
# What does this do?
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled
```
> 

```bash
# What does this do?
aws ec2 create-volume --volume-type gp3 --size 20 --availability-zone eu-west-2a
```
> 

```bash
# What does this do?
aws ec2 create-snapshot --volume-id vol-xxxxx --description "My backup"
```
> 

```bash
# What does this do?
aws ec2 describe-volumes --query "Volumes[].[VolumeId,State,Size,VolumeType]" --output table
```
> 

---

## Hands-On Tasks

- Create an S3 bucket, upload files, and enable versioning
- Configure a lifecycle policy to transition objects to Glacier after 30 days
- Host a simple static website on S3
- Generate a pre-signed URL for a private object
- Write a bucket policy allowing read access from a specific IAM role
- Create an EBS volume, attach it to an instance, format and mount it
- Create a snapshot and restore it to a new volume

---

## Quick Quiz

1. When would you use EBS vs S3 vs EFS?
   > 

2. How do EBS snapshots save costs compared to full backups?
   > 

3. How would you secure an S3 bucket? Walk through your approach.
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________