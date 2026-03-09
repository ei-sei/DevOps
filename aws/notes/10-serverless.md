# 8. Serverless Services

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: What is Serverless

What does "serverless" mean? Are there still servers?
> 

How is serverless different from running code on EC2?
> 

What do you NOT have to manage with serverless?
> 

---

## Part 2: Lambda Basics

What is AWS Lambda?
> 

What is a Lambda function?
> 

What is a handler?
> 

What runtimes does Lambda support?
> 

How is Lambda priced?
> 

---

## Part 3: Lambda Configuration

How does memory allocation affect CPU in Lambda?
> 

What is the maximum memory you can allocate?
> 

What is the maximum timeout for a Lambda function?
> 

What is an execution role? Why does every Lambda need one?
> 

How do you pass configuration values to a Lambda function?
> 

What is reserved concurrency?
> 

What is a dead letter queue? When is it used?
> 

---

## Part 4: Lambda Triggers and Invocation

What triggers a Lambda function? Name at least five common triggers.
> 

What is synchronous invocation? Give an example.
> 

What is asynchronous invocation? Give an example.
> 

What is an event source mapping? Give an example.
> 

What happens if an asynchronous invocation fails?
> 

---

## Part 5: Cold Starts

What is a cold start?
> 

What causes a cold start to happen?
> 

How long can a cold start take?
> 

Which runtimes have the fastest cold starts?
> 

What is provisioned concurrency? How does it help?
>

What is Lambda SnapStart? How is it different from provisioned concurrency?
> 

---

## Part 6: Layers, Versions, and Aliases

What is a Lambda Layer? When would you use one?
> 

What is a Lambda version?
> 

What is a Lambda alias?
> 

How do aliases help with deployments?
> 

How would you do a canary deployment with Lambda aliases?
> 

---

## Part 7: API Gateway Basics

What is API Gateway?
> 

What is the difference between REST API and HTTP API?
> 

Which one is simpler and cheaper?
> 

How does API Gateway connect to Lambda?
> 

What are stages (dev, staging, prod)?
> 

---

## Part 8: API Gateway Features

What is throttling in API Gateway?
> 

What are API keys and usage plans?
> 

How do you configure CORS on API Gateway?
> 

What is a custom domain name on API Gateway?
> 

---

## Part 9: DynamoDB Basics

What is DynamoDB?
> 

What type of database is it? (SQL or NoSQL)
> 

What is a table, an item, and an attribute?
> 

What is a partition key?
> 

What is a sort key? When do you need one?
> 

What is the difference between on-demand and provisioned capacity?
> 

---

## Part 10: DynamoDB Features

What is a Global Secondary Index (GSI)?
> 

What are DynamoDB Streams? What can they trigger?
> 

What is TTL (Time to Live) in DynamoDB?
> 

---

## Part 11: Step Functions and EventBridge

What is Step Functions?
> 

When would you use Step Functions instead of chaining Lambda functions directly?
> 

What is the difference between Standard and Express workflows?
> 

What is EventBridge?
> 

How is EventBridge different from SNS?
> 

How would you schedule a Lambda to run every day at 9am?
> 

---

## Part 12: When Serverless Makes Sense

What types of workloads are ideal for serverless?
> 

What types of workloads are NOT good for serverless?
> 

What are the limitations of Lambda?
> 

At what point might containers or EC2 be cheaper than Lambda?
> 

---

## Part 13: Lambda in VPC

Can Lambda functions access VPC resources by default?
>

How do you configure a Lambda function to access resources in a VPC?
>

What happens to Lambda's internet access when you place it in a VPC?
>

How does a Lambda in a VPC access the internet?
>

What is a Lambda ENI?
>

---

## Part 14: Amazon Cognito

What is Amazon Cognito?
>

What is a User Pool?
>

What is an Identity Pool?
>

What is the difference between User Pools and Identity Pools?
>

How does Cognito integrate with API Gateway?
>

When would you use Cognito?
>

---

## Commands to Learn

```bash
# What does this do?
aws lambda list-functions
```
> 

```bash
# What does this do?
aws lambda create-function --function-name my-function \
  --runtime python3.12 --handler lambda_function.handler \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --zip-file fileb://function.zip
```
> 

```bash
# What does this do?
aws lambda invoke --function-name my-function output.json
```
> 

```bash
# What does this do?
aws lambda update-function-code --function-name my-function \
  --zip-file fileb://function.zip
```
> 

```bash
# What does this do?
aws lambda get-function-configuration --function-name my-function
```
> 

```bash
# What does this do?
aws dynamodb create-table --table-name my-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```
> 

```bash
# What does this do?
aws dynamodb put-item --table-name my-table \
  --item '{"id":{"S":"123"},"name":{"S":"test"}}'
```
> 

```bash
# What does this do?
aws dynamodb get-item --table-name my-table --key '{"id":{"S":"123"}}'
```
> 

---

## Hands-On Tasks

- Create a Lambda function (Python or Node.js) that returns "Hello World", test it
- Create an API Gateway HTTP API that triggers your Lambda function
- Create a Lambda triggered by S3 upload that logs the object key
- Create a DynamoDB table and write a Lambda that reads and writes items
- Set up a scheduled Lambda using EventBridge (run every 5 minutes)
- Create a Lambda Layer with a shared library

---

## Quick Quiz

1. What is Lambda and how does it differ from EC2?
   > 

2. What is a cold start and how do you mitigate it?
   > 

3. How would you build a simple serverless REST API on AWS?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________