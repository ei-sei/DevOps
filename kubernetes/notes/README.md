# Notes

Study notes on Kubernetes, covering core concepts through scheduling, security, and observability.

## Files

| # | Topic | File |
|---|-------|------|
| 01 | Basics & Architecture | [01-basics-and-architecture.md](01-basics-and-architecture.md) |
| 02 | Running & Managing Workloads | [02-running-and-managing-workloads.md](02-running-and-managing-workloads.md) |
| 03 | Exposing Applications (Services) | [03-exposing-applications-services.md](03-exposing-applications-services.md) |
| 04 | Storage | [04-storage.md](04-storage.md) |
| 05 | Config & Secrets Management | [05-config-and-secrets-management.md](05-config-and-secrets-management.md) |
| 06 | Networking | [06-networking.md](06-networking.md) |
| 07 | Ingress & External Access | [07-ingress-and-external-access.md](07-ingress-and-external-access.md) |
| 08 | Security | [08-security.md](08-security.md) |
| 09 | Scheduling & Node Management | [09-scheduling-and-node-management.md](09-scheduling-and-node-management.md) |
| 10 | Observability Fundamentals | [10-observability-fundamentals.md](10-observability-fundamentals.md) |
| - | Cheatsheet | [cheatsheet.md](cheatsheet.md) |

## Topic Index

Every `## Part` heading across all notes files, so you can jump straight to a specific topic (e.g. PVC) without opening each file to search.

### [01 - Basics & Architecture](01-basics-and-architecture.md)
- [Recap of Containers](01-basics-and-architecture.md#part-1-recap-of-containers)
- [The Problem Kubernetes Solves](01-basics-and-architecture.md#part-2-the-problem-kubernetes-solves)
- [What is Kubernetes and Why](01-basics-and-architecture.md#part-3-what-is-kubernetes-and-why)
- [How Containers Run in Kubernetes](01-basics-and-architecture.md#part-4-how-containers-run-in-kubernetes)
- [Kubernetes Architecture](01-basics-and-architecture.md#part-5-kubernetes-architecture)
- [Local Clusters with Kind](01-basics-and-architecture.md#part-6-local-clusters-with-kind)
- [Namespaces](01-basics-and-architecture.md#part-7-namespaces)

### [02 - Running & Managing Workloads](02-running-and-managing-workloads.md)
- [Pods](02-running-and-managing-workloads.md#part-1-pods)
- [Deployments](02-running-and-managing-workloads.md#part-2-deployments)
- [ReplicaSets](02-running-and-managing-workloads.md#part-3-replicasets)
- [Pod Failure & Container Patterns](02-running-and-managing-workloads.md#part-4-pod-failure--container-patterns)
- [Quality of Service (QoS)](02-running-and-managing-workloads.md#part-5-quality-of-service-qos)
- [Probes](02-running-and-managing-workloads.md#part-6-probes)
- [Deployment Strategies](02-running-and-managing-workloads.md#part-7-deployment-strategies)
- [Resource Management](02-running-and-managing-workloads.md#part-8-resource-management)
- [Organising Resources](02-running-and-managing-workloads.md#part-9-organising-resources)
- [Other Workload Controllers](02-running-and-managing-workloads.md#part-10-other-workload-controllers)

### [03 - Exposing Applications (Services)](03-exposing-applications-services.md)
- [Why Services Exist](03-exposing-applications-services.md#part-1-why-services-exist)
- [Service Types](03-exposing-applications-services.md#part-2-service-types)
- [ClusterIP in Practice](03-exposing-applications-services.md#part-3-clusterip-in-practice)
- [Headless Services & DNS](03-exposing-applications-services.md#part-4-headless-services--dns)
- [ExternalName Services](03-exposing-applications-services.md#part-5-externalname-services)
- [The Pod Networking Model](03-exposing-applications-services.md#part-6-the-pod-networking-model)
- [Why Service Meshes Exist](03-exposing-applications-services.md#part-7-why-service-meshes-exist)
- [How a Service Mesh Works (Istio/Linkerd)](03-exposing-applications-services.md#part-8-how-a-service-mesh-works-istiolinkerd)
- [Ingress vs Service Mesh](03-exposing-applications-services.md#part-9-ingress-vs-service-mesh)

### [04 - Storage](04-storage.md)
- [Why Storage Matters](04-storage.md#part-1-why-storage-matters)
- [PersistentVolumes (PV)](04-storage.md#part-2-persistentvolumes-pv)
- [**PersistentVolumeClaims (PVC)**](04-storage.md#part-3-persistentvolumeclaims-pvc)
- [The Problem With Deployments and Storage](04-storage.md#part-4-the-problem-with-deployments-and-storage)
- [StatefulSets & Storage](04-storage.md#part-5-statefulsets--storage)
- [Dynamic Provisioning Flow](04-storage.md#part-6-dynamic-provisioning-flow)
- [Ephemeral Volumes](04-storage.md#part-7-ephemeral-volumes)
- [CSI Overview](04-storage.md#part-8-csi-overview)

### [05 - Config & Secrets Management](05-config-and-secrets-management.md)
- [ConfigMaps](05-config-and-secrets-management.md#part-1-configmaps)
- [ConfigMaps in Practice](05-config-and-secrets-management.md#part-2-configmaps-in-practice)
- [Secrets](05-config-and-secrets-management.md#part-3-secrets)
- [Using Secrets](05-config-and-secrets-management.md#part-4-using-secrets)
- [Secrets in Practice](05-config-and-secrets-management.md#part-5-secrets-in-practice)
- [The Reality of Kubernetes Secrets](05-config-and-secrets-management.md#part-6-the-reality-of-kubernetes-secrets)
- [External Secrets Operator (ESO)](05-config-and-secrets-management.md#part-7-external-secrets-operator-eso)
- [The Proper Secrets Flow](05-config-and-secrets-management.md#part-8-the-proper-secrets-flow)
- [Why We Need Sealed Secrets](05-config-and-secrets-management.md#part-9-why-we-need-sealed-secrets)
- [Sealed Secrets](05-config-and-secrets-management.md#part-10-sealed-secrets)
- [Sealed Secrets vs External Secrets](05-config-and-secrets-management.md#part-11-sealed-secrets-vs-external-secrets)

### [06 - Networking](06-networking.md)
- [Introduction to K8s Networking](06-networking.md#part-1-introduction-to-k8s-networking)
- [Pod-to-Pod Communication](06-networking.md#part-2-pod-to-pod-communication)
- [Service Discovery & DNS](06-networking.md#part-3-service-discovery--dns)
- [Container Network Interface (CNI)](06-networking.md#part-4-container-network-interface-cni)
- [Traditional Endpoints - The Problem](06-networking.md#part-5-traditional-endpoints---the-problem)
- [The Solution - EndpointSlices](06-networking.md#part-6-the-solution---endpointslices)
- [Network Policies](06-networking.md#part-7-network-policies)
- [Ingress Controllers](06-networking.md#part-8-ingress-controllers)
- [North-South vs East-West Traffic](06-networking.md#part-9-north-south-vs-east-west-traffic)

### [07 - Ingress & External Access](07-ingress-and-external-access.md)
- [Multi-Service Routing (Shared Ingress)](07-ingress-and-external-access.md#part-1-multi-service-routing-shared-ingress)
- [Public vs Private Ingress](07-ingress-and-external-access.md#part-2-public-vs-private-ingress)
- [Cert-Manager in Action (Automation)](07-ingress-and-external-access.md#part-3-cert-manager-in-action-automation)
- [Automating DNS with ExternalDNS](07-ingress-and-external-access.md#part-4-automating-dns-with-externaldns)
- [Multi-Cluster / Regional Access](07-ingress-and-external-access.md#part-5-multi-cluster--regional-access)
- [Common Pitfalls & Debugging](07-ingress-and-external-access.md#part-6-common-pitfalls--debugging)
- [Ingress to Gateway API](07-ingress-and-external-access.md#part-7-ingress-to-gateway-api)

### [08 - Security](08-security.md)
- [The K8s API Security Chain](08-security.md#part-1-the-k8s-api-security-chain)
- [Authentication - "Who Are You?"](08-security.md#part-2-authentication---who-are-you)
- [Authorisation - "What Can You Do?"](08-security.md#part-3-authorisation---what-can-you-do)
- [Understanding RBAC](08-security.md#part-4-understanding-rbac)
- [Service Accounts](08-security.md#part-5-service-accounts)
- [Real-World Use of Service Accounts](08-security.md#part-6-real-world-use-of-service-accounts)
- [Pod Security Standards](08-security.md#part-7-pod-security-standards)
- [Network Policies & Zero Trust Networking](08-security.md#part-8-network-policies--zero-trust-networking)
- [Admission Controllers Overview](08-security.md#part-9-admission-controllers-overview)
- [Policy Engines - OPA Gatekeeper vs Kyverno](08-security.md#part-10-policy-engines---opa-gatekeeper-vs-kyverno)
- [Secrets Encryption at Rest](08-security.md#part-11-secrets-encryption-at-rest)
- [Defence in Depth in Kubernetes](08-security.md#part-12-defence-in-depth-in-kubernetes)

### [09 - Scheduling & Node Management](09-scheduling-and-node-management.md)
- [The K8s Scheduler - How It Works](09-scheduling-and-node-management.md#part-1-the-k8s-scheduler---how-it-works)
- [Node Conditions & Readiness](09-scheduling-and-node-management.md#part-2-node-conditions--readiness)
- [Taints & Tolerations](09-scheduling-and-node-management.md#part-3-taints--tolerations)
- [NodeSelectors](09-scheduling-and-node-management.md#part-4-nodeselectors)
- [NodeAffinity](09-scheduling-and-node-management.md#part-5-nodeaffinity)
- [Pod AntiAffinity](09-scheduling-and-node-management.md#part-6-pod-antiaffinity)
- [Topology Spread Constraints](09-scheduling-and-node-management.md#part-7-topology-spread-constraints)
- [Pod Priority & Preemption](09-scheduling-and-node-management.md#part-8-pod-priority--preemption)
- [Pod Disruption Budgets](09-scheduling-and-node-management.md#part-9-pod-disruption-budgets)
- [DaemonSets](09-scheduling-and-node-management.md#part-10-daemonsets)
- [Jobs and CronJobs](09-scheduling-and-node-management.md#part-11-jobs-and-cronjobs)
- [Cordon, Drain and Uncordon](09-scheduling-and-node-management.md#part-12-cordon-drain-and-uncordon)
- [Evictions & Rescheduling](09-scheduling-and-node-management.md#part-13-evictions--rescheduling)
- [Static Pods](09-scheduling-and-node-management.md#part-14-static-pods)

### [10 - Observability Fundamentals](10-observability-fundamentals.md)
- [Observability in K8s](10-observability-fundamentals.md#part-1-observability-in-k8s)
- [Monitoring vs Observability](10-observability-fundamentals.md#part-2-monitoring-vs-observability)
- [Metrics Server](10-observability-fundamentals.md#part-3-metrics-server)
- [Logging Architecture](10-observability-fundamentals.md#part-4-logging-architecture)
- [Basic Debugging with Kubectl](10-observability-fundamentals.md#part-5-basic-debugging-with-kubectl)
- [K8s Events](10-observability-fundamentals.md#part-6-k8s-events)
