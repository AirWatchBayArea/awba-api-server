from fastapi import APIRouter
from ..services.esdr import EsdrService

router = APIRouter()
service = EsdrService()

@router.get('/esdr', 
    tags=["ESDR"], 
    name="Return Basic Function", 
    description="This is a basic function")
async def some_function():
    return service.Get_Something()
    
@router.get('/esdr/feed/{feed_id}', 
    tags=["ESDR"], 
    name="Return a feed id", 
    description="This function returns a feed id")
async def other_function(feed_id: int):
    return service.Other_Function(feed_id)