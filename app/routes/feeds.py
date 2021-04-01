from fastapi import APIRouter, HTTPException
from typing import List
from ..services.esdr import EsdrService
from ..models.esdr import *

router = APIRouter()
service = EsdrService()

# Feeds
@router.get('/feeds/data/{feedId}',
    tags=["Feeds"],
    name="Get Single Feed Data",
    description="Returns data for a single feed",
    responses={200: {"model": FeedData}, 404: {}})
async def get_feed_data(feedId: int):
    result = service.Get_Feed_Data(feedId)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")

@router.get('/feeds/location/{locationId}',
    tags=["Feeds"],
    name="Get Location Feed Data",
    description="Returns data for all feeds in a particular location",
    responses={200: {"model": List[FeedData]}, 404: {}})
async def get_location_data(locationId: int):
    result = await service.Get_Location_Data_Async(locationId)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, detail="No data found")

# @router.get('/feeds/location/{locationId}/sync',
#     tags=["Feeds"],
#     name="Get location data (synchronously)",
#     description="Returns data for all feeds in a particular location",
#     responses={200: {"model": List[FeedData]}, 404: {}})
async def get_location_data_sync(locationId: int):
    result = service.Get_Location_Data_Sync(locationId)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, detail="No data found")

@router.get('/feeds/region/{regionId}',
    tags=["Feeds"],
    name="Get Region Feed Data",
    description="Returns data for all feeds in a particular region",
    responses={200: {"model": List[FeedData]}, 404: {}})
async def get_region_data(regionId: int):
    result = await service.Get_Region_Data_Async(regionId)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, detail="No data found")

@router.get('/feeds/wind',
    tags=["Feeds"],
    name="Get Wind Data",
    description="Returns data for all wind feeds",
    responses={200: {"model": List[FeedData]}, 404: {}})
async def get_wind_data():
    result = await service.Get_Wind_Data_Async()

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, detail="No data found")

# @router.get('/feeds/wind/sync',
#     tags=["Feeds"],
#     name="Get wind data (synchronously)",
#     description="Returns data for all wind feeds",
#     responses={200: {"model": List[FeedData]}, 404: {}})
async def get_wind_data_sync():
    result = service.Get_Wind_Data_Sync()

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, detail="No data found")

