# 10. DNS with Route 53

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: DNS Fundamentals

What does DNS do?
> 

What is a domain name?
> 

Walk through what happens when a browser requests www.example.com:
> 

What is TTL (Time to Live)?
> 

What happens if TTL is set very high?
> 

What happens if TTL is set very low?
> 

What is DNS propagation? Why does it take time?
> 

---

## Part 2: What is Route 53

What is Route 53?
> 

What three things can Route 53 do? (registration, routing, health)
> 

Why is it called "Route 53"?
> 

---

## Part 3: Hosted Zones

What is a hosted zone?
> 

What is a public hosted zone?
> 

What is a private hosted zone? When would you use one?
> 

What records are automatically created when you create a hosted zone?
> 

Can you use Route 53 for DNS without registering the domain through AWS?
> 

How do you point a domain registered elsewhere to Route 53?
> 

---

## Part 4: Record Types

What is an A record?
> 

What is an AAAA record?
> 

What is a CNAME record?
> 

Can you use a CNAME at the zone apex (naked domain like example.com)? Why not?
> 

What is an MX record?
> 

What is a TXT record? What is it commonly used for?
> 

What is an NS record?
> 

---

## Part 5: Alias Records

What is an Alias record?
> 

How is an Alias record different from a CNAME?
> 

Can you use an Alias record at the zone apex?
> 

What AWS resources can be targets for Alias records?
> 

Do Alias queries cost money?
> 

Can you set TTL on an Alias record?
> 

Why are Alias records preferred over CNAMEs for AWS resources?
> 

---

## Part 6: Routing Policies, Simple and Weighted

What is simple routing?
> 

If a simple routing record returns multiple IPs, what does the client do?
> 

What is weighted routing?
> 

Give a use case for weighted routing:
> 

How do you send 70% of traffic to one resource and 30% to another?
> 

---

## Part 7: Routing Policies, Latency and Failover

What is latency-based routing?
> 

How does Route 53 determine which Region has the lowest latency?
> 

What is failover routing?
> 

How does failover routing work with health checks?
> 

What is the difference between the primary and secondary record in failover routing?
> 

---

## Part 8: Routing Policies, Geolocation and Multi-Value

What is geolocation routing?
> 

How is geolocation different from latency-based routing?
> 

What happens if there is no geolocation match for a user's location?
> 

What is geoproximity routing?
> 

What is multi-value routing?
> 

How is multi-value different from simple routing?
>

What is IP-based routing?
>

When would you use IP-based routing?
> 

---

## Part 9: Health Checks

What is a Route 53 health check?
> 

What protocols can health checks use?
> 

Where do health check requests come from?
> 

What happens to DNS resolution when a health check fails?
> 

Can you health check a private resource? If not, what is the workaround?
> 

What is a calculated health check?
> 

---

## Part 10: Domain Registration

Can you register domains through Route 53?
> 

Can you transfer a domain from another registrar to Route 53?
> 

What is domain lock?
> 

What is auto-renew?
> 

---

## Part 11: Route 53 Resolvers and Hybrid DNS

What is Route 53 Resolver?
>

What is an inbound endpoint? When would you use it?
>

What is an outbound endpoint? When would you use it?
>

How does Route 53 Resolver enable hybrid DNS between on-premises and AWS?
>

---

## Commands to Learn

```bash
# What does this do?
aws route53 list-hosted-zones
```
> 

```bash
# What does this do?
aws route53 list-resource-record-sets --hosted-zone-id Z1234567890
```
> 

```bash
# What does this do?
aws route53 change-resource-record-sets --hosted-zone-id Z1234567890 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "1.2.3.4"}]
      }
    }]
  }'
```
> 

```bash
# What does this do?
aws route53 create-health-check --caller-reference "hc-123" \
  --health-check-config '{
    "IPAddress": "1.2.3.4",
    "Port": 80,
    "Type": "HTTP",
    "ResourcePath": "/health"
  }'
```
> 

```bash
# What does this do?
aws route53 list-health-checks
```
> 

---

## Hands-On Tasks

- Create a public hosted zone for a domain you own
- Create an A record pointing to an EC2 instance's public IP
- Create an Alias record pointing to an ALB
- Set up a health check for your web server
- Configure failover routing between two resources
- Set up weighted routing to split traffic 80/20

---

## Quick Quiz

1. What is the difference between a CNAME and an Alias record?
   > 

2. How would you set up automatic failover to a backup site using Route 53?
   > 

3. What routing policies does Route 53 support? Give a use case for each.
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________