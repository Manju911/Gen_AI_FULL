
# Docker FastAPI → Kubernetes Demo

This project demonstrates how to take a simple FastAPI application,
containerize it using Docker, and deploy it on Kubernetes.

We will demonstrate:

1. Docker Image
2. Kubernetes Deployment
3. Self-Healing
4. Service
5. Load Balancing

---

# Project Structure

```text
docker-demo/
│
├── app.py
├── requirements.txt
├── Dockerfile
│
├── deployment.yaml
└── service.yaml
````

---

# Step 1 — Create FastAPI Application

## app.py

```python
from fastapi import FastAPI
import socket

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from Kubernetes!",
        "pod": socket.gethostname()
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
```

The `/` endpoint returns the hostname of the Pod.

This helps us demonstrate load balancing.

Example:

```json
{
    "message": "Hello from Kubernetes!",
    "pod": "fastapi-demo-69fd4658bc-n2ccg"
}
```

---

# Step 2 — requirements.txt

```text
fastapi
uvicorn
```

---

# Step 3 — Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
```

---

# Step 4 — Build Docker Image

From inside the project directory:

```powershell
docker build -t fastapi-demo:v1 .
```

Check the image:

```powershell
docker images
```

You should see:

```text
REPOSITORY      TAG
fastapi-demo    v1
```

---

# Step 5 — Push Image to Docker Hub

Kubernetes needs access to the image.

Login to Docker Hub:

```powershell
docker login
```

Tag the image:

```powershell
docker tag fastapi-demo:v1 YOUR_USERNAME/fastapi-demo:v1
```

Example:

```powershell
docker tag fastapi-demo:v1 vins/fastapi-demo:v1
```

Push:

```powershell
docker push YOUR_USERNAME/fastapi-demo:v1
```

Example:

```powershell
docker push vins/fastapi-demo:v1
```

---

# Step 6 — Kubernetes Deployment

Create:

```text
deployment.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: fastapi-demo

spec:
  replicas: 3

  selector:
    matchLabels:
      app: fastapi

  template:
    metadata:
      labels:
        app: fastapi

    spec:
      containers:
        - name: fastapi

          image: YOUR_USERNAME/fastapi-demo:v1

          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8000
```

Replace:

```text
YOUR_USERNAME
```

with your Docker Hub username.

Example:

```yaml
image: vins/fastapi-demo:v1
```

---

# Step 7 — Deploy to Kubernetes

Apply the Deployment:

```powershell
kubectl apply -f deployment.yaml
```

Check the Deployment:

```powershell
kubectl get deployment
```

Expected:

```text
NAME           READY   UP-TO-DATE   AVAILABLE
fastapi-demo   3/3     3            3
```

Check Pods:

```powershell
kubectl get pods
```

Expected:

```text
NAME                            READY   STATUS
fastapi-demo-xxxxx              1/1     Running
fastapi-demo-yyyyy              1/1     Running
fastapi-demo-zzzzz              1/1     Running
```

We requested:

```yaml
replicas: 3
```

Therefore Kubernetes creates and maintains 3 Pods.

Architecture:

```text
Deployment
    |
    +---- Pod 1
    |
    +---- Pod 2
    |
    +---- Pod 3
```

---

# Step 8 — Demonstrate Self-Healing

Kubernetes automatically maintains the desired number of Pods.

Our desired state:

```text
3 Pods
```

Check the current Pods:

```powershell
kubectl get pods
```

Example:

```text
fastapi-demo-abc123   Running
fastapi-demo-def456   Running
fastapi-demo-ghi789   Running
```

Delete one Pod:

```powershell
kubectl delete pod fastapi-demo-abc123
```

Immediately check:

```powershell
kubectl get pods
```

You may see:

```text
fastapi-demo-def456   Running
fastapi-demo-ghi789   Running
fastapi-demo-new123   ContainerCreating
```

After a few seconds:

```text
fastapi-demo-def456   Running
fastapi-demo-ghi789   Running
fastapi-demo-new123   Running
```

Kubernetes automatically created a replacement Pod.

### Why?

Deployment says:

```text
Desired Pods = 3
```

After deleting one:

```text
Current Pods = 2
```

Kubernetes detects the difference and creates another Pod.

```text
Desired State
      |
      v
    3 Pods

Current State
      |
      v
    2 Pods

      |
      v

Kubernetes creates
a new Pod
```

This is called:

# Self-Healing

---

# Step 9 — Create Kubernetes Service

Create:

```text
service.yaml
```

```yaml
apiVersion: v1
kind: Service

metadata:
  name: fastapi-service

spec:
  selector:
    app: fastapi

  ports:
    - port: 80
      targetPort: 8000

  type: NodePort
```

Important:

The Service selects Pods using:

```yaml
selector:
  app: fastapi
```

Our Pods have:

```yaml
labels:
  app: fastapi
```

Therefore:

```text
Service
   |
   +---- Pod 1
   |
   +---- Pod 2
   |
   +---- Pod 3
```

Apply the Service:

```powershell
kubectl apply -f service.yaml
```

Check:

```powershell
kubectl get service
```

---

# Step 10 — Access the Service

For local testing, use:

```powershell
kubectl port-forward service/fastapi-service 8080:80
```

You should see:

```text
Forwarding from 127.0.0.1:8080 -> 80
```

Open:

```text
http://localhost:8080
```

You should get:

```json
{
    "message": "Hello from Kubernetes!",
    "pod": "fastapi-demo-xxxxx"
}
```

---

# Step 11 — Demonstrate Load Balancing

The Service distributes requests to the Pods.

Architecture:

```text
                    Browser
                       |
                       v
               fastapi-service
                       |
          +------------+------------+
          |            |            |
          v            v            v
        Pod 1        Pod 2        Pod 3
```

Because our application returns the Pod hostname:

```python
socket.gethostname()
```

we can see which Pod handled the request.

Send multiple requests to:

```text
http://localhost:8080
```

Example response:

```json
{
    "message": "Hello from Kubernetes!",
    "pod": "fastapi-demo-69fd4658bc-n2ccg"
}
```

Another request:

```json
{
    "message": "Hello from Kubernetes!",
    "pod": "fastapi-demo-69fd4658bc-nnrtb"
}
```

Another:

```json
{
    "message": "Hello from Kubernetes!",
    "pod": "fastapi-demo-69fd4658bc-w79jh"
}
```

The requests are being distributed across the available Pods.

This demonstrates:

# Load Balancing

---

# Final Architecture

```text
                       USER
                        |
                        v
              +-------------------+
              | Kubernetes Service|
              | fastapi-service    |
              +---------+---------+
                        |
             Load Balancing
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       +------+      +------+      +------+
       | Pod 1|      | Pod 2|      | Pod 3|
       |FastAPI      |FastAPI      |FastAPI
       +------+      +------+      +------+
          ^
          |
          |
    +-----+------+
    | Deployment |
    | replicas:3 |
    +------------+
```

---

# What We Demonstrated

## 1. Deployment

```yaml
replicas: 3
```

Kubernetes creates 3 Pods.

---

## 2. Self-Healing

```powershell
kubectl delete pod <pod-name>
```

Kubernetes automatically creates a replacement Pod.

---

## 3. Load Balancing

```text
User
 |
Service
 |
+--- Pod 1
+--- Pod 2
+--- Pod 3
```

The Service distributes requests among the Pods.

---

# Important Commands

```powershell
# Check cluster
kubectl get nodes

# Deploy application
kubectl apply -f deployment.yaml

# Check deployment
kubectl get deployment

# Check pods
kubectl get pods

# Watch pods
kubectl get pods -w

# Delete pod - test self-healing
kubectl delete pod <pod-name>

# Create service
kubectl apply -f service.yaml

# Check service
kubectl get service

# Access application
kubectl port-forward service/fastapi-service 8080:80

# View pod details
kubectl describe pod <pod-name>

# View application logs
kubectl logs <pod-name>
```

---

# Key Concepts

### Deployment

Manages the desired number of Pods.

### Pod

The smallest deployable unit in Kubernetes.

### Service

Provides a stable endpoint to access Pods and distributes traffic among matching Pods.

### Self-Healing

Kubernetes automatically replaces failed or deleted Pods to maintain the desired state.

### Load Balancing

The Kubernetes Service distributes incoming traffic across the available Pods.

---

# Flow

```text
Dockerfile
    |
    v
Docker Image
    |
    v
Docker Hub
    |
    v
Kubernetes Deployment
    |
    v
3 Pods
    |
    v
Kubernetes Service
    |
    v
Load Balancing
```

Self-healing happens automatically:

```text
Pod
 |
X
 |
Deployment detects missing Pod
 |
v
New Pod
 |
v
3 Pods maintained
```

```
```
