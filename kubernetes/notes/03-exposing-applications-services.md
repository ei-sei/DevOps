# 3. Exposing Applications: Services

---

## Part 1: Why Services Exist

What problem does a Service solve?
> Pods are mortal and get a new IP every time they're recreated - a Service gives a stable, unchanging address that automatically routes to whichever healthy Pods currently exist behind it.

How does a Service know which Pods to send traffic to?
> Via a label selector, the same mechanism Deployments and ReplicaSets use - any Pod matching the Service's selector becomes a routable endpoint.

---

## Part 2: Service Types

| Type | Accessible from | What it does |
|---|---|---|
| **ClusterIP** (default) | Inside the cluster only | Gives the Service a stable internal IP - the standard way Pods talk to each other |
| **NodePort** | Outside the cluster, via `<NodeIP>:<port>` | Opens the same static port (30000-32767) on every node, forwarding to the Service |
| **LoadBalancer** | Outside the cluster, via a cloud LB | Provisions an external cloud load balancer (e.g. AWS NLB) that routes to the Service - builds on top of NodePort/ClusterIP underneath |

Which type should you default to?
> ClusterIP, unless you specifically need external access - NodePort and LoadBalancer both still create a ClusterIP underneath.

---

## Part 3: ClusterIP in Practice

What does a minimal ClusterIP Service look like?
> ```yaml
> apiVersion: v1
> kind: Service
> metadata:
>   name: my-service
> spec:
>   selector:
>     app: my-app
>   ports:
>     - port: 80
>       targetPort: 8080
> ```

What's the difference between `port` and `targetPort`?
> `port` is what the Service itself listens on. `targetPort` is the port on the Pod it forwards traffic to - they don't have to match.

How do other Pods reach a ClusterIP Service?
> By its stable DNS name, `<service-name>.<namespace>.svc.cluster.local` (or just `<service-name>` within the same namespace) - never by tracking individual Pod IPs.

---

## Part 4: Headless Services & DNS

What is a headless Service?
> A Service with `clusterIP: None` - it skips load-balancing and cluster-IP assignment entirely, and instead returns the individual Pod IPs directly via DNS.

Why would you want individual Pod IPs instead of one load-balanced IP?
> When you need to address a specific Pod rather than "any one of them" - e.g. a StatefulSet database replica, or a client that wants to do its own load-balancing/connection logic.

What does DNS resolution look like for a headless Service?
> A normal Service's DNS name resolves to one virtual IP. A headless Service's DNS name resolves to multiple A records, one per matching Pod's real IP.

How does this connect to StatefulSets?
> Each StatefulSet Pod gets its own stable DNS name through a headless Service, e.g. `app-0.my-service.default.svc.cluster.local` - this is what lets you address `app-0` specifically instead of a random replica.

---

## Part 5: ExternalName Services

What is an ExternalName Service?
> A Service with no selector and no Pods behind it at all - it's just a DNS alias (CNAME) that redirects to an external hostname.

What is it used for?
> Referring to something outside the cluster (e.g. an external database, a legacy service, a third-party API) using an in-cluster Service name, so Pods don't need to know the real external address.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.example.com
```

---

## Part 6: The Pod Networking Model

What is the "flat network" model in Kubernetes?
> Every Pod gets its own unique IP, and every Pod can reach every other Pod directly by that IP, across any node, without NAT - the same as if they were all on one big flat network.

What are the core rules of the Kubernetes networking model?
> Pods can communicate with all other Pods without NAT, nodes can communicate with all Pods without NAT, and the IP a Pod sees itself as is the same IP everyone else sees it as.

What implements this flat network in practice?
> A CNI (Container Network Interface) plugin, such as Calico, Flannel, or Cilium - Kubernetes defines the networking model as a requirement, but relies on a CNI plugin to actually make it work.

Why does this model matter for Services?
> Because every Pod already has a routable IP, a Service is really just a stable DNS name plus a virtual IP that load-balances across a changing set of these real Pod IPs - it doesn't need any special new networking mechanism.

---

## Part 7: Why Service Meshes Exist

What problem is left over even after Services solve basic connectivity?
> Services get traffic from A to B, but give you no visibility into traffic (metrics, tracing), no fine-grained traffic control (retries, timeouts, canary splits), and no service-to-service encryption or authorization by default.

What is a service mesh?
> An infrastructure layer that handles service-to-service communication concerns - traffic management, observability, security - outside of your application code, usually by transparently intercepting traffic in and out of each Pod.

---

## Part 8: How a Service Mesh Works (Istio/Linkerd)

What is the sidecar proxy pattern in a service mesh?
> Every Pod gets an extra sidecar proxy container (e.g. Envoy for Istio) injected alongside the main application - all inbound and outbound traffic is transparently routed through this proxy instead of going directly.

What is the control plane's role?
> The control plane (e.g. `istiod`) configures every sidecar proxy with routing rules, security policy, and certificates, without the application itself knowing the mesh exists.

What capabilities does a mesh commonly add?
> Mutual TLS between services automatically, retries/timeouts/circuit breaking, traffic splitting for canary releases, and detailed metrics/tracing for every request - all without changing application code.

---

## Part 9: Ingress vs Service Mesh

What problem does each one solve?
> **Ingress** manages north-south traffic - how external traffic enters the cluster and reaches the right Service. A **service mesh** manages east-west traffic - how services talk to each other once already inside the cluster.

Do you need both?
> They solve different problems and are often used together - Ingress as the front door, a mesh for internal service-to-service concerns - though a small cluster may only need Ingress, or nothing at all if traffic patterns are simple.

When would a mesh be overkill?
> For a small number of services with simple, trusted internal communication - the operational complexity of running a mesh usually isn't worth it until you have many services needing consistent traffic policy, security, and observability.

---

## Commands to Learn

```bash
# Create a ClusterIP Service imperatively
kubectl expose deployment my-app --port=80 --target-port=8080
```

```bash
# List Services
kubectl get services
```

```bash
# Full details of a Service, including its Endpoints
kubectl describe service my-service
```

```bash
# Check which Pod IPs are currently behind a Service
kubectl get endpoints my-service
```

```bash
# Resolve a Service's DNS name from inside the cluster
kubectl run tmp-shell --rm -it --image=busybox -- nslookup my-service
```
