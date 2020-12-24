import requests
import socket
from fastapi import FastAPI
from .routes import esdr_v1

app = FastAPI(debug=True, title="AWBA API Server", description="This provides AWBA API functionality", version="0.0.0b")
app.include_router(esdr_v1.router, prefix="/api/v1")
hostname = socket.gethostname()

@app.get("/")
async def read_root():
    return {
        "name": "AWBA API Server",
        "host": hostname, 
        "version": "1.0"
    }