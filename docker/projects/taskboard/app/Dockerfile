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