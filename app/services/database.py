from ..backend.database import Database

class DatabaseService:

    def __init__(self):
        self.database = Database()

    # Add a new location with feed ids
    def Add_Locations(self, locations):  
        result = {"Succeeded": [], "Failed": []}

        for location in locations: 
            if not(0 in location.feedIds):
                new_item = self.database.Add_Location(location)
            else:
                new_item = {"new_id": 0}

            if new_item["new_id"] > 0:
                location.id = new_item["new_id"]
                result["Succeeded"].append(location)
            else:
                result["Failed"].append(location)

        return result

    # Add a new region with location ids
    def Add_Region(self, regions):  
        result = {"Succeeded": [], "Failed": []}

        for region in regions: 
            if not(0 in region.locationIds):
                new_item = self.database.Add_Region(region)
            else:
                new_item = {"new_id": 0}

            if new_item["new_id"] > 0:
                region.id = new_item["new_id"]
                result["Succeeded"].append(region)
            else:
                result["Failed"].append(region)

        return result

    # Delete a location from the database
    def Delete_Location(self, location_id):
        return self.database.Delete_Location(location_id)

    # Delete a region from the database
    def Delete_Region(self, region_id):
        return self.database.Delete_Region(region_id)

    # Get details about a location id
    def Get_Location(self, location_id):
        return self.database.Get_Location(location_id)

    # Get details about all locations
    def Get_Locations(self, name, feedIds):
        return self.database.Get_Locations(name, feedIds)

    # Get details about a region
    def Get_Region(self, region_id):
        return self.database.Get_Region(region_id)

    # Get details about all regions
    def Get_Regions(self, name):
        return self.database.Get_Regions(name)

    # Update a location
    def Update_Location(self, location_id, location):
        return self.database.Update_Location(location_id, location)

    # Update a region
    def Update_Region(self, region_id, region):
        return self.database.Update_Region(region_id, region)