from ..feeds import ESDR_FEEDS

class Database:

    def Get_Location(self, location_id):
        filtered_list = [item for item in ESDR_FEEDS if item["id"] == location_id]

        if len(filtered_list) > 0:
            return filtered_list[0]
        else:
            return None

    def Get_Locations(self):
        return ESDR_FEEDS

