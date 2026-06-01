# 6. Load Balancing & Scalability

---

## Part 1: Why Load Balancing Exists

A single server is a single point of failure - if it crashes, your app goes down, and it cannot scale beyond its hardware limits.

**Vertical scaling** (what this means: adding more CPU/RAM to the same machine) hits a hard ceiling because hardware has a maximum size, and it requires downtime.

**Horizontal scaling** (what this means: adding more servers to share the load) has no practical ceiling and requires no downtime.

**High availability** (what this means: your application stays up even if individual components fail, achieved by running across multiple AZs) means no single failure takes down the whole system.

A **load balancer** (what this means: a proxy that sits in front of your servers and distributes incoming requests across them) routes traffic, performs health checks, and exposes a single DNS endpoint to users.

The load balancer sits between the internet and your backend servers - users connect to it, and it forwards requests to healthy instances.

AWS **Elastic Load Balancing** (what this means: a managed load balancer service where AWS handles provisioning, patching, capacity, and failover) saves you from running and maintaining your own on EC2.

---

## Part 2: Load Balancer Types

AWS offers three ELB types: **Application Load Balancer (ALB)**, **Network Load Balancer (NLB)**, and **Gateway Load Balancer (GLB)**.

**ALB** (what this means: operates at OSI Layer 7 - the application layer, meaning it can read HTTP headers, paths, and hostnames to make routing decisions) suits web apps and microservices.

**NLB** (what this means: operates at OSI Layer 4 - the transport layer, meaning it routes by IP and TCP/UDP port without inspecting the request content) handles extreme throughput and low latency.

**GLB** (what this means: operates at OSI Layer 3 - the network layer, used to route traffic through third-party virtual appliances like firewalls and intrusion detection systems) is for security inspection, not general application traffic.

NLB is faster than ALB because it skips HTTP parsing and routes at the packet level with no content inspection overhead.

ALB has dynamic IPs that change, so you must reference it by DNS name. NLB has static IPs (one per AZ), which matters when firewalls need a fixed IP to allowlist.

NLB passes the original client IP to your backend, which is useful for logging, geolocation, and IP-based access control.

ALB supports path-based and host-based routing. NLB does not - it routes only by port.

Choose ALB for HTTP/HTTPS web apps, microservices, or anything needing content-based routing. Choose NLB for TCP/UDP workloads, gaming, IoT, or when you need static IPs or ultra-low latency.

You can put an ALB behind an NLB to get static IPs for allowlisting while still using ALB's content-based routing.

---

## Part 3: How ALB Works - Listeners

A **listener** (what this means: a process on the ALB that checks for incoming connections on a specified protocol and port) is the entry point for traffic.

You configure the protocol (HTTP or HTTPS) and the port (e.g., 80 or 443) on each listener.

Yes, an ALB can have multiple listeners - for example, one on port 80 for HTTP and one on port 443 for HTTPS.

The **default action** (what this means: the fallback action taken when no listener rule matches the request) is typically to forward to a default target group or return a fixed response.

---

## Part 4: How ALB Works - Listener Rules

A **listener rule** (what this means: a condition-action pair that tells the ALB how to route a request matching specific criteria) lets you route different requests to different targets.

Each rule has a **condition** (when to apply it) and an **action** (what to do - forward, redirect, return a fixed response, or authenticate).

Conditions can match on: URL path, host header, HTTP method, query string, source IP, or HTTP headers.

Actions include: forward to a target group, redirect (e.g., HTTP to HTTPS), return a fixed response, or authenticate via Cognito/OIDC.

Rules are evaluated in priority order (lowest number first); the default rule at the end acts as a catch-all.

If no rule matches, the default rule applies - usually forwarding to a default target group or returning a 404.

Path routing example: a rule with condition `path is /api/*` forwards to the API target group; a rule with condition `path is /images/*` forwards to the images target group.

Host routing example: requests with host header `app1.example.com` go to target group A; requests with `app2.example.com` go to target group B.

---

## Part 5: Target Groups

A **target group** (what this means: a logical group of backend resources that receive forwarded traffic from a listener rule, with their own health check configuration) is the destination in a routing rule.

Target types: **EC2 instances** (by instance ID), **IP addresses** (including on-premises servers), or **Lambda functions**.

Yes, a single ALB can route to multiple target groups via different listener rules.

Yes, an instance can belong to multiple target groups simultaneously.

Use the IP target type when routing to containers in ECS (where the container IP matters, not the host instance), on-premises servers, or any endpoint not managed as an EC2 instance.

Use the Lambda target type to invoke a serverless function directly from the ALB without an API Gateway.

---

## Part 6: Health Checks

A **health check** (what this means: periodic requests the ALB sends to each target to verify it can serve traffic before routing real requests to it) runs continuously in the background.

Configurable settings include: protocol, path (for HTTP), port, healthy threshold, unhealthy threshold, timeout, and interval.

The **healthy threshold** (what this means: the number of consecutive successful checks required before a target is marked healthy and receives traffic) is typically 2-3.

The **unhealthy threshold** (what this means: the number of consecutive failed checks required before a target is marked unhealthy and removed from rotation) is typically 2-3.

When a target fails its health check: the ALB marks it unhealthy, stops sending new requests to it, and the remaining healthy targets absorb the traffic until the failing target recovers or is replaced.

**Deregistration delay** (what this means: a waiting period after a target is deregistered during which the ALB finishes in-flight requests before fully removing the target) defaults to 300 seconds.

During deployments, connection draining ensures users mid-request are not abruptly disconnected when you replace instances with a new version.

If your health check path is `/health` but the app only responds on `/`, the health check receives a 404, the target is marked unhealthy, and the ALB stops sending traffic to it even though the app is working fine.

---

## Part 7: SSL/TLS on Load Balancers

**SSL/TLS termination** (what this means: the load balancer decrypts HTTPS traffic from the client, then communicates with backends over plain HTTP, so your app servers never handle encryption) offloads the CPU cost of encryption.

Terminating at the load balancer means your backend instances do not need certificates or encryption logic, reducing their CPU load and simplifying certificate management.

**ACM** (what this means: AWS Certificate Manager - a service that provisions, renews, and manages SSL/TLS certificates for use with AWS services) handles renewals automatically at no cost.

Request a certificate in ACM, validate domain ownership via DNS or email, then attach the certificate to your ALB's HTTPS listener.

**SNI** (what this means: Server Name Indication - a TLS extension where the client tells the server which hostname it is connecting to before the handshake completes, allowing one IP to serve multiple certificates) lets you host multiple domains on a single ALB.

The ALB reads the SNI hostname in the TLS handshake and selects the matching certificate for that domain.

Both ALB and NLB support SNI.

Add a listener rule on port 80 with the action "Redirect to HTTPS" - the ALB sends a 301/302 redirect to the client automatically.

---

## Part 8: Sticky Sessions

**Session stickiness** (what this means: a load balancer feature that binds a user's session to one specific backend instance so all their requests go to the same server) is also called session affinity.

It solves the problem of stateful applications that store session data locally on the server - without stickiness, a user might hit a different instance that has no record of their session.

The two cookie types are: **LB-generated cookie** (the ALB creates and manages it, named `AWSALB`) and **application-based cookie** (your app creates its own cookie and the ALB uses it for routing).

Stickiness can overload certain instances because users are pinned to them regardless of current server load.

The better alternative is to store session state in a shared, external store such as ElastiCache (Redis) or DynamoDB so any backend instance can serve any user.

---

## Part 9: Cross-Zone Load Balancing

**Cross-zone load balancing** (what this means: each load balancer node distributes traffic evenly across all registered targets in all AZs, not just the targets in its own AZ) prevents traffic imbalances caused by unequal instance counts per AZ.

Without cross-zone: AZ-A's 2 instances each get 25% of traffic, AZ-B's 8 instances each get 6.25%. The AZ-A instances are overloaded.

With cross-zone enabled: all 10 instances share traffic equally at 10% each, regardless of which AZ they are in.

Cross-zone load balancing is enabled by default on ALB and there is no charge for it.

Cross-zone is disabled by default on NLB, and enabling it incurs inter-AZ data transfer charges.

---

## Part 10: Security Group Chain for Load Balancers

Yes, an ALB needs its own security group separate from the backend instances.

The ALB security group should allow inbound HTTP (port 80) and HTTPS (port 443) from `0.0.0.0/0` (the internet).

The backend EC2 security group should allow inbound traffic only from the ALB's security group ID as the source.

Referencing the ALB security group instead of `0.0.0.0/0` means only the ALB can reach your instances - users cannot bypass the load balancer and connect directly to your EC2s.

---

## Part 11: Why Auto Scaling Exists

Auto Scaling solves the problem of mismatched capacity - having too few instances during peak load or paying for idle instances during low traffic.

Without Auto Scaling, a traffic spike exhausts your fixed instance count, causing slow responses or downtime.

Without Auto Scaling, overnight low traffic means you are paying for instances running at near-zero utilisation.

Auto Scaling works with a load balancer by registering new instances into the target group automatically so the load balancer can send them traffic immediately.

---

## Part 12: Launch Templates

A **Launch Template** (what this means: a reusable configuration that defines exactly how new EC2 instances should be created, so Auto Scaling can launch identical instances without manual input) is the blueprint for your ASG's instances.

A Launch Template contains: AMI ID, instance type, key pair, security groups, IAM role, user data script, storage configuration, and network settings.

A **Launch Configuration** (what this means: the older, deprecated predecessor to Launch Templates - same purpose but immutable and with fewer features) cannot be updated after creation. Launch Templates are versioned and can be modified.

Use Launch Templates - AWS recommends them, they are required for newer features like mixed instance types and Spot instance support.

---

## Part 13: Auto Scaling Groups

An **Auto Scaling Group** (what this means: a group of EC2 instances managed together so AWS can automatically add or remove instances based on demand or health) is the core of Auto Scaling.

**Minimum capacity** (what this means: the floor - the ASG will never reduce instance count below this number) ensures your app always has baseline capacity.

**Maximum capacity** (what this means: the ceiling - the ASG will never exceed this instance count) controls your maximum spend.

**Desired capacity** (what this means: the target number of instances the ASG tries to maintain at all times) is what the ASG actively works toward.

If desired is 2 and you terminate one instance manually, the ASG detects the count has dropped below desired and automatically launches a replacement to restore it to 2.

You configure the ASG with a list of subnets (and therefore AZs) to launch into - the ASG distributes instances across them for high availability.

You attach an ASG to a load balancer's target group - newly launched instances register themselves automatically and deregister on termination.

---

## Part 14: ASG Health Checks

An ASG can use EC2 health checks (default) or ELB health checks.

EC2 health checks only verify the instance is running (not stopped/terminated). ELB health checks use the load balancer's application-level check, which also verifies your app is responding correctly.

You should use ELB health checks when behind a load balancer because an instance might pass the EC2 check (it is running) while your application is crashed - ELB health checks catch this case.

The **health check grace period** (what this means: a delay after launch during which the ASG ignores health check failures, giving the instance time to boot and start the app before being judged unhealthy) prevents premature termination.

If instances take 90 seconds to boot but the grace period is 60 seconds, the ASG evaluates health before the app is ready, marks instances unhealthy, terminates them, and enters a launch-terminate loop.

---

## Part 15: Scaling Policies - Target Tracking

**Dynamic scaling** (what this means: automatically adjusting instance count in real time in response to changing metrics like CPU usage) reacts to actual load rather than a schedule.

**Scaling out** means adding instances; **scaling in** means removing instances.

A **target tracking scaling policy** (what this means: you set a target metric value and the ASG automatically adjusts instance count to keep the metric at that value, similar to a thermostat) is the simplest policy type to configure.

Example: set a target of 50% average CPU utilisation - if CPU rises above 50%, the ASG adds instances; if it drops below, the ASG removes them.

Predefined metrics you can use: `ASGAverageCPUUtilization`, `ALBRequestCountPerTarget`, `ASGAverageNetworkIn`, and `ASGAverageNetworkOut`.

Target tracking is the recommended starting point because it requires no manual threshold math - you just declare the desired state and the policy manages the math for you.

---

## Part 16: Scaling Policies - Step and Simple

**Step scaling** (what this means: a policy that scales by different amounts depending on how far the metric breaches a threshold - larger breaches trigger larger capacity changes) gives you fine-grained control over scaling behaviour.

Step scaling is manually defined with specific thresholds and step sizes, unlike target tracking which calculates adjustments automatically.

Example: if CPU is 60-80%, add 1 instance; if CPU is 80-100%, add 3 instances; if CPU drops below 40%, remove 1 instance.

**Simple scaling** (what this means: an older policy type that adds or removes a fixed number of instances when a single CloudWatch alarm triggers, then waits for a cooldown before acting again) is the most basic form of scaling.

Simple scaling is worse than step scaling because it waits for a full cooldown after each action, making it slow to respond to rapidly changing load, and it only reacts at a single threshold.

---

## Part 17: Scaling Policies - Scheduled and Predictive

**Scheduled scaling** (what this means: pre-configured capacity changes that happen at specific times you define, independent of real-time metrics) suits predictable traffic patterns.

Example: increase desired capacity to 10 every weekday at 08:00 and reduce it to 2 at 20:00 for a business application used only during office hours.

**Predictive scaling** (what this means: AWS analyses your historical traffic patterns with machine learning and proactively scales capacity in advance of predicted demand spikes) scales before the load arrives rather than reacting to it.

Predictive scaling examines your ASG's historical metric data over the past two weeks and forecasts future load to schedule capacity changes ahead of time.

Yes, you can combine multiple policy types on the same ASG - for example, predictive scaling for known patterns plus target tracking as a safety net for unexpected spikes.

---

## Part 18: Cooldown Periods

A **cooldown period** (what this means: a pause after a scaling action during which the ASG ignores new scaling triggers, giving new instances time to start handling traffic before another change is made) prevents thrashing.

Without a cooldown (or with one too short), the ASG may launch or terminate multiple waves of instances before the first wave has started serving traffic, causing instability.

The default cooldown period is 300 seconds (5 minutes).

**Scale-in protection** (what this means: a flag you can set on individual instances to prevent the ASG from terminating them during a scale-in event) is useful for instances running long-running jobs you do not want interrupted.

---

## Part 19: Instance Refresh

**ASG instance refresh** (what this means: a rolling replacement of all instances in the ASG to apply an updated Launch Template - for example, a new AMI - without taking down the whole group) automates blue/green-style deployments within a single ASG.

Use it when you update your AMI (e.g., OS patch, new application version) and need to roll out the change to every running instance without manual intervention.

The **minimum healthy percentage** (what this means: the floor of healthy instances that must remain in service during the refresh - for example, 80% means the ASG replaces at most 20% of instances at a time) controls the blast radius of a bad deployment.

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

---

