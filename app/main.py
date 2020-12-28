import requests
from fastapi import FastAPI
from .routes import esdr

app = FastAPI(debug=True, 
    title="AWBA API Server", 
    version="1.0.0")
app.include_router(esdr.router, prefix="/api/v1")
