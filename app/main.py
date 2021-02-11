import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .backend.database import Database
from .routes import feeds, locations, user_reports

tags_metadata = [
    {
        "name": "Feeds",
        "description": "Operations that get feed data from Esdr.",
    },
    {
        "name": "Locations",
        "description": "Manage locations and feeds which are monitored.",
    },
    {
        "name": "User Reports",
        "description": "Operations that get user reports from Smell Pittsburgh"
    }
]

app = FastAPI(debug=True,
    openapi_tags=tags_metadata,
    title="AWBA API Server", 
    version="1.0.0")

origins = ["*"]

@app.on_event("startup")
async def Verify_Database():
    # Make sure the tables exist
    database = Database()
    database.Verify_Tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=[],
)

app.include_router(feeds.router)
app.include_router(locations.router)
app.include_router(user_reports.router)
