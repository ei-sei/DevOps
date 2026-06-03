# 6. Load Balancing & Scalability

---

## Part 1: Why Load Balancing Exists

What is the problem with a single server?
> A single server is a single point of failure - if it crashes, your app goes down, and it cannot scale beyond its hardware limits.

What is vertical scaling and what is its limitation?
> **Vertical scaling** means adding more CPU or RAM to the same machine. It hits a hard ceiling because hardware has a maximum size, and scaling up requires downtime.

What is horizontal scaling?
> **Horizontal scaling** means adding more servers to share the load. It has no practical ceiling and requires no downtime.

What is high availability?
> **High availability** means your application stays up even if individual components fail, achieved by running across multiple AZs so no single failure takes down the whole system.

What is a load balancer and what does it do?
> A **load balancer** is a proxy that sits in front of your servers and distributes incoming requests across them. It routes traffic, performs health checks, and exposes a single DNS endpoint to users.

What is AWS Elastic Load Balancing?
> **Elastic Load Balancing (ELB)** is a managed load balancer service where AWS handles provisioning, patching, capacity, and failover - saving you from running and maintaining your own on EC2.

---

## Part 2: Load Balancer Types

What are the three ELB types?
> **Application Load Balancer (ALB)**, **Network Load Balancer (NLB)**, and **Gateway Load Balancer (GLB)**.

### ALB

What is an ALB and what layer does it operate at?
> **ALB** operates at OSI Layer 7 - the application layer. It can read HTTP headers, paths, and hostnames to make routing decisions, making it suited for web apps and microservices.

### NLB

What is an NLB and what layer does it operate at?
> **NLB** operates at OSI Layer 4 - the transport layer. It routes by IP and TCP/UDP port without inspecting request content, handling extreme throughput with ultra-low latency.

### GLB

What is a GLB and what is it used for?
> **GLB** operates at OSI Layer 3 - the network layer. It routes traffic through third-party virtual appliances like firewalls and intrusion detection systems. It is for security inspection, not general application traffic.

### ALB vs NLB

Why is NLB faster than ALB?
> NLB skips HTTP parsing and routes at the packet level with no content inspection overhead.

How do ALB and NLB differ in IP addressing?
> ALB has dynamic IPs that change, so you must reference it by DNS name. NLB has static IPs (one per AZ), which matters when firewalls need a fixed IP to allowlist.

Does NLB preserve the original client IP?
> Yes - NLB passes the original client IP to your backend, which is useful for logging, geolocation, and IP-based access control.

Does ALB support content-based routing?
> Yes - ALB supports path-based and host-based routing. NLB does not - it routes only by port.

When would you choose ALB vs NLB?
> Choose ALB for HTTP/HTTPS web apps, microservices, or anything needing content-based routing. Choose NLB for TCP/UDP workloads, gaming, IoT, or when you need static IPs or ultra-low latency.

Can you combine them?
> Yes - you can put an ALB behind an NLB to get static IPs for allowlisting while still using ALB's content-based routing.

---

## Part 3: ALB Listeners

What is a listener?
> A **listener** is a process on the ALB that checks for incoming connections on a specified protocol and port - it is the entry point for traffic.

What do you configure on a listener?
> The protocol (HTTP or HTTPS) and the port (e.g., 80 or 443).

Can an ALB have multiple listeners?
> Yes - for example, one on port 80 for HTTP and one on port 443 for HTTPS.

What is the default action?
> The **default action** is the fallback taken when no listener rule matches the request - typically forwarding to a default target group or returning a fixed response.

---

## Part 4: ALB Listener Rules

What is a listener rule?
> A **listener rule** is a condition-action pair that tells the ALB how to route a request matching specific criteria.

What does each rule contain?
> A **condition** (when to apply it) and an **action** (what to do - forward, redirect, return a fixed response, or authenticate).

What can conditions match on?
> URL path, host header, HTTP method, query string, source IP, or HTTP headers.

What actions are available?
> Forward to a target group, redirect (e.g., HTTP to HTTPS), return a fixed response, or authenticate via Cognito/OIDC.

How are rules evaluated?
> In priority order (lowest number first). The default rule at the end acts as a catch-all.

What happens if no rule matches?
> The default rule applies - usually forwarding to a default target group or returning a 404.

Give an example of path-based routing:
> A rule with condition `path is /api/*` forwards to the API target group. A rule with condition `path is /images/*` forwards to the images target group.

Give an example of host-based routing:
> Requests with host header `app1.example.com` go to target group A. Requests with `app2.example.com` go to target group B.

---

## Part 5: Target Groups

What is a target group?
> A **target group** is a logical group of backend resources that receive forwarded traffic from a listener rule, with their own health check configuration.

What are the target types?
> **EC2 instances** (by instance ID), **IP addresses** (including on-premises servers), or **Lambda functions**.

Can a single ALB route to multiple target groups?
> Yes - via different listener rules.

Can an instance belong to multiple target groups?
> Yes.

When would you use the IP target type?
> When routing to ECS containers (where the container IP matters, not the host instance), on-premises servers, or any endpoint not managed as an EC2 instance.

When would you use the Lambda target type?
> To invoke a serverless function directly from the ALB without an API Gateway.

---

## Part 6: Health Checks

What is a health check?
> A **health check** is a periodic request the ALB sends to each target to verify it can serve traffic before routing real requests to it. It runs continuously in the background.

What settings can you configure?
> Protocol, path (for HTTP), port, healthy threshold, unhealthy threshold, timeout, and interval.

What is the healthy threshold?
> The **healthy threshold** is the number of consecutive successful checks required before a target is marked healthy and starts receiving traffic - typically 2 to 3.

What is the unhealthy threshold?
> The **unhealthy threshold** is the number of consecutive failed checks required before a target is marked unhealthy and removed from rotation - typically 2 to 3.

What happens when a target fails its health check?
> The ALB marks it unhealthy, stops sending new requests to it, and the remaining healthy targets absorb the traffic until the failing target recovers or is replaced.

What is deregistration delay?
> **Deregistration delay** is a waiting period after a target is deregistered during which the ALB finishes in-flight requests before fully removing the target - defaults to 300 seconds.

Why does connection draining matter during deployments?
> It ensures users mid-request are not abruptly disconnected when you replace instances with a new version.

What happens if your health check path is misconfigured?
> If your health check path is `/health` but the app only responds on `/`, the health check receives a 404, the target is marked unhealthy, and the ALB stops sending traffic to it even though the app is working fine.

---

## Part 7: SSL/TLS

### Termination

What is SSL/TLS termination?
> **SSL/TLS termination** means the load balancer decrypts HTTPS traffic from the client, then communicates with backends over plain HTTP. Your app servers never handle encryption, offloading the CPU cost.

What is the benefit of terminating at the load balancer?
> Backend instances do not need certificates or encryption logic, reducing their CPU load and simplifying certificate management.

### ACM

What is ACM?
> **ACM** (AWS Certificate Manager) provisions, renews, and manages SSL/TLS certificates for use with AWS services, handling renewals automatically at no cost.

How do you attach a certificate to an ALB?
> Request a certificate in ACM, validate domain ownership via DNS or email, then attach the certificate to your ALB's HTTPS listener.

### SNI

What is SNI?
> **SNI** (Server Name Indication) is a TLS extension where the client tells the server which hostname it is connecting to before the handshake completes, allowing one IP to serve multiple certificates.

How does the ALB use SNI?
> The ALB reads the SNI hostname in the TLS handshake and selects the matching certificate for that domain.

Which load balancer types support SNI?
> Both ALB and NLB.

### HTTP to HTTPS Redirect

How do you redirect HTTP to HTTPS on an ALB?
> Add a listener rule on port 80 with the action "Redirect to HTTPS" - the ALB sends a 301/302 redirect to the client automatically.

---

## Part 8: Sticky Sessions

What is session stickiness?
> **Session stickiness** (also called session affinity) is a load balancer feature that binds a user's session to one specific backend instance so all their requests go to the same server.

What problem does it solve?
> Stateful applications that store session data locally on the server - without stickiness, a user might hit a different instance that has no record of their session.

What are the two cookie types?
> **LB-generated cookie** - the ALB creates and manages it, named `AWSALB`. **Application-based cookie** - your app creates its own cookie and the ALB uses it for routing.

What is the downside of stickiness?
> It can overload certain instances because users are pinned to them regardless of current server load.

What is the better alternative?
> Store session state in a shared external store such as ElastiCache (Redis) or DynamoDB so any backend instance can serve any user.

---

## Part 9: Cross-Zone Load Balancing

What is cross-zone load balancing?
> **Cross-zone load balancing** means each load balancer node distributes traffic evenly across all registered targets in all AZs, not just the targets in its own AZ.

What problem does it solve?
> It prevents traffic imbalances caused by unequal instance counts per AZ. Without it, AZ-A's 2 instances each get 25% of traffic while AZ-B's 8 instances each get 6.25% - AZ-A is overloaded. With it, all 10 instances share traffic equally at 10% each.

Is cross-zone load balancing enabled by default on ALB?
> Yes - and there is no charge for it.

Is cross-zone load balancing enabled by default on NLB?
> No - and enabling it incurs inter-AZ data transfer charges.

---

## Part 10: Security Group Chain

Does an ALB need its own security group?
> Yes - separate from the backend instances.

What should the ALB security group allow?
> Inbound HTTP (port 80) and HTTPS (port 443) from `0.0.0.0/0`.

What should the backend EC2 security group allow?
> Inbound traffic only from the ALB's security group ID as the source.

Why reference the ALB security group instead of `0.0.0.0/0`?
> It means only the ALB can reach your instances - users cannot bypass the load balancer and connect directly to your EC2s.

---

## Part 11: Why Auto Scaling Exists

What problem does Auto Scaling solve?
> Mismatched capacity - having too few instances during peak load or paying for idle instances during low traffic.

What happens without Auto Scaling during a traffic spike?
> The spike exhausts your fixed instance count, causing slow responses or downtime.

What happens without Auto Scaling during low traffic?
> You pay for instances running at near-zero utilisation.

How does Auto Scaling integrate with a load balancer?
> It registers new instances into the target group automatically so the load balancer can send them traffic immediately.

---

## Part 12: Launch Templates

What is a Launch Template?
> A **Launch Template** is a reusable configuration that defines exactly how new EC2 instances should be created, so Auto Scaling can launch identical instances without manual input.

What does a Launch Template contain?
> AMI ID, instance type, key pair, security groups, IAM role, user data script, storage configuration, and network settings.

What is a Launch Configuration and how does it differ?
> A **Launch Configuration** is the older, deprecated predecessor to Launch Templates - same purpose but immutable and with fewer features. It cannot be updated after creation. Launch Templates are versioned and can be modified.

Should you use Launch Templates or Launch Configurations?
> Launch Templates - AWS recommends them and they are required for newer features like mixed instance types and Spot instance support.

---

## Part 13: Auto Scaling Groups

What is an Auto Scaling Group?
> An **Auto Scaling Group (ASG)** is a group of EC2 instances managed together so AWS can automatically add or remove instances based on demand or health.

What is minimum capacity?
> The floor - the ASG will never reduce instance count below this number, ensuring your app always has baseline capacity.

What is maximum capacity?
> The ceiling - the ASG will never exceed this instance count, controlling your maximum spend.

What is desired capacity?
> The target number of instances the ASG tries to maintain at all times - it is what the ASG actively works toward.

What happens if you manually terminate an instance in an ASG?
> If desired is 2 and you terminate one instance, the ASG detects the count has dropped below desired and automatically launches a replacement to restore it to 2.

How does an ASG distribute instances across AZs?
> You configure the ASG with a list of subnets (and therefore AZs) to launch into - the ASG distributes instances across them for high availability.

How does an ASG integrate with a load balancer?
> You attach the ASG to a load balancer's target group - newly launched instances register themselves automatically and deregister on termination.

---

## Part 14: ASG Health Checks

What health check types can an ASG use?
> EC2 health checks (default) or ELB health checks.

What is the difference between EC2 and ELB health checks?
> EC2 health checks only verify the instance is running (not stopped or terminated). ELB health checks use the load balancer's application-level check, which also verifies your app is responding correctly.

Which should you use when behind a load balancer?
> ELB health checks - an instance might pass the EC2 check (it is running) while your application is crashed. ELB health checks catch this case.

What is the health check grace period?
> A delay after launch during which the ASG ignores health check failures, giving the instance time to boot and start the app before being judged unhealthy.

What happens if the grace period is too short?
> If instances take 90 seconds to boot but the grace period is 60 seconds, the ASG evaluates health before the app is ready, marks instances unhealthy, terminates them, and enters a launch-terminate loop.

---

## Part 15: Scaling Policies

### Target Tracking

What is dynamic scaling?
> **Dynamic scaling** automatically adjusts instance count in real time in response to changing metrics like CPU usage - reacting to actual load rather than a schedule.

What is the difference between scaling out and scaling in?
> **Scaling out** means adding instances. **Scaling in** means removing instances.

What is target tracking scaling?
> A **target tracking scaling policy** lets you set a target metric value and the ASG automatically adjusts instance count to keep the metric at that value - similar to a thermostat.

Give an example of target tracking:
> Set a target of 50% average CPU utilisation - if CPU rises above 50%, the ASG adds instances. If it drops below, the ASG removes them.

What predefined metrics are available for target tracking?
> `ASGAverageCPUUtilization`, `ALBRequestCountPerTarget`, `ASGAverageNetworkIn`, and `ASGAverageNetworkOut`.

Why is target tracking recommended as a starting point?
> It requires no manual threshold math - you declare the desired state and the policy manages the calculations for you.

### Step Scaling

What is step scaling?
> **Step scaling** scales by different amounts depending on how far the metric breaches a threshold - larger breaches trigger larger capacity changes.

How does it differ from target tracking?
> Step scaling is manually defined with specific thresholds and step sizes, whereas target tracking calculates adjustments automatically.

Give an example of step scaling:
> If CPU is 60-80%, add 1 instance. If CPU is 80-100%, add 3 instances. If CPU drops below 40%, remove 1 instance.

### Simple Scaling

What is simple scaling?
> **Simple scaling** adds or removes a fixed number of instances when a single CloudWatch alarm triggers, then waits for a cooldown before acting again. It is the most basic form of scaling.

Why is simple scaling worse than step scaling?
> It waits for a full cooldown after each action, making it slow to respond to rapidly changing load, and it only reacts at a single threshold.

---

## Part 16: Scheduled and Predictive Scaling

### Scheduled Scaling

What is scheduled scaling?
> **Scheduled scaling** pre-configures capacity changes to happen at specific times, independent of real-time metrics - suited to predictable traffic patterns.

Give an example:
> Increase desired capacity to 10 every weekday at 08:00 and reduce it to 2 at 20:00 for a business application used only during office hours.

### Predictive Scaling

What is predictive scaling?
> **Predictive scaling** uses machine learning to analyse your historical traffic patterns and proactively scale capacity in advance of predicted demand spikes - scaling before the load arrives rather than reacting to it.

How does predictive scaling work?
> AWS analyses your ASG's historical metric data over the past two weeks, forecasts future load, and schedules capacity changes ahead of time.

Can you combine multiple policy types?
> Yes - for example, predictive scaling for known patterns plus target tracking as a safety net for unexpected spikes.

---

## Part 17: Cooldown Periods

What is a cooldown period?
> A **cooldown period** is a pause after a scaling action during which the ASG ignores new scaling triggers, giving new instances time to start handling traffic before another change is made.

What happens without a cooldown?
> The ASG may launch or terminate multiple waves of instances before the first wave has started serving traffic, causing instability.

What is the default cooldown period?
> 300 seconds (5 minutes).

What is scale-in protection?
> **Scale-in protection** is a flag you can set on individual instances to prevent the ASG from terminating them during a scale-in event - useful for instances running long-running jobs you do not want interrupted.

---

## Part 18: Instance Refresh

What is ASG instance refresh?
> **Instance refresh** is a rolling replacement of all instances in the ASG to apply an updated Launch Template - for example, a new AMI - without taking down the whole group.

When would you use it?
> When you update your AMI (e.g., OS patch, new application version) and need to roll out the change to every running instance without manual intervention.

What is the minimum healthy percentage in an instance refresh?
> The floor of healthy instances that must remain in service during the refresh. For example, 80% means the ASG replaces at most 20% of instances at a time, controlling the blast radius of a bad deployment.

---

## Commands to Learn

```bash
# Create an Application Load Balancer
aws elbv2 create-load-balancer --name my-alb --type application \
  --subnets subnet-aaa subnet-bbb --security-groups sg-xxxxx
```

```bash
# List load balancers
aws elbv2 describe-load-balancers
```

```bash
# Create a target group
aws elbv2 create-target-group --name my-targets --protocol HTTP --port 80 \
  --vpc-id vpc-xxxxx --health-check-path /health
```

```bash
# Register targets in a target group
aws elbv2 register-targets --target-group-arn arn:aws:... \
  --targets Id=i-xxxxx Id=i-yyyyy
```

```bash
# Check target health
aws elbv2 describe-target-health --target-group-arn arn:aws:...
```

```bash
# Create an Auto Scaling Group
aws autoscaling create-auto-scaling-group --auto-scaling-group-name my-asg \
  --launch-template LaunchTemplateName=my-template,Version='$Latest' \
  --min-size 1 --max-size 3 --desired-capacity 2
```

```bash
# List Auto Scaling Groups
aws autoscaling describe-auto-scaling-groups
```

```bash
# Add a target tracking scaling policy for CPU at 50%
aws autoscaling put-scaling-policy --auto-scaling-group-name my-asg \
  --policy-name cpu-target --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}'
```
