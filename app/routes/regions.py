from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.database import DatabaseService
from ..models.esdr import *

router = APIRouter()
service = DatabaseService()

@router.get('/regions',
    tags=["Regions"],
    name="Get Regions",
    description="Returns the list of available regions with their location IDs",
    response_model=List[Region])
async def get_regions(name: Optional[str] = Query(
                            None, 
                            title="Region Name (Optional)", 
                            description="The name of a region (case insensitive)", 
                            regex="^[A-Za-z ]+$")):
    # Return locations which match
    return service.Get_Regions(name)

# @router.post('/regions',
#     tags=["Regions"],
#     name="Add Regions",
#     description="Adds new region(s) with a list of location IDs",
#     responses={200: {"model": RegionItems}, 500: {}})
async def add_region(regions: List[Region]):
    result = service.Add_Region(regions)

    if len(result["Succeeded"]) > 0:
        return result
    else:
        raise HTTPException(status_code=500, detail="Unable to add regions")

# @router.put('/regions/{region_id}',
#     tags=["Regions"],
#     name="Update a region",
#     description="Updates a region with a list of location IDs",
#     responses={200: {"model": Region}, 500: {}})
async def update_region(region_id: int, region: Region):
    result = service.Update_Region(region_id, region)

    # Return the new region and location Ids from the database
    if (result["region_rows"] > 0):
        return await get_region(region_id)
    else:
        raise HTTPException(status_code=500, detail="Unable to update region")

# @router.delete('/regions/{region_id}',
#     tags=["Regions"],
#     name="Delete a Region",
#     description="Deletes a region from the database",
#     responses={404: {}})
async def delete_region(region_id: int):
    print("Deleting region: {0}",format(region_id))
    result = service.Delete_Region(region_id)

    if (result["region_rows"] == 0) or (result["region_rows"] is None):
        raise HTTPException(status_code=404, detail="Region not found")

@router.get('/regions/{region_id}',
    tags=["Regions"],
    name="Get a Region",
    description="Returns a region with its location IDs",
    responses={200: {"model": Region}, 404: {}})
async def get_region(region_id: int):
    result = service.Get_Region(region_id)

    if result != None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Region {0} not found".format(region_id))
