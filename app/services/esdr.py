from fastapi.responses import JSONResponse
from ..backend.database import Database
from ..backend.esdr import EsdrBackend
from ..feeds import ESDR_FEEDS
from ..models.esdr import Location
import json

class EsdrService:

    def __init__(self):
        self.backend = EsdrBackend()
        self.database = Database()

    def Get_Location(self, location_id):
        return self.database.Get_Location(location_id)

    def Get_Locations(self):
        return self.database.Get_Locations()

    def Get_Something(self):
        return [{"name": "value"}]

    def Other_Function(self, feed_id):
        return [{"feed": feed_id}]