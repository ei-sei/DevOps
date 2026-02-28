# Volumes & Storage

## Why Persist Data?

## Storage Types

### Named Volumes

### Bind Mounts

### tmpfs

#### Named Volumes vs Bind Mounts

## Commands

```bash
docker volume create
docker volume ls
docker volume inspect
docker volume rm
```

## Using Volumes in a Container

```bash
docker run -v <volume-name>:<container-path>
docker run -v <host-path>:<container-path>
```

## Volumes in Docker Compose
