# 11. Content Delivery with CloudFront

> Answer from memory after watching videos. Mark `???` for gaps, then go back and fill them.

---

## Part 1: What is a CDN

What is a CDN?
> 

What problem does a CDN solve?
> 

How does serving content from an edge location improve performance?
> 

What is the difference between a cache hit and a cache miss?
> 

When would you NOT use a CDN?
> 

---

## Part 2: CloudFront Basics

What is CloudFront?
> 

What is an edge location?
> 

What is a regional edge cache?
> 

What is the difference between an edge location and a regional edge cache?
> 

---

## Part 3: Distributions

What is a CloudFront distribution?
> 

What domain name does a new distribution get?
> 

How do you use a custom domain with CloudFront?
> 

How long does it take to deploy or update a distribution?
> 

---

## Part 4: Origins

What is an origin?
> 

What types of origins can CloudFront use?
> 

What is the difference between an S3 origin and a custom origin?
> 

What is an origin group? What is it used for?
> 

How does origin failover work?
> 

---

## Part 5: Cache Behaviours

What is a cache behaviour?
> 

What is the default cache behaviour?
> 

How do path patterns work? Give an example with /api/* and /*.
> 

What determines the cache key?
> 

What is a cache policy?
> 

What is an origin request policy? How is it different from a cache policy?
> 

---

## Part 6: TTL and Cache Invalidation

What is TTL in CloudFront?
> 

What is the difference between default TTL, minimum TTL, and maximum TTL?
> 

How do origin Cache-Control headers interact with CloudFront TTL?
> 

What is cache invalidation?
> 

How do you invalidate the cache?
> 

What does invalidating "/*" do?
> 

Why is versioned file naming (app.v2.js) better than invalidation?
> 

---

## Part 7: Origin Access Control (OAC)

What problem does OAC solve?
> 

Without OAC, what can users do that you might not want?
> 

What is OAI (Origin Access Identity)? Why is it legacy?
> 

What is OAC (Origin Access Control)? What improvements does it have over OAI?
> 

How does the S3 bucket policy need to be configured for OAC?
> 

---

## Part 8: SSL/TLS with CloudFront

What certificate does a new CloudFront distribution use by default?
> 

How do you use a custom SSL certificate with CloudFront?
> 

Why must the ACM certificate be in us-east-1?
> 

What is SNI (Server Name Indication)?
> 

How do you enforce HTTPS for all users?
> 

What is the viewer protocol policy?
> 

---

## Part 9: Signed URLs and Cookies

What is a signed URL?
> 

What is a signed cookie?
> 

When would you use a signed URL vs a signed cookie?
> 

What is the difference between a CloudFront signed URL and an S3 pre-signed URL?
> 

---

## Part 10: Lambda@Edge and CloudFront Functions

What is Lambda@Edge?
> 

What is a CloudFront Function?
> 

What is the difference between them?
> 

What are the four event types in CloudFront (viewer request, viewer response, origin request, origin response)?
> 

Which event types can CloudFront Functions handle?
> 

Which event types can Lambda@Edge handle?
> 

Give three use cases for edge computing on CloudFront:
> 

---

## Part 11: CloudFront vs S3 Static Website Hosting

What does S3 static website hosting give you?
> 

What does CloudFront add on top of S3 hosting?
> 

Can you use HTTPS with a custom domain on S3 hosting alone?
> 

When is S3 hosting alone sufficient?
> 

What goes wrong if you use Cloudflare in front of CloudFront with mismatched SSL settings?
> 

---

## Part 12: AWS Global Accelerator

What is AWS Global Accelerator?
>

What problem does it solve?
>

How is Global Accelerator different from CloudFront?
>

What does Global Accelerator use instead of DNS-based routing?
>

When would you use Global Accelerator instead of CloudFront?
>

Does Global Accelerator provide static IP addresses?
>

---

## Commands to Learn

```bash
# What does this do?
aws cloudfront list-distributions
```
> 

```bash
# What does this do?
aws cloudfront list-distributions \
  --query "DistributionList.Items[].[Id,DomainName,Status]" --output table
```
> 

```bash
# What does this do?
aws cloudfront get-distribution --id E1234567890
```
> 

```bash
# What does this do?
aws cloudfront create-invalidation --distribution-id E1234567890 \
  --paths "/*"
```
> 

```bash
# What does this do?
aws cloudfront create-invalidation --distribution-id E1234567890 \
  --paths "/index.html" "/css/*"
```
> 

```bash
# What does this do?
aws cloudfront list-invalidations --distribution-id E1234567890
```
> 

---

## Hands-On Tasks

- Create an S3 bucket with a static website, put CloudFront in front of it
- Set up OAC so S3 is only accessible through CloudFront
- Add a custom domain with an ACM certificate (us-east-1) and a Route 53 Alias record
- Perform a cache invalidation and verify the updated content is served
- Configure cache behaviours: /api/* to an ALB origin, /* to an S3 origin
- Create a CloudFront Function that adds security headers to responses

---

## Quick Quiz

1. How would you set up a static website with CloudFront, S3, custom domain, and HTTPS?
   > 

2. What is the difference between OAI and OAC?
   > 

3. Why is cache invalidation expensive at scale, and what is the alternative?
   > 

---

## Confidence: 🔴 🟡 🟢

**Date completed:** ___________