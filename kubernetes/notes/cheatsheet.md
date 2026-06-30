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

---

## Debugging & Interacting with Pods

| Command | What it does |
|---|---|
| `kubectl describe pod <name>` | Full pod details + events |
| `kubectl logs <pod>` | Container output |
| `kubectl logs <pod> -f` | Follow logs in real-time |
| `kubectl exec <pod> -- <cmd>` | Run command in container |
| `kubectl exec -it <pod> -- /bin/sh` | Interactive shell |
| `kubectl get pods -l key=value` | Filter by label |

---

## Multi-Container Pods & Init Containers

| Command | What it does |
|---|---|
| `kubectl wait --for=condition=Ready pod/<name> --timeout=60s` | Wait for a pod to become ready before continuing |
| `kubectl get pod <name> -o jsonpath='{.status.podIP}'` | Get a pod's IP address |
| `kubectl logs <pod> -c <container>` | View logs from one specific container in a multi-container pod |
| `kubectl exec <pod> -c <container> -- <cmd>` | Run a command in one specific container (without `-c`, defaults to the first container) |
| `kubectl get pods <name> -w` | Watch a pod's status change in real-time (e.g. `Init:0/1` -> `Running`) |
| `kubectl get pod <name> -o jsonpath='{.status.initContainerStatuses[0].state}'` | Check an init container's state |
| `kubectl get pod <name> -o jsonpath='{.status.containerStatuses[0].state}'` | Check a main container's state |
| `kubectl get pods -l 'app in (a,b,c)'` | Filter pods using a set-based label selector |

---

## Deployments & ReplicaSets

| Command | What it does |
|---|---|
| `kubectl delete pod --all` | Delete every pod in the current namespace |
| `kubectl get deployments` | List Deployments |
| `kubectl get replicasets` | List ReplicaSets |
| `kubectl get pods --show-labels` | List pods with all their labels shown |
| `kubectl get pods -l app=nginx -o jsonpath='{.items[0].metadata.name}'` | Get the name of the first pod matching a label |
| `kubectl describe deployment <name>` | Full Deployment details - replica counts, strategy, events |
| `kubectl rollout status deployment/<name>` | Check whether a Deployment's rollout has finished |
| `kubectl get deployment <name> -o jsonpath='{.status.conditions[*].type}'` | Check a Deployment's status conditions (e.g. `Progressing`, `Available`) |
| `kubectl get deployments,replicasets,pods` | List multiple resource types in one command |
