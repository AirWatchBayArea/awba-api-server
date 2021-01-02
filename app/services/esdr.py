from ..backend.database import Database
from ..backend.esdr import EsdrBackend
from ..models.esdr import Location
import aiohttp
import asyncio

class EsdrService:

    def __init__(self):
        self.backend = EsdrBackend()
        self.database = Database()

    # Gets the feed data synchronously
    def Get_Feed_Data(self, feed_id):
        feed = self.backend.Get_Feed_Data_Sync(feed_id)
        return feed

    # Gets the feed data asynchronously
    async def Get_Location_Data_Async(self, location_id):
        location = self.Get_Location(location_id)
        tasks = []

        async with aiohttp.ClientSession() as session:
            for feedId in location.get("feedIds"):
                tasks.append(self.backend.Get_Feed_Data_Async(session, feedId))
            result = await asyncio.gather(*tasks)

        return result

    # Gets the feed data synchronously
    def Get_Location_Data_Sync(self, location_id):
        location = self.Get_Location(location_id)
        result = []

        for feedId in location.get("feedIds"):
            feed = self.backend.Get_Feed_Data_Sync(feedId)
            result.append(feed)

        return result

    # Gets the wind feed data asynchronously
    async def Get_Wind_Data_Async(self):
        feeds = self.database.Get_Wind_Feeds()
        tasks = []

        async with aiohttp.ClientSession() as session:
            for feedId in feeds:
                tasks.append(self.backend.Get_Feed_Data_Async(session, feedId))
            result = await asyncio.gather(*tasks)

        return result

    # Gets the wind feed data synchronously
    def Get_Wind_Data_Sync(self):
        feeds = self.database.Get_Wind_Feeds()
        result = []

        for feedId in feeds:
            feed = self.backend.Get_Feed_Data_Sync(feedId)
            result.append(feed)

        return result
