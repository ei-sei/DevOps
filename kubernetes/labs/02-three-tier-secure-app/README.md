# Lab 02 - Three-Tier App with Ingress, StatefulSet & NetworkPolicy

## Objective

Deploy a frontend → backend → database stack that goes beyond Lab 01's Deployment/NodePort setup, covering three concepts not yet touched hands-on:

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
```

> A separate cluster from Lab 01's `webapp-mongodb`, so the two labs stay isolated - `kind get clusters` will show both.

---

### Step 1 - Database StatefulSet + PVC

*(TODO - Postgres/Mongo as a StatefulSet with a `volumeClaimTemplate`, plus the Secret for credentials)*

---

### Step 2 - Backend Deployment

*(TODO - reads DB credentials from the Secret, connects to the database via the StatefulSet's headless Service)*

---

### Step 3 - Frontend Deployment

*(TODO - talks to the backend over a ClusterIP Service)*

---

### Step 4 - Ingress Controller + Ingress Resource

*(TODO - install nginx-ingress via Helm, then define an `Ingress` routing a hostname to the frontend Service)*

---

### Step 5 - NetworkPolicy (Default-Deny + Explicit Allow)

*(TODO - deny all pod-to-pod traffic by default, then explicitly allow only backend → database)*
