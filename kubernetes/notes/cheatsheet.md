# kubectl Command Cheatsheet

---

## Cluster Verification

| Command | What it does |
|---|---|
| `kubectl cluster-info` | Verifies your cluster is running and shows the control plane endpoint |
| `kubectl get nodes` | Checks the nodes in the cluster and their status |
| `kubectl get pods` | Checks that pods are running |

---

## Creating Resources

| Command | What it does |
|---|---|
| `kubectl run <name> --image=<image>` | Imperative - creates a Pod directly from the command line |
| `kubectl apply -f <file>.yaml` | Declarative - creates or updates resources from a YAML manifest |

---

## Inspecting & Deleting Pods

| Command | What it does |
|---|---|
| `kubectl get pods -o wide` | Shows extra columns, including which node the pod is on and its IP address |
| `kubectl get pod <name> -o yaml` | Shows the full resource definition in detail, including status fields set by the cluster |
| `kubectl delete pod <name>` | Deletes a pod |
| `kubectl get pods` | Run again after a delete to verify the pod is gone |
