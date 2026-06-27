# 1. K8s Basics, Architecture & Setup

---

## Part 1: Recap of Containers

What problem do containers solve?
> Containers package an application with its dependencies into a single portable unit, so it runs the same way regardless of the host machine - solving "it works on my machine" inconsistency.

What is the difference between a container and a virtual machine?
> A VM virtualises an entire machine, including its own OS kernel, making it heavier and slower to start. A container shares the host's kernel and only packages the application and its dependencies, making it lightweight and fast to start.

Why does sharing the kernel matter?
> It means containers start in seconds rather than minutes, and many containers can run on one host without each needing its own full OS - far better resource efficiency than running the same workload in separate VMs.

---

## Part 2: The Problem Kubernetes Solves

What problem appears once you have more than a handful of containers?
> Running a few containers manually with `docker run` is fine, but at scale you need to decide which host runs which container, restart failed containers, scale up under load, and route traffic to healthy instances - none of which Docker alone manages across multiple machines.

What is container orchestration?
> Container orchestration is the automated management of where containers run, how many copies run, how they recover from failure, how they discover each other, and how they scale - across a cluster of machines rather than a single host.

---

## Part 3: What is Kubernetes and Why

What is Kubernetes?
> Kubernetes (K8s) is an open-source container orchestration platform that automates deploying, scaling, healing, and networking containerised applications across a cluster of machines.

Why "K8s"?
> "K8s" is a numeronym - K, 8 letters, then s - shortening "Kubernetes" the same way "i18n" shortens "internationalization."

What does Kubernetes actually do for you that plain Docker doesn't?
> It schedules containers onto available machines automatically, restarts or replaces containers that crash, scales the number of running copies up or down, gives containers a stable way to find each other regardless of which machine they land on, and rolls out updates without downtime.

When should you not use Kubernetes?
> For a single small application, a side project, or a team without the operational capacity to run a cluster, Kubernetes adds significant complexity and overhead for little benefit - a single server with Docker Compose, or a managed PaaS, is often the better choice until you actually need orchestration at scale.

---

## Part 4: How Containers Run in Kubernetes

Does Kubernetes run containers directly?
> No - Kubernetes does not run containers itself. It delegates that job to a **container runtime** installed on each node, and Kubernetes just tells the runtime what to run.

What is the Container Runtime Interface (CRI)?
> The CRI is the standard interface Kubernetes uses to talk to any compliant container runtime, so Kubernetes itself doesn't need to know the specifics of any one runtime implementation.

What are examples of container runtimes in the current landscape?
> **containerd** (the most widely used, originally extracted from Docker) and **CRI-O** (built specifically for Kubernetes) are the two dominant CRI-compliant runtimes today.

Why isn't Docker itself used as the runtime anymore?
> Kubernetes deprecated direct Docker support (dockershim) in favour of CRI-compliant runtimes like containerd - notably, containerd is the same runtime Docker uses underneath, so the actual container execution layer didn't really change, just the integration path.

---

## Part 5: Kubernetes Architecture

![architecture](https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg)

What are the two broad categories of machines in a Kubernetes cluster?
> **Control plane nodes**, which make cluster-wide decisions, and **worker nodes**, which actually run your application containers.

What runs on the control plane?
> The **API server** (the front door for all cluster communication), **etcd** (the cluster's key-value store holding all state), the **scheduler** (decides which node a new pod runs on), and the **controller manager** (runs control loops that keep actual state matching desired state).

What runs on each worker node?
> The **kubelet** (an agent that talks to the API server and ensures containers are running as instructed), the **container runtime** (actually runs the containers), and **kube-proxy** (handles networking rules so traffic reaches the right pod).

How does a typical request flow through the architecture?
> You send a request to the API server (e.g. via `kubectl`), it's persisted in etcd, the scheduler assigns it to a node, and that node's kubelet instructs the container runtime to start the container.

---

## Part 6: Local Clusters with Kind

What is Kind?
> **Kind** (Kubernetes IN Docker) runs a full Kubernetes cluster using Docker containers as the "nodes," making it fast and lightweight to spin up a local multi-node cluster for learning or testing.

How does Kind differ from Minikube?
> Minikube typically runs a cluster inside a single VM (or container) and is geared toward a simple single-node experience. Kind runs each node as its own Docker container, making it easy to simulate multi-node clusters locally and is popular for CI pipelines that need a throwaway cluster.

What do you need installed before using Kind?
> Docker (or another supported container engine) must already be running, since Kind's "nodes" are themselves containers.

How do you create and verify a Kind cluster?
> `kind create cluster` spins up a cluster, and `kubectl cluster-info --context kind-kind` (or `kubectl get nodes`) confirms it's up and the control plane is reachable.

---

## Part 7: Namespaces

What is a namespace in Kubernetes?
> A namespace is a way to logically divide a single cluster into separate virtual sub-clusters, so resources for different teams, environments, or applications can be isolated from each other within the same physical cluster.

What namespaces exist by default?
> `default` (where resources go if no namespace is specified), `kube-system` (cluster-internal components), `kube-public`, and `kube-node-lease`.

Why use namespaces instead of separate clusters?
> Namespaces give logical isolation (naming, access control via RBAC, resource quotas) without the operational overhead of running and maintaining multiple physical clusters.

Can resources in different namespaces see each other?
> By default most resources are scoped to their namespace, but they can still reach each other over the network using a fully qualified DNS name that includes the namespace.

---

## Part 8: Lab - Touring the Cluster

What does "touring the cluster" with the Kubernetes Dashboard or `kubectl` typically involve?
> Listing nodes and their status, listing the namespaces that exist by default, inspecting what's running in `kube-system`, and confirming the control plane components are healthy - building a mental map of the cluster before deploying anything of your own.

What is the fastest way to sanity-check a new cluster is working?
> `kubectl get nodes` to confirm node status is `Ready`, then `kubectl get pods -A` to see every pod running across all namespaces, including the control plane's own components if running as pods (common in Kind).

---

## What's Missing From This Module

A few foundational pieces aren't in this list and are worth flagging before you move on, since later topics usually assume them:

- **Pods** - the most basic deployable unit in Kubernetes isn't mentioned at all yet. Architecture and namespaces make more sense once you know a Pod is what actually gets scheduled onto a node.
- **kubectl basics & kubeconfig** - the lab assumes you can already run `kubectl` against the right cluster, but how `kubectl` finds and authenticates to a cluster (`~/.kube/config`, contexts) isn't covered as its own topic.
- **Minikube** - your branch README mentions both Minikube and Kind, but this module only covers Kind. Worth a quick comparison note once you've used Kind, even if you primarily stick with Kind going forward.
- **YAML manifests / declarative config** - "how containers run in K8s" is covered, but not yet *how you tell it* what to run (i.e. writing a Pod or Deployment manifest) - likely coming in the next module, but worth checking it's not skipped entirely.

---

## Commands to Learn

```bash
# Create a local cluster with Kind
kind create cluster --name dev
```

```bash
# Confirm the cluster is reachable and control plane is up
kubectl cluster-info --context kind-dev
```

```bash
# Check node status
kubectl get nodes
```

```bash
# List every pod across all namespaces
kubectl get pods -A
```

```bash
# List all namespaces
kubectl get namespaces
```

```bash
# Tear down the Kind cluster
kind delete cluster --name dev
```
