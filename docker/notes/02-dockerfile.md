# Dockerfile

## What is a Dockerfile?

## Instructions

### FROM

### WORKDIR

### COPY / ADD

### RUN

### ENV / ARG

### EXPOSE

### CMD / ENTRYPOINT

#### Difference between CMD and ENTRYPOINT

## Build

```bash
docker build -t <name>:<tag> .
```

## Layer Caching

## Multi-Stage Builds

### What are they?

### When to use them?

### Example structure

```dockerfile
# Stage 1 - Build
FROM ...

# Stage 2 - Runtime
FROM ...
```
