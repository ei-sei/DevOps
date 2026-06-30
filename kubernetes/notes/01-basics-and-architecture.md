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

Clusters, nodes and pods at a glance

![cluster,nodes,pods](https://media.licdn.com/dms/image/v2/D4D22AQEpC2IL_L862g/feedshare-image-high-res/B4DZp9FQnaGgAo-/0/1763035123308?e=1784160000&v=beta&t=8znSVVU2QiVsRwzm5lCUx16XmcOOGDy7c-b8YTWwa_Y)

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

## Key Terminology

| Term | Definition |
|------|------------|
| **Cluster** | A set of machines (nodes) that Kubernetes manages as a single system. |
| **Node** | A single machine (physical or virtual) in the cluster. Can be a control plane node or a worker node. |
| **Pod** | The smallest deployable unit in Kubernetes - one or more tightly coupled containers that share networking and storage. |
| **Container Runtime** | The software that actually runs containers on a node (e.g. containerd, CRI-O). |
| **Control Plane** | The set of components that make cluster-wide decisions: API server, etcd, scheduler, and controller manager. |
| **Worker Node** | A node that runs your application pods. Hosts kubelet, kube-proxy, and the container runtime. |
| **API Server** | The front door of the cluster - all `kubectl` commands and internal components communicate through it. |
| **etcd** | A distributed key-value store that holds all cluster state and configuration. |
| **Scheduler** | Watches for new pods with no assigned node and picks the best node to run them on. |
| **Controller Manager** | Runs control loops that reconcile actual cluster state with the desired state declared in manifests. |
| **kubelet** | An agent on every worker node that ensures the containers described in a pod spec are running and healthy. |
| **kube-proxy** | Maintains network rules on each node so traffic can reach the right pod regardless of which node it lands on. |
| **Namespace** | A logical partition within a cluster used to isolate resources by team, environment, or application. |
| **Manifest / Spec** | A YAML (or JSON) file that declaratively describes a Kubernetes resource (e.g. a Pod or Deployment). |
| **kubectl** | The command-line tool used to interact with the Kubernetes API server to inspect and manage cluster resources. |
| **Kind** | Kubernetes IN Docker - runs a full multi-node cluster locally using Docker containers as nodes, for dev/testing. |
| **CRI** | Container Runtime Interface - the standard API Kubernetes uses to communicate with any compliant container runtime. |

---

## Getting Started: Installing Kind & Creating Your First Cluster

### What is Kind, briefly

Kind (Kubernetes IN Docker) runs each cluster "node" as a Docker container instead of a VM, so a full multi-node cluster comes up in seconds on a single machine. It's built for local development and CI, not for running production workloads.

### Prerequisites

- **Docker** installed and running - Kind's nodes are Docker containers, so Docker has to be up first.
- **kubectl** installed - Kind only creates/destroys the cluster; kubectl is what you actually use to talk to it.

```bash
# Confirm Docker is running
docker ps

# Install kubectl (Fedora)
sudo dnf install kubectl
kubectl version --client
```

### Installing Kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

### Creating your first cluster

A plain `kind create cluster` gives you a single all-in-one node, which hides the control-plane/worker split covered in Part 5. Use a config file instead to get a real multi-node layout:

`kind-config.yml`
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

```bash
kind create cluster --name dev --config lab/kind-config.yml
```

### Verifying the cluster

```bash
kubectl cluster-info --context kind-dev
kubectl get nodes
```

`kubectl get nodes` should list three nodes - one `control-plane` and two `worker` - confirming the multi-node setup actually took effect.

### Tearing it down

```bash
kind delete cluster --name dev
```
