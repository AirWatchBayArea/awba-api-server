from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.database import DatabaseService
from ..models.esdr import *

router = APIRouter()
service = DatabaseService()

@router.get('/locations',
    tags=["Locations"],
    name="Get Locations",
    description="Returns the list of available locations with their ESDR Feed IDs",
    response_model=List[Location])
async def get_locations(name: Optional[str] = Query(
                            None, 
                            title="Location Name (Optional)", 
                            description="The name of a location (case insensitive)", 
                            regex="^[A-Za-z ]+$"), 
                        feedIds: Optional[str] = Query(
                            None,
                            title="Feed Ids (Optional)",
                            description="A comma-delimited list of feed Ids",
                            regex="^[0-9,]+$")):
    # Split any input feedIds into a list
    if not(feedIds is None):
        feedIdList = feedIds.split(",")
    else:
        feedIdList = None

    # Return locations which match
    return service.Get_Locations(name, feedIdList)

@router.post('/locations',
    tags=["Locations"],
    name="Add locations",
    description="Adds new location(s) with a list of feed IDs",
    responses={200: {"model": LocationItems}, 500: {}})
async def add_location(locations: List[Location]):
    result = service.Add_Locations(locations)

    if len(result["Succeeded"]) > 0:
        return result
    else:
        raise HTTPException(status_code=500, detail="Unable to add locations")

@router.put('/locations/{locationId}',
    tags=["Locations"],
    name="Update a Location",
    description="Updates a location with a list of feed IDs",
    responses={200: {"model": Location}, 500: {}})
async def update_location(locationId: int, location: Location):
    result = service.Update_Location(locationId, location)

    # Return the new location and feed Ids from the database
    if (result["location_rows"] > 0) or (result["feed_rows"] > 0):
        return await get_location(locationId)
    else:
        raise HTTPException(status_code=500, detail="Unable to update location")

@router.delete('/locations/{locationId}',
    tags=["Locations"],
    name="Delete a Location",
    description="Deletes a location from the database",
    responses={404: {}})
async def delete_location(locationId: int):
    print("Deleting location: {0}",format(locationId))
    result = service.Delete_Location(locationId)

    if (result["location_rows"] == 0) or (result["location_rows"] is None):
        raise HTTPException(status_code=404, detail="Location not found")

@router.get('/locations/{locationId}',
    tags=["Locations"],
    name="Get a Location",
    description="Returns a location with its Feed IDs",
    responses={200: {"model": Location}, 404: {}})
async def get_location(locationId: int):
    result = service.Get_Location(locationId)

    if result != None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Location {0} not found".format(locationId))
