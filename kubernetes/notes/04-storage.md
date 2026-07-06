# 4. Storage

---

## Part 1: Why Storage Matters

What happens to a container's filesystem by default?
> It's ephemeral - anything written inside the container is lost the moment the container restarts or the Pod is recreated.

What is a Volume, at the most basic level?
> A directory accessible to containers in a Pod, backed by something outside the container's own filesystem - it can outlive a container restart, though not necessarily the Pod itself (e.g. `emptyDir`).

Why isn't a basic Volume enough for real data?
> Types like `emptyDir` are tied to the Pod's lifetime - delete the Pod and the data is gone too. Anything you actually need to persist beyond the Pod needs a **PersistentVolume**.

---

## Part 2: PersistentVolumes (PV)

What is a PersistentVolume?
> A piece of storage in the cluster that exists independently of any Pod - provisioned either by an admin ahead of time (static) or automatically on demand (dynamic), and outliving whatever Pod uses it.

What does a PV represent, conceptually?
> The actual underlying storage resource - an EBS volume, an NFS share, a local disk - wrapped in a Kubernetes object so it can be tracked and allocated like any other resource.

What are common PV attributes?
> Capacity (size), access modes (how many nodes/Pods can use it, and how), a reclaim policy (what happens to the storage after it's released), and the storage backend/driver details.

What is a reclaim policy?
> What happens to the underlying storage once its claim is deleted - `Retain` keeps the data around for manual recovery, `Delete` removes the underlying storage entirely, `Recycle` is deprecated.

---

## Part 3: PersistentVolumeClaims (PVC)

What is a PersistentVolumeClaim?
> A request for storage made by a user or a Pod - it specifies size and access mode needed, and Kubernetes binds it to a matching PersistentVolume.

How does a Pod actually use persistent storage?
> The Pod spec references a PVC as a volume, the PVC is bound to a PV, and the PV is backed by real storage - the Pod itself never talks to a PV directly.

![pod, pvc, pv, storage](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQT7sWohnFPjeRIXrU0iadQkRQdlAdwPSHbB-LFOVIAJtUyiXjT30OhN6d6&s=10)


```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

What are the common access modes?
> - **ReadWriteOnce** (one node can mount it read-write), 
> - **ReadOnlyMany** (many nodes, read-only), 
> - **ReadWriteMany** (many nodes, read-write - not supported by all storage backends).

What happens if no PV matches a PVC's request?
> The PVC stays `Pending` until a matching PV becomes available - either created manually, or automatically via dynamic provisioning.

---

## Part 4: The Problem With Deployments and Storage

Why don't [Deployments](./02-running-and-managing-workloads.md#part-2-deployments) work well for stateful, storage-heavy apps?
> A Deployment's Pods are interchangeable and unordered - if you attach the same PVC to multiple replicas, they'd all fight over the same volume, and a restarted Pod gets a fresh identity with no guarantee of reconnecting to "its" data.

What specifically goes wrong with shared storage under a Deployment?
> Most storage backends only support `ReadWriteOnce` (one node at a time) - scaling a Deployment's replicas won't give each Pod its own volume, and concurrent writes from interchangeable Pods to one volume risk data corruption.

---

## Part 5: StatefulSets & Storage

How do StatefulSets solve this? *(see also [notes/02](02-running-and-managing-workloads.md#part-10-other-workload-controllers) for StatefulSet basics)*
> Each Pod in a StatefulSet gets its own PVC generated from a `volumeClaimTemplate`, and that specific PVC/PV always follows the same Pod identity (`app-0` always gets `app-0`'s volume back), even after a restart or rescheduling.

```yaml
volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

---

## Part 6: Dynamic Provisioning Flow

What problem does dynamic provisioning solve?
> Manually pre-creating PVs for every possible storage request doesn't scale - an admin would have to predict demand and provision volumes ahead of time for every app.

What is a StorageClass?
> A template that tells Kubernetes how to automatically provision a PV on demand - which storage backend/driver to use, what parameters to pass (disk type, IOPS, etc.), and what reclaim policy to apply.

What is the end-to-end dynamic provisioning flow?
> 1. A user creates a PVC referencing a StorageClass. 2. Kubernetes sees no matching PV exists. 3. The StorageClass's provisioner is invoked to create real storage on demand (e.g. calling the cloud provider's API for a new disk). 4. A matching PV is created automatically and bound to the PVC. 5. The Pod mounts the PVC as normal, unaware any of this happened behind the scenes.

What triggers this automatically, versus needing an admin?
> Simply creating a PVC that references a StorageClass is enough - no admin has to pre-provision anything, which is the entire point of "dynamic" provisioning over the static/manual approach in Part 2.

---

## Part 7: Ephemeral Volumes

What is an ephemeral volume?
> Storage that's tied directly to a Pod's lifecycle - created when the Pod starts and destroyed when the Pod is removed, unlike a PVC which persists independently.

When would you use one instead of a PVC?
> When a Pod needs scratch space, caching, or a place to share data between its own containers, but doesn't need that data to survive the Pod being deleted - e.g. `emptyDir`, or a generic ephemeral volume backed by a CSI driver for more advanced cases.

How does a generic ephemeral volume differ from `emptyDir`?
> `emptyDir` is always local, node-backed storage. A generic ephemeral volume can be backed by any CSI driver (like a cloud disk), while still being deleted automatically with the Pod - useful when you want CSI-level features without full PVC lifecycle management.

---

## Part 8: CSI Overview

What is CSI?
> The **Container Storage Interface** - a standard API that lets any storage vendor write a plugin that Kubernetes (and other orchestrators) can use, without Kubernetes needing built-in code for every storage system.

Why did Kubernetes move to CSI instead of built-in storage plugins?
> In-tree volume plugins required changes to Kubernetes core itself for every new storage backend. CSI decouples storage vendors from the Kubernetes release cycle - they can ship and update their own driver independently.

What does a CSI driver actually do?
> Implements the provisioning, attaching, mounting, and deleting operations for a specific storage backend, translating Kubernetes's generic storage requests into whatever API calls that backend needs (e.g. AWS EBS CSI driver calling the EC2 API).

---

## Lab: Data Survives a Pod Restart

**Goal:** Prove that data on a PVC outlives the Pod using it, unlike a Pod's own filesystem.

```yaml
# 1. pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```yaml
# 2. pod.yaml - mounts the PVC and writes a file to it on startup
apiVersion: v1
kind: Pod
metadata:
  name: storage-demo
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "echo 'hello from the first pod' > /data/message.txt && sleep 3600"]
      volumeMounts:
        - name: demo-vol
          mountPath: /data
  volumes:
    - name: demo-vol
      persistentVolumeClaim:
        claimName: demo-pvc
```

```bash
# 3. Apply both and confirm the file exists
kubectl apply -f pvc.yaml -f pod.yaml
kubectl exec storage-demo -- cat /data/message.txt
```

```bash
# 4. Delete the Pod (not the PVC) and recreate it
kubectl delete pod storage-demo
kubectl apply -f pod.yaml
```

```bash
# 5. Confirm the file is still there, from before this Pod ever existed
kubectl exec storage-demo -- cat /data/message.txt
# Expect: "hello from the first pod" - the new Pod re-mounted the same PVC/PV
```

```bash
# 6. Clean up
kubectl delete pod storage-demo
kubectl delete pvc demo-pvc
```

---

## Commands to Learn

```bash
# List PersistentVolumes
kubectl get pv
```

```bash
# List PersistentVolumeClaims
kubectl get pvc
```

```bash
# Full details of a PVC, including binding status
kubectl describe pvc my-pvc
```

```bash
# List available StorageClasses
kubectl get storageclass
```

```bash
# Check which StorageClass is set as default
kubectl get storageclass -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.metadata.annotations.storageclass\.kubernetes\.io/is-default-class}{"\n"}{end}'
```
