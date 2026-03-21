# Application Load Balancer Lab

## Objective

Deploy two EC2 instances behind an ALB with the following:
- Two EC2 instances across different availability zones
- An Application Load Balancer with HTTP listener
- A Target Group with health checks
- Security groups enforcing ALB-only access to EC2

### Architecture

![ALBarchitecture](/assets/02-lab/ALB-architecture.png)

---



### 1. Launch EC2 Instances

Launch two EC2 instances in the same VPC, using different availability zones where possible. Install a simple web server using user data. Each instance should return different content for testing.

---

### 2. Set Up the ALB

Create an ALB in two public subnets with an HTTP (port 80) listener.

Create a Target Group and register both EC2 instances. Configure a health check on the root path `/`.

---

### 3. Security Groups

**ALB SG** - allow HTTP from anywhere

**EC2 SG** - allow HTTP only from the ALB SG. Do not allow direct public access to EC2.

---

### 4. Testing

Visit the ALB DNS name. Refresh to verify traffic alternates between both instances. Confirm health checks are healthy.

---

### 5. Bonus (Optional)

Add a Route53 DNS name and point it to the ALB DNS name via ALIAS record type. Add an HTTPS listener with ACM. Add an Auto Scaling Group behind the ALB.
