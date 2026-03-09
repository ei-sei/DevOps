# 13. Monitoring, Logging, and Auditing

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Why Monitoring Matters

Why do you need monitoring in AWS?
>

What is the difference between monitoring, logging, and auditing?
>

What happens if you have no monitoring and something goes wrong?
>

---

## Part 2: CloudWatch Metrics

What is Amazon CloudWatch?
>

What is a CloudWatch metric?
>

What are some default EC2 metrics that CloudWatch collects automatically?
>

Does CloudWatch collect memory or disk usage by default?
>

What is a custom metric? How do you send one?
>

What is the difference between standard resolution (1 minute) and high resolution (1 second) metrics?
>

What is a CloudWatch namespace?
>

---

## Part 3: CloudWatch Alarms

What is a CloudWatch alarm?
>

What are the three alarm states?
>

What actions can an alarm trigger?
>

How do you create an alarm for CPU utilisation above 80%?
>

What is the difference between a static threshold and an anomaly detection alarm?
>

How do CloudWatch alarms integrate with Auto Scaling?
>

---

## Part 4: CloudWatch Logs

What is CloudWatch Logs?
>

What is a log group?
>

What is a log stream?
>

How do you send logs from an EC2 instance to CloudWatch?
>

What is the CloudWatch Agent?
>

What is the difference between the CloudWatch Agent and the older CloudWatch Logs Agent?
>

Can you set a retention period on log groups?
>

What are metric filters? Give an example.
>

---

## Part 5: CloudWatch Dashboards

What is a CloudWatch dashboard?
>

Can a dashboard show metrics from multiple Regions?
>

Are dashboards free?
>

---

## Part 6: EventBridge (formerly CloudWatch Events)

What is Amazon EventBridge?
>

What is an event bus?
>

What is a rule in EventBridge?
>

What is the difference between event patterns and scheduled rules?
>

How would you schedule a Lambda function to run every day at 9am?
>

How is EventBridge different from SNS?
>

---

## Part 7: CloudTrail

What is AWS CloudTrail?
>

What does CloudTrail record?
>

What is the difference between management events and data events?
>

Is CloudTrail enabled by default?
>

Where can CloudTrail deliver logs?
>

What is a trail?
>

How long does CloudTrail keep events by default (without a trail)?
>

How would you use CloudTrail to investigate who deleted an S3 bucket?
>

---

## Part 8: CloudTrail vs CloudWatch

What is the difference between CloudTrail and CloudWatch?
>

CloudWatch monitors ___. CloudTrail records ___.
>

Give an example of when you would use CloudWatch.
>

Give an example of when you would use CloudTrail.
>

---

## Part 9: AWS Config

What is AWS Config?
>

What does AWS Config track?
>

What is a Config rule? Give an example.
>

What is the difference between AWS managed rules and custom rules?
>

What is a conformance pack?
>

How does AWS Config differ from CloudTrail?
>

Can AWS Config automatically remediate non-compliant resources?
>

---

## Part 10: CloudWatch vs CloudTrail vs Config

Fill in this comparison:

| Feature | CloudWatch | CloudTrail | Config |
|---------|------------|------------|--------|
| Purpose | | | |
| Tracks | | | |
| Use case | | | |

---

## Commands to Learn

```bash
# What does this do?
aws cloudwatch list-metrics --namespace AWS/EC2
```
>

```bash
# What does this do?
aws cloudwatch put-metric-alarm --alarm-name high-cpu \
  --metric-name CPUUtilization --namespace AWS/EC2 \
  --statistic Average --period 300 --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 --alarm-actions arn:aws:sns:...
```
>

```bash
# What does this do?
aws logs describe-log-groups
```
>

```bash
# What does this do?
aws logs filter-log-events --log-group-name my-app \
  --filter-pattern "ERROR"
```
>

```bash
# What does this do?
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=DeleteBucket
```
>

```bash
# What does this do?
aws configservice describe-compliance-by-config-rule
```
>

---

## Hands-On Tasks

- Create a CloudWatch alarm for EC2 CPU above 70%, trigger an SNS notification
- Install the CloudWatch Agent on an EC2 instance to send memory metrics
- Send application logs from EC2 to CloudWatch Logs
- Create a CloudWatch dashboard with EC2 and RDS metrics
- Use CloudTrail to find who launched an EC2 instance
- Set up an AWS Config rule to check if all S3 buckets have versioning enabled

---

## Quick Quiz

1. What is the difference between CloudWatch, CloudTrail, and AWS Config?
   >

2. How would you set up monitoring for a production web application?
   >

3. Someone deleted an important S3 bucket. How do you find out who did it?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
