# Taskboard

A small Node.js/Express todo API with a static frontend, focused on demonstrating a **multi-stage Docker build** that strips build-only tooling out of the final image.

## What it does

A simple task tracker - add, complete, and delete todos via a REST API (`/api/todos`), served alongside a static HTML/CSS/JS frontend from the same Express app.

## What it demonstrates

`app/Dockerfile`:

```dockerfile
# Build stage: installs dependencies, discarded after this stage
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Final stage: only what's needed to run the app, no npm/npx/corepack.
# The base image ships npm regardless of what we install ourselves, and its
# bundled dependencies (brace-expansion, tar, etc.) carry their own CVEs.
# The app doesn't need npm at runtime, only node, so it's removed here.
FROM node:22-alpine

WORKDIR /app

RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack

# Copy installed dependencies from the build stage
COPY --from=builder /app/node_modules ./node_modules

# Copy the rest of the application source code to the container
COPY . .

# Expose port 3000 to the outside world
EXPOSE 3000

# Define environment variable
ENV NODE_ENV=production

# Command to run the application
CMD ["node", "server.js"]
```

The interesting part isn't the two `FROM` lines on their own (that's standard multi-stage) - it's that the **base image's own bundled tooling gets removed** in the final stage, not just the build stage's leftovers. `node:22-alpine` ships `npm`/`npx`/`corepack` regardless of what you actually use, and those carry their own dependencies (and CVEs) that have nothing to do with running this app. Since the app only ever needs `node` at runtime, deleting them shrinks the attack surface of the final image beyond what a "normal" multi-stage build already gets you.

## Run it

```bash
cd app
docker build -t taskboard .
docker run -p 3000:3000 --env-file .env taskboard
```

Then visit `http://localhost:3000`.

**API routes:**
| Method | Route | Purpose |
|--------|-------|---------|
| `GET` | `/health` | Basic health check |
| `GET` | `/api/todos` | List todos, newest first |
| `POST` | `/api/todos` | Create a todo (`{ "text": "..." }`) |
| `PUT` | `/api/todos/:id` | Toggle a todo's completed status |
| `DELETE` | `/api/todos/:id` | Delete a todo |
| `POST` | `/api/admin/reset` | Clear all todos - requires `x-admin-token` header matching `ADMIN_TOKEN` |

**Stack:** Node.js, Express, vanilla JS/HTML/CSS frontend, Docker
