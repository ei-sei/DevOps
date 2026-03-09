# 6. Load Balancing & Scalability

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: Why Load Balancing Exists

What is the problem with running your application on a single server?
> 

What is vertical scaling? What is its limitation?
> 

What is horizontal scaling?
> 

What does "high availability" mean?
> 

What does a load balancer do?
> 

Where does a load balancer sit in relation to users and servers?
> 

Why use AWS Elastic Load Balancing instead of running your own (e.g., nginx on EC2)?
> 

---

## Part 2: Load Balancer Types

What are the three types of Elastic Load Balancer on AWS?
> 

What OSI layer does ALB operate at? What does that mean in practice?
> 

What OSI layer does NLB operate at? What does that mean in practice?
> 

What OSI layer does GLB operate at? What is it used for?
> 

Why is NLB faster than ALB?
> 

ALB has dynamic IPs. NLB has static IPs. Why does this matter?
> 

NLB preserves the client's source IP address. Why is this useful?
> 

Can ALB do path-based routing? Can NLB?
> 

When would you choose ALB over NLB?
> 

When would you choose NLB over ALB?
> 

Can you put an ALB behind an NLB? Why would you do this?
> 

---

## Part 3: How ALB Works, Listeners

What is a listener?
> 

What two things do you configure on a listener?
> 

Can an ALB have multiple listeners? Give an example.
> 

What is the default action on a listener?
> 

---

## Part 4: How ALB Works, Listener Rules

What is a listener rule?
> 

What two parts does a rule have?
> 

What conditions can you use in a rule?
> 

What actions can a rule take?
> 

In what order are rules evaluated?
> 

What happens if no rule matches a request?
> 

Give an example: route /api/* to one place and /images/* to another.
> 

Give an example of host-based routing.
> 

---

## Part 5: Target Groups

What is a target group?
> 

What target types can a target group contain?
> 

Can a single ALB route to multiple target groups?
> 

Can an instance be in multiple target groups?
> 

When would you use the "IP" target type?
> 

When would you use the "Lambda" target type?
> 

---

## Part 6: Health Checks

What is a health check?
> 

What settings can you configure on a health check?
> 

What is the healthy threshold?
> 

What is the unhealthy threshold?
> 

A target fails its health check. What happens step by step?
> 

What is deregistration delay (connection draining)?
> 

Why does connection draining matter during deployments?
> 

Your health check path is `/health` but your app only responds on `/`. What happens?
> 

---

## Part 7: SSL/TLS on Load Balancers

What is SSL/TLS termination?
> 

Why terminate SSL at the load balancer instead of at each backend instance?
> 

What is ACM (AWS Certificate Manager)?
> 

How do you get a free SSL certificate for your ALB?
> 

What is SNI (Server Name Indication)?
> 

You host app1.example.com and app2.example.com on the same ALB with different certificates. How does the ALB know which certificate to present?
> 

Which load balancer types support SNI?
> 

How do you redirect HTTP to HTTPS on an ALB?
> 

---

## Part 8: Sticky Sessions

What is session stickiness (session affinity)?
> 

What problem does it solve?
> 

What are the two types of stickiness cookies?
> 

Why can stickiness cause uneven load distribution?
> 

What is a better alternative to stickiness? Where should session state live instead?
> 

---

## Part 9: Cross-Zone Load Balancing

What is cross-zone load balancing?
> 

Without cross-zone: AZ-A has 2 instances, AZ-B has 8 instances. Each AZ gets 50% of traffic. What is the problem?
> 

With cross-zone enabled, how is traffic distributed in the same setup?
> 

Is cross-zone enabled by default on ALB?
> 

Is cross-zone enabled by default on NLB? Does it cost extra?
> 

---

## Part 10: Security Group Chain for Load Balancers

Does an ALB need its own security group?
> 

What inbound rules should the ALB security group have?
> 

What should the backend EC2 security group allow as its source?
> 

Why should the backend reference the ALB's security group instead of allowing 0.0.0.0/0?
> 

---

## Part 11: Why Auto Scaling Exists

What problem does Auto Scaling solve?
> 

Without Auto Scaling, your site gets a traffic spike. What happens?
> 

Without Auto Scaling, traffic drops to near-zero at night. What are you wasting?
> 

What is the relationship between Auto Scaling and a load balancer?
> 

---

## Part 12: Launch Templates

What is a Launch Template?
> 

What information goes in a Launch Template?
> 

What is the difference between a Launch Template and a Launch Configuration?
> 

Which one should you use and why?
> 

---

## Part 13: Auto Scaling Groups

What is an Auto Scaling Group (ASG)?
> 

What is minimum capacity?
> 

What is maximum capacity?
> 

What is desired capacity?
> 

Desired is 2, min is 1, max is 4. You manually terminate one instance. What happens?
> 

How does an ASG know which subnets and AZs to launch instances in?
> 

How does an ASG connect to a load balancer?
> 

---

## Part 14: ASG Health Checks

What health check types can an ASG use?
> 

What is the difference between EC2 health checks and ELB health checks on an ASG?
> 

Why should you use ELB health checks when your ASG is behind a load balancer?
> 

What is the health check grace period?
> 

Your instances take 90 seconds to boot. The grace period is 60 seconds. What goes wrong?
> 

---

## Part 15: Scaling Policies, Target Tracking

What is dynamic scaling?
> 

What is the difference between scaling out and scaling in?
> 

What is a target tracking scaling policy?
> 

Give an example using CPU utilisation.
> 

What predefined metrics can you target track?
> 

Why is target tracking the recommended starting point?
> 

---

## Part 16: Scaling Policies, Step and Simple

What is step scaling?
> 

How does step scaling differ from target tracking?
> 

Give an example with multiple thresholds.
> 

What is simple scaling?
> 

Why is simple scaling generally worse than step scaling?
> 

---

## Part 17: Scaling Policies, Scheduled and Predictive

What is scheduled scaling?
> 

Give a real-world example of when you would use it.
> 

What is predictive scaling?
> 

How does predictive scaling know when to scale?
> 

Can you combine multiple scaling policy types on the same ASG?
> 

---

## Part 18: Cooldown Periods

What is a cooldown period?
> 

What happens if you do not have one or it is too short?
> 

What is the default cooldown period?
> 

What is scale-in protection? When would you use it?
> 

---

## Part 19: Instance Refresh

What is ASG instance refresh?
> 

When would you use it?
> 

What is the minimum healthy percentage setting?
> 

---

## Commands to Learn

```bash
# What does this do?
aws elbv2 create-load-balancer --name my-alb --type application \
  --subnets subnet-aaa subnet-bbb --security-groups sg-xxxxx
```
> 

```bash
# What does this do?
aws elbv2 describe-load-balancers
```
> 

```bash
# What does this do?
aws elbv2 create-target-group --name my-targets --protocol HTTP --port 80 \
  --vpc-id vpc-xxxxx --health-check-path /health
```
> 

```bash
# What does this do?
aws elbv2 register-targets --target-group-arn arn:aws:... \
  --targets Id=i-xxxxx Id=i-yyyyy
```
> 

```bash
# What does this do?
aws elbv2 describe-target-health --target-group-arn arn:aws:...
```
> 

```bash
# What does this do?
aws autoscaling create-auto-scaling-group --auto-scaling-group-name my-asg \
  --launch-template LaunchTemplateName=my-template,Version='$Latest' \
  --min-size 1 --max-size 3 --desired-capacity 2
```
> 

```bash
# What does this do?
aws autoscaling describe-auto-scaling-groups
```
> 

```bash
# What does this do?
aws autoscaling put-scaling-policy --auto-scaling-group-name my-asg \
  --policy-name cpu-target --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}'
```
> 

---

## Hands-On Tasks

- Create an ALB with two EC2 instances serving different pages, verify traffic distribution
- Set up path-based routing: /api to target group A, /web to target group B
- Configure HTTPS on ALB using an ACM certificate, redirect HTTP to HTTPS
- Create an ASG with min=1, max=3, desired=2 behind the ALB
- Terminate one instance and watch the ASG replace it
- Add a target tracking policy for CPU and stress-test it

---

## Quick Quiz

1. What is the difference between ALB and NLB? When would you use each?
   > 

2. Walk through what happens when an ASG health check fails on an instance behind an ALB.
   > 

3. You are designing a highly available web app. Describe your ALB and ASG setup.
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________