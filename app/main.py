import requests
from fastapi import FastAPI
from .routes import feeds, locations

tags_metadata = [
    {
        "name": "Feeds",
        "description": "Operations that get feed data from Esdr.",
    },
    {
        "name": "Locations",
        "description": "Manage locations and feeds which are monitored.",
    }
]

app = FastAPI(debug=True,
    openapi_tags=tags_metadata,
    title="AWBA API Server", 
    version="1.0.0")
# app.include_router(feeds.router, prefix="/api/v1")
app.include_router(feeds.router)
app.include_router(locations.router)
