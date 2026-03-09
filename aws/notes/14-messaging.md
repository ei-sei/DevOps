# 14. Messaging and Integration

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Why Decoupling Matters

What does "tightly coupled" mean in architecture?
>

What does "loosely coupled" mean?
>

What problem does decoupling solve?
>

What AWS services help decouple applications?
>

---

## Part 2: SQS Basics

What is Amazon SQS (Simple Queue Service)?
>

What is a message queue?
>

What is a producer? What is a consumer?
>

What is the maximum message size in SQS?
>

How long can a message stay in the queue? What is the default?
>

What happens to a message after a consumer processes it?
>

---

## Part 3: SQS Standard vs FIFO

What is a Standard queue?
>

What is a FIFO queue?
>

What is the difference between them?
>

What does "at-least-once delivery" mean?
>

What does "exactly-once processing" mean?
>

When would you choose FIFO over Standard?
>

What is the throughput limit of a FIFO queue?
>

---

## Part 4: SQS Features

What is the visibility timeout? What problem does it solve?
>

What happens if the visibility timeout is too short?
>

What is long polling? How is it different from short polling?
>

Why is long polling preferred?
>

What is a dead letter queue (DLQ)? When are messages sent there?
>

What is the redrive policy?
>

---

## Part 5: SQS with Auto Scaling

How can SQS be used with an Auto Scaling Group?
>

What CloudWatch metric would you use to scale based on queue depth?
>

Walk through the architecture: messages arrive in SQS, EC2 instances process them, ASG scales based on demand.
>

---

## Part 6: SNS Basics

What is Amazon SNS (Simple Notification Service)?
>

What is the pub/sub pattern?
>

What is an SNS topic?
>

What is a subscription?
>

What protocols can SNS deliver to? (email, SMS, HTTP, SQS, Lambda, etc.)
>

How is SNS different from SQS?
>

---

## Part 7: SNS and SQS Fan-Out

What is the fan-out pattern?
>

How do you combine SNS with SQS for fan-out?
>

Give a real-world example of the fan-out pattern.
>

Why is fan-out better than sending messages to multiple queues individually?
>

---

## Part 8: Amazon Kinesis

What is Amazon Kinesis?
>

What is Kinesis Data Streams?
>

What is a shard?
>

How is Kinesis different from SQS?
>

When would you use Kinesis over SQS?
>

What is Amazon Data Firehose (formerly Kinesis Data Firehose)?
>

What destinations can Firehose deliver to?
>

---

## Part 9: Amazon MQ

What is Amazon MQ?
>

When would you use Amazon MQ instead of SQS or SNS?
>

What protocols does Amazon MQ support?
>

---

## Part 10: Choosing the Right Service

Fill in this comparison:

| Feature | SQS | SNS | Kinesis |
|---------|-----|-----|---------|
| Pattern | | | |
| Message retention | | | |
| Consumers | | | |
| Use case | | | |

---

## Commands to Learn

```bash
# What does this do?
aws sqs create-queue --queue-name my-queue
```
>

```bash
# What does this do?
aws sqs send-message --queue-url https://sqs... \
  --message-body "Hello from CLI"
```
>

```bash
# What does this do?
aws sqs receive-message --queue-url https://sqs... \
  --wait-time-seconds 20
```
>

```bash
# What does this do?
aws sns create-topic --name my-topic
```
>

```bash
# What does this do?
aws sns subscribe --topic-arn arn:aws:sns:... \
  --protocol email --notification-endpoint me@example.com
```
>

```bash
# What does this do?
aws sns publish --topic-arn arn:aws:sns:... \
  --message "Alert: CPU high"
```
>

---

## Hands-On Tasks

- Create an SQS Standard queue, send and receive messages via the CLI
- Create a FIFO queue and verify message ordering
- Set up a dead letter queue and trigger it by not processing messages
- Create an SNS topic, subscribe your email, and publish a message
- Set up fan-out: SNS topic with two SQS queues subscribed
- Create a Lambda function triggered by an SQS queue

---

## Quick Quiz

1. What is the difference between SQS and SNS? When would you use each?
   >

2. What is the fan-out pattern and how do you implement it on AWS?
   >

3. When would you choose Kinesis over SQS?
   >

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________
