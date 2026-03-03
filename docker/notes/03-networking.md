# Networking
Docker networking controls how containers communicate with each other and the outside world. Each container is isolated by default, and you use networks to connect them or port mapping to expose them to your host machine.

## Network Types

- **Bridge (default):** Default for containers on a single host. Containers get their own IP and can talk to each other via container name if on the same custom bridge network.

- **Host:**
Removes network isolation, container shares the host's network directly. No port mapping needed but less secure.

- **None:**
Disables networking entirely. Fully isolated container

- **Overlay:**
Spans multiple Docker hosts (used with Docker Swarm/Kubernetes)

## Port Mapping
```bash
docker run -p <host-port>:<container-port>

# -p maps host to container, e.g. "-p 8080:5000" means host port 8080 forwards to container port 5000
```

## Container-to-Container Communication

- **Same network:**
Containers can reach each other by container name (Docker has built-in DNS) e.g. `ping my-container`

- **Different networks:**
They can not communicate by default. You either connect one to the other's network with `docker network connect`, or put them on the same network 

## DNS in Docker
Docker runs an internal DNS server at `127.0.0.11`. On custom bridge networks, container names resolve automatically. On the default bridge, they don't. You would need `--link`(deprecated) or a custom network.

## Commands
```bash
docker network ls       # List networks
docker network create   # Create a new network
docker network inspect  # See details/connected containers
docker network connect  # Attach a running container to a network
docker network rm       # Remove a network
```

## Examples
```bash
# List all networks
docker network ls

# Create a custom bridge network
docker network create my-network

# Inspect a network (see connected containers, IP ranges, etc.)
docker network inspect my-network

# Connect a running container to a network
docker network connect my-network my-container

# Remove a network
docker network rm my-network
```

**Flask connecting to MySQL by container name:**
```python
import MySQLdb
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    db = MySQLdb.connect(host="mydb", user="root", passwd="secret", db="mysql")
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    return f'MySQL version: {version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

**Full example - two containers talking to each other:**
```bash
# Create a shared network for both containers
docker network create my-network

# Run MySQL container in the background, named "mydb", on my-network
docker run -d --name mydb --network my-network mysql

# Run Flask container in the background, named "flask-app", on my-network
# Expose port 5002 on the host so we can access it from the browser
docker run -d --name flask-app --network my-network -p 5002:5002 flask-app

# Flask can now reach MySQL using hostname "mydb"
```

| Container | Image | Network |
|---|---|---|
| `mydb` | `mysql` | `my-network` |
| `flask-app` | `flask-app` | `my-network` |

Each `docker run` starts one container. Because both use `--network my-network`, Docker's internal DNS lets `flask-app` resolve the hostname `"mydb"` to the MySQL container's IP, that's how Flask connects to the database.