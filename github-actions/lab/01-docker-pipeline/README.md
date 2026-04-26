Objective:

- Set up a pipeline that builds and pushes a certain container image to a Docker Hub or ECS registry. 

- Then create a pipeline with automated tests such as automated linting for your Terraform.


## Step 1: Build a simple python application

app/app.py

```py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h1>Lab 01 - Docker Pipeline</h1><p>Flask app running in a container.</p>
    <a href="/health"><button>Health</button></a>
    '''

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

app/requirements.txt

```
flask==3.1.0
```

## Step 2: Docker

### 2.1: Create app/Dockerfile 

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 2.2: Build the image

`docker build -t lab01-pipeline`
> Make sure you run the command inside /app directory

Test the image
`docker run -p 5000:5000 lab01-pipeline`

### 2.3: Push to Docker Hub

Tag the image to your Docker Hub repo

`docker tag lab01-pipeline:latest eisei25/lab01-pipeline:latest`  

Push to repo

`docker push eisei25/lab01-pipeline:latest`


## Step 3: Build the workflow

The workflow should:
    1. Checkout the code
    2. Login to DockerHub usings secrets
    3. Build the image
    4. Push to DockerHub

```yml
name: docker workflow

on:
  push:
    branches: [ github-actions ]

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:

      # Clones the repo onto the runner so the workflow has access to the code
      - name: checkout
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # Create and boot a builder using by default the docker-container driver (recommended)
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      # GitHub Action to build and push Docker images with Buildx
      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          context: lab/01-docker-pipeline/app # Context tells Docker where to find the Dockerfile and which files are available to COPY

          push: true
          tags: ${{ vars.DOCKERHUB_USERNAME }}/lab01-pipeline:latest
```