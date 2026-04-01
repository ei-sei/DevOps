# 11. Content Delivery with CloudFront

---

## Part 1: What is a CDN

What is a CDN?
> A content Delivery Network is a globally distributed network of servers that stores copies of your content close to users around the world.

What problem does a CDN solve?
> It eliminates the latency (delay) caused by users having to fetch content from a single, far-away origin server.

How does serving content from an edge location improve performance?
> Instead of your requests travelling across the globe to the origin server, it hits a nearby edge server (a CDN node close to you), so the round-trip is milliseconds instead of seconds.

What is the difference between a cache hit and a cache miss?
> A cache hit means the edge server already has a stored copy of the file and serves it instantly; a cache miss means it doesn't, so it fetches the file from the origin server first, then caches it for future requests.

When would you NOT use a CDN?
> Avoid a CDN for highly dynamic or personalised content (like real-time dashboards or user-specific API responses) where acting would serve stale or wrong data to users.

---

## Part 2: CloudFront Basics

What is CloudFront?
> CloudFront is AWS's CDN service that distributes your content through a global network of servers to deliver it faster to users.

What is an edge location?
> An edge location is a small AWS data centre situated close to end users where CloudFront caches and serves your content with minimal latency.

What is a regional edge cache?
> A regional edge cache is a larger, mid-tier CloudFront server between your origin and the edge locations that holds content longer and serves as a backstop when an edge location doesn't have a cached copy.

What is the difference between an edge location and a regional edge cache?
> Edge locations are the frontline servers closest to users with smaller, shorter-lived caches; regional edge caches sit behind them with larger, longer-lived caches to reduce how often requests have to travel all the way back to your origin.

---

## Part 3: Distributions

What is a CloudFront distribution?
> A CloudFront distribution is the configuration unit that tells CloudFront where your content lives (the origin) and how to cache and deliver it to users.

What domain name does a new distribution get?
> Every new distribution gets an auto-generated domain like `d1234abcd.cloudfront.net`

How do you use a custom domain with CloudFront?
> You add your custom domain as an "alternate domain name" (CNAME) in the distribution, then create a DNS record pointing your domain to the CloudFront distribution URL

How long does it take to deploy or update a distribution?
> Deploying a new distribution or pushing changes typically takes 5-15 minutes to propagate across all edge locations worldwide.

---

## Part 4: Origins

What is an origin?
> An origin is the source server where CloudFront fetches your content when it doesn't have a cached copy at the edge.

What types of origins can CloudFront use?
> CloudFront can use S3 buckets, Application Load Balancers, EC2 instances, Lambda Function URLs, API Gateway, or any public HTTP/HTTPS server as an origin.

What is the difference between an S3 origin and a custom origin?
> An S3 origin is a native AWS integration with extra features like Origin Access Control (restricting bucket access to CloudFront only), while a custom origin is any HTTP/HTTPS endpoint that CloudFront treats as a generic web server.

What is an origin group? What is it used for?
> An origin group is a set of two origins (primary + fallback) used to provide high availability - if the primary origin fails, CloudFront automatically retries the request against the fallback.

How does origin failover work?
> CloudFront sends the request to the primary origin, and if it returns a failure status code (like 500 or 503), CloudFront automatically re-sends the same request to the secondary origin in the group.

---

## Part 5: Cache Behaviours

What is a cache behaviour?
> A cache behaviour is a rule in your CloudFront distribution that defines how to handle requests matching a specific URL path pattern - things like TTL, allowed HTTP methods, and which origin to forward to 

What is the default cache behaviour?
> The default cache behaviour is the catch-all rule (matching /*) that applies to any request that doesn't match a more specific path pattern.

How do path patterns work? Give an example with /api/* and /*.
> CloudFront matches the most specific pattern first, so a request to `/api/users` would hit the `/api/*` behaviour (e.g. no caching, forward to your backend), while a request to `/image/logo.png` falls through to `/*` (e.g. aggressive caching from S3)

What determines the cache key?
> The cache key is the unique identifier CloudFront uses to look up a cached response, made up of the URL path plus any headers, query strings, or cookies you explicitly include in your cache policy.

What is a cache policy?
> A cache policy is a reusable CloudFront config that controls what goes into the cache key and how long objects are cached (TTL - Time To Live)

What is an origin request policy? How is it different from a cache policy?
> An origin request policy controls what headers, cookies, and query string get forwarded to your origin on a cache miss, separate from the cache policy, so you can pass extra context to your origin without those values polluting your cache key.

---

## Part 6: TTL and Cache Invalidation

What is TTL in CloudFront?
> Time To Live is how long CloudFront keeps a cached copy of your content at the edge before checking the origin for a fresh version.

What is the difference between default TTL, minimum TTL, and maximum TTL?
> - Default TTL is used when the origin sends no cache headers
> - Minimum TTL is the floor CloudFront will never cache shorter than
> - Maximum TTL is the ceiling CloudFront will never cache longer than, regardless of what the origin says.

How do origin Cache-Control headers interact with CloudFront TTL?
> If your origin sends a `Cache-Control: max-age=3600` header, CloudFront uses that value - but only if it falls within your configured minimum and maximum TTL bounds.

What is cache invalidation?
> Cache invalidation is forcing CloudFront to immediately discard a cached file so the next request fetches a fresh copy from the origin.

How do you invalidate the cache?
> Go to your distribution in the CloudFront console, open the invalidations tab, click Create invalidation, and enter the path(s) you want to purge.

What does invalidating "/*" do?
> It immediately purges every cached file across all edge locations for that distribution, forcing all subsequent requests to go back to the origin.

Why is versioned file naming (app.v2.js) better than invalidation?
> Invalidation costs money after 1,000 paths/month and takes time to propagate, whereas versioned filenames mean the old and the new file coexist in cache simultaneously - old users get `app.v1.js` and new deploys serve `app.v2.js` instantly with no purge needed.

---

## Part 7: Origin Access Control (OAC)

What problem does OAC solve?
> OAC ensures users can only access your S3 content through CloudFront, preventing them from bypassing your CDN and hitting the S3 bucket directly.

Without OAC, what can users do that you might not want?
> They can access your files directly via the S3 URL, bypassing CloudFront entirely - skipping your cache, your security policies, and potentially exposing content you intended to restrict

What is OAI (Origin Access Identity)? Why is it legacy?
> OAI was the original CloudFront-to-S3 authentication method using a special CloudFront "user" identity, but it's legacy because it doesn't support newer AWS features like SSE-KMS encryption or granular IAM conditions that OAC provides.

What is OAC (Origin Access Control)? What improvements does it have over OAI?
> OAC is the modern replacement for AOI that uses IAM-based request signing (SigV4) to authenticate CloudFront to S3, adding support for SSE-KMS encrypted buckets, all S3 regions, and strong security controls.

How does the S3 bucket policy need to be configured for OAC?
> The bucket must be private (block all public access), and you add a policy that grants `s3:GetObject` permission specifically to the CloudFront service principal (`cloudfront.amazonaws.com`) with a condition restricting it to your specific distribution ARN.

---

## Part 8: SSL/TLS with CloudFront

What certificate does a new CloudFront distribution use by default?
> A new distribution uses the default CloudFront certificate, which only covers the `*.cloudfront.net` domain.

How do you use a custom SSL certificate with CloudFront?
> Request or import a certificate in AWS Certificate Manager (ACM), then select it in your distribution's setting under "Custom SSL certificate"

Why must the ACM certificate be in us-east-1?
> CloudFront is a global service that only reads ACM certificates from `us-east-1` (North Virginia) - certificates in any other region simply won't appear as an option

What is SNI (Server Name Indication)?
> SNI is a TLS extension that lets the client tell the server which domain it's connecting to during the handshake, allowing one server/IP to host multiple SSL certificates without needing a dedicated IP per domain.

How do you enforce HTTPS for all users?
> Set the viewer protocol policy to "Redirect HTTP to HTTPS" so any plain HTTP request is automatically redirected to the secure version

What is the viewer protocol policy?
> The viewer protocol policy is a per-cached behaviour setting that controls whether CloudFront allows HTTP only, HTTPS only, or redirects HTTP to HTTPS for requests between users and CloudFront

---

## Part 9: Signed URLs and Cookies

What is a signed URL?
> A signed URL is a time-limited, cryptographically signed link that rants a specific user access to a single private CloudFront resource

What is a signed cookie?
> A signed cookie works like a signed URL but grants access to multiple restricted files at once by embedding the authorisation token in the user's browser cookie instead of the URL

When would you use a signed URL vs a signed cookie?
> Use a signed URL for a single file (e.g. a download link for on video); use a signed cookie when a user needs access to many files at once (e.g. a paid subscriber streaming an entire course)/

What is the difference between a CloudFront signed URL and an S3 pre-signed URL?
> A CloudFront signed URL grants temporary access through CloudFront's edge network (keeping S3 private behind OAC), while an S3 pre-signed URL grants temporary direct access to the S3 bucket itself - bypassing CloudFront entirely.

---

## Part 10: Lambda@Edge and CloudFront Functions

What is Lambda@Edge?
> Lambda@Edge is a full AWS Lambda functions that run at CloudFront edge locations, letting you execute complex server-side logic (up to 5-30 seconds) close to users without a regional server.

What is a CloudFront Function?
> A CloudFront Function is a lightweight JavaScript function that runs at the edge in under 1ms, designed for simple, high-volume/response manipulations.

What is the difference between them?
> CloudFront Functions are faster, cheaper, and simpler but limited to viewer events and basic JS; Lambda@Edge supports all four event types, any Node.js/Python logic, network calls, and longer execution - but costs more and is slower to invoke.

What are the four event types in CloudFront (viewer request, viewer response, origin request, origin response)?
> - Viewer request - when CloudFront receives a request from a user, before checking the cache
> - Viewer response - before CloudFront sends the response back to the user
> - Origin request - when CloudFront forwards a cache miss to the origin
> - Origin response - when CloudFront receives the response back from the origin

Which event types can CloudFront Functions handle?
> Only viewer request and viewer response

Which event types can Lambda@Edge handle?
> All four - viewer request, viewer response, origin request, and origin response.

Give three use cases for edge computing on CloudFront:
> 1. URL rewrites and redirects (e.g. `/old-page` to `/new-page`) using CloudFront Functions
> 2. A/B testing by routing a percentage of users to a different origin at the edge
> 3. Authentication - validating a JWT token before allowing access to a private resource

---

## Part 11: CloudFront vs S3 Static Website Hosting

What does S3 static website hosting give you?
> A public HTTP endpoint that serves your bucket's files as a website, with support for index documents and custom error pages.

What does CloudFront add on top of S3 hosting?
> HTTPS with a custom domain, global edge caching for lower latency, OAC to keep S3 private, security headers, and WAF integration 

Can you use HTTPS with a custom domain on S3 hosting alone?
> No - S3 static website hosting only supports HTTP; you need CloudFront with an ACM certificate to serve a custom domain over HTTPS

When is S3 hosting alone sufficient?
> When you only need a quick internal or temporary site, don't need a custom domain, and are fine with plain HTTP and a single-region endpoint

What goes wrong if you use Cloudflare in front of CloudFront with mismatched SSL settings?
> You can get an SSL handshake loop or error - for example, if Cloudflare is set to "Flexible" (sending HTTP to CloudFront) but CloudFront is set to "HTTPS only," CloudFront rejects the connection and users see a 525 or redirect loop error

---

## Part 12: AWS Global Accelerator

What is AWS Global Accelerator?
> Global Accelerator is an AWS networking service that routes user traffic through AWS's private global network to your application endpoints, reducing latency and improving availability

What problem does it solve?
>Public internet routing is unpredictable - traffic bounces through many hops with variable latency; Global Accelerator gets traffic onto AWS's fast private backbone as close to the user as possible.

How is Global Accelerator different from CloudFront?
>CloudFront is a CDN that caches content at the edge; Global Accelerator doesn't cache anything - it just accelerates the network path to your origin, making it suited for dynamic or non-cacheable traffic like APIs, gaming, or VoIP

What does Global Accelerator use instead of DNS-based routing?
> It uses **Anycast IP** - two static IPs that automatically route users to the nearest AWS edge location, bypassing DNS propagation delays entirely.

When would you use Global Accelerator instead of CloudFront?
> When you have non-cacheable dynamic traffic (e.g. TCP/UDP applications, real-time APIs, gaming), need static IPs for whitelisting, or require instant failover without DNS TTLS delays

Does Global Accelerator provide static IP addresses?
> Yes - you get two static IPv4 addresses that never change, regardless of what endpoints are behind them, which is useful for clients that whitelist IPs in firewalls

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
> Lists all CloudFront distributions in your account, showing the ID, domain name, and status (e.g. Deployed) in a table format.

```bash
# What does this do?
aws cloudfront get-distribution --id E1234567890
```
> Returns the full configuration and metadata for a specific distribution by ID, including origins, cache behaviours, and SSL settings.

```bash
# What does this do?
aws cloudfront create-invalidation --distribution-id E1234567890 \
  --paths "/*"
```
> Invalidates every cached file across all edge locations for the distribution, forcing all subsequent requests to fetch fresh content from the origin.

```bash
# What does this do?
aws cloudfront create-invalidation --distribution-id E1234567890 \
  --paths "/index.html" "/css/*"
```
> Invalidates only `index.html` and all files under `/css/`, leaving the rest of the cache untouched - more targeted and cheaper than a full `/*` invalidation.

```bash
# What does this do?
aws cloudfront list-invalidations --distribution-id E1234567890
```
> Lists all invalidation requests for a distribution, showing their IDs, status (InProgress or Completed), and when they were created.

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