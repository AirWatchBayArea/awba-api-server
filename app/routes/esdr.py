from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from ..services.esdr import EsdrService
from ..models.esdr import *
from ..models.routes import ErrorMessage

router = APIRouter()
service = EsdrService()

# Feeds
@router.get('/feeds/{feed_id}/data',
    tags=["Feeds"],
    name="Get Feed Data",
    description="Returns data for a single feed ID",
    responses={200: {"model": FeedData}, 404: {"model": ErrorMessage}})
async def get_feed_data(feed_id: int):
    result = service.Get_Feed_Data(feed_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/feeds/location/{location_id}',
    tags=["Feeds"],
    name="Get location data (asynchronously)",
    description="Returns data for all feeds in a particular location",
    responses={200: {"model": List[FeedData]}, 404: {"model": ErrorMessage}})
async def get_location_data(location_id: int):
    result = await service.Get_Location_Data_Async(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/feeds/location/{location_id}/sync',
    tags=["Feeds"],
    name="Get location data (synchronously)",
    description="Returns data for all feeds in a particular location",
    responses={200: {"model": List[FeedData]}, 404: {"model": ErrorMessage}})
async def get_location_data_sync(location_id: int):
    result = service.Get_Location_Data_Sync(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/feeds/wind',
    tags=["Feeds"],
    name="Get wind data (asynchronously)",
    description="Returns data for all wind feeds",
    responses={200: {"model": List[FeedData]}, 404: {"model": ErrorMessage}})
async def get_wind_data():
    result = await service.Get_Wind_Data_Async()

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/feeds/wind/sync',
    tags=["Feeds"],
    name="Get wind data (synchronously)",
    description="Returns data for all wind feeds",
    responses={200: {"model": List[FeedData]}, 404: {"model": ErrorMessage}})
async def get_wind_data_sync():
    result = service.Get_Wind_Data_Sync()

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/locations',
    tags=["Locations"],
    name="Get the list of locations",
    description="Returns the list of locations with their ESDR Feed IDs",
    response_model=List[Location])
async def get_locations():
    return service.Get_Locations()

@router.get('/locations/{location_id}',
    tags=["Locations"],
    name="Get a specific location",
    description="Returns the location details with its ESDR Feed IDs",
    responses={200: {"model": Location}, 404: {"model": ErrorMessage}})
async def get_location(location_id: int):
    result = service.Get_Location(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
