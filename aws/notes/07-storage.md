# 5. AWS Storage Services

---

## Part 1: Storage Types Overview

What is block storage?
> Storage divided into fixed-size blocks (like a hard drive). Data is accessed by block address, not filename. Fast and efficient for databases and applications.

What is object storage?
> Storage for unstructured data (files, images, videos), organised as objects with metadata. Access via HTTP/REST API, not as a file system.

What is file storage?
> Storage organised as a traditional file system with folders and files. Multiple users or application can access the files simultaneously over a network.

Which AWS service provides each type?
> - Block storage: EBS (Elastic Block Store)
> - Object storage: S3 (Simple Storage Service)
> - File storage: EFS (Elastic File System) or FSx (managed file servers)

---

## Part 2: EBS Basics

What is EBS (Elastic Block Store)?
> Managed block storage service that provides persistent, network-attached storage volumes for EC2 instances

What is an EBS volume?
> A virtual hard drive that you create and attach to an EC2 instance. It persists independently from the instance and can be detached and reattached.

Is an EBS volume tied to a specific AZ?
> Yes, an EBS volume exists in a single AZ and can only be attached to instances in that same AZ

Can you attach an EBS volume to instances in different AZs?
> No, you must create a snapshot, copy it to another AZ, and create a new volume from that snapshot to use it in a different AZ

What is a root volume?
> The primary EBS volume attached to an EC2 instance that contains the operating system and is used to boot the instance.

What happens to the root volume when you terminate an instance? (default behaviour)
> The root volume is deleted by default (unless "Delete on Termination" is disabled).

What is the "Delete on Termination" setting?
> This option determines if the root volume will be deleted if the instance is terminated.

---

## Part 3: EBS Volume Types

What is gp2? What is it used for?
> gp2 (General Purpose 2) is AWS's default EBS volume type. It balances prices and performance for most workloads.
> - **Performance**: Up to 16000 IOPS (Input/Output Operations Per Second), up to 250 MB/s throughput
> - **Used for**: Web servers, small databases, dev/test environments, general purpose applications.
> - **Burst capability**: Can burst above baseline IOPS for short periods (burst bucket model)
> - **Cost**: Mid-range pricing

What is gp3? How does it differ from gp2?
> gp3 is the newer, improved General Purpose volume type
> - **Performance:** up to 16000 IOPS, up to 1000 MB/s throughput (4x better throughput than gp2)
> - **Key difference:** IOPS and throughput are decoupled - you provision them independently, no burst model
> - **Baseline:** 3000 IOPS, and 125 MB/s are included by default; pay for only what you add above that.
> - **Cost:** 20% cheaper than gp2 for equivalent performance
> - **Better for:** most modern workloads (gp3 is now the recommended default)

Why should you use gp3 over gp2 for most workloads?
> 1. Better value: 20% cheaper than gp2
> 2. Predictable performance: No burst model - you control exactly what you provision
> 3. Higher throughput: 1000 MB/s vs. 20 MB/s (4x more)
> 4. Independent scaling: Increase IOPS without increasing volume size (gp2 ties IOPS to size)
> 5. Future proofed: AWS recommends gp3 for new deployments
> Bottom line: gp3 is faster, cheaper, and more flexible than gp2

What is io1/io2? When would you use it?
> io1/io2 (Provisioned IOPS SSD) are high-performance volumes for mission-critical, I/O-intensive workloads
> - Performance: Up to 64,000 IOPS (io2 can go higher with Block Express), very high throughput
> - Key feature: IOPS are provisioned and guaranteed - you pay for what you reserve
> - When to use: 
>     - Large relational/NoSQL databases (MySQL, PostgreSQL, MongoDB), Data warehouses
>     - Real-time analytics
>     - High-frequency trading systems
>     - Any workload requiring consistent, guaranteed IOPS
> - io2 vs io1: io2 is newer, more durable (99.999% vs 99.9%), same or better price
> - Cost: Most expensive option (you pay per IOPS provisioned)

What is st1? What is it optimised for?
> st1 (Throughput Optimised HDD) is optimized for sequential, high-throughput workloads.
> - Performance: Up to 500 IOPS, up to 500 MB/s throughput
> - Optimized for: Streaming workloads that need sustained throughput, not random access
> - Used for:
>     - Big data and data warehouses (Hadoop, Spark)
>     - Log processing
>     - Video streaming
>     - Machine learning training
> - Cost: Cheaper than SSD options (gp3, io1, io2)
> - Key trait: HDD-based, designed for sequential reads/writes, not random access

What is sc1? When would you use it?
> sc1 (Cold HDD) is the cheapest EBS option, optimized for infrequent access.
> - Performance: Up to 250 IOPS, up to 250 MB/s throughput
> - When to use:
>     - Infrequently accessed data
>     - Archive storage
>     - Disaster recovery (cold standby data)
>     - Development/test environments with minimal performance needs
> - Cost: Lowest of all EBS types
> - Tradeoff: Much lower performance, but extremely cost-effective for cold data

What is the difference between IOPS and throughput?
> - IOPS (Input/Output Operations Per Second): Measures the number of operations per second. Relevant for random access patterns (e.g., database queries hitting random blocks).
>     - Think: How many individual read/write requests can happen per second?
> - Throughput (MB/s): Measures the amount of data transferred per second. Relevant for sequential access patterns (e.g., streaming, bulk data transfers).
>     - Think: How much data can move in one second
> Example:
> - gp2: 16,000 IOPS = 16,000 random reads/writes per second; 250 MB/s = 250 MB flowing per second
> - gp3: Can have 16,000 IOPS and 1,000 MB/s—both independently provisioned
> In practice: A database needs IOPS; a video stream needs throughput. Some workloads need both.

---

## Part 4: EBS Snapshots

What is an EBS snapshot?
> An EBS snapshot is a point in time of an EBS volume. It captures all the data on the volume at the moment you take the snapshot. Snapshots are incremental, meaning only the changed blocks since the last snapshot are stored. You can create snapshots while a volume is running - no downtime needed.

Where are snapshots stored?
> Snapshots are stored in Amazon S3, though AWS manages this automatically for you. You don't interact with S3 directly. The snapshots exist in the region where the original volume is located and are replicated across availability zones in that region for durability

Are snapshots full or incremental? What does that mean for cost?
> Snapshots are incremental. The first snapshot is a full copy of the volume, but every snapshot after that only stores the blocks that have changed since the last one. This means you only pay for the changed data, not the entire volume each time. For example if you have a 100GB volume but only 5GB changed since the last snapshot, you only pay for about 5GB of storage

How do you use a snapshot to create a volume in a different AZ?
> You take a snapshot of the original volume, then create a new volume from that snapshot and specify a different availability zone. Once the volume is created, you can attach it to an instance in that AZ. Since snapshots are regional, you can restore to any AZ within the same Region without any extra steps.

How do you copy a snapshot to a different Region? Why would you do this?
> To copy a snapshot to another region, you go to the snapshot, select "Copy Snapshot," and choose the target region. AWS will copy it across the network. You'd do this for disaster recovery (keeping backups in a different geographical area), multi-region deployments, compliance requirements, or to enable failover if your primary Region goes down.

What is the relationship between snapshots and AMIs?
> An AMI is a template for launching instances that include one or more snapshots of EBS volumes plus metadata like the operating system. Snapshots are the storage part of an AMI, while an AMI is the complete package. When you create an AMI from a running instance, it captures snapshots of all attached volumes. You can then launch multiple instances from that AMI, and each instance gets new volumes created from those snapshots.

What are snapshot lifecycle policies?
> Snapshot lifecycle policies automate the creation and deletion of snapshots. You can set them to automatically create snapshots on a schedule (daily, weekly, monthly) and automatically delete old snapshots after a certain period. This removes the need for manual snapshot management, helps control costs by deleting unused backups, and ensure you always have regular backups for compliance reasons. You set the policy once and AWS handles everything else.

---

## Part 5: EBS Encryption

How does EBS encryption work?
> EBS encryption encrypts all data on a volume at rest using AES-256 encryption. When you create an encrypted volume, AWS encrypts the data before writing it to disk. When you read data from the volume, AWS automatically decrypts it. Encryption also applies to snapshots created from encrypted volumes and to any volumes created from those snapshots. The encryption happens transparently - you don't need to do anything special in your application.

What service manages the encryption keys?
> AWS Key Management Service (KMS) manages the encryption keys. By default, AWS uses a service-managed key (aws/ebs) that AWS maintains for you. You can also use a customer-managed key if you want more control over key rotation and permissions. Either way, KMS handles all the encryption and decryption operations behind the scenes.

How do you encrypt an existing unencrypted volume?
> You cannot directly encrypt an existing unencrypted volume. Instead, you create a snapshot of the unencrypted volume, then copy that snapshot and specify that you want the copy to be encrypted. Once the encrypted snapshot is ready, you create a new encrypted volume from it and attach it to your instance. You can then migrate your data to the new volume and delete the old one. This is a manual process but ensures your data is encrypted.

Are snapshots of encrypted volumes also encrypted?
> Yes, snapshots of encrypted volumes are automatically encrypted using the same KMS key. If you copy an encrypted snapshot to another Region, it remains encrypted in the target Region (using the KMS key in that Region). You cannot create an unencrypted snapshot from an encrypted volume - the encryption is maintained throughout the snapshot lifecycle.

Does encryption have a noticeable performance impact?
> No, encryption has minimal to no noticeable performance impact. Modern CPUs have hardware acceleration for AES encryption, so the encryption and decryption happen very quickly. AWS design ensures that encryption doesn't degrade IOPS or throughput. You should not hesitate to enable encryption due to performance concerns - the security benefit far outweighs any negligible performance cost.

---

## Part 6: S3 Basics

What is S3 (Simple Storage Service)?
> S3 is AWS's object storage service. It stores data as objects (files) inside buckets (containers) rather than in a traditional file system or block storage. S3 is highly scalable, durable, and available. You can store virtually unlimited amounts of data and access it from anywhere. It's designed for web-scale applications, backups, archives, data lakes, and static website hosting.

What is the difference between object storage and block storage?
> Block storage (like EBS) divides data into fixed-size blocks and stores them on a device. You mount block storage like a hard drive and interact with it using a file system. Object storage (like S3) stores entire files as objects with metadata and a unique key. You access objects via HTTP/HTTPS using an API. There's no file system. Block storage is fast and good for databases and applications. Object storage is scalable and good for backups, archives, and distributed access.

What is a bucket?
> A bucket is a container in S3 that holds objects (files). Think of it like a folder, but it's actually a top-level namespace. A bucket can contain any number of objects and you organize them using key prefixes (which look like folder paths, but aren't true folders). All objects in a bucket are stored in the same Region, though you can replicate buckets across Regions.

Why must bucket names be globally unique?
> Bucket names must be globally unique across all AWS accounts and all Regions because S3 bucket names form part of the URL used to access objects. For example, mybucket.s3.amazonaws.com must be unique worldwide so there's no ambiguity about which bucket you're accessing. If two accounts could have the same bucket name, the URL would be ambiguous.

What is an object? What does it consist of?
> An object is a file stored in S3. Each object consists of the actual data (the file content) plus metadata. The metadata includes the object key (the name or path), version ID, content type, size, creation date, and any custom metadata you add. You refer to objects by their key, which is the full path including bucket name. For example: mybucket/folder/myfile.txt.

What is the maximum size of a single object?
> The maximum size of a single object in S3 is 5 terabytes (5 TB). For objects larger than 5 GB, AWS recommends using multipart upload, which breaks the file into smaller parts, uploads them in parallel, and reassembles them. This makes large uploads faster and more reliable.

What does "11 nines of durability" mean practically?
> "11 nines of durability" (99.999999999%) means that if you store 10 million objects in S3, you would expect to lose one object every 10,000 years due to hardware failure. Practically, it means your data is extremely unlikely to be lost due to AWS infrastructure failures. S3 automatically replicates your data across multiple availability zones and data centers, so even catastrophic hardware failures won't cause data loss.

What is the difference between durability and availability?
> Durability is about whether your data survives and doesn't get lost. Availability is about whether you can access your data when you need it. S3 offers 11 nines durability (data won't be lost) and 99.99% availability (service will be up and accessible). High durability means AWS protects against hardware failure and data corruption. High availability means the service is running and responsive most of the time. You can have one without the other. A system could be durable but temporarily unavailable during maintenance.

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