from fastapi.responses import JSONResponse
from ..backend.database import Database
from ..backend.esdr import EsdrBackend
from ..feeds import ESDR_FEEDS
from ..models.esdr import Location
import aiohttp
import asyncio
import json
import time

class EsdrService:

    def __init__(self):
        self.backend = EsdrBackend()
        self.database = Database()

    # Gets the feed data asynchronously
    async def Get_Location_Data_Async(self, location_id):
        starttime = time.time()
        location = self.Get_Location(location_id)
        tasks = []

        async with aiohttp.ClientSession() as session:
            for feedId in location.get("feedIds"):
                tasks.append(self.backend.Get_Feed_Data_Async(session, feedId))
            result = await asyncio.gather(*tasks)

        stoptime = time.time()
        print("Processing Time: {0} seconds".format(stoptime-starttime))
        return result

    # Gets the feed data synchronously
    def Get_Location_Data_Sync(self, location_id):
        starttime = time.time()
        location = self.Get_Location(location_id)
        result = []

        for feedId in location.get("feedIds"):
            feed = self.backend.Get_Feed_Data_Sync(feedId)
            result.append(feed)

        stoptime = time.time()
        print("Processing Time: {0} seconds".format(stoptime-starttime))
        return result

    def Get_Location(self, location_id):
        return self.database.Get_Location(location_id)

    def Get_Locations(self):
        return self.database.Get_Locations()

    def Get_Something(self):
        return [{"name": "value"}]

    def Other_Function(self, feed_id):
        return [{"feed": feed_id}]