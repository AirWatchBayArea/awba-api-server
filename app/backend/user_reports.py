from ..config import SMELL_PITTSBURGH_API_ROOT_URL
import json
import requests

class UserReportsBackend:

    QRY_SMELL_REPORTS = "{0}/smell_reports?format=json&client_ids=2&timezone_string=America/Los_Angeles"

    # Gets the user_reports asynchronously (uses asyncio's ClientRequest and ClientResponse)
    async def Get_User_Reports_Async(self):
        async with session.get(self.QRY_SMELL_REPORTS.format(SMELL_PITTSBURGH_API_ROOT_URL)) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("data")
            else:
                return None

    # Gets the user_reports synchronously (uses requests/response)
    def Get_User_Reports_Sync(self):
        response = requests.get(self.QRY_SMELL_REPORTS.format(SMELL_PITTSBURGH_API_ROOT_URL))
        if response.status_code == 200:
            return response.json()
        else:
            return None
