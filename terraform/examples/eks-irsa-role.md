# IRSA - IAM Role for a Kubernetes ServiceAccount

Reference example: an IAM role that a specific Kubernetes ServiceAccount on an EKS cluster can assume directly - no static AWS credentials stored in the cluster, no node-wide IAM role shared by every pod. This is the standard pattern behind things like `cluster-autoscaler`, the AWS Load Balancer Controller, and the EBS CSI driver all needing their own scoped AWS permissions.

## Why this, not a normal IAM role

A normal IAM role's trust policy just says "an AWS principal can assume this." IRSA's trust policy is federated to the cluster's **OIDC provider** instead, and scoped down to one exact namespace + ServiceAccount pair via a condition on the token's `sub` claim - see `main.tf` below. Any other ServiceAccount, in any other namespace, cannot assume this role, even though they're all part of the same cluster and share the same OIDC provider.

The `aud` (audience) condition alongside it is the detail a lot of tutorials skip - without it, the trust policy only checks *who* the token claims to be (`sub`), not *what it was issued for*. Requiring `aud = sts.amazonaws.com` confirms the token was actually minted for an AWS STS call, not some other purpose.

## Code

`providers.tf`:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.41.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

`variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region the EKS cluster lives in"
  type        = string
  default     = "eu-west-2"
}

variable "role_name" {
  description = "Name for the IAM role a Kubernetes ServiceAccount will assume"
  type        = string
}

variable "oidc_provider_arn" {
  description = "ARN of the EKS cluster's IAM OIDC provider (aws eks describe-cluster + aws iam list-open-id-connect-providers)"
  type        = string
}

variable "oidc_provider_url" {
  description = "The OIDC issuer URL, without the leading https:// (e.g. oidc.eks.eu-west-2.amazonaws.com/id/EXAMPLE123)"
  type        = string
}

variable "namespace" {
  description = "Kubernetes namespace the ServiceAccount lives in"
  type        = string
}

variable "service_account_name" {
  description = "Name of the Kubernetes ServiceAccount this role is scoped to"
  type        = string
}

variable "policy_arns" {
  description = "AWS managed or customer-managed policy ARNs to attach to the role - e.g. AmazonEBSCSIDriverPolicy"
  type        = list(string)
  default     = []
}
```

`main.tf`:

```hcl
# Trust policy: allows a specific k8s ServiceAccount (identified via the OIDC token
# it presents) to assume this role - not just anyone with the cluster's OIDC provider ARN.
data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    # "sub" scopes this to one exact namespace + ServiceAccount pair.
    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${var.service_account_name}"]
    }

    # "aud" confirms the token was actually issued for AWS STS, not some other
    # audience - without this, the trust policy is broader than intended.
    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

# Attach whatever permissions this ServiceAccount actually needs - deliberately
# left as a list so the same role definition works for any use case
# (cluster-autoscaler, aws-load-balancer-controller, ebs-csi-driver, ...).
resource "aws_iam_role_policy_attachment" "this" {
  for_each = toset(var.policy_arns)

  role       = aws_iam_role.this.name
  policy_arn = each.value
}
```

`outputs.tf`:

```hcl
output "role_arn" {
  description = "Annotate a k8s ServiceAccount with eks.amazonaws.com/role-arn set to this value"
  value       = aws_iam_role.this.arn
}
```

## Getting the two OIDC variables from a real cluster

`oidc_provider_arn` and `oidc_provider_url` aren't invented - they come from the actual EKS cluster:

```bash
# The issuer URL (this becomes oidc_provider_url, minus the https:// prefix)
aws eks describe-cluster --name <cluster-name> \
  --query "cluster.identity.oidc.issuer" --output text

# The IAM OIDC provider ARN (this becomes oidc_provider_arn) - only exists if
# the cluster already has an OIDC provider registered in IAM
aws iam list-open-id-connect-providers
```

If no OIDC provider is registered yet for the cluster, it needs to be created first - typically via `eksctl utils associate-iam-oidc-provider` or an `aws_iam_openid_connect_provider` resource.

## Usage

```hcl
module "ebs_csi_irsa" {
  source = "../examples/eks-irsa-role"

  role_name             = "ebs-csi-driver-irsa"
  oidc_provider_arn     = "arn:aws:iam::123456789012:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/EXAMPLE123"
  oidc_provider_url     = "oidc.eks.eu-west-2.amazonaws.com/id/EXAMPLE123"
  namespace             = "kube-system"
  service_account_name  = "ebs-csi-controller-sa"
  policy_arns           = ["arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"]
}
```

Then on the Kubernetes side, the ServiceAccount needs the matching annotation (this is what actually wires the two together at runtime):

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebs-csi-controller-sa
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: <output.role_arn from this module>
```

## Verified

This code has been checked with `terraform validate` and `terraform plan` (using placeholder OIDC values) - both succeeded, and the plan output showed exactly the trust policy JSON described above (correct `sub`/`aud` conditions, correct `Federated` principal). It hasn't been applied against a real cluster.
