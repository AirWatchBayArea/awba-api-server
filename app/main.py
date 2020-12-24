import hypercorn
import requests
from fastapi import FastAPI
from .routes import esdr_v1

app = FastAPI(debug=True, title="AWBA API Server", description="This provides AWBA API functionality", version="0.0.0b")
app.include_router(esdr_v1.router, prefix="/api/v1")