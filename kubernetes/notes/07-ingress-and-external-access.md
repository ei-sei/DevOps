# 7. Ingress & External Access

*Builds on [notes/06 Part 8: Ingress Controllers](06-networking.md#part-8-ingress-controllers) - start there for the Ingress vs Ingress Controller basics.*

---

## Part 1: Multi-Service Routing (Shared Ingress)

Why route multiple Services through one Ingress instead of one LoadBalancer each?
> One external load balancer per Service gets expensive and hard to manage - a shared Ingress lets a single entry point fan out to many Services based on host or path rules.

What does host-based routing look like?
> Requests to `app1.example.com` go to one Service, `app2.example.com` to another - defined as separate `rules` entries in the same Ingress, each matching on `host`.

What does path-based routing look like?
> Requests to `/api` route to the API Service, `/` to the frontend Service - defined via `path` and `pathType` under a single host's rules.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shared-ingress
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

---

## Part 2: Public vs Private Ingress

What's the difference between a public and private Ingress?
> A **public** Ingress is reachable from the internet via an external load balancer. A **private** Ingress is only reachable from inside the VPC/private network, using an internal load balancer.

Why would you want a private Ingress at all?
> For internal tools, admin dashboards, or service-to-service traffic that should never be internet-exposed - keeping it off the public internet is safer than relying on auth alone.

How do you typically configure which one you get?
> Via a cloud-specific annotation on the Ingress or its Ingress Controller Service (e.g. AWS's `service.beta.kubernetes.io/aws-load-balancer-internal: "true"`) that tells the underlying cloud load balancer to provision as internal rather than internet-facing.

Can one cluster run both?
> Yes - a common pattern is two separate Ingress Controllers (or one controller with two IngressClasses), one fronted by a public load balancer and one by an internal one, and each Ingress object picks which it uses via `ingressClassName`.

---

## Part 3: Cert-Manager in Action (Automation)

What problem does cert-manager solve?
> Manually requesting, renewing, and installing TLS certificates for every Ingress hostname doesn't scale - cert-manager automates issuing and renewing certificates so HTTPS "just works."

What are the two core cert-manager objects?
> An **Issuer** (or **ClusterIssuer** for cluster-wide use) defines *where* certificates come from - e.g. Let's Encrypt via ACME. A **Certificate** requests a specific cert for a specific hostname, referencing that Issuer.

How does cert-manager typically prove domain ownership to Let's Encrypt?
> Via the **ACME HTTP-01** challenge (serving a token at a specific URL the Ingress routes to) or **DNS-01** challenge (creating a TXT record via a DNS provider API) - DNS-01 also supports wildcard certs, HTTP-01 doesn't.

How does this connect to an Ingress in practice?
> Adding `cert-manager.io/cluster-issuer: <name>` as an annotation on an Ingress is usually enough - cert-manager watches for that annotation, requests the cert automatically, and stores it as a Secret the Ingress Controller then uses for TLS termination.

What happens as a certificate nears expiry?
> cert-manager automatically renews it well before expiry and updates the underlying Secret - no manual intervention needed once it's set up correctly.

---

## Part 4: Automating DNS with ExternalDNS

What problem does ExternalDNS solve?
> Manually creating a DNS record every time you add an Ingress hostname or LoadBalancer Service is error-prone and easy to forget - ExternalDNS automates keeping DNS in sync with what's actually running in the cluster.

How does ExternalDNS work?
> It watches Ingress and Service objects for hostnames, then creates/updates/deletes matching records in a real DNS provider (Route53, Cloudflare, Google Cloud DNS, etc.) via that provider's API.

How does it know which hostnames to manage?
> From the `host` field on an Ingress, or an explicit `external-dns.alpha.kubernetes.io/hostname` annotation on a Service - it reconciles the DNS provider's records to match what it observes in the cluster.

How does ExternalDNS complement cert-manager?
> Together they close the full loop - ExternalDNS makes the hostname resolve to your Ingress, cert-manager gets that hostname a valid TLS cert, and the Ingress Controller serves it - all without manually touching a DNS console or CA.

---

## Part 5: Multi-Cluster / Regional Access

Why would a single cluster's Ingress not be enough?
> For availability across regions, or to keep traffic close to users globally, one cluster in one region becomes a single point of failure and adds latency for distant users.

What is the general pattern for multi-cluster access?
> A global load balancer (e.g. AWS Global Accelerator, Cloudflare, GCP's multi-cluster Ingress) sits in front of multiple regional clusters, routing users to the nearest or healthiest one, with each cluster running its own Ingress underneath.

What's the difference between this and just having replicas across AZs in one region?
> AZ-level replicas protect against a single data center failure, but the whole region is still one geographic point of failure - multi-cluster/regional setups protect against a full region going down and reduce latency for geographically distant users.

---

## Part 6: Common Pitfalls & Debugging

| Symptom | Likely cause |
|---|---|
| Ingress created but nothing happens | No Ingress Controller installed, or `ingressClassName` doesn't match any installed controller |
| 404 from the Ingress Controller itself | Path/host rule doesn't match the request, or `pathType` mismatch (`Exact` vs `Prefix`) |
| 502/503 from the Ingress Controller | Backend Service has no healthy Endpoints - check `kubectl get endpoints` |
| TLS cert not issuing | cert-manager Issuer misconfigured, ACME challenge failing (check DNS propagation for DNS-01, or Ingress routing for HTTP-01) |
| DNS not resolving to the Ingress | ExternalDNS not running, missing IAM/API permissions to the DNS provider, or hostname doesn't match what it's watching for |
| Works via ClusterIP but not through Ingress | Ingress Controller's own Service (often a LoadBalancer) misconfigured or not provisioned yet |

What's the first command to run when an Ingress isn't working?
> `kubectl describe ingress <name>` - it surfaces most misconfigurations directly in its Events section, including backend/service resolution failures.

---

## Part 7: Ingress to Gateway API

Why is the Gateway API replacing Ingress?
> Ingress's spec is intentionally minimal and vendor extensions live in annotations (non-portable, inconsistent across controllers). Gateway API is a newer, more expressive standard built to be portable across implementations without relying on custom annotations.

What are the core Gateway API objects?
> **GatewayClass** (like IngressClass - which controller implements it), **Gateway** (the actual listener - ports, hosts, TLS), and **HTTPRoute** (routing rules - similar to Ingress paths/hosts, but far more expressive).

What can Gateway API express that Ingress can't natively?
> Traffic splitting/weighting between backends, header-based routing, request/response modification, and clean support for non-HTTP protocols (TCP, gRPC) - all as first-class spec fields instead of controller-specific annotations.

Should you use Gateway API instead of Ingress today?
> Ingress is still extremely widely used and well understood, but Gateway API is the direction the ecosystem is moving - worth learning conceptually, but Ingress remains the safer default until a project specifically needs what Gateway API offers.

---

## Commands to Learn

```bash
# List Ingress resources and their hosts/addresses
kubectl get ingress
```

```bash
# Full details and events for an Ingress - the first debugging step
kubectl describe ingress my-ingress
```

```bash
# Check cert-manager Certificate status
kubectl get certificate
kubectl describe certificate my-cert
```

```bash
# Check a cert-manager Issuer/ClusterIssuer is ready
kubectl get clusterissuer
```

```bash
# Check ExternalDNS logs for sync activity/errors
kubectl logs -l app.kubernetes.io/name=external-dns
```

```bash
# List Gateway API resources
kubectl get gateway
kubectl get httproute
```
