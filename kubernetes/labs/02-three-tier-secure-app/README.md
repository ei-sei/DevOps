# Lab 02 - Three-Tier App with Ingress, StatefulSet & NetworkPolicy

## Objective

Deploy a frontend → backend → database stack, covering three concepts not yet touched hands-on:

- The database runs as a **StatefulSet** with a PVC, not a plain Deployment - stable identity and storage that survives rescheduling.
- External access goes through a real **Ingress Controller** (nginx-ingress via Helm), not `kubectl port-forward`.
- A **default-deny NetworkPolicy** restricts pod-to-pod traffic so only the backend can reach the database - nothing else can, not even the frontend directly.

See [`04-storage.md` Part 5](../../notes/04-storage.md#part-5-statefulsets--storage) and [`08-security.md` Part 8](../../notes/08-security.md#part-8-network-policies--zero-trust-networking) for the underlying concepts.

---

### Step 0 - Start kind

```bash
kind create cluster --name three-tier-secure-app
kubectl cluster-info --context kind-three-tier-secure-app
kubectl get nodes

# tear the cluster down completely
kind delete cluster --name webapp-mongodb            
```

> A separate cluster from `webapp-mongodb`, so the two stay isolated - `kind get clusters` will show both.

---

### Step 1 - Database StatefulSet + PVC

`db-statefulset.yml`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db-service
  replicas: 1
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
        - name: mongodb
          image: mongo:5.0
          volumeMounts:
            - name: db-storage
              mountPath: /data/db
  volumeClaimTemplates:
    - metadata:
        name: db-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
---
apiVersion: v1
kind: Service
metadata:
  name: db-service
spec:
  clusterIP: None
  selector:
    app: db
  ports:
    - port: 27017
```

> Unlike a plain Deployment with a manually-created PVC, `volumeClaimTemplates` here generates a **separate PVC per replica** automatically, each permanently bound to that specific pod's identity (`db-0` always gets `db-0`'s storage back, even after a restart or reschedule). There's no standalone `PersistentVolumeClaim` object and no `volumes`/`claimName` on the pod spec - the template replaces both, which is what makes a StatefulSet the correct pattern for stateful workloads instead of a Deployment.
>
> `db-service` is **headless** (`clusterIP: None`) - required by any StatefulSet referenced via `serviceName`. Instead of load-balancing across pods behind one virtual IP like a normal Service, it gives each pod its own stable DNS name (`db-0.db-service`), which is the other half of "stable identity" alongside the per-pod storage above.

Apply and verify:

```bash
kubectl apply -f db-statefulset.yml
kubectl get statefulset db
kubectl get pods -l app=db
kubectl get pvc
```

> Watch the naming: the pod comes up as `db-0` (not a random suffix like a Deployment's pods get), and the PVC it claims is named `db-storage-db-0` - the `<volumeClaimTemplate name>-<pod name>` pattern.

---

### Step 2 - Database Credentials

*(TODO - Secret for DB username/password, consumed by the backend)*

---

### Step 3 - Backend Deployment

*(TODO - reads DB credentials from the Secret, connects to the database via the StatefulSet's headless Service)*

---

### Step 4 - Frontend Deployment

*(TODO - talks to the backend over a ClusterIP Service)*

---

### Step 5 - Ingress Controller + Ingress Resource

*(TODO - install nginx-ingress via Helm, then define an `Ingress` routing a hostname to the frontend Service)*

---

### Step 6 - NetworkPolicy (Default-Deny + Explicit Allow)

*(TODO - deny all pod-to-pod traffic by default, then explicitly allow only backend → database)*
