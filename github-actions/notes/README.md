# GitHub Actions Notes

## Contents

1. [Core Concepts](#core-concepts)
2. [Workflow Structure](#workflow-structure)
3. [Triggers (on)](#triggers-on)
4. [Jobs](#jobs)
5. [Steps](#steps)
6. [Runners](#runners)
7. [Contexts and Expressions](#contexts-and-expressions)
8. [Secrets and Variables](#secrets-and-variables)
9. [Common Patterns](#common-patterns)

---

## Core Concepts

GitHub Actions is a CI/CD platform built into GitHub. It lets you automate tasks in response to events in your repository.

| Term | Description |
|------|-------------|
| **Workflow** | A YAML file that defines automation - lives in `.github/workflows/` |
| **Event** | What triggers the workflow (push, PR, schedule, manual) |
| **Job** | A unit of work inside a workflow - runs on a runner |
| **Step** | An individual task inside a job - runs a command or an action |
| **Action** | A reusable unit of code (from the marketplace or your own) |
| **Runner** | The machine that executes jobs (GitHub-hosted or self-hosted) |

Workflows run in response to events. Events trigger jobs. Jobs contain steps. Steps run commands or actions.

---

## Workflow Structure

Workflows live in `.github/workflows/<name>.yml`.

```yaml
name: My Workflow           # displayed in the Actions tab

on:                         # what triggers this workflow
  push:
    branches: [main]

jobs:
  my-job:                   # job ID (your name for it)
    runs-on: ubuntu-latest  # runner to use
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run a command
        run: echo "Hello"
```

---

## Triggers (on)

Controls when the workflow runs.

```yaml
on:
  push:                        # runs on every push
    branches: [main, develop]  # only these branches
    paths: ['**.tf']           # only when .tf files change

  pull_request:                # runs when a PR is opened or updated
    branches: [main]

  schedule:
    - cron: '0 9 * * 1'       # every Monday at 9am UTC

  workflow_dispatch:           # adds a manual "Run workflow" button in GitHub UI
```

> `paths` is useful for monorepos - only trigger when relevant files change.

---

## Jobs

Jobs run in parallel by default. Use `needs` to make one wait for another.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "building"

  deploy:
    runs-on: ubuntu-latest
    needs: build              # waits for build to succeed before running
    steps:
      - run: echo "deploying"
```

---

## Steps

Each step runs in sequence within a job. A failed step stops the job.

```yaml
steps:
  - name: Checkout code             # uses a marketplace action
    uses: actions/checkout@v4

  - name: Run shell command         # runs a shell command directly
    run: terraform validate

  - name: Multi-line command
    run: |
      terraform init
      terraform plan

  - name: Set env var for next steps
    run: echo "TF_ENV=dev" >> $GITHUB_ENV
```

> `uses` pulls in a pre-built action. `run` executes shell commands directly.

---

## Runners

The machine that executes a job.

| Runner | Description |
|--------|-------------|
| `ubuntu-latest` | GitHub-hosted Ubuntu (most common) |
| `windows-latest` | GitHub-hosted Windows |
| `macos-latest` | GitHub-hosted macOS |
| `self-hosted` | Your own machine or server |

GitHub-hosted runners come with common tools pre-installed (git, Docker, Terraform, AWS CLI).

---

## Contexts and Expressions

Contexts give you access to information about the run, repo, and environment.

```yaml
steps:
  - run: echo "Branch is ${{ github.ref_name }}"
  - run: echo "Triggered by ${{ github.actor }}"
  - run: echo "Repo is ${{ github.repository }}"
```

Common contexts:

| Context | Example | Description |
|---------|---------|-------------|
| `github.ref_name` | `main` | Branch or tag name |
| `github.sha` | `abc1234` | Commit SHA |
| `github.actor` | `ei-sei` | User who triggered the run |
| `github.event_name` | `push` | Event that triggered the workflow |

---

## Secrets and Variables

Secrets are encrypted values stored in GitHub (Settings - Secrets and variables).

```yaml
steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      aws-region:            eu-west-2
```

> Never hardcode credentials. Secrets are masked in logs - if a secret appears in output, GitHub replaces it with `***`.

Variables (non-sensitive) can be set at repo or environment level and accessed via `${{ vars.MY_VAR }}`.

---

## Common Patterns

### Terraform validate on push

```yaml
name: Terraform Validate

on:
  push:
    paths: ['**.tf']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - run: terraform init
        working-directory: lab/01-wordpress/my-terraform-wordpress-project

      - run: terraform validate
        working-directory: lab/01-wordpress/my-terraform-wordpress-project
```

### Only run on PR to main

```yaml
on:
  pull_request:
    branches: [main]
```

### Conditional step

```yaml
- name: Only on main
  if: github.ref_name == 'main'
  run: echo "This is main"
```
