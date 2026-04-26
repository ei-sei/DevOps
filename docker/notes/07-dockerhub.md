# Pushing Images to DockerHub

## Overview

DockerHub is the default public registry. Pushing an image makes it available to pull from anywhere.

The full flow is: **build - tag - login - push**

---

## Step 1 - Create a DockerHub account

Sign up at [hub.docker.com](https://hub.docker.com). Your username is part of every image name you push.

---

## Step 2 - Build your image

```bash
docker build -t myapp .
```

---

## Step 3 - Tag the image

DockerHub expects images in the format `<username>/<repository>:<tag>`:

```bash
docker tag myapp:latest ei-sei/myapp:1.0.0
docker tag myapp:latest ei-sei/myapp:latest
```

> Always tag with both a version and `latest`. Version tags are immutable references, `latest` always points to the most recent build.

---

## Step 4 - Login

```bash
docker login
```

Prompts for your DockerHub username and password. To avoid storing your password in plain text, use an access token instead - generate one in DockerHub under **Account Settings - Security - Access Tokens**.

```bash
docker login -u ei-sei --password-stdin <<< "your-access-token"
```

---

## Step 5 - Push

```bash
docker push ei-sei/myapp:1.0.0
docker push ei-sei/myapp:latest
```

Both tags need to be pushed separately.

---

## Step 6 - Verify

```bash
docker pull ei-sei/myapp:1.0.0
```

Or check [hub.docker.com](https://hub.docker.com) under your repositories.

---

## Full example

```bash
docker build -t ei-sei/myapp:1.0.0 .
docker tag ei-sei/myapp:1.0.0 ei-sei/myapp:latest
docker login
docker push ei-sei/myapp:1.0.0
docker push ei-sei/myapp:latest
```

---

## Notes

- Public repos on DockerHub are free and visible to anyone
- Private repos are limited on the free tier
- In CI/CD pipelines, store DockerHub credentials as secrets and use `docker login` non-interactively
- In industry, ECR (AWS) or GCR (Google) are more common than DockerHub for private images
