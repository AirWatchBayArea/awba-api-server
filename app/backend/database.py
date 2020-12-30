from ..feeds import ESDR_FEEDS, WIND_FEEDS
from typing import Dict, List
import os
import psycopg2

class Database:

    AWBA_LOCATIONS = "awba_locations"
    AWBA_FEEDS = "awba_feeds"
    DATABASE_URL = os.environ['DATABASE_URL']

    def __init__(self):
        # Create a connection to the database
        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

        # Create the tables necessary for the API
        if not(self.Check_Table(self.AWBA_LOCATIONS)):
            self.Create_Location_Table()
        if not(self.Check_Table(self.AWBA_FEEDS)):
            self.Create_Feeds_Table()

    # Simple check to make sure a table exists
    def Check_Table(self, table_name):
        cur = self.conn.cursor()
        sql = "SELECT * FROM {0} WHERE 0=1;".format(table_name)

        try:
            cur.execute(sql)
            print("Table [{0}]: exists".format(table_name))
            return True
        except:
            print("Table [{0}]: does not exist".format(table_name))
            return False

    # Creates the feeds table if it doesn't already exist
    def Create_Feeds_Table(self):
        cur = self.conn.cursor()
        sql = (
                "CREATE TABLE {0} ("
                " id INT GENERATED ALWAYS AS IDENTITY,"
                " location_id INT NOT NULL,"
                " feed_id INT NOT NULL,"
                " PRIMARY KEY(id),"
                " CONSTRAINT fk_location"
                " FOREIGN KEY(location_id)"
                " REFERENCES {1}(location_id)"
                "); COMMIT;"
        ).format(self.AWBA_FEEDS, self.AWBA_LOCATIONS)

        try:
            cur.execute(sql)
            print("Table [{0}]: created".format(self.AWBA_FEEDS))
            return True
        except Exception as e:
            print("Table [{0}]: not created. Reason: {1}".format(self.AWBA_FEEDS, e))
            return False
            
    # Creates the location table if it doesn't already exist
    def Create_Location_Table(self):
        cur = self.conn.cursor()
        sql = (
                "CREATE TABLE {0} ("
                " location_id INT GENERATED ALWAYS AS IDENTITY,"
                " location_name VARCHAR(80),"
                " PRIMARY KEY(location_id)"
                "); COMMIT;"
        ).format(self.AWBA_LOCATIONS)

        try:
            cur.execute(sql)
            print("Table [{0}]: created".format(self.AWBA_LOCATIONS))
            return True
        except Exception as e:
            print("Table [{0}]: not created.  Reason: {1}".format(self.AWBA_LOCATIONS, e))
            return False
            
    def Get_Location(self, location_id):
        filtered_list = [item for item in ESDR_FEEDS if item["id"] == location_id]

        if len(filtered_list) > 0:
            return filtered_list[0]
        else:
            return None

    def Get_Locations(self):
        return ESDR_FEEDS

    def Get_Wind_Feeds(self):
        return WIND_FEEDS

