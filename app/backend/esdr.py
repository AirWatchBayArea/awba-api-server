from ..config import ESDR_API_ROOT_URL
from ..feeds import ESDR_FEEDS
import json
import requests

class EsdrBackend:

    # Gets the feed data asynchronously (uses asyncio's ClientRequest and ClientResponse)
    async def Get_Feed_Data_Async(self, session, feed_id):
        async with session.get(ESDR_API_ROOT_URL + '/feeds/' + str(feed_id)) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("data")
            else:
                return None

    # Gets the feed data synchronously (uses requests/response)
    def Get_Feed_Data_Sync(self, feed_id):
        response = requests.get(ESDR_API_ROOT_URL + '/feeds/' + str(feed_id))
        if response.status_code == 200:
            return response.json().get("data")
        else:
            return None

    def Get_Something(self):
        return [{"name": "value"}]

    def Other_Function(self, feed_id):
        return [{"feed": feed_id}]