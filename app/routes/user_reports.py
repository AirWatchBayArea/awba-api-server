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
    responses={200: {"model": UserReport}, 204: {}, 404: {}})
async def get_user_reports():
    result = service.Get_User_Reports()

    if result != None:
        return result
    else:
        return HTTPException(status_code=404, details="No data found")
