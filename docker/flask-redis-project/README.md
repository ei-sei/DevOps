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
        <h1>Welcome to Flask + Redis!</h1>
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
> We could just list out the dependencies as `RUN pip install flask redis` but using requirements.txt is just much more conventional for readbility, portability, layer caching and tooling.

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

# Define network for inter-services communication
networks:
  app-network:
    driver: bridge

```

**What each section does:**
| Section | Purpose |
|---------|---------|
| `web:` | Flask application service |
| `build: ./app` | Build from Dockerfile in ./app |
| `ports: "5002:5002"` | Map host port 5002 to container port 5002 |
| `depends_on: redis` | Start redis before web |
| `redis:` | Redis database service |
| `image: redis:7-alpine` | Use official Redis image (lightweight) |
| `networks: app-network` | Both services on same network, can communicate by hostname |

---

## Part 3 - Build and run

`docker compose build`

`docker compose up`

You should now be able to visit `http://localhost:5002` and verify the API is running.

**Notable commands**
- `docker compose stop` - Stop services (keep containers)
- `docker compose down` - Stop and remove containers
- `docker compose down --rmi all` - Remove everything (container, images)