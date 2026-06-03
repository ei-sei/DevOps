# AWS Learning Journey

Hands-on notes and projects documenting my AWS learning path towards the Solutions Architect Associate (SAA-C03) certification.

## Structure

```
lab/
├── 01-vpc-networking/
├── 02-application-load-balancer/
├── 03-s3-cloudfront-route53/
└── 04-serverless-api-with-lambda-iam-api-gateway/

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


```

## Labs

| Lab                                                                       | Description                                                                                              | Architecture                                                           |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [01 - VPC Networking](lab/01-vpc-networking/)                             | Custom VPC with public/private subnets, route tables, internet gateway, and NAT gateway                  | VPC, Subnets, IGW, NAT Gateway, Route Tables                           |
| [02 - Application Load Balancer](lab/02-application-load-balancer/)       | ALB with target groups, health checks, and EC2 instances across multiple AZs                             | ALB, EC2, Target Groups, Security Groups                               |
| [03 - S3 + CloudFront + Custom Domain](lab/03-s3-cloudfront-route53/)     | Static website hosted on S3, served via CloudFront CDN with HTTPS and a custom domain via Cloudflare DNS | S3, CloudFront, ACM, Lambda@Edge, CloudFront Functions, GitHub Actions |
| [04 - Serverless API](lab/04-serverless-api-with-lambda-iam-api-gateway/) | REST API using API Gateway, Lambda, and DynamoDB with IAM least-privilege permissions, API keys, and WAF | API Gateway, Lambda, DynamoDB, IAM, WAF                                |

## Topics

See [notes/README.md](notes/README.md) for the full topic list.
