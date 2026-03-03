# Volumes & Storage
By default, data inside a container is lost when the container stops. Volumes let you persist data outside the container so it survives restarts and deletions.

## Why Persist Data?
Containers are stateless by design. If you store a database inside a container with no volume, all your data disappears the moment you stop it. Volumes solve this by storing data on the host machine instead.

## Storage Types

- **Named Volumes:** Managed by Docker. Docker decides where to store the data on the host. Best for databases and app data you don't need to access directly.

- **Bind Mounts:** You choose the exact folder on your host to share with the container. Useful for development, changes to files on your host instantly reflect inside the container.

- **tmpfs:** Stored in memory only, never written to disk. Data is gone when the container stops. Useful for sensitive or temporary data.

#### Named Volumes vs Bind Mounts

| | Named Volume | Bind Mount |
|---|---|---|
| Storage location | Managed by Docker | You specify the path |
| Best for | Databases, persistent data | Local development |
| Portable | Yes | No (tied to host path) |

## Commands

```bash
docker volume create my-volume   # Create a named volume
docker volume ls                 # List all volumes
docker volume inspect my-volume  # See details about a volume
docker volume rm my-volume       # Delete a volume
```

## Using Volumes in a Container

```bash
# Mount a named volume into a container
docker run -v my-volume:/app/data my-image

# Mount a host folder into a container (bind mount)
docker run -v /home/user/project:/app my-image
```

## Volumes in Docker Compose

```yaml
services:
  db:
    image: mysql
    volumes:
      - db-data:/var/lib/mysql  # named volume mounted into the container

volumes:
  db-data:  # declare the volume here so Compose manages it
```
