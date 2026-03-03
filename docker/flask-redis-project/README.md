# Flask + Redis + Docker Compose Challenge

## Objective
Create a multi-container application that consists of a simple Python Flask web application and a Redis database. The Flask application should use Redis to store and retrieve data.

### Requirements

1. Flask Application

   Must include two routes:
   - `/` - returns a welcome message
   - `/count` - increments and displays a visit count stored in Redis

2. Redis Service
   - Used as a key-value store
   - Stores the visit counter

3. Dockerisation

   You must:
   - Write a Dockerfile for the Flask app
   - Use Redis's official image (or write your own Dockerfile if you want the bonus)
   - Write a docker-compose.yml to run both services together

### Overview
```
┌──────────────────────────────────┐
│   Docker Compose Setup           │
│                                  │
│  ┌────────────┐  ┌────────────┐  │
│  │   Flask    │  │   Redis    │  │
│  │  :5002     │─►│   :6379    │  │
│  └────────────┘  └────────────┘  │
│    web service    redis service  │
│                                  │
│  Shared network (auto DNS)       │
│  Flask → Redis by hostname       │
└──────────────────────────────────┘
```

---

## Part 1 - Create the Flask application

```python
# Flask is the web framework - handles routing and HTTP requests
from flask import Flask
# redis-py is the Python client library for talking to Redis
import redis

# Create the Flask app instance
app = Flask(__name__)

# Connect to Redis - 'redis' resolves to the Redis container via Docker Compose networking
# decode_responses=True returns strings instead of raw bytes
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Route for the home page - returns a welcome message with a link to the counter
@app.route('/')
def home():
    return '''
        <h4>Welcome to Flask + Redis!</h4>
        <a href="/count"><button>Go to Counter</button></a>
    '''

# Route for the counter - every visit increments the count in Redis
@app.route('/count')
def count():
    # INCR atomically increments 'visit_count' by 1 and returns the new value
    # If the key doesn't exist yet, Redis creates it starting at 0 before incrementing
    visit_count = redis_client.incr('visit_count')
    return f'Visit count: {visit_count}'

# Only runs when executed directly (not when imported or run via a WSGI server)
# 0.0.0.0 makes the app reachable from outside the container
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

**Create the `requirements.txt`**
```
Flask==3.0.0
redis==5.0.1
```
> We could just list out the dependencies as `RUN pip install flask redis` but using requirements.txt is just much more conventional for readability, portability, layer caching and tooling.

**Create the `Dockerfile`**
```dockerfile
# Build Flask image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (documentation)
EXPOSE 5002

# Run Flask app
CMD ["python", "app.py"]
```

---

## Part 2 - Docker Compose configuration
Create the `docker-compose.yml` (inside project root)
```yaml
version: '3.9'

services:
  # Flask Web Application
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: flask-app
    ports:
      - "5002:5002"
    depends_on:
      - redis
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    container_name: redis-db
    ports:
      - "6379:6379"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

```

**What each section does:**
| Section | Purpose |
|---------|---------|
| `build` | Used for `web` because it's our custom app - points Docker at our Dockerfile |
| `image` | Used for `redis` because we just need the official image with no changes |
| `ports: "5002:5002"` | `host:container` - forwards port 5002 on your machine into the container |
| `depends_on: redis` | Starts Redis before Flask - waits for the container to start, not Redis to be ready |
| `networks: app-network` | Shared network so Flask can reach Redis by hostname (`host='redis'` in app.py) |
| `redis:7-alpine` | Alpine base image - much smaller than the default, faster to pull |

---

## Part 3 - Build and run

`docker compose build`

`docker compose up`

You should now be able to visit `http://localhost:5002` and verify the API is running.

**Command reference**
- `docker compose stop` - Stop services (keep containers)
- `docker compose down` - Stop and remove containers
- `docker compose down --rmi all` - Remove everything (container, images)


---

# Section 2 - Persistent storage
This section will look to add persistent storage to Redis so data survives container restarts.

**PROBLEM WE'RE SOLVING**

```
CURRENT (Without Persistence):

Start app → Visit counter 5 times → Counter = 5
Stop containers → docker-compose down
Restart → docker-compose up -d
Visit counter → Counter = 0 ✗ (lost!)

AFTER (With Persistence):

Start app → Visit counter 5 times → Counter = 5
Stop containers → docker-compose down
Restart → docker-compose up -d
Visit counter → Counter = 6 ✓ (persisted!)
```

We will mount a named [volume](../notes/05-volumes.md) for storage and enable AOF (Append-Only File) so Redis writes changes to disk. The volume is managed by Docker and stored at `/var/lib/docker/volumes/redis-data/_data/`

To implement persistent storage, you will need to update `docker-compose.yml` with these changes:
```yaml
version: '3.9'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: flask-app
    ports:
      - "5002:5002"
    depends_on:
      - redis
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    container_name: redis-db
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data              # CHANGE 1: Mount named volume
    networks:
      - app-network
    command: redis-server --appendonly yes  # CHANGE 2: Enable AOF persistence

volumes:                              # CHANGE 3: Define the named volume
  redis-data:

networks:
  app-network:
    driver: bridge
```


**Testing persistence**
Start application:
```bash
docker compose up -d
```

Verify volume was created:
```bash
docker volume ls
# Output: local     flask-redis-project_redis-data
```

Refresh `/count` a few times to get the counter up, then bring the containers down and back up:
```bash
docker compose down
docker compose up -d
```

Visit `/count` again - the counter should continue from where it left off, not reset to 1.