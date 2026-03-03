# Dockerfile

## What is a Dockerfile?
A text-based document that is used to create a container image. It provides instructions (like a blueprint) to the image builder on the commands to run, files to copy, startup command and more.

## Instructions

### FROM
Specifies the base image that the buiild will extend. Every Dockerfile starts with this.
```dockerfile
FROM <image>[:<tag>]

#Example:
FROM ubuntu:22.04
```

### WORKDIR
Sets the working directory inside the container for subsequen instructions.
```dockerfile
WORKDIR /app

# Creates the dirtectory if it doesn't exist
# ALL RUN, COPY, CMD paths are relative to this
```

### COPY / ADD
Copes files from your host into the image.
```dockerfile
COPY <src> <dest>

#Example:
# Install the application dependencies
COPY requirements.txt ./

# ADD is like COPY but also:
# - auto-extracts .tar files
# - can fetch remote URLs (avoid this, use curl in RUN instead)
```

### RUN
Executes a commmand during the build (creates a new layer).
```dockerfile
RUN <command>

#Example:
RUN apt-get update && apt-get install -y curl
RUN npm install
RUN go build -o app .

# Chain commands with && to minimize layers
```

### ENV / ARG
Sets an environment variable that a running container will use.
```dockerfile
#Example:
ENV NODE_ENV=production
ENV PORT=3000

# ARG - build-time variables only (not available in the running container)
ARG VERSION=1.0
```

### EXPOSE
This instruction sets configuration on the image that indicates a port the image would like to expose.
```dockerfile
#Example:
EXPOSE 3000
EXPOSE 8080/tcp
```

### CMD / ENTRYPOINT
CMD sets the default command to run when a container starts and can be overridden at runtime.
ENTRYPOINT sets the fixed executable that always runs when the container starts.
```dockerfile
# CMD - default command to run when container starts (can be overridden)
CMD ["node", "server.js"]

# ENTRYPOINT - sets the main executable (harder to override)
ENTRYPOINT ["./app"]

# Common pattern: ENTRYPOINT defines the executable, CMD provides default args
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```


#### Difference between CMD and ENTRYPOINT
| | CMD | ENTRYPOINT |
|---|---|---|
| Purpose | Default args/command | Fixed executable |
| Override | `docker run image <cmd>` replaces it | `docker run --entrypoint` to replace |
| Use case | Flexible defaults | Always-run binaries |

## Build
Builds an image from a Dockerfile in the current directory.
- `-t` tags the image with a name and optional tag
- `.` sets the build context (files Docker can access during build)
```bash
docker build -t <name>:<tag> .
```

## Layer Caching
Each instruction in a Dockerfile creates a layer. Docker caches these layers and reuses them on subsequent builds if nothing has changed. If a layer changes, all layers after it are rebuilt.

Best practice: order instructions from least-changed to most-changed.

```dockerfile
# Good - source code changes don't trigger npm install
COPY package.json ./
RUN npm install
COPY . .

# Bad - any source code change forces npm install to rerun
COPY . .
RUN npm install
```

## Multi-Stage Builds

### What are they?
A way to use multiple FROM instructions in one Dockerfile. Each FROM starts
a new stage. You can copy artifacts from one stage to another, leaving behind
everything you don't need (build tools, compilers, source code).

### When to use them?
- Compiled languages (Go, Java, Rust, C++) - compile in one stage, run in another
- When you want a small final image without build dependencies
- When you want to separate build/test/runtime environments

### Example structure
```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o app .

# Stage 2: Production
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/app .
CMD ["./app"]
```
