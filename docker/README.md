# Docker Lab Notebook

Documentation of my Docker and containerisation journey, including hands-on projects and notes.

---

## Notes

| # | Topic | File |
|---|-------|------|
| 00 | Docker Setup (Fedora) | [00-docker-setup.md](notes/00-docker-setup.md) |
| 01 | Core Concepts | [01-core-concepts.md](notes/01-core-concepts.md) |
| 02 | Dockerfile | [02-dockerfile.md](notes/02-dockerfile.md) |
| 03 | Networking | [03-networking.md](notes/03-networking.md) |
| 04 | Docker Compose | [04-compose.md](notes/04-compose.md) |
| 05 | Volumes & Storage | [05-volumes.md](notes/05-volumes.md) |
| 06 | Best Practices | [06-best-practices.md](notes/06-best-practices.md) |
| 07 | Pushing Images to DockerHub | [07-dockerhub.md](notes/07-dockerhub.md) |

### Topic Index

Every topic heading across all notes files, so you can jump straight to a specific one instead of opening each file to search.

**[01 - Core Concepts](notes/01-core-concepts.md)**
- [What is Docker?](notes/01-core-concepts.md#1-what-is-docker)
- [The Docker Architecture](notes/01-core-concepts.md#2-the-docker-architecture)
- [Core Building Blocks](notes/01-core-concepts.md#3-core-building-blocks)
- [The Container Lifecycle](notes/01-core-concepts.md#4-the-container-lifecycle)
- [Images Deep Dive](notes/01-core-concepts.md#5-images-deep-dive)
- [Namespaces & Cgroups - How Isolation Works](notes/01-core-concepts.md#6-namespaces--cgroups---how-isolation-works)
- [Key Concepts to Reinforce](notes/01-core-concepts.md#7-key-concepts-to-reinforce)
- [Summary - Mental Model](notes/01-core-concepts.md#summary---mental-model)
- [Next Steps](notes/01-core-concepts.md#next-steps)

**[02 - Dockerfile](notes/02-dockerfile.md)**
- [What is a Dockerfile?](notes/02-dockerfile.md#what-is-a-dockerfile)
- [Instructions](notes/02-dockerfile.md#instructions)
- [Build](notes/02-dockerfile.md#build)
- [Layer Caching](notes/02-dockerfile.md#layer-caching)
- [Multi-Stage Builds](notes/02-dockerfile.md#multi-stage-builds)

**[03 - Networking](notes/03-networking.md)**
- [Network Types](notes/03-networking.md#network-types)
- [Port Mapping](notes/03-networking.md#port-mapping)
- [Container-to-Container Communication](notes/03-networking.md#container-to-container-communication)
- [DNS in Docker](notes/03-networking.md#dns-in-docker)
- [Commands](notes/03-networking.md#commands)
- [Examples](notes/03-networking.md#examples)

**[04 - Docker Compose](notes/04-compose.md)**
- [docker-compose.yml Structure](notes/04-compose.md#docker-composeyml-structure)
- [Services](notes/04-compose.md#services)
- [Networks in Compose](notes/04-compose.md#networks-in-compose)
- [Volumes in Compose](notes/04-compose.md#volumes-in-compose)
- [Commands](notes/04-compose.md#commands)
- [Environment Variables](notes/04-compose.md#environment-variables)
- [Full Example - Flask + MySQL App](notes/04-compose.md#full-example---flask--mysql-app)

**[05 - Volumes & Storage](notes/05-volumes.md)**
- [Why Persist Data?](notes/05-volumes.md#why-persist-data)
- [Storage Types](notes/05-volumes.md#storage-types)
- [Commands](notes/05-volumes.md#commands)
- [Using Volumes in a Container](notes/05-volumes.md#using-volumes-in-a-container)
- [Volumes in Docker Compose](notes/05-volumes.md#volumes-in-docker-compose)

**[06 - Best Practices](notes/06-best-practices.md)**
- [Image Optimisation](notes/06-best-practices.md#image-optimisation)
- [.dockerignore](notes/06-best-practices.md#dockerignore)
- [Security](notes/06-best-practices.md#security)
- [Tagging Strategy](notes/06-best-practices.md#tagging-strategy)
- [Logging & Observability](notes/06-best-practices.md#logging--observability)
- [Multi-Stage Builds for Production](notes/06-best-practices.md#multi-stage-builds-for-production)

**[07 - Pushing Images to DockerHub](notes/07-dockerhub.md)**
- [Overview](notes/07-dockerhub.md#overview)
- [Step 1 - Create a DockerHub account](notes/07-dockerhub.md#step-1---create-a-dockerhub-account)
- [Step 2 - Build your image](notes/07-dockerhub.md#step-2---build-your-image)
- [Step 3 - Tag the image](notes/07-dockerhub.md#step-3---tag-the-image)
- [Step 4 - Login](notes/07-dockerhub.md#step-4---login)
- [Step 5 - Push](notes/07-dockerhub.md#step-5---push)
- [Step 6 - Verify](notes/07-dockerhub.md#step-6---verify)
- [Full example](notes/07-dockerhub.md#full-example)
- [Notes](notes/07-dockerhub.md#notes)

---

## Projects

| Project | Description | Stack |
|---------|--------------|-------|
| [Flask + Redis](projects/flask-redis/README.md) | Multi-container visit-counter app - Flask increments a count in Redis on every request, nginx in front as reverse proxy and load balancer. Covers Compose networking, volume persistence, env vars, and scaling. | Python, Flask, Redis, nginx, Docker Compose |
| [Taskboard](projects/taskboard/README.md) | Node/Express todo API + static frontend, focused on a multi-stage build that strips the base image's own bundled npm/npx/corepack from the final image, not just the build stage's leftovers. | Node.js, Express, Docker |

---

## Repository Structure

```
docker/
├── README.md
├── assets/
│   ├── containers-vs-VMs.png
│   ├── docker-architecture.png
│   └── docker-overview.png
├── notes/
│   ├── 00-docker-setup.md
│   ├── 01-core-concepts.md
│   ├── 02-dockerfile.md
│   ├── 03-networking.md
│   ├── 04-compose.md
│   ├── 05-volumes.md
│   ├── 06-best-practices.md
│   └── 07-dockerhub.md
└── projects/
    ├── flask-redis/
    │   ├── README.md
    │   ├── docker-compose.yml
    │   ├── nginx.conf
    │   └── app/
    │       ├── app.py
    │       ├── Dockerfile
    │       └── requirements.txt
    └── taskboard/
        ├── README.md
        └── app/
            ├── server.js
            ├── package.json
            ├── Dockerfile
            └── public/
```
