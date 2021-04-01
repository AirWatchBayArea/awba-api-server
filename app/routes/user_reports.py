from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.user_reports import UserReportsService
from ..models.user_reports import *

router = APIRouter()
service = UserReportsService()

# Feeds
@router.get('/user-reports',
    tags=["User Reports"],
    name="Get all AWBA user reports",
    description="Returns all user-submitted smell reports for the AWBA client",
    responses={200: {"model": List[UserReport]}, 204: {}, 404: {}})
async def get_user_reports():
    result = await service.Get_User_Reports_Sync()

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")

@router.get('/user-reports/location/{locationId}',
    tags=["User Reports"],
    name="Get user reports for a given location",
    description="Returns user-submitted smell reports for a specific location",
    responses={200: {"model": List[UserReport]}, 204: {}, 404: {}})
async def get_user_reports(locationId: int):
    result = await service.Get_User_Reports_Location_Sync(locationId)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")
