# 5. Config & Secrets Management

---

## Part 1: ConfigMaps

What is a ConfigMap?
> An object that stores non-sensitive configuration data as key-value pairs, decoupling config from the container image so the same image can run in different environments.

Why not just bake config into the image?
> You'd need to rebuild the image for every config change or every environment (dev/staging/prod) - a ConfigMap lets you change config without touching the image at all.

What can a ConfigMap hold?
> Plain key-value pairs, or entire config files (e.g. an `nginx.conf`) stored as a single value under a filename key.

---

## Part 2: ConfigMaps in Practice

How do you create a ConfigMap?
> Declaratively from YAML, or imperatively with `kubectl create configmap my-config --from-literal=key=value` or `--from-file=path/to/file`.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: "production"
  LOG_LEVEL: "info"
```

What are the ways a Pod can consume a ConfigMap?
> As environment variables (`envFrom` or individual `valueFrom.configMapKeyRef`), or mounted as files in a volume - each key becomes a separate file containing that key's value.

What happens if a ConfigMap is updated after a Pod is already using it?
> Volume-mounted ConfigMaps update automatically after a short delay (the kubelet syncs periodically). Environment-variable-based ConfigMaps do **not** update - the Pod needs to be restarted to pick up new values.

---

## Part 3: Secrets

What is a Secret?
> Like a ConfigMap, but intended for sensitive data - passwords, tokens, keys - stored as base64-encoded values and handled with slightly more care by the cluster (e.g. not printed in plain `kubectl describe` output).

Is base64 encoding the same as encryption?
> No - base64 is just an encoding, trivially reversible by anyone with access to the Secret object. A Secret is only as secure as who can read it via the API and whether etcd itself is encrypted at rest.

What are common built-in Secret types?
> `Opaque` (generic key-value, the default), `kubernetes.io/dockerconfigjson` (registry credentials), and `kubernetes.io/tls` (a TLS cert/key pair).

---

## Part 4: Using Secrets

How does a Pod consume a Secret?
> The same two ways as a ConfigMap - as environment variables, or mounted as files in a volume - referenced by name in the Pod spec.

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-secret
        key: password
```

Which method is generally preferred for Secrets, and why?
> Volume mounts - environment variables can leak more easily (visible in `kubectl describe`, process listings, crash dumps, or child process environments), whereas file-based secrets are a bit more contained.

---

## Part 5: Secrets in Practice

How do you create a Secret imperatively?
> `kubectl create secret generic db-secret --from-literal=password=hunter2`

How do you inspect a Secret without exposing its value by accident?
> `kubectl get secret db-secret -o yaml` shows the base64 value directly - decode deliberately with `echo <value> | base64 -d` rather than assuming `describe` hides it completely (it hides the value, but `get -o yaml` does not).

---

## Part 6: The Reality of Kubernetes Secrets

Are Secrets actually secure by default?
> Not particularly - they're base64-encoded (not encrypted) by default in etcd unless you've explicitly enabled encryption at rest, and anyone with RBAC read access to Secrets in a namespace can read them in plaintext.

What's the biggest practical risk with native Secrets?
> They're often committed to Git as plain YAML during development, or over-permissioned via broad RBAC rules - the object type signals "sensitive," but Kubernetes doesn't enforce much beyond that on its own.

What do teams typically use to manage Secrets properly?
> A dedicated secrets management tool - synced in from a real secrets manager (AWS Secrets Manager, Vault) via an operator, or encrypted before ever touching Git - rather than relying on native Secrets alone.

---

## Part 7: External Secrets Operator (ESO)

What is the External Secrets Operator?
> A Kubernetes operator that syncs secrets from an external secrets manager (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, etc.) into native Kubernetes Secrets automatically.

Why use ESO instead of just creating Secrets directly?
> The real secret lives and is managed in a proper secrets manager (with rotation, audit logging, fine-grained access control) - ESO just keeps a synced copy in-cluster, so nothing sensitive has to be manually created or committed to Git.

What does the sync flow look like?
> You define an `ExternalSecret` resource pointing at a path in the external store, ESO polls that store on an interval, and it creates/updates a native Kubernetes Secret to match - your Pods consume it exactly like any other Secret.

---

## Part 8: The Proper Secrets Flow

What does a "proper" end-to-end secrets flow look like?
> Secret is created and stored in an external secrets manager -> ESO (or similar) syncs it into the cluster as a native Secret -> the Pod mounts/consumes that Secret as normal -> the actual sensitive value is never written to Git, never manually typed into `kubectl`, and centrally rotatable at the source.

Why does this matter for GitOps?
> GitOps tooling (e.g. ArgoCD, Flux) applies everything from Git - if raw Secrets lived in Git, they'd be plaintext in your repo history forever. Syncing operators like ESO let you commit the *reference* to a secret, not the secret itself.

---

## Part 9: Why We Need Sealed Secrets

What problem do Sealed Secrets solve?
> The same core problem as ESO - keeping actual secret values out of Git - but by encrypting the secret itself so it's safe to commit, rather than syncing from an external store.

Why not just commit a regular Secret's YAML to Git?
> A Secret's value is only base64-encoded, not encrypted - committing it to Git means anyone with repo access (and anyone in its history, forever) has the plaintext value.

---

## Part 10: Sealed Secrets

What is Sealed Secrets?
> A tool (by Bitnami) with two parts: a controller running in-cluster holding a private key, and a `kubeseal` CLI that encrypts a Secret into a `SealedSecret` using the matching public key - safe to commit to Git since only the in-cluster controller can decrypt it.

What happens after a SealedSecret is applied to the cluster?
> The controller decrypts it using its private key and creates a normal native Secret from it - from that point on, Pods consume it exactly like any other Secret.

What's the tradeoff of this approach?
> The encrypted SealedSecret is genuinely safe in Git, but it's tied to one cluster's private key - move to a new cluster and you lose the ability to decrypt existing SealedSecrets unless the key is migrated too.

---

## Part 11: Sealed Secrets vs External Secrets

| | Sealed Secrets | External Secrets Operator |
|---|---|---|
| Source of truth | The encrypted SealedSecret in Git | An external secrets manager (Vault, AWS, etc.) |
| What's in Git | The encrypted secret itself | Just a reference to where the real secret lives |
| Rotation | Manual - re-encrypt and recommit | Centralised in the external store, synced automatically |
| Best fit | Simple setups, no existing secrets manager | Teams already using a secrets manager, needing rotation/audit |

---

## Lab: Config & Secrets in Practice

**Goal:** Create a ConfigMap and a Secret, mount both into a Pod, and confirm the app can read each.

```bash
# 1. Create a ConfigMap
kubectl create configmap app-config --from-literal=APP_MODE=production

# 2. Create a Secret
kubectl create secret generic db-secret --from-literal=password=hunter2
```

```yaml
# 3. pod.yaml - consume both, one as env var, one as a mounted file
apiVersion: v1
kind: Pod
metadata:
  name: config-secret-demo
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "echo $APP_MODE && cat /etc/secret/password && sleep 3600"]
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
      volumeMounts:
        - name: secret-vol
          mountPath: /etc/secret
          readOnly: true
  volumes:
    - name: secret-vol
      secret:
        secretName: db-secret
```

```bash
# 4. Apply and verify
kubectl apply -f pod.yaml
kubectl logs config-secret-demo
# Expect: "production" printed from the env var, then "hunter2" read from the mounted file
```

```bash
# 5. Clean up
kubectl delete pod config-secret-demo
kubectl delete configmap app-config
kubectl delete secret db-secret
```

---

## Commands to Learn

```bash
# Create a ConfigMap from literals or a file
kubectl create configmap app-config --from-literal=KEY=value
kubectl create configmap app-config --from-file=config.properties
```

```bash
# Create a Secret from literals
kubectl create secret generic db-secret --from-literal=password=hunter2
```

```bash
# List and inspect ConfigMaps/Secrets
kubectl get configmaps
kubectl get secrets
kubectl describe secret db-secret
```

```bash
# Decode a Secret value manually
kubectl get secret db-secret -o jsonpath='{.data.password}' | base64 -d
```
