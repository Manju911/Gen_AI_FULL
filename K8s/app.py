from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello from Kubernetes",
        "pod": socket.gethostname()
    }