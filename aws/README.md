# AWS Learning Journey

Hands-on notes and projects documenting my AWS learning path towards the Solutions Architect Associate (SAA-C03) certification.

## Structure

```
notes/
├── 01-intro.md
├── 02-iam.md
├── 03-networking.md
├── 04-ec2.md
├── 05-security-groups.md
├── 06-load-balancing.md
├── 07-storage.md
├── 08-route53.md
├── 09-containers.md
├── 10-serverless.md
├── 11-cloudfront.md
├── 12-databases.md
├── 13-monitoring.md
├── 14-messaging.md
├── 15-security.md
├── 16-disaster-recovery.md
└── 17-well-architected.md

lab/
├── 01-vpc-networking/
├── 02-application-load-balancer/
├── 03-s3-cloudfront-route53/
└── 04-serverless-api-with-lambda-iam-api-gateway/
```

## Labs

| Lab | Description | Architecture |
|-----|-------------|--------------|
| [01 - VPC Networking](lab/01-vpc-networking/) | Custom VPC with public/private subnets, route tables, internet gateway, and NAT gateway | VPC, Subnets, IGW, NAT Gateway, Route Tables |
| [02 - Application Load Balancer](lab/02-application-load-balancer/) | ALB with target groups, health checks, and EC2 instances across multiple AZs | ALB, EC2, Target Groups, Security Groups |
| [03 - S3 + CloudFront + Custom Domain](lab/03-s3-cloudfront-route53/) | Static website hosted on S3, served via CloudFront CDN with HTTPS and a custom domain via Cloudflare DNS | S3, CloudFront, ACM, Lambda@Edge, CloudFront Functions, GitHub Actions |
| [04 - Serverless API](lab/04-serverless-api-with-lambda-iam-api-gateway/) | REST API using API Gateway, Lambda, and DynamoDB with IAM least-privilege permissions, API keys, and WAF | API Gateway, Lambda, DynamoDB, IAM, WAF |

## Topics

- 01 - Intro to AWS
- 02 - IAM
- 03 - VPC & Networking
- 04 - EC2 & Compute
- 05 - Security Groups & NACLs
- 06 - Load Balancing & Scalability
- 07 - Storage (S3, EBS, EFS, FSx, Snow Family)
- 08 - DNS (Route 53)
- 09 - Containers (ECS, EKS, ECR)
- 10 - Serverless (Lambda, API Gateway, DynamoDB)
- 11 - CDN (CloudFront)
- 12 - Databases (RDS, Aurora, ElastiCache)
- 13 - Monitoring (CloudWatch, CloudTrail, Config)
- 14 - Messaging (SQS, SNS, Kinesis)
- 15 - Security & Encryption (KMS, WAF, Shield, GuardDuty)
- 16 - Disaster Recovery & Migration
- 17 - Well-Architected Framework, CloudFormation, Beanstalk
- 


## Environment

- **Console:** AWS Management Console
- **CLI:** AWS CLI v2
- **Region:** eu-west-2 (London)
