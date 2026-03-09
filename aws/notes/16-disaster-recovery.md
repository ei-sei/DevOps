# 16. Disaster Recovery and Migration

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Disaster Recovery Concepts

What is disaster recovery (DR)?
>

What is RPO (Recovery Point Objective)?
>

What is RTO (Recovery Time Objective)?
>

What is the relationship between RPO/RTO and cost?
>

---

## Part 2: DR Strategies

What are the four DR strategies from cheapest to fastest recovery?
>

What is Backup and Restore? What are the RPO and RTO?
>

What is Pilot Light?
>

What is Warm Standby?
>

What is Multi-Site / Hot Standby?
>

When would you choose each strategy?
>

---

## Part 3: AWS Backup

What is AWS Backup?
>

What resources can AWS Backup protect?
>

What is a backup plan?
>

What is a backup vault?
>

Can AWS Backup work across Regions?
>

---

## Part 4: Database Migration Service (DMS)

What is AWS DMS?
>

What is a source and target in DMS?
>

Can you migrate between different database engines (e.g. Oracle to Aurora)?
>

What is the AWS Schema Conversion Tool (SCT)? When do you need it?
>

What is continuous replication in DMS?
>

---

## Part 5: Application Migration Service (MGN)

What is AWS Application Migration Service?
>

What is "lift and shift"?
>

How does MGN work at a high level?
>

---

## Part 6: Transferring Large Datasets

What are your options for transferring large amounts of data into AWS?
>

When would you use Snowball over the internet?
>

What is AWS DataSync used for in migration?
>

What is the general rule for choosing internet vs Snow Family vs Direct Connect?
>

---

## Commands to Learn

```bash
# What does this do?
aws backup list-backup-plans
```
>

```bash
# What does this do?
aws backup start-backup-job --backup-vault-name my-vault \
  --resource-arn arn:aws:ec2:... --iam-role-arn arn:aws:iam:...
```
>

```bash
# What does this do?
aws dms describe-replication-instances
```
>

---

## Hands-On Tasks

- Create a backup plan in AWS Backup for your RDS instance
- Set up a DMS replication instance and migrate a MySQL database to Aurora
- Use the SCT to analyse a schema conversion

---

## Quick Quiz

1. What are the four DR strategies and how do they compare on cost vs RTO?
   >

2. How would you migrate a large on-premises Oracle database to Aurora?
   >

3. What is the difference between RPO and RTO?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
