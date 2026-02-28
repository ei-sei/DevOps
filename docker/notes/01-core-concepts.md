1. What is Docker?

The problem it solves (works on my machine, dependency conflicts)
Containers vs VMs — key distinction
How Docker fits into a DevOps/SRE workflow

2. The Docker Architecture

Docker Engine (daemon, CLI, REST API)
Client-server model — how docker CLI talks to the daemon
containerd and runc (brief mention — good to know exists)

3. Core Building Blocks

Images — read-only templates, layered filesystem
Containers — running instance of an image
Dockerfile — blueprint for building images (just introduce it here, detail in 02)
Registry — where images live (Docker Hub, ECR, etc.)

4. The Container Lifecycle

create → start → run → stop → remove
Key commands: docker run, docker ps, docker stop, docker rm
Difference between docker run and docker start

5. Images Deep Dive

Union filesystem / layer caching
docker pull, docker images, docker rmi
Image naming: repository:tag (e.g. nginx:1.25-alpine)
What latest actually means (and why it's unreliable)

6. Namespaces & Cgroups (How Isolation Works)

PID, NET, MNT, UTS namespaces — what each isolates
cgroups — resource limiting (CPU, memory)
Why this matters vs a VM hypervisor

7. Key Concepts to Reinforce

Ephemeral by default — containers don't persist state
Immutability — don't modify running containers, rebuild the image
Port mapping basics (-p 8080:80) — just introduce, detail in 03