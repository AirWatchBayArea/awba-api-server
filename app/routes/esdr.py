from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from ..services.esdr import EsdrService
from ..models.esdr import Location
from ..models.routes import ErrorMessage

router = APIRouter()
service = EsdrService()

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

@router.get('/test', 
    tags=["Test"], 
    name="Return Basic Function", 
    description="This is a basic function")
async def some_function():
    return service.Get_Something()
    
@router.get('/test/feed/{feed_id}', 
    tags=["Test"], 
    name="Return a feed id", 
    description="This function returns a feed id")
async def other_function(feed_id: int):
    return service.Other_Function(feed_id)

