# 12. Databases on AWS

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Database Types

What is the difference between a relational database and a non-relational (NoSQL) database?
>

When would you choose a relational database?
>

When would you choose a NoSQL database?
>

What database engines does AWS offer as managed services?
>

---

## Part 2: RDS Basics

What is Amazon RDS?
>

What does "managed" mean in this context? What does AWS handle for you?
>

What database engines does RDS support?
>

Can you SSH into an RDS instance?
>

What is the difference between RDS and running a database on EC2?
>

---

## Part 3: RDS Storage and Scaling

What storage types does RDS support?
>

What is RDS storage auto-scaling?
>

Can you scale an RDS instance vertically (change instance type)?
>

Does scaling an RDS instance cause downtime?
>

---

## Part 4: RDS Read Replicas

What is a Read Replica?
>

What problem do Read Replicas solve?
>

How many Read Replicas can you create?
>

Can a Read Replica be in a different AZ? A different Region?
>

Is replication synchronous or asynchronous?
>

Can you promote a Read Replica to a standalone database? When would you do this?
>

Do Read Replicas incur data transfer costs within the same Region?
>

---

## Part 5: RDS Multi-AZ

What is Multi-AZ deployment?
>

How is Multi-AZ different from a Read Replica?
>

Is Multi-AZ replication synchronous or asynchronous?
>

Can you read from the standby instance in Multi-AZ?
>

What happens during a failover?
>

When would you use Multi-AZ vs Read Replicas vs both?
>

---

## Part 6: RDS Security

How do you control network access to RDS?
>

What is RDS encryption at rest? What service manages the keys?
>

Can you encrypt an existing unencrypted RDS instance?
>

What is IAM database authentication?
>

---

## Part 7: RDS Backups and Snapshots

What are automated backups? How long are they retained?
>

What is a manual snapshot? How is it different from an automated backup?
>

What is the backup window?
>

How do you restore an RDS backup? Does it restore to the same instance?
>

What is point-in-time recovery?
>

---

## Part 8: RDS Proxy

What is RDS Proxy?
>

What problem does it solve?
>

How does RDS Proxy help with Lambda functions?
>

Does RDS Proxy support IAM authentication?
>

---

## Part 9: Amazon Aurora

What is Amazon Aurora?
>

How is Aurora different from standard RDS?
>

What database engines is Aurora compatible with?
>

How does Aurora storage work? (shared distributed storage)
>

How many copies of your data does Aurora maintain?
>

What is an Aurora cluster endpoint vs a reader endpoint?
>

What is Aurora Serverless? When would you use it?
>

What is Aurora Global Database?
>

---

## Part 10: ElastiCache

What is Amazon ElastiCache?
>

What is the difference between Redis and Memcached on ElastiCache?
>

What is caching? What problem does it solve?
>

Where does ElastiCache sit in a typical architecture? (between app and database)
>

What are common caching strategies (lazy loading, write-through)?
>

When would you use ElastiCache?
>

---

## Part 11: RDS Custom

What is RDS Custom?
>

How is it different from standard RDS?
>

What databases does it support?
>

When would you use RDS Custom instead of standard RDS?
>

---

## Part 12: Choosing the Right Database

Fill in this comparison:

| Feature | RDS | Aurora | DynamoDB | ElastiCache |
|---------|-----|--------|----------|-------------|
| Type | | | | |
| Use case | | | | |
| Scaling | | | | |
| Managed by | | | | |

---

## Commands to Learn

```bash
# What does this do?
aws rds describe-db-instances
```
>

```bash
# What does this do?
aws rds create-db-instance --db-instance-identifier my-db \
  --db-instance-class db.t3.micro --engine mysql \
  --master-username admin --master-user-password secret123 \
  --allocated-storage 20
```
>

```bash
# What does this do?
aws rds create-db-snapshot --db-instance-identifier my-db \
  --db-snapshot-identifier my-backup
```
>

```bash
# What does this do?
aws rds create-read-replica --db-instance-identifier my-db \
  --source-db-instance-identifier my-db-primary
```
>

```bash
# What does this do?
aws elasticache describe-cache-clusters
```
>

---

## Hands-On Tasks

- Create an RDS MySQL instance in a private subnet
- Connect to it from an EC2 instance in the same VPC
- Create a Read Replica and verify replication
- Enable Multi-AZ and simulate a failover
- Take a manual snapshot and restore it to a new instance
- Create an ElastiCache Redis cluster

---

## Quick Quiz

1. What is the difference between a Read Replica and Multi-AZ?
   >

2. When would you choose Aurora over standard RDS?
   >

3. How would you reduce database load for a read-heavy application?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
