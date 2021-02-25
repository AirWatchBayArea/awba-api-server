from ..backend.database import Database
from ..backend.user_reports import UserReportsBackend
from ..models.user_reports import UserReport, LocationBounds
from ..services.esdr import EsdrService
import aiohttp
import asyncio

class UserReportsService:

    def __init__(self):
        self.backend = UserReportsBackend()
        self.database = Database()
        self.esdrService = EsdrService()

    # Gets user reports from Smell Pittsburgh
    async def Get_User_Reports_Sync(self):
        reports = self.backend.Get_User_Reports_Sync()
        return reports

    # Gets user reports from Smell Pittsburgh
    async def Get_User_Reports_Location_Sync(self, location_id):
        feeds = await self.esdrService.Get_Location_Data_Async(location_id)
        bounds = LocationBounds(maxLatitude=0, minLatitude=0, maxLongitude=0, minLongitude=0)

        for feed in feeds:
            if (bounds.minLatitude == 0) or (bounds.minLatitude > feed['latitude']):
                bounds.minLatitude = feed['latitude']
            if (bounds.minLongitude == 0) or (bounds.minLongitude > feed['longitude']):
                bounds.minLongitude = feed['longitude']
            if (bounds.maxLatitude == 0) or (bounds.maxLatitude < feed['latitude']):
                bounds.maxLatitude = feed['latitude']
            if (bounds.maxLongitude == 0) or (bounds.maxLongitude < feed['longitude']):
                bounds.maxLongitude = feed['longitude']
          
        # Expand bounds slightly
        bounds.minLatitude = bounds.minLatitude - 0.01
        bounds.maxLatitude = bounds.maxLatitude + 0.01
        bounds.minLongitude = bounds.minLongitude - 0.01
        bounds.maxLongitude = bounds.maxLongitude + 0.01

        reports = self.backend.Get_User_Reports_Location_Sync(bounds)
        return reports
        return {}
