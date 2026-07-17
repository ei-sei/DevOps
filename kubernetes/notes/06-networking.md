# 6. Networking in Kubernetes

---

## Part 1: Introduction to K8s Networking

What does the Kubernetes networking model fundamentally promise?
> Every Pod gets its own IP, and every Pod can reach every other Pod directly, on any node, without NAT - see the [flat network model](03-exposing-applications-services.md#part-6-the-pod-networking-model) covered in the Services notes.

What are the four networking problems Kubernetes has to solve?
> Container-to-container communication (inside one Pod), Pod-to-Pod communication (across the cluster), Pod-to-Service communication (stable addressing), and external-to-Service communication (getting traffic in from outside).

---

## Part 2: Pod-to-Pod Communication

How do containers in the same Pod talk to each other?
> Via `localhost` - they share one network namespace, so there's no real "networking" involved, just different processes on the same virtual network stack.

How does one Pod reach another Pod on the same node?
> Through a virtual bridge on the node - each Pod gets a virtual ethernet (`veth`) pair, one end in the Pod's network namespace and one end attached to the node's bridge, letting Pods on the same node route through it directly.

How does one Pod reach a Pod on a *different* node?
> The CNI plugin sets up routes (or an overlay network) between nodes so traffic can cross the physical network boundary while each Pod keeps its own IP - the exact mechanism depends entirely on which CNI plugin is installed.

---

## Part 3: Service Discovery & DNS

How do Pods find Services without hardcoding IPs?
> Through **CoreDNS**, which runs as a cluster add-on and automatically creates a DNS record for every Service, resolvable from any Pod.

What is the DNS naming pattern for a Service?
> `<service-name>.<namespace>.svc.cluster.local` - within the same namespace, just `<service-name>` is enough to resolve it.

Where does CoreDNS itself run?
> As Pods in the `kube-system` namespace, exposed via its own Service - meaning DNS resolution itself depends on cluster networking already working correctly.

---

## Part 4: Container Network Interface (CNI)

What is CNI, in one line?
> A standard interface between Kubernetes and whatever plugin actually implements Pod networking - Kubernetes defines the networking *rules*, CNI plugins make them real.

What is a CNI plugin actually responsible for?
> Assigning each Pod an IP address, wiring up its network interface, and configuring routes so that IP is reachable from the rest of the cluster according to the flat-network rules.

When does the CNI plugin get invoked?
> By the kubelet, every time a Pod is created or removed on a node - the kubelet calls the CNI plugin to set up (or tear down) that Pod's networking before/after the Pod's containers run.

What are common CNI plugin choices?
> **Calico** (network policy enforcement, BGP routing), **Flannel** (simple overlay network, easy to set up), **Cilium** (eBPF-based, high performance, deep observability) - each implements the same Kubernetes networking contract differently.

Does Kubernetes ship with a CNI plugin by default?
> No - a cluster has no Pod networking at all until a CNI plugin is installed; this is why a fresh `kubeadm` cluster shows nodes as `NotReady` until one is applied.

---

## Part 5: Traditional Endpoints - The Problem

What is an Endpoints object?
> The original object Kubernetes used to track which Pod IPs currently back a Service - automatically kept in sync as Pods come and go.

What breaks down with Endpoints at scale?
> A Service with thousands of backing Pods means one single Endpoints object holding thousands of IPs - every single change (one Pod added or removed) requires rewriting and redistributing that entire large object to every node watching it.

---

## Part 6: The Solution - EndpointSlices

What is an EndpointSlice?
> A newer object that splits a Service's backing Pod IPs across multiple smaller objects (capped at 100 addresses each by default) instead of one giant Endpoints object.

Why does splitting into slices help?
> A change to one Pod only requires updating the one small slice it belongs to, not the entire set - dramatically reducing the amount of data propagated through the cluster on every Pod change.

Do EndpointSlices replace Endpoints entirely?
> They're the modern default that Services use automatically at scale, though the legacy Endpoints object is still created for backward compatibility - you generally don't interact with either directly.

---

## Part 7: Network Policies

What problem do NetworkPolicies solve?
> By default, every Pod can talk to every other Pod in the cluster - NetworkPolicies let you restrict that, defining exactly which traffic is allowed in and out of a set of Pods.

What does a NetworkPolicy select and restrict?
> A `podSelector` picks which Pods the policy applies to, then `ingress`/`egress` rules define what traffic is allowed in/out - anything not explicitly allowed is denied once a policy exists for a Pod.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-from-other-namespaces
spec:
  podSelector: {}
  ingress:
    - from:
        - podSelector: {}
```

Does a NetworkPolicy work without a CNI plugin supporting it?
> No - NetworkPolicy is just an API object; it has no effect unless the cluster's CNI plugin actually implements policy enforcement (e.g. Calico or Cilium do, plain Flannel does not).

---

## Part 8: Ingress Controllers

What is the difference between an Ingress and an Ingress Controller?
> **Ingress** is just the API object describing routing rules (host/path -> Service). The **Ingress Controller** is the actual running component (e.g. NGINX Ingress Controller, Traefik) that reads those rules and configures a real proxy/load balancer to implement them.

Why doesn't Ingress work out of the box on a fresh cluster?
> Like NetworkPolicy, Ingress is just an API spec - creating an Ingress object does nothing until an Ingress Controller is installed and watching for them.

How does an Ingress compare to a LoadBalancer Service?
> A LoadBalancer Service typically provisions one external load balancer per Service, which gets expensive and unwieldy with many services. An Ingress lets one entry point (and one external LB) route to many Services based on host/path rules.

---

## Part 9: North-South vs East-West Traffic

What is North-South traffic?
> Traffic entering or leaving the cluster - a client outside the cluster talking to a Service inside it, typically through an Ingress or LoadBalancer.

What is East-West traffic?
> Traffic between services *inside* the cluster - one Pod calling another Pod's Service, which stays entirely within the cluster network.

Why does this distinction matter for tooling choice?
> Ingress Controllers are built for North-South traffic (external entry). Service meshes (see [notes/03](03-exposing-applications-services.md#part-9-ingress-vs-service-mesh)) are built for East-West traffic (internal service-to-service concerns like mTLS and retries) - picking the right tool depends on which direction of traffic you're actually trying to manage.

---

## Lab: K8s & DNS

**Goal:** Confirm Service DNS resolution actually works from inside the cluster, and see what CoreDNS looks like under the hood.

```bash
# 1. Create a Deployment and expose it
kubectl create deployment web --image=nginx:latest
kubectl expose deployment web --port=80

# 2. Confirm CoreDNS is running
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

```bash
# 3. Launch a temporary Pod and resolve the Service by name
kubectl run dns-test --rm -it --image=busybox -- nslookup web
# Expect: resolves to the Service's ClusterIP
```

```bash
# 4. Resolve it by its full DNS name too
kubectl run dns-test --rm -it --image=busybox -- nslookup web.default.svc.cluster.local
```

```bash
# 5. Check the CoreDNS config directly
kubectl get configmap coredns -n kube-system -o yaml
```

```bash
# 6. Clean up
kubectl delete service web
kubectl delete deployment web
```

---

## Commands to Learn

```bash
# List Endpoints/EndpointSlices for a Service
kubectl get endpoints my-service
kubectl get endpointslices -l kubernetes.io/service-name=my-service
```

```bash
# List NetworkPolicies
kubectl get networkpolicies
```

```bash
# List Ingress resources
kubectl get ingress
```

```bash
# Check which CNI plugin a node is using (varies by install method)
kubectl get pods -n kube-system -o wide
```

```bash
# Resolve DNS from inside the cluster using a throwaway Pod
kubectl run dns-test --rm -it --image=busybox -- nslookup <service-name>
```
