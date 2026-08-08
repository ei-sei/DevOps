# 10. Observability Fundamentals

---

## Part 1: Observability in K8s

What is observability, broadly?
> The ability to understand what's happening inside a system from the outside, based on the data it produces - built on three pillars: **metrics** (numeric measurements over time), **logs** (discrete event records), and **traces** (the path a single request takes through a system).

Why does observability matter more in Kubernetes than on a traditional server?
> Workloads are ephemeral and distributed by design - a Pod that crashed five minutes ago and got replaced no longer exists to SSH into, and a single request might cross several Pods on several nodes. Without observability tooling, that history and context is simply gone.

---

## Part 2: Monitoring vs Observability

What's the difference?
> **Monitoring** answers questions you already thought to ask - predefined dashboards and alerts for known failure modes (CPU high, Pod restarting). **Observability** is the underlying capability to ask *new* questions of a running system when something unexpected happens, without shipping new code to answer them.

Give a concrete example of the distinction.
> A CPU-usage alert firing is monitoring - you decided in advance that metric mattered. Being able to then ask "which specific requests, from which users, were slow during that spike" using existing logs/traces without redeploying anything is observability.

Are they in competition?
> No - monitoring is really a use case built on top of observability data. Good observability makes monitoring easier to build and keep relevant as the system changes.

---

## Part 3: Metrics Server

What is `metrics-server`?
> A cluster add-on that collects basic CPU/memory resource usage from every kubelet and exposes it through the Kubernetes **Metrics API** - lightweight, in-memory, no historical storage.

What does it actually get used for?
> - `kubectl top pods` / `kubectl top nodes` - live resource usage on the command line.
> - The **Horizontal Pod Autoscaler** reads from it directly to decide when to scale a Deployment up or down.

What does `metrics-server` deliberately *not* do?
> No history - it only holds the latest data point, nothing is stored for later querying. It's not a monitoring stack, just the minimum plumbing Kubernetes itself needs for autoscaling and `kubectl top`.

Where does real historical monitoring fit in, then?
> A separate stack (Prometheus, Grafana, etc.) scrapes and stores metrics over time for dashboards, alerting, and trend analysis - covered in depth on the `monitoring-stack` branch of this repo, not here.

```bash
kubectl top nodes
kubectl top pods -A
```

---

## Part 4: Logging Architecture

Where do a container's logs actually go?
> Whatever the process writes to **stdout/stderr** is captured by the container runtime and written to a log file on the node's disk - Kubernetes never asks an app to log to a specific file, it just captures the standard streams.

How does `kubectl logs` actually retrieve them?
> The kubelet on that Pod's node exposes those on-disk log files over an API, which `kubectl logs` calls through the API server - there's no central log store involved by default.

What happens to those logs when the Pod is deleted or the node is replaced?
> They're gone - node-local log files aren't retained beyond the Pod's (and often the node's) lifetime, which is exactly why relying on `kubectl logs` alone doesn't scale for debugging things after the fact.

What's the standard way to solve this at cluster level?
> A **node-level logging agent** (Fluent Bit, Fluentd, Promtail) deployed as a DaemonSet - see [notes/09 Part 10](09-scheduling-and-node-management.md#part-10-daemonsets) - reads every node's container log files and ships them to a central backend (Loki, Elasticsearch) where they persist and stay searchable after the Pod is gone.

---

## Part 5: Basic Debugging with Kubectl

What's the first command to reach for when a Pod isn't behaving?
> `kubectl describe pod <name>` - it surfaces status, resource requests, probe results, and the Events section (Part 6), which is usually where the actual reason lives.

When is `kubectl logs --previous` useful?
> When a container has already crashed and restarted - by default `kubectl logs` shows the *current* container's output, which is empty or just started; `--previous` gets the logs from the container instance that just died.

What does `kubectl exec -it <pod> -- sh` give you that `logs` doesn't?
> A live interactive shell inside the running container, for poking at the filesystem, checking environment variables, or testing connectivity from inside the Pod's network namespace - assuming the image actually has a shell.

What do you do when the image has no shell at all (e.g. a minimal distroless image)?
> `kubectl debug` - it attaches an **ephemeral container** (a separate debugging image with a full toolset) into the target Pod's namespaces, without needing a shell to already exist in the original container.

```bash
kubectl logs my-pod --previous
kubectl exec -it my-pod -- sh
kubectl debug my-pod -it --image=busybox --target=my-pod
```

---

## Part 6: K8s Events

What are Events?
> Objects the API server stores recording state changes reported by control plane components and kubelets - a Pod being scheduled, an image pull failing, a probe failing, a container being OOMKilled.

How long do Events stick around?
> Not long - by default they expire after about an hour, since the API server treats them as a lightweight rolling log, not a permanent audit trail.

How do you view them?
> ```bash
> kubectl get events --sort-by=.metadata.creationTimestamp
> kubectl get events --watch
> ```
> Or scoped to one object via `kubectl describe <resource> <name>`, which shows only that object's recent Events inline.

If Events are this useful, why not just rely on `kubectl get events` for debugging history?
> The short retention window means anything that happened more than an hour ago is already gone - if you need durable event history, it has to be exported to an external system (same problem, and often the same tooling, as Part 4's logging pipeline).

---

## Commands to Learn

```bash
# Live resource usage (needs metrics-server installed)
kubectl top nodes
kubectl top pods -A
```

```bash
# Logs, including from a crashed container
kubectl logs my-pod
kubectl logs my-pod --previous
kubectl logs my-pod -f
```

```bash
# Interactive debugging
kubectl exec -it my-pod -- sh
kubectl debug my-pod -it --image=busybox --target=my-pod
```

```bash
# Events - cluster-wide and object-scoped
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe pod my-pod
```
