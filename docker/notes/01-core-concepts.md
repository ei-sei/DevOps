# DOCKER CORE CONCEPTS

---

## 1. What is Docker?

### The Problem It Solves

**"Works on my machine"** - Your app runs locally but fails in production because:
- Different OS
- Different library versions
- Missing dependencies
- Environment variables misaligned

Docker solves this by **bundling your app + all dependencies into a container** that runs identically everywhere.

```
┌─────────────────────────────────────────────────────┐
│ WITHOUT DOCKER                                      │
│                                                     │
│ My Laptop          Production Server                │
│ ┌──────────┐      ┌──────────┐                      │
│ │ Python   │      │ Python   │  ← Different!        │
│ │ 3.9      │      │ 3.11     │                      │
│ ├──────────┤      ├──────────┤                      │
│ │ Flask    │      │ Flask    │  ← Version clash     │
│ │ 2.0      │      │ 3.0      │                      │
│ ├──────────┤      ├──────────┤                      │
│ │ Works    │      │ Broken   │                      │
│ └──────────┘      └──────────┘                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ WITH DOCKER                                         │
│                                                     │
│ My Laptop          Production Server                │
│ ┌──────────────┐  ┌──────────────┐                  │
│ │ CONTAINER    │  │ CONTAINER    │  ← Identical     │
│ │ Python 3.9   │  │ Python 3.9   │                  │
│ │ Flask 2.0    │  │ Flask 2.0    │                  │
│ │ + all deps   │  │ + all deps   │                  │
│ │              │  │              │                  │
│ │ Works        │  │ Works        │                  │
│ └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────┘
```

---

### Containers vs VMs - Key Distinction

| | Container | VM |
|---|---|---|
| **Virtualisation Level** | OS-level (processes) | Hardware-level (full OS) |
| **Size** | 10-100 MB | 1-10 GB |
| **Startup Time** | Milliseconds | Seconds/Minutes |
| **Performance** | Native (minimal overhead) | Slower (emulation layer) |
| **Isolation** | Process isolation via namespaces | Complete OS isolation |
| **Density** | 100s per host | 10s per host |


![comparison](/assets/containers-vs-VMs.png)


**Rule of thumb:**
- **Containers** = Process-level isolation (fast, lightweight)
- **VMs** = Complete OS isolation (safer, heavier)

---

### How Docker Fits into DevOps/SRE Workflow

```
┌─────────────────────────────────────────────────────┐
│ APPLICATION LIFECYCLE                               │
│                                                     │
│ 1. DEVELOPMENT                                      │
│    ┌──────────────────────────────────────────┐     │
│    │ Write code → Test in container locally   │     │
│    │ docker run -it myapp:dev                 │     │
│    └──────────────────────────────────────────┘     │
│                  │                                  │
│                  ▼                                  │
│ 2. BUILD                                            │
│    ┌──────────────────────────────────────────┐     │
│    │ docker build → Push to registry          │     │
│    │ myapp:1.0.0 pushed to Docker Hub/ECR     │     │
│    └──────────────────────────────────────────┘     │
│                  │                                  │
│                  ▼                                  │
│ 3. DEPLOY                                           │
│    ┌──────────────────────────────────────────┐     │
│    │ Orchestrator (Kubernetes, Docker Swarm)  │     │
│    │ pulls image → runs container in prod     │     │
│    │ Automatic updates, scaling, health checks│     │
│    └──────────────────────────────────────────┘     │
│                  │                                  │
│                  ▼                                  │
│ 4. MONITOR & SCALE                                  │
│    ┌──────────────────────────────────────────┐     │
│    │ SRE monitors metrics (logs, errors)      │     │
│    │ Auto-scales containers based on load     │     │
│    │ Rollback or rolling updates on failures  │     │
│    └──────────────────────────────────────────┘     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Why DevOps/SRE love Docker:**
- **Consistency**: Same image in dev, staging, production
- **Scalability**: Spin up 1 container or 1000 in seconds
- **Reliability**: Failed container? Orchestrator restarts it
- **Agility**: Deploy new versions in minutes, not hours

---

## 2. THE DOCKER ARCHITECTURE

### Docker Engine Overview

Docker isn't a single program, it's a **client-server architecture**:

![docker overview](/assets/docker-overview.png)

---

### Client-Server Model - How Docker CLI Talks to the Daemon

When you run `docker run nginx`:

```
┌──────────────┐
│ docker run   │  ← You type this
│   nginx      │
└──────┬───────┘
       │
       │ 1. CLI sends request via socket
       │    (Unix socket: /var/run/docker.sock)
       ▼
┌──────────────────────────────────────┐
│  Docker Daemon (dockerd)             │
│  Listens on socket                   │
│  Processes request                   │
└──────┬───────────────────────────────┘
       │
       │ 2. Daemon checks:
       │    - Is nginx image cached?
       │    - If not, pull from Docker Hub
       │    - Create container
       │    - Start container
       │
       │ 3. Return response to CLI
       ▼
┌──────────────┐
│ Container    │
│ running      │
│ (output)     │
└──────────────┘
```

**Key point:** The CLI and daemon don't have to be on the same machine. You can run `docker` on your laptop but control a daemon on a remote server.

![docker architecture](/assets/docker-architecture.png)

```bash
# Local daemon (default)
docker run nginx

# Remote daemon (via TCP or SSH)
docker -H tcp://192.168.1.100:2375 run nginx
docker -H ssh://user@remote.com run nginx
```

---

### containerd and runc - What They Are

You don't need deep knowledge yet, but good to know:

```
Docker CLI
    │
    ▼
Docker Daemon (dockerd)
    │
    ▼
containerd (container runtime)
    │  ← "Give me a container"
    ▼
runc (low-level runtime)
    │  ← Manages namespaces, cgroups, runs process
    ▼
Linux Kernel (creates isolated process)
```

**In simple terms:**
- **containerd** = "Container manager" (orchestrates containers)
- **runc** = "Container executor" (actually runs the process with isolation)

You'll rarely interact with these directly-Docker handles it for you. But they exist, and knowing they're there explains how Docker works under the hood.

---

## 3. CORE BUILDING BLOCKS

### Images - Read-Only Templates, Layered Filesystem

**Image** - A read-only blueprint containing your application, dependencies, and OS libraries. Think of it like a Git commit snapshot.

```
┌─────────────────────────────────────┐
│   DOCKER IMAGE (myapp:1.0)          │
│   Read-only, immutable              │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Base Layer (FROM ubuntu)    │    │
│  │ 50MB (OS + utils)           │    │
│  └─────────────────────────────┘    │
│           │                         │
│           ├─→ (cached on disk)      │
│           │                         │
│  ┌─────────────────────────────┐    │
│  │ Layer 2 (RUN apt-get)       │    │
│  │ +15MB (python, pip, etc)    │    │
│  └─────────────────────────────┘    │
│           │                         │
│           ├─→ (cached on disk)      │
│           │                         │
│  ┌─────────────────────────────┐    │
│  │ Layer 3 (COPY app code)     │    │
│  │ +5MB (your app files)       │    │
│  └─────────────────────────────┘    │
│           │                         │
│           ├─→ (cached on disk)      │
│           │                         │
│  ┌─────────────────────────────┐    │
│  │ Layer 4 (CMD python app.py) │    │
│  │ Config (what to run)        │    │
│  └─────────────────────────────┘    │
│                                     │
│  Total: ~70MB (shared across        │
│          containers)                │
└─────────────────────────────────────┘
```

**Key insight:** Layers are **cached**. If you rebuild and only Layer 4 changes, Docker reuses Layers 1-3 from cache (seconds, not minutes).

---

### Containers - Running Instance of an Image

**Container** - A writable instance created from an image. Think of it like a Git checkout.

```
┌──────────────────────────────┐
│ IMAGE (myapp:1.0)            │
│ (read-only on disk)          │
└──────────────┬───────────────┘
               │
        docker run
               │
               ▼
┌──────────────────────────────┐
│ CONTAINER (running)          │
│                              │
│ ┌─ Image layers (RO)         │
│ │  (base, dependencies, etc) │
│ │                            │
│ └─ Container Layer (RW)  ◄── Writable!
│    (changes, logs, etc)      │
│                              │
│ Process running              │
└──────────────────────────────┘
```

**You can:**
- Modify files (but changes disappear when container stops)
- View logs
- Execute commands inside
- See processes running

**You should NOT:**
- Manually modify running containers (rebuild the image instead)
- Expect changes to persist (use volumes for data)

---

### Dockerfile - Blueprint for Building Images

**Dockerfile** - A text file with instructions to build an image (like a recipe).

```
Dockerfile            docker build            Image
┌──────────┐          ─────────────►    ┌──────────────┐
│ FROM     │         (executes each     │              │
│ RUN      │          instruction)      │   myapp:1.0  │
│ COPY     │                            │              │
│ CMD      │                            └──────────────┘
└──────────┘
```

**Example Dockerfile:**
```dockerfile
FROM python:3.9-slim          # Start with Python 3.9 base
WORKDIR /app                  # Set working directory
COPY requirements.txt .       # Copy dependency file
RUN pip install -r requirements.txt  # Install dependencies
COPY . .                      # Copy app code
CMD ["python", "app.py"]      # What to run
```

More details on Dockerfile syntax in section 02. For now: **it's just instructions to assemble an image layer by layer**.

---

### Registry - Where Images Live

**Registry** - A server storing images (like npm for Node, PyPI for Python).

```
┌─────────────────────────────────────────┐
│         DOCKER REGISTRY                 │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ nginx   │  │ postgres│  │ myapp   │  │
│  │ :latest │  │ :15     │  │ :1.0.0  │  │
│  │ :1.25   │  │ :14     │  │ :0.9.8  │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│                                         │
│         Docker Hub, ECR, GCR            │
│      (public + private registries)      │
└─────────────────────────────────────────┘
           ▲              │
           │              │
  docker pull    docker push
           │              │
    Download      Upload image
```

**Common registries:**
- **Docker Hub** (`docker.io`) - Public images, free for public repos
- **AWS ECR** - Private, integrates with AWS
- **GCP GCR** - Private, integrates with Google Cloud
- **Azure ACR** - Private, integrates with Azure
- **Self-hosted** - Private registries you run yourself

**Example:**
```bash
docker pull nginx                    # From Docker Hub (default)
docker pull ghcr.io/myuser/myapp    # From GitHub Container Registry
docker pull 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0
```

---

## 4. THE CONTAINER LIFECYCLE

### States: create → start → run → stop → remove

```
         docker create
              │
              ▼
    ┌─────────────────┐
    │ CREATED         │
    │ (exists, not    │
    │  running)       │
    └────────┬────────┘
             │
      docker start
             │
             ▼
    ┌─────────────────┐         docker restart
    │ RUNNING         │◄──┐     (stop + start)
    │ (process is     │   │
    │  executing)     │   │
    └────────┬────────┘   │
             │            │
      docker stop         │
             │            │
             ▼            │
    ┌─────────────────┐   │
    │ STOPPED/EXITED  │───┘
    │ (not running,   │
    │  still exists)  │
    └────────┬────────┘
             │
      docker rm
             │
             ▼
    ┌─────────────────┐
    │ REMOVED/DELETED │
    │ (gone forever)  │
    └─────────────────┘
```

---

### Key Commands: docker run, docker ps, docker stop, docker rm

**docker run** - Create + start in one command:
```bash
docker run nginx
# Equivalent to:
# docker create nginx
# docker start <container_id>
```

**docker ps** - List running containers:
```bash
docker ps              # Running containers only
docker ps -a          # All containers (running + stopped)
```

**docker stop** - Gracefully stop (SIGTERM → wait 10s → SIGKILL):
```bash
docker stop <container_id>
```

**docker rm** - Remove stopped container:
```bash
docker rm <container_id>
docker rm -f <container_id>    # Force-remove even if running
```

---

### Difference Between docker run and docker start

| | docker run | docker start |
|---|---|---|
| **Creates container?** | Yes | No |
| **Starts container?** | Yes | Yes |
| **Image required?** | Yes | No |
| **Use case** | First time running | Restarting stopped container |

**Scenario:**
```bash
# First time
docker run nginx
# Creates new container, starts it

# Container stops, you want to restart
docker start <container_id>
# Restarts the same container (no new one created)

# Wrong:
docker run nginx     # Creates ANOTHER container (wasteful)
```

---

## 5. IMAGES DEEP DIVE

### Union Filesystem / Layer Caching

Docker images are built in **layers**. Each instruction in a Dockerfile creates a layer.

```
┌──────────────────────────────────────┐
│ Dockerfile:                          │
│ FROM ubuntu:22.04                    │
│ RUN apt-get update                   │
│ RUN apt-get install -y python3       │
│ COPY app.py /app/                    │
│ CMD ["python3", "/app/app.py"]       │
└──────────────────────────────────────┘
         │
         │ docker build
         ▼
┌──────────────────────────────────────┐
│ Image: myapp:1.0 (70MB)              │
│                                      │
│  Layer 1: ubuntu:22.04 (60MB)        │
│  ├─ /bin, /usr, /etc, /lib, ...      │
│  └─ (cached on disk)                 │
│                                      │
│  Layer 2: apt-get update +           │
│           apt-get install (8MB)      │
│  ├─ /usr/bin/python3                 │
│  └─ (cached on disk)                 │
│                                      │
│  Layer 3: COPY app.py (2MB)          │
│  ├─ /app/app.py                      │
│  └─ (cached on disk)                 │
│                                      │
│  Layer 4: CMD metadata               │
│  └─ (cached on disk)                 │
└──────────────────────────────────────┘
```

**How caching speeds up rebuilds:**

```bash
# First build: ~30 seconds
FROM ubuntu:22.04          # Layer 1 (pulled from registry) 20s
RUN apt-get update && install python3  # Layer 2 (executed) 10s
COPY app.py /app           # Layer 3 (executed) <1s

# Second build (only app.py changed): ~1 second
FROM ubuntu:22.04          # Layer 1 (CACHED) 0s
RUN apt-get update && install python3  # Layer 2 (CACHED) 0s
COPY app.py /app           # Layer 3 (rebuilds, app.py newer) <1s
```

**Why order matters:**
```dockerfile
# FAST: Change app code frequently
FROM ubuntu
RUN apt-get update && apt-get install -y python3  # Layer 2 cached
COPY app.py /app                                   # Layer 3 rebuilds

# SLOW: Every app code change rebuilds dependencies
FROM ubuntu
COPY app.py /app                                   # Layer 2 rebuilds
RUN apt-get update && apt-get install -y python3  # Layer 3 rebuilds
```

---

### docker pull, docker images, docker rmi

**docker pull** - Download image from registry:
```bash
docker pull nginx              # Download nginx:latest
docker pull nginx:1.25-alpine  # Download specific version
```

**docker images** - List images on your system:
```bash
docker images
# Shows: REPOSITORY  TAG      IMAGE ID      SIZE
#        nginx       latest   e7dd1e9c3f22  147MB
#        postgres    15       08e4c7be2bb8  413MB
```

**docker rmi** - Delete image (must not be in use):
```bash
docker rmi nginx              # Remove nginx:latest
docker rmi <image_id>         # Remove by ID
docker rmi -f nginx           # Force-remove (risky)
```

---

### Image Naming: repository:tag

Images follow a **repository:tag** naming convention:

```
┌──────────────────────────────────────────────────┐
│  nginx:1.25-alpine                               │
│  ├─ nginx = repository (image name)              │
│  └─ 1.25-alpine = tag (version/variant)          │
│                                                  │
│  Full format:                                    │
│  [registry]/[repository]:[tag]                   │
│                                                  │
│  Examples:                                       │
│  nginx                       (Docker Hub, latest)│
│  nginx:1.25                  (Docker Hub, v1.25) │
│  docker.io/nginx:latest      (explicit)          │
│  ghcr.io/myuser/myapp:1.0.0  (GitHub registry)   │
│  gcr.io/project/app:v2       (Google registry)   │
└──────────────────────────────────────────────────┘
```

**Tag vs Image ID:**
```bash
docker images
# REPOSITORY    TAG         IMAGE ID
# nginx         latest      e7dd1e9c3f22
# nginx         1.25        e7dd1e9c3f22  ← Same image!
# myapp         1.0         abc123def456
```

Multiple tags can point to the **same image ID** (different labels for the same image).

---

### What "latest" Actually Means (and Why It's Unreliable)

**latest** is just a **tag** - it has no special meaning in Docker.

```
When you push:

docker build -t myapp .
docker tag myapp:1.0.0 myapp:latest
docker push myapp:1.0.0
docker push myapp:latest

# Both tags point to the SAME image!
# "latest" is just a label (arbitrary convention)

┌──────────────────────┐
│ Image SHA256:xyz...  │
│   ├─ Tag: 1.0.0      │
│   ├─ Tag: latest     │
│   └─ Tag: stable     │
└──────────────────────┘
```

**Why "latest" is unreliable:**

```bash
docker run nginx              # Grabs latest tag
# Tomorrow, Docker Hub updates latest → nginx 1.26
# Your container suddenly gets a new major version
# Breaking changes? Too late.
```

**Best practice:**
```bash
# ALWAYS pin versions
docker run nginx:1.25-alpine   # Explicit version (safe)
docker run -it nginx           # Don't do this in production
```

---

## 6. NAMESPACES & CGROUPS - HOW ISOLATION WORKS

### PID, NET, MNT, UTS Namespaces

Containers aren't true virtual machines-they're **isolated processes** using Linux namespaces.

**What they isolate:**

```
┌────────────────────────────────────────────────────┐
│ PID NAMESPACE (Process IDs)                        │
│                                                    │
│ Container View          Host View                  │
│ ┌──────────────┐        ┌──────────────┐           │
│ │ PID 1: bash  │ ←───→  │ PID 8293     │           │
│ │ PID 2: nginx │ ←───→  │ PID 8294     │           │
│ │ PID 3: app   │ ←───→  │ PID 8295     │           │
│ └──────────────┘        └──────────────┘           │
│                                                    │
│ Container sees PIDs 1,2,3                          │
│ Host sees PIDs 8293,8294,8295                      │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ NET NAMESPACE (Network)                            │
│                                                    │
│ Container View          Host View                  │
│ ┌──────────────┐        ┌──────────────┐           │
│ │ eth0: 172... │ ←───→  │ veth123: ... │           │
│ │ localhost    │ ←───→  │ docker0 br   │           │
│ └──────────────┘        └──────────────┘           │
│                                                    │
│ Container has own IP, can't see host's eth0        │
│ Host can see virtual eth (veth) connected to br    │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ MNT NAMESPACE (Mount Points / Filesystem)          │
│                                                    │
│ Container View          Host View                  │
│ ┌──────────────┐        ┌──────────────┐           │
│ │ /            │ ←───→  │ /            │           │
│ │ /app (vol)   │ ←───→  │ /var/lib/... │           │
│ │ /etc, /usr   │ ←───→  │ layered fs   │           │
│ └──────────────┘        └──────────────┘           │
│                                                    │
│ Container sees only its own filesystem             │
│ Can mount volumes to see host directories          │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ UTS NAMESPACE (Hostname)                           │
│                                                    │
│ Container View          Host View                  │
│ ┌──────────────┐        ┌──────────────┐           │
│ │ hostname:    │ ←───→  │ hostname:    │           │
│ │ abc123d5f6a  │        │ my-server    │           │
│ └──────────────┘        └──────────────┘           │
│                                                    │
│ Each container sees its own hostname               │
└────────────────────────────────────────────────────┘
```

**Summary:**
- **PID** = Processes (container only sees its own)
- **NET** = Network (container has own IP, ports)
- **MNT** = Filesystem (container has own root `/`)
- **UTS** = Hostname (container has own name)

There are others (IPC, USER, CGROUP) but these 4 are the core isolation boundaries.

---

### cgroups - Resource Limiting (CPU, Memory)

**Namespaces** isolate (separate), but **cgroups** limit (restrict).

```
┌─────────────────────────────────────────────────┐
│ HOST: 16 CPUs, 32GB RAM                         │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │ cgroup: Container 1                     │    │
│  │ ├─ CPU limit: 2 CPUs (can't exceed)     │    │
│  │ ├─ Memory limit: 4GB (OOM killed if >)  │    │
│  │ └─ I/O limit: 50MB/s                    │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │ cgroup: Container 2                     │    │
│  │ ├─ CPU limit: 4 CPUs                    │    │
│  │ ├─ Memory limit: 8GB                    │    │
│  │ └─ I/O limit: 100MB/s                   │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Remaining: 10 CPUs, ~20GB (for host + others)  │
└─────────────────────────────────────────────────┘
```

**Example:**
```bash
# Container can use max 2 CPUs and 512MB RAM
docker run --cpus=2 --memory=512m nginx

# Without limits (dangerous!)
docker run nginx
# Container can consume ALL host resources
# → Other containers starve → Everything crashes
```

---

### Why This Matters vs a VM Hypervisor

```
CONTAINERS (Namespaces + Cgroups)
┌─────────────────────────────────┐
│ Container 1    Container 2      │
│ Process        Process          │  ← User space
│ Isolated by    Isolated by      │     (app code)
│ namespace      namespace        │
│    │              │             │
│    └──────┬───────┘             │
│           │                     │
├───────────┼─────────────────────┤  ← Kernel space
│     Shared Linux Kernel         │     (system)
│  (fast, low overhead)           │
├─────────────────────────────────┤
│      HOST OS + Hardware         │
└─────────────────────────────────┘


VMS (Hypervisor)
┌────────────────────────────────┐
│ Guest OS 1      Guest OS 2     │
│ ┌──────────┐    ┌──────────┐   │  ← Full OS
│ │Kernel    │    │Kernel    │   │     per VM
│ │Process   │    │Process   │   │
│ │(isolated)│    │(isolated)│   │
│ └──────────┘    └──────────┘   │
├────────────────────────────────┤
│    Hypervisor (emulation)      │  ← Overhead
├────────────────────────────────┤
│      HOST OS + Hardware        │
└────────────────────────────────┘
```

**Why containers are faster:**
- No full OS per container (VM needs complete OS)
- Shared kernel (immediate syscalls, no emulation)
- Instant startup (process, not OS boot)
- Minimal memory overhead (per-process vs per-OS)

**Trade-off:** VMs are more isolated (different kernels = separate security domains). Containers are lighter but share the same kernel.

---

## 7. KEY CONCEPTS TO REINFORCE

### Ephemeral by Default - Containers Don't Persist State

By default, container data is **temporary**:

```
WRONG:
┌──────────────────────────────┐
│ docker run postgres          │
│ ┌────────────────────────────┐
│ │ Container                  │
│ │ /var/lib/postgresql/data   │
│ │ 1000 records added         │
│ │                            │
│ │ docker stop                │
│ │ docker rm ← Container gone!│
│ └────────────────────────────┘
│ Data = LOST                  │
└──────────────────────────────┘

RIGHT:
┌──────────────────────────────────────────────┐
│ docker run -v mydata:/var/lib/postgresql/... │
│ ┌────────────────────────────┐               │
│ │ Container                  │               │
│ │ /var/lib/postgresql (mount)│───┐           │
│ │ 1000 records added         │   │           │
│ │                            │   │           │
│ │ docker stop                │   │ VOLUME    │
│ │ docker rm                  │   │ (persists)│
│ └────────────────────────────┘   │           │
│                                  │           │
│ ┌──────────────────────────────┐ │           │
│ │ Host: /var/lib/docker/...    │◄┘           │
│ │ 1000 records STILL HERE      │             │
│ └──────────────────────────────┘             │
│ Data = SAVED                                 │
└──────────────────────────────────────────────┘
```

**Rule:** Always use **volumes** for persistent data (databases, file uploads, logs, config).

---

### Immutability - Don't Modify Running Containers, Rebuild the Image

Anti-pattern:
```bash
docker run myapp
docker exec -it <container_id> bash
# Edit files manually inside container
# Maybe delete a file by accident
# Now the container is in an unknown state
# Other developers don't know what you did
```

Correct pattern:
```bash
# Changes needed?
# 1. Edit Dockerfile
# 2. Rebuild image
# 3. Run new container

docker build -t myapp:2.0 .
docker run myapp:2.0
# Everyone knows exactly what's in myapp:2.0
# Can rebuild anytime
# Can version it
```

**Benefits:**
- **Reproducibility** - Same image = same behavior everywhere
- **Version control** - Track changes in Git (Dockerfile)
- **Rollback** - Old version still exists, just run it
- **Auditability** - Can see exact changes (git log)

---

### Port Mapping Basics (-p 8080:80) - Introduction

Containers have isolated networks. To expose ports to the outside:

```
BEFORE PORT MAPPING:
┌──────────────┐
│ Container    │
│ :80 (nginx)  │
│              │
│ Not visible! │
└──────────────┘

AFTER PORT MAPPING (-p 8080:80):
┌──────────────┐
│ Container    │
│ :80 (nginx)  │
└──────┬───────┘
       │
   Port Mapping
   :8080 ← → :80
       │
┌──────────────┐
│ Host         │
│ :8080 ←→ ext │
└──────────────┘

Browser: localhost:8080 → Host :8080 → Container :80
```

**Syntax:**
```bash
docker run -p HOST_PORT:CONTAINER_PORT image
docker run -p 8080:80 nginx
# :8080 on host maps to :80 in container
```

**Common mistakes:**
```bash
docker run -p 80:80 nginx    # Works, but ties up port 80
docker run -p 3000:3000 myapp   # Good: non-privileged port
docker run nginx             # WRONG: No port mapping, can't access
```

We'll detail networking in section 03. For now: **port mapping connects outside world to container ports**.

---

## SUMMARY - MENTAL MODEL

```
┌────────────────────────────────────────────────────┐
│ YOU START HERE: Want to run an app                 │
│                                                    │
│ Step 1: WRITE DOCKERFILE                           │
│ ├─ FROM: base OS                                   │
│ ├─ RUN: install dependencies                       │
│ ├─ COPY: add your code                             │
│ └─ CMD: what to run                                │
│                                                    │
│ Step 2: BUILD IMAGE                                │
│ └─ docker build -t myapp:1.0 .                     │
│    └─ Creates layers, caches them                  │
│                                                    │
│ Step 3: PUSH TO REGISTRY (optional)                │
│ └─ docker push docker.io/myuser/myapp:1.0          │
│    └─ Makes it available everywhere                │
│                                                    │
│ Step 4: RUN CONTAINER (locally or cloud)           │
│ └─ docker run myapp:1.0                            │
│    └─ Creates isolated process                     │
│    └─ Starts with ephemeral state                  │
│    └─ Can map ports, mount volumes                 │
│                                                    │
│ Step 5: MANAGE CONTAINERS                          │
│ ├─ docker ps: see what's running                   │
│ ├─ docker stop: gracefully stop                    │
│ └─ docker rm: delete when done                     │
│                                                    │
│ EVERYTHING ELSE is optimization & tooling          │
└────────────────────────────────────────────────────┘
```

---

## NEXT STEPS

1. **Section 02** → Dockerfile deep dive (every instruction)
2. **Section 03** → Networking & port mapping
3. **Section 04** → Storage (volumes, bind mounts)
4. **Section 05** → Docker Compose (multi-container apps)
5. **Section 06** → Best practices & troubleshooting