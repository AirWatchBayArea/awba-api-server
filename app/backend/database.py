from ..feeds import ESDR_FEEDS, WIND_FEEDS
from ..models.esdr import Location
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
    DATABASE_URL = os.environ['DATABASE_URL']

    # def __init__(self):
        # Create a connection to the database
        # self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

    def New_Connection(self):
        return psycopg2.connect(self.DATABASE_URL, sslmode='require')

    # Adds a new location with feed ids to the database
    def Add_Location(self, location: Location):
        result = {"new_id": -1}
        conn = self.New_Connection()
        cur = conn.cursor()

        try:
            # Insert into Locations table
            sql = (
                    "INSERT INTO {0}"
                    " (location_id, location_name) "
                    "VALUES"
                    " (DEFAULT, %s) "
                    "RETURNING location_id;"
            ).format(self.AWBA_LOCATIONS)

            cur.execute(sql, (location.name,))
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
        
    # Simple check to make sure a table exists
    def Check_Table(self, conn, table_name):
        cur = conn.cursor()
        sql = "SELECT * FROM {0} WHERE 0=1;".format(table_name)

        try:
            cur.execute(sql)
            print("Table [{0}]: exists".format(table_name))
            return True
        except:
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
            print("Table [{0}]: created".format(self.AWBA_FEEDS))
            return True
        except Exception as e:
            print("Table [{0}]: not created. Reason: {1}".format(self.AWBA_FEEDS, e))
            raise e
            
    # Creates the location table if it doesn't already exist
    def Create_Location_Table(self, conn):
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
            print("Table [{0}]: created".format(self.AWBA_LOCATIONS))
            return True
        except Exception as e:
            print("Table [{0}]: not created.  Reason: {1}".format(self.AWBA_LOCATIONS, e))
            raise e
            
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
                "SELECT l.location_id, l.location_name, f.feed_id "
                "FROM {0} as l "
                "JOIN {1} as f on (l.location_id = f.location_id) "
                "WHERE l.location_id = {2} "
                "ORDER BY l.location_id, f.feed_id;"
        ).format(self.AWBA_LOCATIONS, self.AWBA_FEEDS, location_id)

        try:
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                result["id"] = row[0]
                result["name"] = row[1]
                result.setdefault("feedIds", []).append(row[2])
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
                "SELECT l.location_id, l.location_name, f.feed_id "
                "FROM {0} as l "
                "JOIN {1} as f on (l.location_id = f.location_id) "
        ).format(self.AWBA_LOCATIONS, self.AWBA_FEEDS)

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
        print(sql)

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

                # Add the field ID
                item.setdefault("feedIds", []).append(row[2])

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
        
    # Make sure the database tables exist
    # If they don't, create them so they're available
    def Verify_Tables(self):
        # Create a connection to the database
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

        try:
            if not(self.Check_Table(conn, self.AWBA_LOCATIONS)):
                self.Create_Location_Table(conn)
            if not(self.Check_Table(conn, self.AWBA_FEEDS)):
                self.Create_Feeds_Table(conn)

            conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()

