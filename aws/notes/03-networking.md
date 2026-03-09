# 9. VPC & Networking

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: What is a VPC

What is a VPC (Virtual Private Cloud)?
> 

Why do you need a VPC?
> 

What is the default VPC? Does every Region have one?
> 

What is the difference between the default VPC and a custom VPC?
> 

---

## Part 2: CIDR Blocks

What is a CIDR block?
> 

What does 10.0.0.0/16 mean?
> 

How many IP addresses does /16 give you?
> 

How many IP addresses does /24 give you?
> 

Can you change a VPC's CIDR block after creating it?
> 

What CIDR ranges are commonly used for private networks?
> 

---

## Part 3: Subnets

What is a subnet?
> 

Can a subnet span multiple Availability Zones?
> 

How many IP addresses does AWS reserve per subnet? Which ones?
> 

How many usable IPs are in a /24 subnet?
> 

Why should you create subnets in at least 2 AZs?
> 

---

## Part 4: Public vs Private Subnets

What makes a subnet "public"?
> 

What makes a subnet "private"?
> 

Why would you put resources in a private subnet?
> 

What types of resources typically go in public subnets?
> 

What types of resources typically go in private subnets?
> 

---

## Part 5: Internet Gateway

What is an Internet Gateway (IGW)?
> 

How many IGWs can a VPC have?
> 

What are ALL the requirements for an EC2 instance to reach the internet?
> 

Is an IGW a single point of failure?
> 

What happens if you remove the IGW route from a route table?
> 

---

## Part 6: Route Tables

What is a route table?
> 

What is the "local" route? Can you remove it?
> 

What route entry makes a subnet public?
> 

What is the main route table?
> 

Can different subnets use different route tables?
> 

How does route priority work? (most specific route wins)
> 

---

## Part 7: NAT Gateway

What is a NAT Gateway?
> 

Why would a private subnet need outbound internet access?
> 

Which subnet does the NAT Gateway go in, public or private?
> 

What does the private subnet's route table entry look like for NAT?
> 

What is the difference between an Internet Gateway and a NAT Gateway?
> 

Does a NAT Gateway allow inbound connections from the internet?
> 

How do you make a NAT Gateway highly available?
> 

What does a NAT Gateway cost?
> 

What is the difference between a NAT Gateway and a NAT Instance?
> 

---

## Part 8: Putting it Together

Draw the architecture of a VPC with public and private subnets across 2 AZs. Include the IGW, NAT Gateway, and route tables:
> 

Walk through the flow: a user makes an HTTP request to your app in a public subnet.
> 

Walk through the flow: an instance in a private subnet needs to download a package from the internet.
> 

---

## Part 9: VPC Peering

What is VPC Peering?
> 

What does "no transitive peering" mean?
> 

Can CIDR blocks overlap between peered VPCs?
> 

Can you peer VPCs across Regions?
> 

Can you peer VPCs across accounts?
> 

What needs to be configured on both sides of a peering connection?
> 

---

## Part 10: VPC Endpoints

What is a VPC Endpoint?
> 

What problem does it solve?
> 

What is a Gateway Endpoint? Which services support it?
> 

What is an Interface Endpoint?
> 

Why is a Gateway Endpoint for S3 better than going through a NAT Gateway?
> 

What is AWS PrivateLink?
> 

---

## Part 11: Transit Gateway

What is Transit Gateway?
> 

What problem does it solve that VPC Peering cannot?
> 

What is the hub-and-spoke model?
> 

When would you use Transit Gateway instead of VPC Peering?
> 

---

## Part 12: VPN and Direct Connect

What is a Site-to-Site VPN?
> 

What is a Virtual Private Gateway?
> 

What is a Customer Gateway?
> 

What is AWS Direct Connect?
> 

What is the difference between VPN and Direct Connect?
> 

When would you need Direct Connect over VPN?
> 

---

## Part 13: Troubleshooting Connectivity

Walk through the troubleshooting order for connectivity issues:
1. > 
2. > 
3. > 
4. > 
5. > 

What are VPC Flow Logs? What do they capture?
> 

What is the VPC Reachability Analyzer?
> 

---

## Part 14: Bastion Hosts

What is a bastion host?
>

Where does a bastion host sit in relation to public and private subnets?
>

How do you SSH to an instance in a private subnet using a bastion host?
>

What Security Group rules does a bastion host need?
>

What is a better alternative to bastion hosts for accessing private instances?
>

---

## Part 15: IPv6 and Egress Only Internet Gateway

Does AWS support IPv6 in VPCs?
>

Can a subnet be dual-stack (both IPv4 and IPv6)?
>

What is an Egress Only Internet Gateway?
>

How is an Egress Only Internet Gateway different from a NAT Gateway?
>

Why would you use an Egress Only Internet Gateway?
>

---

## Part 16: Networking Costs in AWS

Does traffic within the same AZ cost money?
>

Does traffic between AZs cost money?
>

Does traffic between Regions cost money?
>

Why should you keep resources in the same AZ when possible?
>

Is inbound (ingress) traffic to AWS free?
>

Is outbound (egress) traffic from AWS free?
>

How do VPC Endpoints help reduce networking costs?
>

---

## Part 17: AWS Network Firewall

What is AWS Network Firewall?
>

How is it different from Security Groups and NACLs?
>

What layer does Network Firewall operate at?
>

When would you use Network Firewall instead of NACLs?
>

---

## Commands to Learn

```bash
# What does this do?
aws ec2 describe-vpcs
```
> 

```bash
# What does this do?
aws ec2 create-vpc --cidr-block 10.0.0.0/16
```
> 

```bash
# What does this do?
aws ec2 create-subnet --vpc-id vpc-xxxxx --cidr-block 10.0.1.0/24 \
  --availability-zone eu-west-2a
```
> 

```bash
# What does this do?
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxx"
```
> 

```bash
# What does this do?
aws ec2 create-internet-gateway
```
> 

```bash
# What does this do?
aws ec2 attach-internet-gateway --internet-gateway-id igw-xxxxx --vpc-id vpc-xxxxx
```
> 

```bash
# What does this do?
aws ec2 create-route --route-table-id rtb-xxxxx \
  --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxxxx
```
> 

```bash
# What does this do?
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-xxxxx"
```
> 

```bash
# What does this do?
aws ec2 create-nat-gateway --subnet-id subnet-public --allocation-id eipalloc-xxxxx
```
> 

```bash
# What does this do?
aws ec2 create-vpc-endpoint --vpc-id vpc-xxxxx \
  --service-name com.amazonaws.eu-west-2.s3 --route-table-ids rtb-xxxxx
```
> 

```bash
# What does this do?
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-xxxxx \
  --traffic-type ALL --log-destination-type cloud-watch-logs \
  --log-group-name vpc-flow-logs
```
> 

---

## Hands-On Tasks

- Create a custom VPC with 10.0.0.0/16
- Create 2 public subnets and 2 private subnets across 2 AZs
- Attach an IGW and configure the public subnet route table
- Launch an instance in the public subnet, verify internet access
- Launch an instance in the private subnet, verify NO internet access
- Create a NAT Gateway, verify the private instance can reach the internet outbound
- Create an S3 Gateway Endpoint, verify S3 access from the private subnet without NAT
- Enable VPC Flow Logs and review traffic

---

## Quick Quiz

1. What is the difference between an Internet Gateway and a NAT Gateway?
   > 

2. Design a VPC for a three-tier web application. Walk through your subnet, routing, and gateway setup.
   > 

3. Why is a VPC Endpoint for S3 better than going through a NAT Gateway?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________