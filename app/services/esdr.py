from fastapi.responses import JSONResponse
from ..backend.esdr import EsdrBackend
from ..feeds import ESDR_FEEDS
from ..models.esdr import Location
import json

class EsdrService:

    def __init__(self):
        self.backend = EsdrBackend()

    def Get_Location(self, location_id):
        filtered_list = [item for item in ESDR_FEEDS if item["id"] == location_id]

        if len(filtered_list) > 0:
            return filtered_list[0]
        else:
            return None

    def Get_Locations(self):
        return ESDR_FEEDS

    def Get_Something(self):
        return [{"name": "value"}]

    def Other_Function(self, feed_id):
        return [{"feed": feed_id}]