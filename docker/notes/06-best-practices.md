# Best Practices

## Image Optimisation

### Use minimal base images
Start with the smallest image that works for your app. Smaller images build faster, pull faster, and have a smaller attack surface.
```dockerfile
# Instead of full Ubuntu
FROM ubuntu

# Use slim or alpine variants
FROM python:3.11-slim
FROM node:20-alpine
```

### Reduce layers
Each `RUN`, `COPY`, and `ADD` creates a layer. Chain related commands together to keep the image smaller.
```dockerfile
# Bad - creates 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good - creates 1 layer
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

### Order instructions for cache efficiency
Put things that change rarely at the top, and things that change often at the bottom. This way Docker can reuse cached layers and only rebuild what changed.
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./      # rarely changes - cached
RUN pip install -r requirements.txt
COPY . .                      # changes often - rebuilt last
CMD ["python", "app.py"]
```

### Clean up in the same layer
If you install something and then delete temporary files, do it in the same `RUN` command. If you split it into two, the files still exist in the first layer.
```dockerfile
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
```

## .dockerignore
Like `.gitignore`, this tells Docker what to exclude from the build context. This speeds up builds and prevents sensitive files from ending up in the image.
```
# .dockerignore
.git
.env
node_modules
__pycache__
*.pyc
*.log
```

## Security

### Run as non-root user
By default containers run as root, which is a security risk. Create a dedicated user and switch to it.
```dockerfile
RUN useradd -m appuser
USER appuser
```

### Avoid storing secrets in images
Never put passwords, API keys, or tokens in your Dockerfile or image. Use environment variables or secret management tools instead.
```dockerfile
# Bad - secret is baked into the image
ENV DB_PASSWORD=mysecret

# Good - inject at runtime via Compose or docker run
ENV DB_PASSWORD=""
```

### Scan images for vulnerabilities
Use tools like `docker scout` to check your images for known security issues.
```bash
docker scout cves my-image:latest
```

## Tagging Strategy

### Avoid using `latest` in production
`latest` is ambiguous and can break things when a new version is pushed. Always use specific version tags in production.
```bash
# Bad
docker pull my-app:latest

# Good
docker pull my-app:1.4.2
```

### Semantic versioning
Tag images with meaningful version numbers so you can roll back if something breaks.
```bash
docker build -t my-app:1.4.2 .
docker build -t my-app:1.4 .    # also tag the minor version
```

## Logging & Observability
Write logs to stdout and stderr instead of files. Docker captures these automatically and you can view them with `docker logs` or forward them to a logging service.
```python
# Good - logs go to stdout, Docker captures them
print("Server started")

# Avoid writing logs to files inside the container
# They won't persist and are harder to access
```

```bash
docker logs my-container          # view logs
docker logs -f my-container       # follow logs in real time
docker logs --tail 50 my-container  # last 50 lines
```

## Multi-Stage Builds for Production
Use multi-stage builds to keep the final image lean. Build in one stage, copy only the output to the final stage.
```dockerfile
# Stage 1: Build
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production - only copy the built output
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

The final image has no source code, dev dependencies, or build tools - just what's needed to run.
