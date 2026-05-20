# DevOps - GitHub Actions

Learning CI/CD by building real pipelines with GitHub Actions.

## Structure

```
.
├── .github/workflows/ci.yml     # Active pipeline: tests + Docker build/push
├── lab/
│   └── 01-docker-pipeline/      # Flask app containerized and deployed via Actions
├── workflow-examples/
│   ├── 01-basics/               # Simple push-triggered workflow
│   ├── 02-matrix/               # Matrix strategy across Python versions
│   ├── 03-secrets/              # Using encrypted secrets
│   └── 04-manual-trigger/       # workflow_dispatch trigger
└── notes/README.md              # GitHub Actions reference notes
```

## Labs

### Lab 01 - Docker Pipeline

Builds a Flask app, runs tests and linting, then builds and pushes a Docker image to Docker Hub.

Pipeline stages:

1. **tests** - installs dependencies, runs pytest and Ruff linter
2. **docker** - logs into Docker Hub, builds image with Buildx, pushes to registry

The `docker` job only runs if `tests` passes (`needs: tests`).

Tools: `actions/checkout`, `docker/login-action`, `docker/setup-buildx-action`, `docker/build-push-action`

## Workflow Examples

| Folder | Concept |
|--------|---------|
| `01-basics` | Minimal workflow triggered on push |
| `02-matrix` | Run the same job across multiple Python versions in parallel |
| `03-secrets` | Access encrypted secrets inside a workflow |
| `04-manual-trigger` | Add a manual "Run workflow" button via `workflow_dispatch` |

## Notes

See [notes/README.md](notes/README.md) for a reference guide covering:
- Workflow structure and triggers
- Jobs, steps, and runners
- Contexts and expressions
- Secrets and variables
- Matrix strategy
- Marketplace actions and common patterns
