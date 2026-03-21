# 9. VPC & Networking

---

## Part 1: What is a VPC

What is a VPC (Virtual Private Cloud)?
> A secure, isolated, and logically private network within the public cloud.

Why do you need a VPC?
> To build a network infrastructure within the cloud. You can control the security, IP addressing, routing, access.

What is the default VPC? Does every Region have one?
> A preconfigured, logically isolated network automatically created by AWS for each region

What is the difference between the default VPC and a custom VPC?
> default VPC is pre-configured, whereas custom VPC offer more flexibility in customising your network with CIDR range, subnet layout, route tables, gateways.

---

## Part 2: CIDR Blocks

What is a CIDR block?
> Classless Inter-Domain Routing - a method for defining a range of IP addresses using a base IP and a prefix length (e.g. 10.0.0.0/16)

What does 10.0.0.0/16 mean?
> The first 16 bits are the fixed network portion (10.0), the remaining 16 bits are available for hosts, giving a range of 10.0.0.0 - 10.0.255.255

How many IP addresses does /16 give you?
> 65,536 (2^16)

How many IP addresses does /24 give you?
> 256 (2^8)

Can you change a VPC's CIDR block after creating it?
> You cannot change the original CIDR block, but you can add secondary CIDR blocks to expand the VPC

What CIDR ranges are commonly used for private networks?
> 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC 1918)

---

## Part 3: Subnets

What is a subnet?
> a logical, segmented partition of a larger IP network. Each subnet gets its own CIDR block (e.g. 10.0.1.0/24) and sits in one AZ

Can a subnet span multiple Availability Zones?
> No

How many IP addresses does AWS reserve per subnet? Which ones?
> AWS reserves exactly 5 IP addresses in every subnet for networking management:
> - First address: Network address
> - Second address: VPC router address
> - Third address: DNS server (base of the VPC network range +2)
> - Fourth address: Future use
> - Last address: Broadcast address

How many usable IPs are in a /24 subnet?
> 251

Why should you create subnets in at least 2 AZs?
> High-availability, if one AZ goes down you will have redundancy as your app will still be running over the other subnet

---

## Part 4: Public vs Private Subnets

What makes a subnet "public"?
> Route table has a route to an internet gateway (e.g. 0.0.0.0/0 to IGW). Also instances need a public IP assigned.

What makes a subnet "private"?
> No route to an Internet Gateway in its route table.

Why would you put resources in a private subnet?
> To protect the resources within the subnet from direct exposure to the internet

What types of resources typically go in public subnets?
> load-balancers, NAT gateways, bastion hosts.

What types of resources typically go in private subnets?
> Databases, application servers, caches, anything that shouldn't be directly reachable from the internet.

---

## Part 5: Internet Gateway

What is an Internet Gateway (IGW)?
> a VPC component that allows communication between your VPC and the internet

How many IGWs can a VPC have?
> One

What are ALL the requirements for an EC2 instance to reach the internet?
> VPC, Subnet, Public IP assigned to the instance, route table point 0.0.0.0/0 to the IGW, security group.

Is an IGW a single point of failure?
> No, it is highly available and horizontally scaled and redundant component.

What happens if you remove the IGW route from a route table?
> the subnet becomes a private subnet. Resources in it lose internet access but can still communicate within the VPC.

---

## Part 6: Route Tables

What is a route table?
> a set of rules that determine where network traffic is directed within a VPC

What is the "local" route? Can you remove it?
> The default route for communication within the VPC, can not be removed.

What route entry makes a subnet public?
> 0.0.0.0/0 -> IGW

What is the main route table?
> The main route table is the default routing table automatically created with an Amazon Virtual Private Cloud (VPC) that manages traffic for all subnets not explicitly associated with a custom table.

Can different subnets use different route tables?
> Yes

How does route priority work? (most specific route wins)
> Route priority determines traffic flow by prioritizing the most specific network prefix (longest subnet mask) in the routing table, regardless of source or protocol. A /24 route is always chosen over a /23 or default route (0.0.0.0/0)

---

## Part 7: Elastic IP

What is an Elastic IP?
> A static, public IPv4 address assigned to your AWS account that you can associate and disassociate with EC2 instances or NAT Gateways. Unlike regular public IPs, it persists even when the resource is stopped.

What is the difference between a public IP and an Elastic IP?
> A public IP is automatically assigned when you launch an instance in a public subnet, but changes when the instance stops or reboots. An Elastic IP is static and remains associated with your account until you explicitly release it.

What are the main use cases for Elastic IPs?
> NAT Gateways (require an Elastic IP to function), bastion hosts (stable access), failover scenarios (quickly reassign to another instance), or DNS aliases that need to remain constant.

Can an Elastic IP be moved between instances?
> Yes, you can disassociate an Elastic IP from one instance and associate it with another. This is useful for failover scenarios.

Is an Elastic IP specific to an AZ?
> No, an Elastic IP is regional but can be associated with instances in any AZ within that region.

How much does an Elastic IP cost?
> Charges per hour for each address not currently associated with a running instance. If associated with a running instance, there is no additional charge (you only pay for data transfer if applicable).

What happens if you don't use an Elastic IP?
> You'll be charged for it. This is why you should release unused Elastic IPs.

Can you have Elastic IPs across different regions?
> No, Elastic IPs are region-specific. You need separate Elastic IPs for each region.

---

## Part 8: NAT Gateway

What is a NAT Gateway?
> NAT Gateway lets instances in private subnets make outbound internet requests while keeping them unreachable from the internet. This sits inside the public subnet because it will need access to the IGW to reach the internet. It requires an [Elastic IP](./03-networking.md#part-7-elastic-ip) to function.

Why would a private subnet need outbound internet access?
> To allow updates from external resources such as OS updates, downloading packages, calling external APIs

Which subnet does the NAT Gateway go in, public or private?
> public

What does the private subnet's route table entry look like for NAT?
> 0.0.0.0/0 -> NAT Gateway

What is the difference between an Internet Gateway and a NAT Gateway?
> IGW allows inbound and outbound internet traffic whereas NAT Gateway only allows outbound.

Does a NAT Gateway allow inbound connections from the internet?
> No

How do you make a NAT Gateway highly available?
> Deploy a NAT gateway in each AZ. Each requires its own [Elastic IP](./03-networking.md#part-7-elastic-ip). A single NAT Gateway only covers its own AZ, so if that AZ goes down, private subnets in other AZs lose outbound access.

What does a NAT Gateway cost?
> Charges per hour and per GB of data processed. They're one of the more expensive VPC components.

What is the difference between a NAT Gateway and a NAT Instance?
> NAT Gateway is a managed AWS service (highly available, scales automatically). NAT Instance is an EC2 instance you manage yourself running NAT software. NAT Gateway is preferred, NAT Instance is cheaper but more work.

---

## Part 9: Putting it Together

Draw the architecture of a VPC with public and private subnets across 2 AZs. Include the IGW, NAT Gateway, and route tables:
![VPC architecture](/assets/notes/vpc-subnet-az-igw-natgateway.png)

Walk through the flow: a user makes an HTTP request to your app in a public subnet.
> 1. User sends HTTP request from the internet
> 2. Request hits the IGW
> 3. Route table directs traffic to the public subnet
> 4. Security group checks if inbound traffic on port 80/443 is allowed
> 5. Request reaches the EC2 instance

Walk through the flow: an instance in a private subnet needs to download a package from the internet.
> 1. Instance in private subnet sends outbound request
> 2. Route table sends 0.0.0.0/0 traffic to the NAT Gateway
> 3. NAT Gateway (in the public subnet) translates the private IP to its own public IP
> 4. Traffic goes through the IGW to the internet
> 5. Response comes back the same path in reverse.

---

## Part 10: VPC Peering

What is VPC Peering?
> A network connection between two VPCs that allows traffic to route between them using Private IP addresses, acting as if they are on the same network.

What does "no transitive peering" mean?
> "No transitive peering" means that VPC (Virtual Private Cloud) peering connections are one-to-one and cannot be chained. If VPC A is connected to VPC B, and VPC B is connected to VPC C, traffic cannot pass through VPC B to communicate between VPC A and VPC C.

Can CIDR blocks overlap between peered VPCs?
> No, the whole point of peering a network is so that they behave as one. 

Can you peer VPCs across Regions?
> Yes

Can you peer VPCs across accounts?
> Yes

What needs to be configured on both sides of a peering connection?
> Both VPCs need their route tables updated to point at the peering connection.


---

## Part 11: VPC Endpoints

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

## Part 12: Transit Gateway

What is Transit Gateway?
> 

What problem does it solve that VPC Peering cannot?
> 

What is the hub-and-spoke model?
> 

When would you use Transit Gateway instead of VPC Peering?
> 

---

## Part 13: VPN and Direct Connect

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

## Part 14: Troubleshooting Connectivity

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

## Part 15: Bastion Hosts

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

## Part 16: IPv6 and Egress Only Internet Gateway

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

## Part 17: Networking Costs in AWS

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

## Part 18: AWS Network Firewall

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