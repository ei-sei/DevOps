# Lab 01 - Deploy WebApp with MongoDB

## Objective

Deploy a full web app + MongoDB stack on a local Kubernetes cluster (KinD), covering Deployments, Services, PVCs, and Secrets end-to-end.

---

### Step 0 - Start kind

Check kind is installed:

```bash
kind version
```

> If it's missing, install it via your distro's package manager or the official binary - see [kind.sigs.k8s.io/docs/user/quick-start](https://kind.sigs.k8s.io/docs/user/quick-start/). kind also needs Docker (or Podman) running, since every "node" is actually a container.

Create the cluster:

```bash
kind create cluster --name webapp-mongodb
```

> `--name` matters once you're running more than one kind cluster at a time - without it, kind defaults to a cluster named `kind`. This also auto-configures your kubeconfig context.

Verify the cluster is up:

```bash
kubectl cluster-info --context kind-webapp-mongodb
kubectl get nodes
```

> kind prefixes the kubeconfig context with `kind-`, so `--context kind-webapp-mongodb` targets this specific cluster if you have others.

Useful commands while working with the cluster:

```bash
kind get clusters                                   # list all kind clusters
kind load docker-image <image>:<tag> --name webapp-mongodb   # push a locally built image into the cluster
kind delete cluster --name webapp-mongodb            # tear the cluster down completely
```

---

### Step 1 - ConfigMap for the Mongo URL

`mongo-config.yml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongo-config
data:
  mongo-url: mongo-service
```

> A ConfigMap holds non-sensitive configuration as key-value pairs, decoupling it from the app's own code/image - here it's a single value, `mongo-url`, set to `mongo-service`. That's not an IP or hostname you're inventing; it's the **Service name** the MongoDB Deployment will be exposed under later in this lab, and Kubernetes' internal DNS resolves any Service name to its ClusterIP automatically. The web app reads this ConfigMap instead of having the Mongo address hardcoded, so the connection target can change without touching the app's image.

---

### Step 2 - Secret for Mongo Credentials

`mongo-secret.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mongo-secret
type: Opaque
data:
  mongo-user: bW9uZ291c2Vy
  mongo-password: bW9uZ29wYXNzd29yZA==
```

> A Secret is the same shape as a ConfigMap - key-value pairs - but intended for sensitive data, and `type: Opaque` just means "unstructured, arbitrary key-value data" (the default and most common type, as opposed to built-in types like `kubernetes.io/tls` or `kubernetes.io/dockerconfigjson`). The values here decode to `mongouser` and `mongopassword` - Secret data is **base64-encoded, not encrypted**, so it's obfuscation for accidental exposure (e.g. `kubectl get -o yaml`), not real security. Anyone with API access to read the Secret can trivially decode it with `echo <value> | base64 -d`; genuine protection depends on RBAC restricting who can read Secrets, and ideally encryption at rest on the cluster.

Apply it and verify:

```bash
kubectl apply -f mongo-secret.yml
kubectl get secret mongo-secret -o yaml
```

To confirm a value decodes correctly:

```bash
kubectl get secret mongo-secret -o jsonpath="{.data.mongo-user}" | base64 -d
```

---

### Step 3 - MongoDB Deployment and Service

`mongo.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-deployment
  labels:
    app: mongo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo
  template:
    metadata:
      labels:
        app: mongo
    spec:
      containers:
        - name: mongodb
          image: mongo:5.0
          ports:
            - containerPort: 27017
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              valueFrom:
                secretKeyRef:
                  name: mongo-secret
                  key: mongo-user
            - name: MONGO_INITDB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mongo-secret
                  key: mongo-password
---
apiVersion: v1
kind: Service
metadata:
  name: mongo-service
spec:
  selector:
    app: mongo
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

> `MONGO_INITDB_ROOT_USERNAME`/`MONGO_INITDB_ROOT_PASSWORD` are the official `mongo` image's own bootstrap env vars - its startup script reads these to create the root user on first launch, sourced here from the Secret via `secretKeyRef` instead of being typed in plaintext. The Service has no `type` set, so it defaults to `ClusterIP` - only reachable from inside the cluster, which is correct for a database that should never be exposed directly to the outside world. `port: 27017` (what the Service listens on) matches `targetPort: 27017` (the container's actual port) deliberately, so `mongo-service:27017` is the natural, unsurprising connection address - this is also exactly the Service name `mongo-config.yml`'s `mongo-url` value already points at.

Apply it and verify:

```bash
kubectl apply -f mongo.yml
kubectl get pods -l app=mongo
kubectl get svc mongo-service
```

---

### Step 4 - WebApp Deployment and Service

`webapp.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
  labels:
    app: webapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: nanajanashia/k8s-demo-app:v1.0
          ports:
            - containerPort: 3000
          env:
            - name: USER_NAME
              valueFrom:
                secretKeyRef:
                  name: mongo-secret
                  key: mongo-user
            - name: USER_PWD
              valueFrom:
                secretKeyRef:
                  name: mongo-secret
                  key: mongo-password
            - name: DB_URL
              valueFrom:
                configMapKeyRef:
                  name: mongo-config
                  key: mongo-url
---
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
spec:
  type: NodePort
  selector:
    app: webapp
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
      nodePort: 30100
```

> The webapp reads three env vars at startup: `USER_NAME`/`USER_PWD` from the same Mongo Secret (so it can authenticate), and `DB_URL` from the ConfigMap (`mongo-service` - resolved via cluster DNS to reach Mongo without a hardcoded address). This Service is `type: NodePort`, not `ClusterIP` like Mongo's - it needs to be reachable from outside the cluster, since it's the actual app a user visits, not an internal-only database. `nodePort: 30100` is the fixed external-facing port; Kubernetes requires NodePort values to fall within `30000-32767` by default.

Apply it and verify:

```bash
kubectl apply -f webapp.yml
kubectl get pods -l app=webapp
kubectl get svc webapp-service
```

---

### Step 5 - Access the WebApp

kind doesn't expose NodePort services to your host machine automatically (unlike minikube, which has a `minikube service` helper that does this for you) - its "nodes" are just Docker containers, and their ports aren't published to `localhost` unless the cluster was created with an `extraPortMappings` config. The simplest workaround is `kubectl port-forward`, which tunnels traffic through the API server instead of relying on the node's network being reachable:

```bash
kubectl port-forward service/webapp-service 3000:3000
```

> The syntax is `<host-port>:<service-port>` - the first `3000` is the port on your machine, the second is what `webapp-service` listens on (`port: 3000` in its spec). They don't have to match. This command blocks/holds the connection open in your terminal rather than running in the background - leave it running, and `Ctrl+C` to stop forwarding.

Then visit:

```
http://localhost:3000
```

The request path: browser → `kubectl port-forward` → API server → `webapp-service` → the webapp Pod → (via `DB_URL`) → `mongo-service` → the Mongo Pod.

---

