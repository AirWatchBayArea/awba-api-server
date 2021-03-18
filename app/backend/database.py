from ..feeds import ESDR_FEEDS, WIND_FEEDS
from ..models.esdr import Location, Region
from fastapi import HTTPException
from psycopg2._psycopg import ProgrammingError
from typing import Dict, List
import os
import psycopg2

class Database:

    # For local debugging purposes with PostgreSQL, do the following steps:
    # 1. Install postgresql and psycopg2 based on the following document:
    #    - https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
    # 2. If using Linux / Mac, use the following export command (ignore the export step in the above doc link):
    #    - export DATABASE_URL=postgres:///$(whoami)

    AWBA_FEEDS = "awba_feeds"
    AWBA_LOCATIONS = "awba_locations"
    AWBA_REGIONS = "awba_regions"
    DATABASE_URL = os.environ['DATABASE_URL']

    # def __init__(self):
        # Create a connection to the database
        # self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

    def New_Connection(self):
        return psycopg2.connect(self.DATABASE_URL, sslmode='require')

    # Adds a new constraint to a column
    def Add_Column_Constraint(self, conn, table_name, constraint_name, constraint_definition):
        cur = conn.cursor()
        sql = (
                "ALTER TABLE {0}"
                " ADD CONSTRAINT {1} {2};"
        ).format(table_name, constraint_name, constraint_definition)

        try:
            cur.execute(sql)
            conn.commit()
            print("Constraint [{0}]: created".format(constraint_name))
            return True
        except Exception as e:
            conn.rollback()
            print("Constraint [{0}]: not created.  Reason: {1}".format(constraint_name, e))
            return False
            
    # Adds a new column to a table
    def Add_Table_Column(self, conn, table_name, column_name, data_type):
        cur = conn.cursor()
        sql = (
                "ALTER TABLE {0}"
                " ADD COLUMN {1} {2};"
        ).format(table_name, column_name, data_type)

        try:
            cur.execute(sql)
            conn.commit()
            print("Column [{0}]: created".format(column_name))
            return True
        except Exception as e:
            conn.rollback()
            print("Column [{0}]: not created.  Reason: {1}".format(column_name, e))
            return False
            
    # Adds a new location with feed ids to the database
    def Add_Location(self, location: Location):
        result = {"new_id": -1}
        conn = self.New_Connection()
        cur = conn.cursor()

        try:
            # Insert into Locations table
            sql = (
                    "INSERT INTO {0}"
                    " (location_id, location_name, region_id) "
                    "VALUES"
                    " (DEFAULT, %s, %s) "
                    "RETURNING location_id;"
            ).format(self.AWBA_LOCATIONS)

            cur.execute(sql, (location.name, location.regionId))
            result["new_id"] = cur.fetchone()[0]

            if result["new_id"] > 0:
                # Insert into Feeds table
                for feedId in location.feedIds:
                    sql = (
                            "INSERT INTO {0}"
                            " (id, location_id, feed_id) "
                            "VALUES"
                            " (DEFAULT, %s, %s)"
                    ).format(self.AWBA_FEEDS)

                    cur.execute(sql, (result["new_id"], feedId))

            # Finally, commit the transaction
            if result["new_id"] > 0:
                conn.commit()
            else:
                raise ProgrammingError("No location added")
        except Exception as e:
            conn.rollback()
            result["new_id"] = -1
            result["error_message"] = e
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    # Adds a new region with location ids to the database
    def Add_Region(self, region: Region):
        result = {"new_id": -1}
        conn = self.New_Connection()
        cur = conn.cursor()

        try:
            # Insert into Locations table
            sql = (
                    "INSERT INTO {0}"
                    " (region_id, region_name) "
                    "VALUES"
                    " (DEFAULT, %s) "
                    "RETURNING region_id;"
            ).format(self.AWBA_REGIONS)

            cur.execute(sql, (region.name,))
            result["new_id"] = cur.fetchone()[0]

            # Create comma-delimited list of locations
            if not(region.locationIds is None):
                locationList = ",".join(str(id) for id in region.locationIds)
            else:
                locationList = ""

            if (result["new_id"] > 0) and (locationList != ""):
                # Update Location table
                sql = (
                    "UPDATE {0}"
                    " SET region_id = {1}"
                    " WHERE location_id in ({2});"
                ).format(self.AWBA_LOCATIONS, result["new_id"], locationList)

                cur.execute(sql)

            # Finally, commit the transaction
            if result["new_id"] > 0:
                conn.commit()
            else:
                raise ProgrammingError("No region added")
        except Exception as e:
            conn.rollback()
            result["new_id"] = -1
            result["error_message"] = e
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    # Simple check to make sure a column exists in a table
    def Check_Column(self, conn, table_name, column_name):
        cur = conn.cursor()
        sql = "SELECT {0} FROM {1} WHERE 0=1;".format(column_name, table_name)

        try:
            cur.execute(sql)
            print("Column [{0}]: exists".format(column_name))
            return True
        except:
            conn.rollback()
            print("Column [{0}]: does not exist".format(column_name))
            return False

    # Simple check to make sure a table exists
    def Check_Table(self, conn, table_name):
        cur = conn.cursor()
        sql = "SELECT * FROM {0} WHERE 0=1;".format(table_name)

        try:
            cur.execute(sql)
            print("Table [{0}]: exists".format(table_name))
            return True
        except:
            conn.rollback()
            print("Table [{0}]: does not exist".format(table_name))
            return False

    # Creates the feeds table if it doesn't already exist
    def Create_Feeds_Table(self, conn):
        cur = conn.cursor()
        sql = (
                "CREATE TABLE {0} ("
                " id INT GENERATED ALWAYS AS IDENTITY,"
                " location_id INT NOT NULL,"
                " feed_id INT NOT NULL,"
                " PRIMARY KEY(id),"
                " CONSTRAINT fk_location"
                " FOREIGN KEY(location_id)"
                " REFERENCES {1}(location_id)"
                ");"
        ).format(self.AWBA_FEEDS, self.AWBA_LOCATIONS)

        try:
            cur.execute(sql)
            conn.commit()
            print("Table [{0}]: created".format(self.AWBA_FEEDS))
            return True
        except Exception as e:
            conn.rollback()
            print("Table [{0}]: not created. Reason: {1}".format(self.AWBA_FEEDS, e))
            return False
            
    # Creates the location table if it doesn't already exist
    def Create_Locations_Table(self, conn):
        cur = conn.cursor()
        sql = (
                "CREATE TABLE {0} ("
                " location_id INT GENERATED ALWAYS AS IDENTITY,"
                " location_name VARCHAR(80),"
                " PRIMARY KEY(location_id)"
                ");"
        ).format(self.AWBA_LOCATIONS)

        try:
            cur.execute(sql)
            conn.commit()
            print("Table [{0}]: created".format(self.AWBA_LOCATIONS))
            return True
        except Exception as e:
            conn.rollback()
            print("Table [{0}]: not created.  Reason: {1}".format(self.AWBA_LOCATIONS, e))
            return False
            
    # Creates the regions table if it doesn't already exist
    def Create_Regions_Table(self, conn):
        cur = conn.cursor()
        sql = (
                "CREATE TABLE {0} ("
                " region_id INT GENERATED ALWAYS AS IDENTITY,"
                " region_name VARCHAR(80),"
                " PRIMARY KEY(region_id)"
                ");"
        ).format(self.AWBA_REGIONS)

        try:
            cur.execute(sql)
            conn.commit()
            print("Table [{0}]: created".format(self.AWBA_REGIONS))
            return True
        except Exception as e:
            conn.rollback()
            print("Table [{0}]: not created.  Reason: {1}".format(self.AWBA_REGIONS, e))
            return False
            
    # Deletes a location with feed ids within the database
    def Delete_Location(self, location_id):
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {}

        try:
            # Delete from the Feeds table
            sql = (
                    "DELETE FROM {0}"
                    " WHERE location_id = %s;"
            ).format(self.AWBA_FEEDS)

            cur.execute(sql, (location_id,))
            result["feed_rows"] = cur.rowcount

            # Delete from the Locations table
            sql = (
                    "DELETE FROM {0}"
                    " WHERE location_id = %s;"
            ).format(self.AWBA_LOCATIONS)

            cur.execute(sql, (location_id,))
            result["location_rows"] = cur.rowcount

            # Finally, commit the transaction
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    # Deletes a region with location ids within the database
    def Delete_Region(self, region_id):
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {}

        try:
            # Update Location table
            sql = (
                "UPDATE {0}"
                " SET region_id = NULL"
                " WHERE region_id = %s;"
            ).format(self.AWBA_LOCATIONS)

            cur.execute(sql, (region_id,))
            result["location_rows"] = cur.rowcount

            # Delete the Region table
            sql = (
                    "DELETE FROM {0}"
                    " WHERE region_id = %s;"
            ).format(self.AWBA_REGIONS)

            cur.execute(sql, (region_id,))
            result["region_rows"] = cur.rowcount

            # Finally, commit the transaction
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    def Get_Location(self, location_id):
        # filtered_list = [item for item in ESDR_FEEDS if item["id"] == location_id]

        # if len(filtered_list) > 0:
        #     return filtered_list[0]
        # else:
        #     return None
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {}
        sql = (
                "SELECT l.location_id, l.location_name, l.region_id, r.region_name, f.feed_id "
                "FROM {0} as l "
                "JOIN {1} as f on (l.location_id = f.location_id) "
                "LEFT OUTER JOIN {2} as r on (l.region_id = r.region_id) "
                "WHERE l.location_id = {3} "
                "ORDER BY l.location_id, f.feed_id;"
        ).format(self.AWBA_LOCATIONS, self.AWBA_FEEDS, self.AWBA_REGIONS, location_id)

        try:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                result["id"] = row[0]
                result["name"] = row[1]
                result["regionId"] = row[2]
                result["regionName"] = row[3]
                result.setdefault("feedIds", []).append(row[4])
        finally:
            cur.close()
            conn.close()
            if result != {}:
                return result
            else:
                return None

    def Get_Locations(self, name, feedIds):
        # return ESDR_FEEDS
        conn = self.New_Connection()
        cur = conn.cursor()
        result = []
        sql = (
                "SELECT l.location_id, l.location_name, l.region_id, r.region_name, f.feed_id "
                "FROM {0} as l "
                "JOIN {1} as f on (l.location_id = f.location_id) "
                "LEFT OUTER JOIN {2} as r on (l.region_id = r.region_Id) "
        ).format(self.AWBA_LOCATIONS, self.AWBA_FEEDS, self.AWBA_REGIONS)

        # build where clause based on optional search parameters
        search_cond = ""

        if not(name is None):
            search_cond = "(l.location_name ilike '{0}')".format(name)

        if not(feedIds is None):
            # Convert the list to a comma-delimited list
            ids = [str(item) for item in feedIds]
            id_list = ",".join(ids)

            # Add to search condition
            if search_cond != "":
                search_cond = search_cond + " or "

            search_cond = search_cond + (
                "(l.location_id in ("
                "  SELECT f2.location_id "
                "  FROM {0} as f2 "
                "  WHERE f2.feed_id in ({1})"
                "))"
            ).format(self.AWBA_FEEDS, id_list)

        # Finish sql statement
        if (search_cond != ""):
            sql = sql + "WHERE " + search_cond

        sql = sql + " ORDER BY l.location_id, f.feed_id;"

        try:
            cur.execute(sql)
            rows = cur.fetchall()
            curId = -1
            item = {}

            for row in rows:
                # If this is a new LocationId, create a new record
                if (row[0] != curId):
                    # Set new curId
                    curId = row[0]

                    # Add current item if it's a Location
                    if (item != {}):
                        result.append(item)
                        item = {}
                    
                    # Assign basic values
                    item["id"] = row[0]
                    item["name"] = row[1]
                    item["regionId"] = row[2]
                    item["regionName"] = row[3]

                # Add the field ID
                item.setdefault("feedIds", []).append(row[4])

            # Add the last item
            if (item != {}):
                result.append(item)
        finally:
            cur.close()
            conn.close()
            return result

    def Get_Region(self, region_id):
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {}
        sql = (
                "SELECT r.region_id, r.region_name, l.location_id "
                "FROM {0} as r "
                "LEFT OUTER JOIN {1} as l on (r.region_id = l.region_id) "
                "WHERE r.region_id = {2} "
                "ORDER BY r.region_id, l.location_id;"
        ).format(self.AWBA_REGIONS, self.AWBA_LOCATIONS, region_id)

        try:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                result["id"] = row[0]
                result["name"] = row[1]
                result.setdefault("locationIds", []).append(row[2])
        finally:
            cur.close()
            conn.close()
            if result != {}:
                return result
            else:
                return None

    def Get_Regions(self, name):
        # return ESDR_FEEDS
        conn = self.New_Connection()
        cur = conn.cursor()
        result = []
        sql = (
                "SELECT r.region_id, r.region_name, l.location_id "
                "FROM {0} as r "
                "LEFT OUTER JOIN {1} as l on (r.region_id = l.region_id) "
        ).format(self.AWBA_REGIONS, self.AWBA_LOCATIONS)

        # build where clause based on optional search parameters
        search_cond = ""

        if not(name is None):
            search_cond = "(r.region_name ilike '{0}')".format(name)

        # Finish sql statement
        if (search_cond != ""):
            sql = sql + "WHERE " + search_cond

        sql = sql + " ORDER BY r.region_id, l.location_id;"

        try:
            cur.execute(sql)
            rows = cur.fetchall()
            curId = -1
            item = {}

            for row in rows:
                # If this is a new LocationId, create a new record
                if (row[0] != curId):
                    # Set new curId
                    curId = row[0]

                    # Add current item if it's a Location
                    if (item != {}):
                        result.append(item)
                        item = {}
                    
                    # Assign basic values
                    item["id"] = row[0]
                    item["name"] = row[1]

                # Add the location ID
                item.setdefault("locationIds", []).append(row[2])

            # Add the last item
            if (item != {}):
                result.append(item)
        finally:
            cur.close()
            conn.close()
            return result

    def Get_Wind_Feeds(self):
        return WIND_FEEDS

    # Updates a location within the database
    def Update_Location(self, location_id: int, location: Location):
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {"location_rows": 0, "feed_rows": 0}

        try:
            # Update the Locations table
            sql = (
                    "UPDATE {0}"
                    " SET location_name = %s"
                    " WHERE (location_id = %s);"
            ).format(self.AWBA_LOCATIONS)

            cur.execute(sql, (location.name, location_id))
            result["location_rows"] = cur.rowcount

            if (location.regionId is None):
                # Update the Region in the Location table
                sql = (
                        "UPDATE {0}"
                        " SET region_id = %s"
                        " WHERE (location_id = %s);"
                ).format(self.AWBA_LOCATIONS)

                cur.execute(sql, (location.regionId, location_id))
                result["location_rows"] = cur.rowcount

            if result["location_rows"] > 0:
                # Delete the feeds for this location
                sql = (
                        "DELETE FROM {0}"
                        " WHERE location_id = %s;"
                ).format(self.AWBA_FEEDS)

                cur.execute(sql, (location_id,))

                # Add new feedIds to the Feeds table
                for feedId in location.feedIds:
                    sql = (
                            "INSERT INTO {0}"
                            " (id, location_id, feed_id) "
                            "VALUES"
                            " (DEFAULT, %s, %s)"
                    ).format(self.AWBA_FEEDS)

                    cur.execute(sql, (location_id, feedId))

                result["feed_rows"] = location.feedIds.count

            # Finally, commit the transaction
            if (result["location_rows"] > 0) or (result["feed_rows"] > 0):
                conn.commit()
            else:
                raise ProgrammingError("No locations updated")
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    # Updates a region within the database
    def Update_Region(self, region_id: int, region: Region):
        conn = self.New_Connection()
        cur = conn.cursor()
        result = {"region_rows": 0}

        try:
            # Update the Regions table
            sql = (
                    "UPDATE {0}"
                    " SET region_name = %s"
                    " WHERE (region_id = %s);"
            ).format(self.AWBA_REGIONS)

            cur.execute(sql, (region.name, region_id))
            result["region_rows"] = cur.rowcount

            # Finally, commit the transaction
            if (result["region_rows"] > 0):
                conn.commit()
            else:
                raise ProgrammingError("No regions updated")
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
            return result
        
    # Make sure the database tables exist
    # If they don't, create them so they're available
    def Verify_Tables(self):
        # Create a connection to the database
        conn = self.New_Connection()

        try:
            if not(self.Check_Table(conn, self.AWBA_REGIONS)):
                self.Create_Regions_Table(conn)
            if not(self.Check_Table(conn, self.AWBA_LOCATIONS)):
                self.Create_Locations_Table(conn)
            if not(self.Check_Table(conn, self.AWBA_FEEDS)):
                self.Create_Feeds_Table(conn)

            # Add region column to awba_locations
            if not(self.Check_Column(conn, self.AWBA_LOCATIONS, 'region_id')):
                self.Add_Table_Column(conn, self.AWBA_LOCATIONS, 'region_id', 'integer')
                self.Add_Column_Constraint(conn, self.AWBA_LOCATIONS, 'fk_region', 'FOREIGN KEY (region_id) REFERENCES {0}'.format(self.AWBA_REGIONS))
        finally:
            conn.close()
