from ..backend.database import Database
from ..backend.user_reports import UserReportsBackend
from ..models.user_reports import UserReport
import aiohttp
import asyncio

class UserReportsService:

    def __init__(self):
        self.backend = UserReportsBackend()
        self.database = Database()

    # Gets user reports from Smell Pittsburgh
    async def Get_User_Reports_Sync(self):
        reports = self.backend.Get_User_Reports_Sync()
        return reports
