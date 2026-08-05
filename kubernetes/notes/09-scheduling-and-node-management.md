# 9. Scheduling & Node Management

---

## Part 1: The K8s Scheduler - How It Works

What is `kube-scheduler` responsible for?
> Watching for newly created Pods with no `nodeName` set, and assigning each one to the best available node - it only decides *where* a Pod runs, it never runs the Pod itself.

How does it pick a node, at a high level?
> Two phases: **Filtering** narrows the full node list down to only those that could run the Pod at all (enough CPU/memory, satisfies taints/affinity/selectors), then **Scoring** ranks the surviving nodes and picks the highest-scoring one.

Give examples of what Filtering and Scoring check.
> - **Filtering** - `PodFitsResources` (enough free CPU/memory), `PodToleratesNodeTaints`, node selectors/affinity rules being satisfied.
> - **Scoring** - spreading Pods evenly across nodes (`SelectorSpread`), preferring nodes with images already cached, balancing resource utilisation across the cluster.

What happens if no node passes Filtering?
> The Pod stays **Pending** with an `Unschedulable` condition - it's retried on a loop as cluster state changes (a node freeing resources, a new node joining), rather than failing outright.

---

## Part 2: Node Conditions & Readiness

What are Node Conditions?
> A set of status fields on a Node object reporting its health, checked continuously by the kubelet and read by the scheduler before placing new Pods.

List the common conditions.
> - **Ready** - node is healthy and can accept Pods.
> - **MemoryPressure** - node is running low on memory.
> - **DiskPressure** - node is running low on disk space.
> - **PIDPressure** - node is running low on process IDs.
> - **NetworkUnavailable** - node's network isn't correctly configured.

How does the scheduler use these?
> A node reporting anything other than `Ready: True` (or under any pressure condition) is filtered out during scheduling - no new Pods are placed there, though Pods already running aren't necessarily evicted immediately.

How do you check a node's conditions?
> ```bash
> kubectl describe node <node-name>
> ```
> The `Conditions` section lists each one with its status, last transition time, and reason.

---

## Part 3: Taints & Tolerations

What is a taint?
> A marker applied to a **node** that repels Pods, unless a Pod explicitly tolerates it - the opposite direction to node affinity, which pulls Pods towards nodes.

What is a toleration?
> A field on a **Pod** declaring it can be scheduled onto a node with a matching taint - tolerating a taint doesn't force placement there, it only removes the repulsion.

What are the three taint effects?
> - **NoSchedule** - new Pods without a matching toleration won't be scheduled here.
> - **PreferNoSchedule** - the scheduler tries to avoid it, but will place a Pod here if there's no better option.
> - **NoExecute** - new Pods are repelled *and* any already-running Pods without the toleration are evicted.

```bash
kubectl taint nodes node1 gpu=true:NoSchedule
```

```yaml
tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
```

Give a real-world use case.
> Dedicating a pool of GPU nodes to ML workloads - taint the GPU nodes so ordinary Pods are repelled, then only the ML Deployment's Pods carry the matching toleration.

---

## Part 4: NodeSelectors

What is `nodeSelector`?
> The simplest way to constrain a Pod to specific nodes - a key/value map on the Pod spec that must exactly match labels present on the node.

```yaml
spec:
  nodeSelector:
    disktype: ssd
```

What's its main limitation?
> It only supports exact-match equality on labels, ANDed together - no OR logic, no "prefer but don't require," and no expressing relationships like "not this node." NodeAffinity exists to cover those cases.

---

## Part 5: NodeAffinity

What problem does NodeAffinity solve that `nodeSelector` doesn't?
> Richer matching - operators like `In`, `NotIn`, `Exists`, and `Gt`/`Lt`, plus the ability to express a preference instead of a hard requirement.

What do `requiredDuringSchedulingIgnoredDuringExecution` and `preferredDuringSchedulingIgnoredDuringExecution` mean?
> - **required** - a hard constraint; the scheduler won't place the Pod anywhere that doesn't match.
> - **preferred** - a soft constraint with a weight; the scheduler favours matching nodes but will still schedule elsewhere if needed.

What does "IgnoredDuringExecution" mean in both names?
> Once a Pod is already running, changes to node labels that would break the affinity rule don't cause it to be evicted - affinity is only evaluated at scheduling time, not continuously enforced afterwards.

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: disktype
              operator: In
              values: ["ssd"]
```

---

## Part 6: Pod AntiAffinity

How does Pod affinity/anti-affinity differ from Node affinity?
> Node affinity matches a Pod against **node labels**; Pod (anti-)affinity matches a Pod against **labels on other Pods already running**, letting you express "run near" or "run away from" other workloads.

What is `topologyKey` for?
> It defines the scope the rule applies over - e.g. `kubernetes.io/hostname` means "per node," while `topology.kubernetes.io/zone` means "per availability zone."

Give a real-world use case for Pod anti-affinity.
> Spreading a Deployment's replicas across different nodes (or zones) for high availability, so a single node failure can't take down every replica at once.

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app
              operator: In
              values: ["my-app"]
        topologyKey: "kubernetes.io/hostname"
```

---

## Part 7: Topology Spread Constraints

What problem does this solve that Pod anti-affinity handles clumsily?
> Anti-affinity is binary (co-locate or don't) and gets awkward at scale - Topology Spread Constraints instead let you define an even distribution target directly, e.g. "no more than 1 Pod difference between any two zones."

What is `maxSkew`?
> The maximum allowed difference in Pod count between the most- and least-loaded topology domain (node, zone, etc.) - the scheduler actively balances placement to stay within it.

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: my-app
```

When would you reach for this over Pod anti-affinity?
> When you want proportional, cluster-wide balance (e.g. across many zones) rather than a simple pairwise "don't run with" rule.

---

## Part 8: Pod Priority & Preemption

What is a PriorityClass?
> A cluster-scoped object assigning a numeric priority value that Pods can reference - higher numbers mean higher priority when the scheduler has to make trade-offs.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "Critical workloads"
```

What is preemption?
> When a high-priority Pod can't be scheduled due to insufficient resources, the scheduler may evict (preempt) lower-priority Pods on a node to free up room for it, rather than leaving the high-priority Pod Pending.

Does preemption guarantee the preempted Pods' work is preserved?
> No - preempted Pods are terminated the same as any other eviction; the workload's controller is responsible for rescheduling them elsewhere, and any in-flight work is lost unless the application handles it.

---

## Part 9: Pod Disruption Budgets

What problem do PodDisruptionBudgets (PDBs) solve?
> They protect against **voluntary disruptions** (node drains, cluster upgrades, scaling down) taking too many replicas of an application offline at once, by capping how much of it can be disrupted simultaneously.

What's the difference between `minAvailable` and `maxUnavailable`?
> Two ways to express the same budget - `minAvailable` sets a floor on how many Pods must stay up, `maxUnavailable` sets a ceiling on how many can be down at once. Only one is set per PDB.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

Does a PDB protect against every kind of disruption?
> No - only voluntary ones initiated through the Eviction API (like `kubectl drain`). It has no effect on involuntary disruptions like a node crashing or being killed outright (see Part 13).

---

## Part 10: DaemonSets

Where does a DaemonSet fit against the other workload types compared in [notes/02](02-running-and-managing-workloads.md#part-10-other-workload-controllers)?
> It runs exactly one Pod per node automatically, tracking the node count rather than a fixed replica number - used for per-node infrastructure like log collectors, monitoring agents, and CNI components.

How does DaemonSet scheduling differ from a normal Deployment's Pods?
> By default it doesn't - since Kubernetes 1.12, DaemonSet Pods go through the same `kube-scheduler` as everything else, using a built-in node affinity rule to target every node rather than picking one.

How does a DaemonSet run on control-plane nodes, which are normally tainted against workloads?
> It needs an explicit toleration for the control-plane taint, same as any other Pod - many DaemonSets (e.g. CNI plugins) ship with this toleration built in, since they need to run everywhere including the control plane.

```yaml
tolerations:
  - key: "node-role.kubernetes.io/control-plane"
    operator: "Exists"
    effect: "NoSchedule"
```

---

## Part 11: Jobs and CronJobs

What is a Job, as distinct from a Deployment?
> A workload meant to run to **completion** rather than indefinitely - it creates Pods, tracks them until a target number succeed, and doesn't restart them once they've finished successfully.

What do `completions` and `parallelism` control?
> `completions` is how many successful Pod runs are needed overall; `parallelism` is how many Pods can run at once working towards that total.

What does `backoffLimit` do?
> Caps how many times a failed Pod is retried before the Job itself is marked as failed.

How does a CronJob build on a Job, per the summary in [notes/02](02-running-and-managing-workloads.md#part-10-other-workload-controllers)?
> It creates a new Job on a recurring cron schedule (`schedule: "0 * * * *"`), with history capped via `successfulJobsHistoryLimit`/`failedJobsHistoryLimit`, and can be triggered manually with `kubectl create job --from=cronjob/<name>`.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup-tool:latest
          restartPolicy: OnFailure
```

---

## Part 12: Cordon, Drain and Uncordon

What does `kubectl cordon` do?
> Marks a node `Unschedulable`, so the scheduler stops placing new Pods there - existing Pods on the node are left running untouched.

What does `kubectl drain` do?
> Cordons the node, then evicts its Pods (respecting any PDBs from Part 9) so they get rescheduled elsewhere, leaving the node empty and ready for maintenance.

```bash
kubectl drain node1 --ignore-daemonsets --delete-emptydir-data
```

Why is `--ignore-daemonsets` usually needed?
> DaemonSet Pods are meant to run on every node by design, so `drain` can't evict them without breaking that guarantee - the flag tells it to leave them running rather than fail the whole drain.

What does `kubectl uncordon` do?
> Reverses a cordon, marking the node schedulable again - it does not automatically move any Pods back onto it, new scheduling decisions simply become eligible to land there again.

---

## Part 13: Evictions & Rescheduling

What's the difference between a voluntary and an involuntary disruption?
> **Voluntary** disruptions are initiated deliberately through the Eviction API (drains, PDB-aware scale-downs) and respect PodDisruptionBudgets. **Involuntary** disruptions - a node crashing, being preempted by the cloud provider, or hitting resource pressure - happen regardless of any PDB.

How does the kubelet decide which Pods to evict under node resource pressure?
> It ranks Pods by QoS class first (`BestEffort` evicted before `Burstable` before `Guaranteed`), then by how far each Pod is over its resource requests within that class - the least-protected, most resource-hungry Pods go first.

What happens to a Pod after it's evicted?
> The Pod itself is gone for good - it's the owning controller (Deployment, StatefulSet, DaemonSet, etc.) that notices and creates a replacement, which then goes through scheduling again like any new Pod. A bare Pod with no controller is not recreated.

---

## Part 14: Static Pods

What is a static Pod?
> A Pod managed directly by the **kubelet** on a specific node, from manifest files in a local directory, rather than being created via the API server.

How does the kubelet know to run them?
> It watches a configured directory (commonly `/etc/kubernetes/manifests`) for Pod YAML files, and creates/updates/removes the corresponding Pod to match whatever's in that directory.

What's the most common real-world use of static Pods?
> Running the control plane components themselves - `kube-apiserver`, `kube-scheduler`, `kube-controller-manager`, and `etcd` are typically deployed as static Pods on control-plane nodes, so the cluster can bootstrap itself before the API server (which normally schedules Pods) even exists.

How can you tell a Pod is static from `kubectl get pods`?
> Its name is suffixed with the node's hostname (e.g. `kube-apiserver-node1`), and the API server shows a read-only **mirror Pod** representing it - editing or deleting that mirror Pod via `kubectl` has no lasting effect, since the kubelet just recreates it from the manifest file.

---

## Commands to Learn

```bash
# Inspect a node's conditions and capacity
kubectl describe node <node-name>
kubectl get nodes -o wide
```

```bash
# Taint and label nodes
kubectl taint nodes node1 gpu=true:NoSchedule
kubectl label nodes node1 disktype=ssd
```

```bash
# Find which node a Pod landed on, and which Pods are on a given node
kubectl get pods -o wide
kubectl get pods --field-selector spec.nodeName=node1 -A
```

```bash
# Check PodDisruptionBudgets before draining
kubectl get pdb -A
```

```bash
# Take a node out for maintenance, then bring it back
kubectl cordon node1
kubectl drain node1 --ignore-daemonsets --delete-emptydir-data
kubectl uncordon node1
```

```bash
# Inspect Jobs/CronJobs
kubectl get jobs,cronjobs
kubectl create job --from=cronjob/nightly-backup manual-run-1
```

```bash
# List static Pod manifests on a control-plane node
ls /etc/kubernetes/manifests
```
