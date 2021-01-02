import requests
from fastapi import FastAPI
from .backend.database import Database
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

@app.on_event("startup")
async def Verify_Database():
    # Make sure the tables exist
    database = Database()
    database.Verify_Tables()

app.include_router(feeds.router)
app.include_router(locations.router)
