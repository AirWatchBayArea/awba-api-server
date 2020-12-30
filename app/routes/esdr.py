from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from ..services.esdr import EsdrService
from ..models.esdr import Location
from ..models.routes import ErrorMessage

router = APIRouter()
service = EsdrService()

# Feeds
@router.get('/feeds/data/async/{location_id}',
    tags=["Feeds"],
    name="Get location data (asynchronously)",
    description="Returns data for all feeds in a particular location",
    responses={200: {"model": []}, 404: {"model": ErrorMessage}})
async def get_location_data(location_id: int):
    result = await service.Get_Location_Data_Async(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/feeds/data/sync/{location_id}',
    tags=["Feeds"],
    name="Get location data (synchronously)",
    description="Returns data for all feeds in a particular location",
    responses={200: {"model": []}, 404: {"model": ErrorMessage}})
def get_location_data_sync(location_id: int):
    result = service.Get_Location_Data_Sync(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "No data found"})

@router.get('/locations',
    tags=["Locations"],
    name="Get the list of locations",
    description="Returns the list of locations with their ESDR Feed IDs",
    response_model=List[Location])
def get_locations():
    return service.Get_Locations()

@router.get('/locations/{location_id}',
    tags=["Locations"],
    name="Get a specific location",
    description="Returns the location details with its ESDR Feed IDs",
    responses={200: {"model": Location}, 404: {"model": ErrorMessage}})
def get_location(location_id: int):
    result = service.Get_Location(location_id)

    if result != None:
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

@router.get('/test', 
    tags=["Test"], 
    name="Return Basic Function", 
    description="This is a basic function")
def some_function():
    return service.Get_Something()
    
@router.get('/test/feed/{feed_id}', 
    tags=["Test"], 
    name="Return a feed id", 
    description="This function returns a feed id")
def other_function(feed_id: int):
    return service.Other_Function(feed_id)

