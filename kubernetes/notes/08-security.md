# 8. Security in Kubernetes

---

## Part 1: The K8s API Security Chain

What happens to every request that hits the Kubernetes API server?
> It passes through three sequential stages before anything happens: 
> - **Authentication** (who are you), 
> - **Authorisation** (what are you allowed to do), 
> - **Admission Control** (should this specific request be allowed/modified, even if authorised).

Why does the order matter?
> Each stage can reject the request outright - an unauthenticated request never reaches authorisation, and an unauthorised request never reaches admission control. Only requests that pass all three actually get persisted to etcd.

---

## Part 2: Authentication - "Who Are You?"

What is authentication responsible for?
> Establishing *identity* - confirming who (or what) is making the request, with no opinion yet on what they're allowed to do.

What are the common ways a request authenticates to the API server?
> - **Client certificates** - the traditional method for users and control plane components.
> - **Service account tokens** - how Pods authenticate as themselves.
> - **OIDC tokens** - integrating with an external identity provider (e.g. Google, Okta, AWS IAM via EKS).
> - **Static tokens/basic auth** - legacy methods, discouraged in modern clusters.

Does Kubernetes have its own user database?
> No - there's no `User` object in the API. Kubernetes only ever sees an identity's certificate/token and trusts whatever external system authenticated it (a CA, an OIDC provider, etc.).

---

## Part 3: Authorisation - "What Can You Do?"

What is authorisation responsible for?
> Once identity is established, deciding whether that identity is allowed to perform the specific action being requested (e.g. `get pods` in namespace `prod`).

What authorisation modes does Kubernetes support?
> - **RBAC** (Role-Based Access Control) - the standard, most widely used mode.
> - **ABAC** (Attribute-Based Access Control) - older, policy-file based, rarely used now.
> - **Webhook** - delegates the authorisation decision to an external service.
> - **Node** - a special-purpose mode authorising kubelet requests specifically.

Which mode does virtually every modern cluster use?
> RBAC - it's the default and the one worth learning in depth.

---

## Part 4: Understanding RBAC

What are the four core RBAC objects?
> - **Role** - a set of permissions, scoped to one namespace.
> - **ClusterRole** - the same, but cluster-wide (or reusable across namespaces).
> - **RoleBinding** - grants a Role (or ClusterRole) to a user/group/ServiceAccount, within one namespace.
> - **ClusterRoleBinding** - grants a ClusterRole cluster-wide.

What does a Role actually contain?
> A list of rules, each specifying `apiGroups`, `resources`, and `verbs` (get, list, watch, create, update, delete, etc.) - defining exactly which actions are permitted on which resource types.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

Why use a ClusterRole + RoleBinding combo instead of just a Role?
> A common pattern - define reusable permission sets as ClusterRoles (e.g. a generic "view" role), then bind them per-namespace via RoleBindings, avoiding duplicate Role definitions across every namespace.

What's the default behaviour if no Role/binding grants an action?
> Deny - RBAC is default-deny; without an explicit binding granting a permission, it's not allowed.

---

## Part 5: Service Accounts

What is a ServiceAccount?
> An identity for **processes running inside Pods**, distinct from human user identities - it's how a Pod authenticates to the API server when it needs to call it.

Does every Pod have a ServiceAccount?
> Yes - if none is specified, it uses the namespace's `default` ServiceAccount automatically.

How does a Pod actually use its ServiceAccount to talk to the API?
> The token is automatically mounted into the Pod's filesystem (typically `/var/run/secrets/kubernetes.io/serviceaccount/token`), which any in-cluster client library reads to authenticate API calls.

How do you grant a ServiceAccount specific permissions?
> The same way as any identity - a RoleBinding or ClusterRoleBinding referencing the ServiceAccount as its subject.

---

## Part 6: Real-World Use of Service Accounts

Why shouldn't every Pod just use the `default` ServiceAccount?
> The `default` ServiceAccount is shared cluster-wide within a namespace - if it's overly permissioned, every Pod in that namespace inherits those permissions, even ones that never call the API at all.

What's the recommended practice?
> Create a dedicated ServiceAccount per application with only the permissions it actually needs, and disable automatic token mounting (`automountServiceAccountToken: false`) for Pods that never call the API at all.

Give a real-world example.
> A CI/CD controller running in-cluster (e.g. ArgoCD) needs a ServiceAccount with broad permissions to deploy resources across namespaces, while a simple stateless web app's Pod needs none of that - giving both the same permissions would be a real privilege-escalation risk if the web app were ever compromised.

How does this connect to cloud IAM?
> Many cloud providers let you map a Kubernetes ServiceAccount to a cloud IAM role (e.g. AWS's IRSA, GCP's Workload Identity) - letting a Pod securely call cloud APIs without static cloud credentials baked into the image or a Secret.

---

## Part 7: Pod Security Standards

What problem do Pod Security Standards solve?
> Left unrestricted, a Pod can request dangerous capabilities - running as root, mounting the host filesystem, gaining host network access - any of which can be used to escape the container and compromise the node.

What are the three predefined policy levels?
> - **Privileged** - unrestricted, no security controls enforced.
> - **Baseline** - blocks the most obviously dangerous settings (e.g. host namespaces, privileged containers), while staying broadly compatible.
> - **Restricted** - heavily locked down, enforcing security best practices (non-root, no privilege escalation, dropped capabilities).

How are Pod Security Standards enforced?
> Via the built-in **Pod Security Admission** controller, configured per-namespace with a label (e.g. `pod-security.kubernetes.io/enforce: restricted`) - it replaced the older, now-removed PodSecurityPolicy object.

---

## Part 8: Network Policies & Zero Trust Networking

What is Zero Trust networking, conceptually?
> The principle that nothing is trusted by default just because it's "inside" the network - every connection must be explicitly allowed, regardless of where it originates.

How does this relate to Kubernetes's default networking behaviour?
> It's the opposite of the default - out of the box, every Pod can reach every other Pod ([notes/06 Part 7](06-networking.md#part-7-network-policies)). Applying Zero Trust means using NetworkPolicies to deny all traffic by default, then explicitly allowing only the specific Pod-to-Pod paths an application actually needs.

What does a default-deny NetworkPolicy look like?
> ```yaml
> apiVersion: networking.k8s.io/v1
> kind: NetworkPolicy
> metadata:
>   name: default-deny-all
> spec:
>   podSelector: {}
>   policyTypes: ["Ingress", "Egress"]
> ```

---

## Part 9: Admission Controllers Overview

What is an admission controller?
> A piece of code that intercepts requests to the API server after authentication and authorisation, but before the object is persisted - able to **validate** (accept/reject) or **mutate** (modify) the request.

What are the two categories of admission webhooks?
> - **MutatingAdmissionWebhook** - runs first, can modify the object (e.g. injecting a sidecar container automatically).
> - **ValidatingAdmissionWebhook** - runs after mutation, can only accept or reject, not modify.

Give examples of what admission control is used for.
> - Enforcing Pod Security Standards (Part 7).
> - Automatically injecting a service mesh sidecar (Istio does this via a mutating webhook).
> - Enforcing custom organisational policy (e.g. "every Pod must have a `team` label") via a policy engine.

---

## Part 10: Policy Engines - OPA Gatekeeper vs Kyverno

How do policy engines relate to the admission controllers from Part 9?
> They aren't a separate mechanism - they're policy engines packaged as ready-made webhook servers, registered as the same ValidatingAdmissionWebhook/MutatingAdmissionWebhook types. Installing Gatekeeper or Kyverno deploys a pod and a WebhookConfiguration that tells the apiserver to call it, so your custom policy runs through the exact same admission path built-in controllers use.

What problem do policy engines solve that built-in admission control doesn't?
> Built-in admission controllers are fixed, compiled-in behaviours - policy engines let you define **custom** validating/mutating rules declaratively, without writing and deploying your own webhook server from scratch.

| | OPA Gatekeeper | Kyverno |
|---|---|---|
| Policy language | Rego (general-purpose policy language) | Plain YAML |
| Learning curve | Steeper - Rego is its own DSL | Gentler - feels native to Kubernetes users |
| Scope | General-purpose, used beyond Kubernetes too | Kubernetes-native only |
| Common use | Complex, cross-cutting policy logic | Straightforward validate/mutate/generate rules |

Give an example of a policy either could enforce.
> "Every Deployment must set resource requests and limits" or "no container image may use the `latest` tag" - both expressible as either a Gatekeeper ConstraintTemplate or a Kyverno ClusterPolicy.

---

## Part 11: Secrets Encryption at Rest

Are Kubernetes Secrets encrypted in etcd by default?
> No - see [notes/05 Part 6](05-config-and-secrets-management.md#part-6-the-reality-of-kubernetes-secrets). By default they're only base64-encoded, and etcd itself is not encrypted unless explicitly configured.

How do you actually enable encryption at rest?
> Configure an `EncryptionConfiguration` on the API server, specifying a provider (e.g. `aescbc`, or a KMS provider backed by a cloud key management service) - the API server then transparently encrypts Secret data before writing it to etcd.

What is the KMS provider option, and why prefer it?
> Instead of the API server managing the raw encryption key itself, KMS delegates to an external key management service (AWS KMS, GCP Cloud KMS, Vault) - centralising key rotation, auditing, and access control outside the cluster.

Does enabling encryption at rest change how a Pod consumes a Secret?
> No - it's entirely transparent to Pods and the API; only the on-disk etcd representation changes, not how Secrets are created, read, or mounted.

---

## Part 12: Defence in Depth in Kubernetes

What does "defence in depth" mean here?
> No single control is assumed to be sufficient - security is layered, so that if one control fails or is bypassed, others still limit the damage.

What do the layers covered in this file look like stacked together?
> - **Authentication** - confirms identity before anything else is considered.
> - **RBAC (Authorisation)** - limits what an authenticated identity can do via the API.
> - **Admission Control / Policy Engines** - enforces organisational rules on top of raw permissions.
> - **Pod Security Standards** - restricts what a Pod itself is allowed to do at runtime.
> - **Network Policies / Zero Trust** - limits what a running Pod can reach over the network.
> - **Secrets Encryption at Rest** - protects sensitive data even if the underlying storage is compromised.

Why does layering matter in practice?
> A compromised Pod with an overly-permissioned ServiceAccount is far less damaging if NetworkPolicies also block it from reaching sensitive services, and Pod Security Standards prevented it from escaping to the host in the first place - each layer catches what the others might miss.

---

## Commands to Learn

```bash
# Check what actions your current identity can perform
kubectl auth can-i create pods --namespace default
kubectl auth can-i --list
```

```bash
# List Roles/ClusterRoles and their bindings
kubectl get roles,rolebindings -n default
kubectl get clusterroles,clusterrolebindings
```

```bash
# Inspect a ServiceAccount and what it's bound to
kubectl get serviceaccount my-app-sa -o yaml
kubectl describe rolebinding my-app-binding
```

```bash
# Check which Pod Security Standard level applies to a namespace
kubectl get ns default -o jsonpath='{.metadata.labels}'
```

```bash
# List installed admission webhooks
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations
```

```bash
# List Kyverno or Gatekeeper policies (whichever is installed)
kubectl get clusterpolicies
kubectl get constrainttemplates
```
