# 4. Security Groups & NACLs

---

## Part 1: What is a Security Group

What is a Security Group?
> A virtual firewall that controls inbound and outbound traffic, by defining allow/deny rules based on protocols, ports and source/destination IPs or other security groups. By default all inbound traffic is denied and outbound traffic allowed.

What is a Security Group attached to? (hint: not directly to an instance)
> A Network Interface (ENI). Since an instance can have multiple ENIs, it can have multiple security groups.

Is a Security Group stateful or stateless?
> stateful

What does "stateful" mean in this context?
> If you allow inbound traffic on a port, the return outbound traffic is automatically allowed - you don't need a separate outbound rule. AWS tracks the connection state.

---

## Part 2: Security Group Rules

What is the default inbound rule for a new Security Group?
> There will be no inbound rule, so all inbound traffic is denied

What is the default outbound rule for a new Security Group?
> Allow

Can you create a DENY rule in a Security Group?
> No

What happens if you attach multiple Security Groups to one instance?
> all attached SGs are merged together and evaluated as one set. It's a union of all allow rules.

When do Security Group changes take effect?
> Immediately after applied

---

## Part 3: Configuring Rules

What three things do you specify in a Security Group rule?
> Protocol, port range, source (for inbound) or destination (for outbound)

What does `0.0.0.0/0` mean as a source?
> Allow request from all IP addresses

Why is opening port 22 to 0.0.0.0/0 dangerous?
> Anyone will have the ability to SSH

What should you set as the source for SSH access instead?
> Your public IP

---

## Part 4: Security Group Chaining

What does it mean to reference another Security Group as a source?
> Instead of allowing traffic from a specific IP address, you allow traffic from any instance that has a particular security group attached. This is useful for allowing communication between groups of instances (e.g., allow web servers' security group to receive traffic from load balancer's security group).

Give an example of a 3-tier security group chain (web, app, database):
> Having a security group for each service such as: web, app, database. This allows flexibility on who can access what. For example you can set the inbound rule for app to allow traffic from anyone, but for security purposes, you may want to restrict the inbound rule to your IP only.

Why is referencing a Security Group better than hardcoding IP addresses?
> When you reference a security group, traffic is automatically allowed from any instance with that security group—no manual IP updates needed. If instances are replaced or scaled up, the rule still works. Hardcoding IPs breaks when instances change.

How does chaining help with Auto Scaling?
> When you reference security groups instead of hardcoding IPs, new instances launched by Auto Scaling automatically inherit the security group and are allowed through the firewall rules without manual reconfiguration.

---

## Part 5: Network ACLs

What is a Network ACL (NACL)?
> Network Access Control List, a firewall that controls inbound and outbound traffic using numbered rules (processed in order)

What level does a NACL operate at?
> Subnet level

Is a NACL stateful or stateless?
> stateless

What does "stateless" mean practically?
> Return traffic is not automatically allowed. If you allow inbound traffic on port 80, you must also explicitly allow outbound traffic on port 80 (or ephemeral ports). The NACL doesn't track connection state like a Security Group does.

Can you create DENY rules in a NACL?
> Yes

---

## Part 6: NACL Rule Evaluation

How does rule evaluation order work in NACLs?
> NACLs process rules in numerical order (lowest number first) and stop at the first match

What does the default NACL allow?
> all inbound and outbound IPv4 traffic

What does a custom (newly created) NACL allow by default?
> denies all inbound and outbound traffic

What are ephemeral ports?
> short-lived, transport-layer network endpoints automatically assigned by an operating system to client applications for outgoing connections. Typically ranging from 1024-65535

Why do ephemeral ports matter for NACLs but not for Security Groups?
> because they are stateless, requiring explicit inbound/outbound rules for both requests and responses

---

## Part 7: Security Groups vs NACLs

Fill in this comparison:

| Feature | Security Group | NACL |
|---------|---------------|------|
| Operates at | Instance (ENI) level | Subnet level |
| Stateful or Stateless | Stateful | Stateless |
| Rule types (Allow/Deny) | Allow only | Allow and Deny |
| How rules are evaluated | All rules checked, most permissive wins | Rules checked in order by rule number, first match wins |
| Default behaviour | Deny all inbound, allow all outbound | Allow all inbound and outbound |
 
When would you use a NACL in addition to Security Groups?
> When you need explicit deny rules (Security Groups can't deny), want a subnet-wide firewall as a second layer of defense, or need to block specific malicious IPs/ranges at the subnet boundary before traffic reaches instances.

---

## Part 8: Troubleshooting

You cannot SSH to your EC2 instance. What do you check, in order?
> - Check the Security Group – Is port 22 explicitly allowed inbound from your source IP?
> - Check the NACL – Is port 22 allowed inbound AND are ephemeral ports (1024-65535) allowed outbound for the return traffic?
> - Check the instance has a public IP or Elastic IP – Is it assigned and active?
> - Check the route table – Does the subnet have a route to the Internet Gateway (0.0.0.0/0 → IGW)?
> - Check the Internet Gateway – Is it attached to the VPC?
> - Check your SSH key pair – Do you have the correct private key and is it readable (chmod 400)?
> - Check the instance is running – Is the instance in a "running" state, not stopped or terminated?
> - Check network connectivity – Can you ping the instance's public IP or reach it on other ports?

You cannot reach your web app on port 443. Walk through your troubleshooting steps:
> - Check the Security Group – Is port 443 explicitly allowed inbound from your source IP/security group?
> - Check the NACL – Is port 443 allowed inbound AND are ephemeral ports (1024-65535) allowed outbound for the return traffic?
> - Check the instance is listening – SSH into the instance and verify the web app is actually running on port 443 (e.g. `netstat -tlnp | grep 443`).
> - Check the route table – Does the subnet have a route to your source (e.g. 0.0.0.0/0 → Internet Gateway for public traffic)?
> - Check the Internet Gateway – Is it attached to the VPC and is the instance in a public subnet with a public IP or Elastic IP?
> - Check the web app logs – Are there connection errors or is the app crashing on startup?
> Verify DNS - Is the domain name resolving to the correct IP address?

What are VPC Flow Logs?
> captures metadata about IP traffic flowing to and from network interfaces in a Virtual Private Cloud

What information do VPC Flow Logs capture?
> source/destination IP addresses, ports, protocols, packet/byte counts, action (ACCEPT/REJECT), and timestamps

What is the VPC Reachability Analyzer?
> a static configuration analysis tool used to troubleshoot and verify network connectivity between source and destination resources within or across VPCs

---

## Commands to Learn

```bash
# Create a security group called "web-sg" in the specified VPC
aws ec2 create-security-group --group-name web-sg \
  --description "Web server SG" --vpc-id vpc-xxxxx
```
> 

```bash
# Allow inbound SSH (port 22) from a single IP address
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 22 --cidr 203.0.113.0/32
```
> 

```bash
# Allow inbound HTTP (port 80) from all IP addresses
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```
> 

```bash
# Allow inbound MySQL (port 3306) from instances in the sg-app security group
aws ec2 authorize-security-group-ingress --group-id sg-db \
  --protocol tcp --port 3306 --source-group sg-app
```
> 

```bash
# Describe the rules and details of a specific security group
aws ec2 describe-security-groups --group-ids sg-xxxxx
```
> 

```bash
# Remove the inbound SSH (port 22) rule that was open to all IPs
aws ec2 revoke-security-group-ingress --group-id sg-xxxxx \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```
> 

```bash
# List all NACLs in a specific VPC
aws ec2 describe-network-acls --filters "Name=vpc-id,Values=vpc-xxxxx"
```
> 

---

## Hands-On Tasks

- Launch an EC2 instance with SSH allowed only from your IP, verify it works
- Add HTTP (port 80), install nginx, verify web access
- Create a second instance that only accepts traffic from the first instance's Security Group
- Create a custom NACL that blocks a specific IP and attach it to a subnet
- Deliberately misconfigure a rule and troubleshoot the connectivity issue
- Enable VPC Flow Logs and review the traffic

---

## Quick Quiz

1. What is the key difference between a Security Group and a NACL?
   > Security Groups are stateful and operate at the instance (ENI) level with allow-only rules. NACLs are stateless and operate at the subnet level with both allow and deny rules.

2. An EC2 instance cannot be reached on port 443. Walk through your troubleshooting steps.
   > - Check if the instance is running and has a public IP
   > - Check if the web server is actually listening on port 443
   > - Check the Security Group allows inbound on port 443
   > - Check the NACL allows inbound on port 443 and outbound on ephemeral ports (1024-65535) for return traffic
   > - Check the route table has a route to the IGW (0.0.0.0/0 -> IGW)
   > - Check the IGW is attached to the VPC

3. Why do NACLs require you to think about ephemeral ports but Security Groups do not?
   > NACLs are stateless, so you must explicitly allow outbound traffic on ephemeral ports (1024-65535) for return traffic. Security Groups are stateful, so return traffic is automatically allowed without needing additional rules.

---

## Confidence: 🟢

**Date completed:** 12/03/26