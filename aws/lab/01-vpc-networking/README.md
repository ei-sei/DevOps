# VPC and Networking Lab

## Objective

Create a custom VPC with the following:
- One public subnet and one private subnet
- An Internet Gateway for public internet access
- Route tables for public and private subnet traffic
- EC2 instances in both subnets
- Security groups controlling inbound/outbound traffic
- A bastion host for secure SSH access to private instances
- CloudWatch monitoring and logging

### Architecture

![vpc networking architecture](/assets/01-lab/vpc-networking-architecture.png)

---

### 1. Create the [VPC](/notes/03-networking.md#part-1-what-is-a-vpc)

- Custom VPC (`10.0.0.0/16`)
- One public subnet
- One private subnet

Create the VPC:

![vpc](/assets/01-lab/vpc.png)

Create the subnets for the associated VPC:

- **Public subnet:** `10.0.1.0/24`

![public subnet](/assets/01-lab/public-subnet.png)

- **Private subnet:** `10.0.2.0/24`

![private subnet](/assets/01-lab/private-subnet.png)

---

### 2. Internet Access

Create and attach an [Internet Gateway](/notes/03-networking.md#part-5-internet-gateway):

![igw](/assets/01-lab/igw.png)

Create an [Elastic IP](/notes/03-networking.md#part-7-elastic-ip):

![elastic ip](/assets/01-lab/elastic-ip.png)

Create a [NAT Gateway](/notes/03-networking.md#part-8-nat-gateway) in the public subnet:

![nat gateway](/assets/01-lab/nat-gateway.png)

---

### 3. [Route Tables](/notes/03-networking.md#part-6-route-tables)

**Public route table** - default route via IGW

![public route table](/assets/01-lab/public-route-table.png)

**Private route table** - default route via NAT Gateway

![private route table](/assets/01-lab/private-route-table.png)

> **Resource map**
>
> ![resource map](/assets/01-lab/resource-map.png)

---

### 4. [EC2](/notes/04-ec2.md#part-1-what-is-ec2) Instances

**Public EC2** - launch in public subnet with public IP

![public ec2](/assets/01-lab/public-ec2-instance.png)

**Private EC2** - launch in private subnet without public IP

![private ec2](/assets/01-lab/private-ec2-instance.png)

**Bastion Host** - deploy to access the private EC2

![bastion host](/assets/01-lab/bastion-host.png)

---

### 5. [Security Groups](/notes/05-security-groups.md#part-1-what-is-a-security-group)

**Public EC2 SG** - allow SSH/HTTP only from your IP

![public sg](/assets/01-lab/sg-public.png)

**Bastion EC2 SG** - allow SSH only from your IP

![bastion sg](/assets/01-lab/bastion-sg.png)

**Private EC2 SG** - allow only internal access from bastion host

![private sg](/assets/01-lab/sg-private.png)

---

### 6. Testing

SSH into public EC2 instance:

![ssh public](/assets/01-lab/ssh-public-ec2.png)

SSH into private instance via bastion host:

```bash
# Start SSH agent on local machine
eval $(ssh-agent -s)

# Add your private keys to the agent
ssh-add ~/Documents/private.pem
ssh-add ~/Documents/bastion-key.pem

# SSH into bastion with agent forwarding
ssh -A -i ~/Documents/bastion-key.pem ec2-user@52.56.190.227

# From inside bastion, SSH to private EC2
ssh ec2-user@10.0.2.71
```

> **Note:**
> - Replace `~/Documents/bastion-key.pem` with the path to your SSH key
> - Replace `52.56.190.227` with the public IP of your bastion host
> - Replace `10.0.2.71` with the private IP of your private instance

![SSH via bastion host](/assets/01-lab/ssh-bastion-private-instance.png)

---

### 7. CloudWatch

Create an IAM Role for EC2:
- Select: EC2
- Search for and attach policy: CloudWatchAgentServerPolicy
- Name it: ec2-cloudwatch-role
- Create role

![iam role](/assets/01-lab/iam-role-cloudwatch.png)


**Attach Role to EC2 Instances:**

![iam attach](/assets/01-lab/iam-attach.png)

**Install CloudWatch Agent** - SSH into each instance and run:
    
```bash
# Download agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm

# Install agent
sudo rpm -U ./amazon-cloudwatch-agent.rpm

# Optional: Launch CloudWatch configuration wizard
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c default \
  -s
```

**View in CloudWatch:**
- Go to CloudWatch > Dashboards
- Create dashboard or view metrics under Metrics section
- You'll see your instance metrics and logs

![cloudwatch](/assets/01-lab/cloudwatch.png)