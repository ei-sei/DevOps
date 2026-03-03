# Docker Compose
Docker Compose lets you define and run multiple containers together using a single YAML file. Instead of running several `docker run` commands manually, you describe your whole app in one file and start everything with one command.

## docker-compose.yml Structure

```yaml
services:   # define your containers here
  app:
    image: my-app

networks:   # optional, define custom networks
volumes:    # optional, define named volumes
```

## Services
Each service is one container. You give it a name and configure how it runs.

### image vs build
```yaml
services:
  web:
    image: nginx          # use a pre-built image from Docker Hub

  app:
    build: .              # build from a Dockerfile in the current directory
```

### ports
Maps a host port to a container port, same as `-p` in `docker run`.
```yaml
ports:
  - "5002:5002"           # host:container
```

### environment
Set environment variables inside the container.
```yaml
environment:
  - NODE_ENV=production
  - PORT=3000
```

### volumes
Mount a named volume or host folder into the container.
```yaml
volumes:
  - db-data:/var/lib/mysql    # named volume
  - ./app:/app                # bind mount (host folder)
```

### depends_on
Makes one service wait for another to start before it runs.
```yaml
depends_on:
  - db                        # app won't start until db starts
```

### health checks
Checks if a container is actually ready, not just running.
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Networks in Compose
Compose automatically creates a shared network for all services, so they can reach each other by service name. You can also define custom networks if needed.

```yaml
networks:
  my-network:

services:
  app:
    networks:
      - my-network
  db:
    networks:
      - my-network
```

## Volumes in Compose
Named volumes must be declared at the top level so Compose manages them.

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:                    # Compose creates and manages this volume
```

## Commands

```bash
docker compose up             # Start all services (foreground)
docker compose up -d          # Start all services in the background
docker compose down           # Stop and remove containers
docker compose ps             # List running services
docker compose logs           # View logs from all services
docker compose build          # Build images without starting containers
```

## Environment Variables

### .env file
Compose automatically reads a `.env` file in the same directory and substitutes variables in the compose file.
```
# .env
DB_PASSWORD=secret
PORT=5002
```

### env_file directive
Load variables from a specific file into a service.
```yaml
services:
  app:
    env_file:
      - .env
```

### Inline environment
Define variables directly in the compose file.
```yaml
services:
  app:
    environment:
      - DB_PASSWORD=secret
      - PORT=5002
```

## Full Example - Flask + MySQL App

The Flask app reads DB connection details from environment variables injected by Compose:
```python
# app.py
import os
import MySQLdb
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    db = MySQLdb.connect(
        host=os.environ.get('DB_HOST'),         # reads "db" from environment
        user="root",
        passwd=os.environ.get('DB_PASSWORD'),   # reads "secret" from environment
        db="myapp"
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    return f'MySQL version: {version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

The Compose file wires everything together:
```yaml
# docker-compose.yml

services:

  # Flask web app
  app:
    build: .                          # build image from Dockerfile in current directory
    ports:
      - "5002:5002"                   # expose port 5002 to the host
    environment:
      - DB_HOST=db                    # "db" is the service name below, Docker resolves it
      - DB_PASSWORD=secret
    depends_on:
      - db                            # wait for db to start before app starts
    networks:
      - my-network

  # MySQL database
  db:
    image: mysql:8.0                  # pull MySQL image from Docker Hub
    environment:
      - MYSQL_ROOT_PASSWORD=secret    # set the root password
      - MYSQL_DATABASE=myapp          # create this database on startup
    volumes:
      - db-data:/var/lib/mysql        # persist database data so it survives restarts
    networks:
      - my-network

networks:
  my-network:                         # shared network so app and db can talk by name

volumes:
  db-data:                            # Compose creates and manages this volume
```

To run it:
```bash
docker compose up -d        # start everything in the background
docker compose logs -f      # follow logs from all services
docker compose down         # stop and remove containers
docker compose down -v      # stop and also delete volumes
```
