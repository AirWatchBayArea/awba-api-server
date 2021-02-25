from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.user_reports import UserReportsService
from ..models.user_reports import *

router = APIRouter()
service = UserReportsService()

# Feeds
@router.get('/user-reports',
    tags=["User Reports"],
    name="Get user reports",
    description="Returns user-submitted smell reports",
    responses={200: {"model": List[UserReport]}, 204: {}, 404: {}})
async def get_user_reports():
    result = await service.Get_User_Reports_Sync()

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")

@router.get('/user-reports/location/{location_id}',
    tags=["User Reports"],
    name="Get user reports for a given location ID",
    description="Returns user-submitted smell reports for a specific location ID",
    responses={200: {"model": List[UserReport]}, 204: {}, 404: {}})
async def get_user_reports(location_id: int):
    result = await service.Get_User_Reports_Location_Sync(location_id)

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")
