# 2. Running & Managing Workloads in K8s

---

## Part 1: Pods

What is a Pod?
> A **Pod** is the smallest deployable unit in Kubernetes - a wrapper around one or more containers that share the same network namespace and storage, always scheduled together onto the same node.

Why does Kubernetes schedule Pods instead of containers directly?
> Some workloads need more than one tightly coupled container running side by side (e.g. an app plus a helper process) sharing the same IP and volumes - the Pod is the unit that groups them, while still letting Kubernetes manage single-container workloads the same way.

What do containers in the same Pod share?
> The same network namespace (so they share one IP and can reach each other via `localhost`) and any volumes mounted into the Pod.

What does a minimal Pod manifest look like?
> ```yaml
> apiVersion: v1
> kind: Pod
> metadata:
>   name: my-pod
> spec:
>   containers:
>     - name: app
>       image: nginx:latest
>       ports:
>         - containerPort: 80
> ```

How do you create a Pod imperatively, without a YAML file?
> `kubectl run my-pod --image=nginx:latest` creates a Pod directly from the command line - useful for quick tests, but not reproducible or version-controlled the way a YAML manifest is.

What are the main Pod phases?
> - **Pending** (accepted but not yet scheduled or still pulling images),
> - **Running** (at least one container is running),
> - **Succeeded** (all containers exited successfully, won't restart),
> - **Failed** (all containers terminated and at least one failed), and
> - **Unknown** (state can't be determined, usually a node communication issue).

What is the difference between a Pod's phase and a container's state within it?
> The Pod phase is a coarse summary of the whole Pod, while each container inside it has its own state (`Waiting`, `Running`, `Terminated`) - a Pod can show `Running` while one of its containers is still `Waiting` to start.

---

## Part 2: Deployments

Why not just create Pods directly in production?
> A bare Pod has no self-healing - if its node dies or the Pod crashes, nothing recreates it. A **Deployment** wraps Pods with a controller that ensures a desired number of replicas are always running and handles rolling updates.

What is a Deployment?
> A **Deployment** is a controller that manages a set of identical Pods (via a ReplicaSet underneath), ensuring the desired replica count is maintained and providing declarative, versioned rollout and rollback of changes.

What does a minimal Deployment manifest look like?
> ```yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: my-app
> spec:
>   replicas: 3
>   selector:
>     matchLabels:
>       app: my-app
>   template:
>     metadata:
>       labels:
>         app: my-app
>     spec:
>       containers:
>         - name: app
>           image: nginx:latest
> ```

What is the `template` field in a Deployment for?
> It defines the Pod spec that the Deployment will stamp out for every replica - effectively a Pod manifest nested inside the Deployment.

How do you create a Deployment imperatively?
> `kubectl create deployment my-app --image=nginx:latest --replicas=3` - quick for testing, but like imperative Pods, not the recommended approach for anything you want to track in version control.

**Pod vs Deployment**

| Aspect          | Pod         | Deployment |
| --------------- | ----------- | ---------- |
| Self-healing    | ❌           | ✅          |
| Scaling         | Manual      | Built-in   |
| Rolling updates | ❌           | ✅          |
| Rollback        | ❌           | ✅          |
| Production use  | Never alone | Always     |

---

## Part 3: ReplicaSets

What is a ReplicaSet?
> A **ReplicaSet** ensures a specified number of identical Pod replicas are running at any given time, replacing any that fail or are deleted.

How does a ReplicaSet know which Pods belong to it?
> Via a label selector - any Pod matching the ReplicaSet's `selector.matchLabels` is considered one of its own, whether the ReplicaSet created it or not.

What is the relationship between a Deployment and a ReplicaSet?
> A Deployment creates and manages ReplicaSets on your behalf. When you update a Deployment's Pod template, it creates a new ReplicaSet and scales it up while scaling the old one down - that rollout mechanics live at the Deployment level, not the ReplicaSet level.

Why use a Deployment instead of a ReplicaSet directly?
> A bare ReplicaSet keeps the replica count steady but has no built-in concept of rolling out a new version or rolling back - you'd have to manage that yourself. A Deployment adds that layer on top.

---

## Part 4: Pod Failure & Container Patterns

What is CrashLoopBackOff?
> A Pod status meaning a container keeps crashing shortly after starting, and Kubernetes is repeatedly restarting it with an increasing delay between attempts (exponential backoff) rather than restarting it instantly forever.

What usually causes CrashLoopBackOff?
> An application error on startup, a missing dependency or config, a failed health check causing a restart, or insufficient resources causing the process to be killed - `kubectl logs` and `kubectl describe pod` are the first places to look.

What is an Init Container?
> A container that runs to completion **before** the main application containers in a Pod start, commonly used to wait for a dependency, run a setup script, or fetch configuration.

How does an Init Container differ from a regular container in the same Pod?
> Init containers run sequentially and must each complete successfully before the next one (or the main containers) start. Regular containers in a Pod all start together and run concurrently.

What is the Sidecar pattern?
> Running a helper container alongside the main application container in the same Pod to extend or support it - for example, a log-shipping container that reads the main container's logs and forwards them elsewhere.

What is the Adapter pattern?
> A sidecar variant that transforms or standardises the main container's output into a different format expected by external monitoring or logging systems, without changing the main application itself.

What is an Ephemeral Container?
> A temporary container you can inject into an already-running Pod for debugging, without restarting the Pod or its existing containers - useful when a minimal production image has no shell or debugging tools built in.

**Key Patterns Summary**

| Pattern        | Description           | Example Use                  |
| -------------- | --------------------- | ---------------------------- |
| Sidecar        | Helper alongside main | Logging, proxies, sync       |
| Ambassador     | Proxy to external     | Database connection pooling  |
| Adapter        | Transform output      | Log format conversion        |
| Init Container | Setup before main     | Wait for DB, download config |

---

## Part 5: Quality of Service (QoS)

What is Kubernetes QoS used for?
> QoS classes determine which Pods are evicted first when a node runs low on resources - Kubernetes uses them to decide what to sacrifice under pressure rather than letting the whole node fail.

What are the three QoS classes?
> **Guaranteed**, **Burstable**, and **BestEffort**.

What makes a Pod Guaranteed?
> Every container in the Pod has both requests and limits set, and requests equal limits, for both CPU and memory - the Pod is guaranteed the exact resources it asked for and is the last to be evicted under pressure.

What makes a Pod Burstable?
> At least one container has a request or limit set, but they don't all match exactly (e.g. limits are higher than requests) - it gets at least its requested resources and can burst higher if available, but is evicted before Guaranteed Pods.

What makes a Pod BestEffort?
> No container in the Pod sets any requests or limits at all - it gets whatever is left over and is the first to be evicted when a node is under resource pressure.

---

## Part 6: Probes

What is a probe in Kubernetes?
> A probe is a periodic check the kubelet performs against a container to determine its health or readiness, used to decide whether to restart it or route traffic to it.

What are the three probe types?
> - **Liveness** (is the container still working - restart it if not), 
> - **Readiness** (is the container ready to receive traffic - remove it from service endpoints if not, without restarting it), 
> - **Startup** (has the container finished starting up - delays liveness/readiness checks until it passes).

Give an example of a liveness probe:
> ```yaml
> livenessProbe:
>   httpGet:
>     path: /healthz
>     port: 8080
>   initialDelaySeconds: 5
>   periodSeconds: 10
> ```

Why is a separate Readiness probe useful alongside Liveness?
> A container can be alive but not ready - for example, still loading a large dataset on startup. Readiness lets Kubernetes hold back traffic without killing and restarting a perfectly healthy container.

What happens if your liveness probe path is misconfigured?
> The probe fails even though the app is healthy, so Kubernetes repeatedly restarts a working container, often producing a CrashLoopBackOff for an application that was never actually broken.

---

## Part 7: Deployment Strategies

What is a Rolling Deployment?
> The default Deployment strategy - old Pods are gradually replaced with new ones a few at a time, keeping the application available throughout with no downtime window.

What is the Recreate strategy?
> All existing Pods are terminated first, and only then are new Pods created - causing a brief downtime window, but guaranteeing no old and new versions ever run simultaneously.

When would you choose Recreate over Rolling?
> When your application can't tolerate two versions running side by side at once, such as one with a breaking database schema change that old and new Pods can't both safely use.

What is a Rollback?
> Reverting a Deployment to a previous revision, using `kubectl rollout undo`, when a new rollout turns out to be broken - Kubernetes keeps a revision history specifically to make this possible.

How does Kubernetes know what to roll back to?
> Each Deployment update is recorded as a new revision (tracked via its ReplicaSets), and `kubectl rollout history` lets you see and target a specific prior revision to return to.

**Deployment Strategies Comparison**

| Strategy                | Downtime | Two versions live | Use when                                               |
| ----------------------- | -------- | ----------------- | ------------------------------------------------------ |
| RollingUpdate (default) | None     | Briefly, yes      | App tolerates mixed versions during rollout            |
| Recreate                | Brief    | Never             | Breaking changes - old and new can't run together      |
| Rollback                | None     | Briefly, yes      | Bad deployment detected - reverts to previous revision |

---

## Part 8: Resource Management

What are resource Requests and Limits?
> A **request** is the amount of CPU/memory the scheduler guarantees a container when placing it on a node. A **limit** is the maximum it's allowed to use - exceeding a memory limit gets the container killed (OOMKilled), exceeding a CPU limit just throttles it.

Why does the scheduler care about requests specifically, not limits?
> The scheduler places Pods based on whether a node has enough unreserved capacity to satisfy the sum of requests - limits aren't used for placement, only for capping usage once running.

What is a LimitRange?
> A namespace-level policy that sets default, minimum, and maximum resource requests/limits for Pods or containers in that namespace, so individual manifests don't have to specify them and can't go outside bounds.

What is a ResourceQuota?
> A namespace-level cap on the total resources (CPU, memory, object counts like Pods or Services) that can be consumed across everything in that namespace combined, used to stop one team or app from exhausting a shared cluster.

How do LimitRange and ResourceQuota differ?
> LimitRange constrains individual Pods/containers within a namespace. ResourceQuota constrains the namespace's total combined usage across everything in it.

---

## Part 9: Organising Resources

What does "Namespaces & Friends" typically cover?
> How Namespaces interact with the other organisational tools in this module - LimitRanges and ResourceQuotas are themselves namespace-scoped, and Labels/Annotations are commonly used to further organise resources within a namespace.

What is a Label?
> A key-value pair attached to a resource's metadata (e.g. `app: my-app`, `env: prod`) used to identify and organise resources for selection and grouping.

What is a LabelSelector?
> A query that matches resources by their labels - this is how Deployments, Services, and ReplicaSets know which Pods belong to them, via `matchLabels` or `matchExpressions`.

What is the difference between a Label and an Annotation?
> Labels are meant to be queried and selected against (and have character/format restrictions to support that). Annotations store arbitrary, non-identifying metadata - such as a build version, a contact email, or tooling-specific config - that you wouldn't select resources by.

Give an example of an annotation:
> ```yaml
> metadata:
>   annotations:
>     build-version: "2026.06.27-1"
>     maintainer: "ei-sei"
> ```

---

## Part 10: Other Workload Controllers

| Controller              | What it does                                                   | Key trait                                                                                                                                                                  | Use case                                                     |
| ----------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| ReplicaSet (standalone) | Keeps N identical Pods running                                 | Rarely created directly - a Deployment already creates and manages one for you, plus adds rollouts/rollback                                                                | Underlying mechanism behind Deployments                      |
| DaemonSet               | Runs exactly one Pod per node (or a subset via `nodeSelector`) | Pod count tracks node count automatically, not a fixed number                                                                                                              | Log collectors, monitoring agents, CNI/networking components |
| StatefulSet             | Like a Deployment, but for workloads needing stable identity   | Predictable Pod names (`app-0`, `app-1`...), ordered create/scale/delete, headless Service for per-Pod DNS, `volumeClaimTemplate` for per-Pod storage that follows the Pod | Databases and anything needing stable identity + storage     |
| Job                     | Runs a Pod to completion for a one-off task                    | Retries until `completions` target is met; `parallelism` controls how many run at once                                                                                     | Batch processing, one-off scripts                            |
| CronJob                 | Creates a Job on a recurring cron schedule                     | Trigger manually with `kubectl create job --from=cronjob/<name>`; history capped via `successfulJobsHistoryLimit`/`failedJobsHistoryLimit`                                 | Backups, reports, scheduled cleanup                          |

---

## Lab: Self-Healing - Pods vs Deployments

**Goal:** See first-hand why bare Pods aren't used in production, by comparing what happens when you delete each.

```bash
# 1. Create a standalone Pod
kubectl run lonely-pod --image=nginx:latest

# 2. Delete it, then check
kubectl delete pod lonely-pod
kubectl get pods
# Expect: nothing - it's gone for good, nothing recreates it
```

```bash
# 3. Create the same workload as a Deployment instead
kubectl create deployment nginx-deploy --image=nginx:latest --replicas=3
kubectl get pods -l app=nginx-deploy
```

```bash
# 4. Delete one of its Pods
POD_NAME=$(kubectl get pods -l app=nginx-deploy -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $POD_NAME

# 5. Check again immediately
kubectl get pods -l app=nginx-deploy
# Expect: still 3 Pods - a replacement was already scheduled by the ReplicaSet
```

```bash
# 6. Clean up
kubectl delete deployment nginx-deploy
```

---