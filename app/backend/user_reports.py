from ..config import SMELL_PITTSBURGH_API_ROOT_URL
from ..models.user_reports import LocationBounds
import json
import requests

class UserReportsBackend:

    QRY_SMELL_AWBA_CLIENT = "&client_ids=2"
    QRY_SMELL_BBOX = "&latlng_bbox={0},{1},{2},{3}"
    QRY_SMELL_REPORTS = "{0}/smell_reports?format=json&timezone_string=America/Los_Angeles"

    # Gets the user_reports asynchronously (uses asyncio's ClientRequest and ClientResponse)
    async def Get_User_Reports_Async(self, session):
        query = self.QRY_SMELL_REPORTS.format(SMELL_PITTSBURGH_API_ROOT_URL) + self.QRY_SMELL_AWBA_CLIENT
        #print(query)

        async with session.get(query) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return None

    # Gets the user_reports synchronously (uses requests/response)
    def Get_User_Reports_Sync(self):
        query = self.QRY_SMELL_REPORTS.format(SMELL_PITTSBURGH_API_ROOT_URL) + self.QRY_SMELL_AWBA_CLIENT
        #print(query)

        response = requests.get(query)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Gets the user_reports synchronously (uses requests/response)
    def Get_User_Reports_Location_Sync(self, bounds: LocationBounds):
        query = self.QRY_SMELL_REPORTS.format(SMELL_PITTSBURGH_API_ROOT_URL)
        bbox = self.QRY_SMELL_BBOX.format(bounds.minLatitude, bounds.minLongitude, bounds.maxLatitude, bounds.maxLongitude)
        #print(query + bbox)

        response = requests.get(query + bbox)
        if response.status_code == 200:
            return response.json()
        else:
            return None
