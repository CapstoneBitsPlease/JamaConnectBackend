from flask import g
import sqlite3
from sqlite3 import Error
from datetime import timezone
from datetime import datetime
import os
import logging
import functions

# Utility class. Contains methods to connect to database, create table, rename column, add entry
# to table, update an existing entry, retrieve an existing entry, and delete an existing entry.
class DatabaseOperations:

    def __init__(self, path):
        self.db_file = path

    # Establishes connection to DB if path is valid. NOTE: connection must be closed by calling method.
    def connect_to_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            return conn

    # Closes an existing connection.
    def close_connection(self, conn):
        if conn:
            conn.close()

    # Inserts one item into a given table and verifies that values added to table match expected.
    def insert_into_db(self, table_name, primary_key, c2, c3, c4, c5, c6 = None, c7 = None):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON;")
            conn.commit()
            if c6 == None:
                c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5))
            elif c7 == None:
                c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5, c6))
            else: 
                c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5, c6, c7))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")
        return 0

    # Updates an existing entry. Column to search should probably be some unique identifier.
    def update_existing_entry(self, table_name, column_to_search, column_to_update, value_to_search, value_to_update):
        conn = self.connect_to_db()
        if conn:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("UPDATE "+table_name+" SET "+column_to_update+" = ? WHERE "+column_to_search+" = ?", (value_to_update, value_to_search))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")

    # Retrieves all items that match the value in the specified column.
    def retrieve_by_column_value(self, table_name, column_to_search, value = None, col2 = None, distinct = False):
        row = None
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            # If value to compare against is None, user wants to get all items in specified column.
            if value == None:
                # If distinct, then only return unique values from that column (no duplicates).
                if distinct != False:
                    c.execute("SELECT DISTINCT " + column_to_search + " FROM " + table_name + "")
                else:
                    c.execute("SELECT " + column_to_search + " FROM " + table_name + "")
            # If there is a value to compare to, either the user wants all items that match that item,
            # OR they want all items from a column that match the value specified for column 2.
            else:
                if distinct != False and col2 != None:
                    c.execute(
                        "SELECT DISTINCT " + column_to_search + " FROM " + table_name + " WHERE " + col2 + " = ?",
                        (value,))
                else:
                    c.execute("SELECT * FROM " + table_name + " WHERE " + column_to_search + " = ?", (value,))
            row = c.fetchall()
            self.close_connection(conn)
        else:
            print("Failed to connect")
        return row

    # Deletes an entry in a given table that matches the ID in the specified column.
    def delete_entry(self, table_name, column, id):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("DELETE FROM "+table_name+" WHERE "+column+" = ?", (id,))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")

    # Renames column.
    def rename_column(self, table_name, current_column_name, new_column_name):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("ALTER TABLE "+table_name+" RENAME COLUMN "+current_column_name+" TO "+new_column_name+"")
            conn.commit()
            self.close_connection(conn)

    # Creates a new table based on parameters.
    def create_table(self, table_name, columns, types):
        conn = self.connect_to_db()
        if conn:
            num_columns = len(columns)
            num_types = len(types)
            if num_columns != num_types:
                print("Mismatching number of columns and types. Please double check your entry and try again.")
            else:
                conn = sqlite3.connect(self.db_file)
                c = conn.cursor()
                sql = "CREATE TABLE "+table_name+"("
                for i in range(0, num_columns):
                    sql += columns[i] + " "
                    sql += types[i]
                    if i + 1 != num_columns:
                        sql += ", "
                sql += ");"
                print(sql)
                c.execute(sql)
                conn.commit()
                self.close_connection(conn)

    # Adds a column to an existing table. Note: cannot have UNIQUE or PRIMARY KEY contraints.
    def add_column(self, table_name, column_name, column_type):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("ALTER TABLE "+table_name+" ADD COLUMN "+column_name+" "+column_type+"")
            conn.commit()
            self.close_connection(conn)

    # Deletes an existing table. ***USE WITH CAUTION
    def delete_table(self, table_name):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("DROP TABLE "+table_name+"")
            conn.commit()
            self.close_connection(conn)


# Operations for the Items table. When columns are added or updated, make sure to update them in
# the __init__ method.
class ItemsTableOps:

    def __init__(self, path):
        self.item_id_col = "ID" # TYPE: PRIMARY KEY INT
        self.title_col = "Title" # TYPE: STRING
        self.linked_id_col = "LinkedID" # TYPE: INT
        self.service_col = "Service" # TYPE: STRING
        self.type_col = "Type" # TYPE: STRING
        self.project_id_col = "ProjectID" # TYPE: UNIQUE INT
        self.last_sync_time_col = "LastSyncTime" # TYPE: DATETIME, ms precision
        self.table_name = "Items"
        self.db_ops = DatabaseOperations(path)
    
    # # # RETRIEVE METHODS FOR ITEMS TABLE # # #

    def retrieve_by_item_id(self, item_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, str(item_id))

    def retrieve_by_title(self, name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.title_col, name)

    def retrieve_by_linked_id(self, linked_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.linked_id_col, str(linked_id))

    def retrieve_by_service(self, service):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.service_col, service)
    
    def retrieve_by_type(self, type_):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.type_col, type_)

    def retrieve_by_project_id(self, project_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.project_id_col, str(project_id))

    def retrieve_by_last_sync_time(self, last_sync_time):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.last_sync_time_col, last_sync_time)

    def get_all_jama_types(self):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.type_col, "Jama", self.service_col, True)

    def get_all_jira_types(self):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.type_col, "Jira", self.service_col, True)

     # # # UPDATE METHODS FOR ITEMS TABLE # # #

     # Updates item title based on unique integer id.
    def update_item_title(self, unique_id, new_title):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.title_col, str(unique_id), new_title)

    # Takes unique integer ID and updates corresponding entry's linked id value.
    def update_linked_id(self, unique_id, new_linked_id):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.linked_id_col, str(unique_id), str(new_linked_id))

    def update_type(self, unique_id, new_type):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.type_col, str(unique_id), new_type)

    def update_service(self, unique_id, new_service):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.service_col, str(unique_id), new_service)

    def update_item_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.item_id_col, str(unique_id), str(new_unique_id))

    def update_project_id(self, unique_id, new_project_id):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.project_id_col, str(unique_id), str(new_project_id))

    def update_last_sync_time(self, unique_id, updated_sync_time):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.last_sync_time_col, str(unique_id), updated_sync_time)

    # # # INSERT METHODS FOR ITEMS TABLE # # #
    
    # Inserts one item into the Items table.
    def insert_into_items_table(self, id_, title, linked_id, service, type_, project_id, last_sync_time):
        self.db_ops.insert_into_db(self.table_name, str(id_), title, str(linked_id), service, type_, str(project_id), last_sync_time)

    # # # DELETE METHODS FOR ITEMS TABLE # # #
    def delete_item(self, item_id):
        self.db_ops.delete_entry(self.table_name, self.item_id_col, str(item_id))

    # # # OTHER SPROCS # # #

    # Retrieve all linked items from the Items table as a list of tuples
    def get_linked_items(self):
        conn = self.db_ops.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Items WHERE LinkedID IS NOT ? AND LinkedID IS NOT ?", ("NULL","None"))
            linked_items = c.fetchall()
            self.db_ops.close_connection(conn)
        return linked_items

    # Retrieves service of a given item
    def get_service_of_item_id(self, item_id):
        _, _, _, service, _, _, _ = self.retrieve_by_item_id(item_id)[0]
        return service

# Operations for the fields table. When columns are added or updated, make sure to update them in
# the __init__ method.
class FieldsTableOps:
    # field_id is primary key (unique identifier in table.)
    def __init__(self, path):
        self.field_id_col = "FieldID" # TYPE: PRIMARY KEY INT
        self.item_id_col = "ItemID" # TYPE: INT, FOREIGN KEY
        self.last_updated_col = "LastUpdated" # TYPE: DATETIME, ms precision.
        self.name_col = "Name" # TYPE: STRING
        self.field_service_id = "FieldServiceID" # TYPE: STRING
        self.linked_id_col = "LinkedID" # TYPE: INT
        self.table_name = "Fields"
        self.db_ops = DatabaseOperations(path)

    # # # RETRIEVE METHODS FOR FIELDS TABLE # # #

    def retrieve_by_field_id(self, field_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.field_id_col, str(field_id))

    def retrieve_by_item_id(self, item_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, str(item_id))

    def retrieve_by_last_updated(self, last_updated):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.last_updated_col, last_updated)

    def retrieve_by_name(self, name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.name_col, name)

    def retrieve_by_field_service_id(self, field_service_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.field_service_id, field_service_id)

    def retrieve_by_linked_id(self, linked_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.linked_id_col, str(linked_id))

    # # # UPDATE METHODS FOR FIELDS TABLE # # #

    def update_field_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.field_id_col, str(unique_id), str(new_unique_id))

    def update_item_id(self, unique_id, new_item_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.item_id_col, str(unique_id), str(new_item_id))

    def update_last_updated_time(self, unique_id, new_time_updated):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.last_updated_col, str(unique_id), new_time_updated)
    
    def update_name(self, unique_id, new_name):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.name_col, str(unique_id), new_name)
            
    def update_field_service_id(self, unique_id, new_field_service_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.field_service_id, str(unique_id), new_field_service_id)
    
    def update_linked_id(self, unique_id, linked_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.linked_id_col, str(unique_id), str(linked_id))

    # # # INSERT METHODS FOR FIELDS TABLE # # #

    # Inserts one item into the Fields table.
    def insert_into_fields_table(self, field_id, item_id, last_updated, name, field_service_id, linked_id):
        self.db_ops.insert_into_db(self.table_name, str(field_id), str(item_id), last_updated, name, field_service_id, str(linked_id))

    # # # DELETE METHODS FOR FIELDS TABLE # # #
    def delete_fields_in_item(self, item_id):
        self.db_ops.delete_entry(self.table_name, self.item_id_col, str(item_id))

    def delete_field(self, field_id):
        self.db_ops.delete_entry(self.table_name, self.field_id_col, str(field_id))

    # OTHER SPROCS #

    # Retrieves all linked fields ready to be synced. Returns an array containing the number of fields and their content.
    def get_fields_to_sync(self, items_table, sync_table):
        num_fields_to_sync = 0
        fields_to_sync = []
        # get all linked items and their fields
        linked_items = items_table.get_linked_items()
        for item in linked_items:
            item_id = item[0]
            fields = self.retrieve_by_item_id(item_id)
            for field in fields:
                if(field):
                    _, item_id, last_updated, _, _, _ = field
                    last_updated = functions.convert_to_seconds(last_updated)
                    # get last sync from syncinfo table
                    last_sync = sync_table.get_most_recent_sync()
                    _, _, end_time, _, _ = last_sync[0]
                    if(end_time):
                        last_sync_end_time = functions.convert_to_seconds(end_time)
                        # check if field needs to be synced, increment and append if so
                        if last_updated > last_sync_end_time:
                            num_fields_to_sync += 1
                            fields_to_sync.append(field)
        return [num_fields_to_sync, fields_to_sync]

    # Get the most recent field ID (ie: largest ID number) from the database.
    def get_next_field_id(self):
        conn = self.db_ops.connect_to_db()
        most_recent_field_id = ""
        if conn:
            c = conn.cursor()
            c.execute("SELECT MAX(FieldID) FROM Fields")
            most_recent_field = c.fetchall()
            most_recent_field_id = most_recent_field[0]
            self.db_ops.close_connection(conn)
        return most_recent_field_id


# Operations for the SyncInformation table. When columns are added or updated, make sure to update them in
# the __init__ method.
class SyncInformationTableOps:

    def __init__(self, path):
        self.sync_id_col = "SyncID" # TYPE: PRIMARY KEY INT
        self.start_time_col = "StartTime" # TYPE: DATETIME, ms precision.
        self.end_time_col = "EndTime" # TYPE: DATETIME, ms precision.
        self.completion_status_col = "CompletedSuccessfully" # TYPE: INT, 0 or 1. (functionally a boolean)
        self.description_col = "Description"  # TYPE: TEXT
        self.table_name = "SyncInformation"
        self.db_ops = DatabaseOperations(path)

    # # # RETRIEVE METHODS # # #

    def retrieve_by_sync_id(self, sync_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.sync_id_col, str(sync_id))
    
    def retrieve_by_start_time(self, start_time):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.start_time_col, start_time)

    def retrieve_by_end_time(self, end_time):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.end_time_col, end_time)

    def retrieve_by_completion_status(self, completed_successfully):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.completion_status_col, str(completed_successfully))

    def retrieve_by_description(self, description):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.description_col, description)

    # # # UPDATE METHODS # # #
    
    def update_sync_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.sync_id_col, str(unique_id), str(new_unique_id))
    
    def update_start_time(self, unique_id, new_start_time):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.start_time_col, str(unique_id), new_start_time)
    
    def update_end_time(self, unique_id, new_end_time):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.end_time_col, str(unique_id), new_end_time)

    def update_completion_status(self, unique_id, new_completion_status):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.completion_status_col, str(unique_id), str(new_completion_status))

    def update_description(self, unique_id, description):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.description_col, str(unique_id), description)

    # # # INSERT METHODS # # #

    def insert_into_sync_table(self, sync_id, start_time, end_time, completed_successfully, description):
        self.db_ops.insert_into_db(self.table_name, str(sync_id), start_time, end_time, str(completed_successfully), description)

    # # # DELETE METHODS # # #

    # Deletes a record of sync. Not advised but possibly necessary.
    def delete_sync_record(self, sync_id):
        self.db_ops.delete_entry(self.table_name, self.sync_id_col, str(sync_id))

    # # # OTHER SPROCS # # #

    def get_recent_sync_failures(self, recent_date):
        failed_syncs = self.retrieve_by_completion_status(0)
        failed_syncs_after_date = []
        length = len(failed_syncs)
        for i in range(0, length):
            sync_id, start_time, end_time, completion_status, description = failed_syncs[i]
            end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
            date = datetime.strptime(recent_date, '%Y-%m-%dT%H:%M:%S.%f%z')

            print("#########################")
            print("CURRENT DATE", date)
            print("#########################")

            if date <= end:
                failed_syncs_after_date.append((sync_id, start_time, end_time, completion_status, description))
        return failed_syncs_after_date

    # Gets the most recent sync time from the database.
    def get_most_recent_sync(self):
        conn = self.db_ops.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("SELECT MAX(EndTime) FROM SyncInformation")
            last_sync_array = c.fetchall()
            last_sync_tuple = last_sync_array[0]
            last_sync_time = ''.join(last_sync_tuple)
            c.execute("SELECT * FROM " + self.table_name + " WHERE " + self.end_time_col + " = ?", (last_sync_time,))
            last_sync = c.fetchall()
            self.db_ops.close_connection(conn)
        return last_sync


    # Retrieves last successful sync
    def get_last_successful_sync(self):
        conn = self.db_ops.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("SELECT MAX(EndTime) FROM SyncInformation WHERE CompletedSuccessfully = 1")
            last_sync_array = c.fetchall()
            last_sync_tuple = last_sync_array[0]
            last_sync_time = ''.join(last_sync_tuple)
            c.execute("SELECT * FROM " + self.table_name + " WHERE " + self.end_time_col + " = ?", (last_sync_time,))
            last_successful_sync = c.fetchall()
            self.db_ops.close_connection(conn)
        return last_successful_sync


    # Retrieves length of time of last successful sync. Returns an array containing the length of time of the last sync,
    # the time units, and the end time
    def get_last_sync_time(self):
        _, start_time, end_time, _, _ = self.get_last_successful_sync()[0]
        start_time = functions.convert_to_seconds(start_time)
        end_time = functions.convert_to_seconds(end_time)
        last_sync_time = end_time - start_time
        if last_sync_time <= 120:
            units = "seconds"
        elif last_sync_time > 120 and last_sync_time < 3600:
            last_sync_time /= 60
            units = "minutes"
        elif last_sync_time >= 3600:
            last_sync_time /= 3600
            units = "hours"
        last_sync_time = format(last_sync_time, '.4f')
        return [last_sync_time, units, end_time]


def demo_sync_methods(db_path):
    sync_id = 107
    sync_table_ops = SyncInformationTableOps(db_path)
    recent_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # Demo create SyncInformation table.
    #db_ops = DatabaseOperations(db_path)
    #columns = ["SyncID", "StartTime", "EndTime", "CompletedSuccessfully", "Description"]
    #types = ["INT PRIMARY KEY NOT NULL", "DATETIME", "DATETIME DEFAULT NULL", "INT", "TEXT"]
    #db_ops.create_table("SyncInformation", columns, types)

    sync_start_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.insert_into_sync_table(sync_id, sync_start_time, "NULL", "0", "Sync in progress")

    print("Retrieved sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    sync_table_ops.update_completion_status(sync_id, "1")
    sync_end_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.update_end_time(sync_id, sync_end_time)
    sync_table_ops.update_description(sync_id, "Sync completed successfully")

    sync_id += 1
    sync_start_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.insert_into_sync_table(sync_id, sync_start_time, "NULL", "0", "Sync in progress")

    print("Retrieved sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    sync_end_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.update_end_time(sync_id, sync_end_time)
    sync_table_ops.update_description(sync_id, "ERROR: sync failed to complete, interrupted by manual override")

    sync_id += 1
    sync_start_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.insert_into_sync_table(sync_id, sync_start_time, "NULL", "0", "Sync in progress")

    print("Retrieved sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    sync_end_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    sync_table_ops.update_end_time(sync_id, sync_end_time)
    sync_table_ops.update_description(sync_id, "ERROR: sync failed to complete, unknown error")

    print("Entries where sync failed: ", sync_table_ops.get_recent_sync_failures(recent_date))

    print("Most recent sync: ", sync_table_ops.get_most_recent_sync())

    sync_table_ops.delete_sync_record(sync_id)
    sync_table_ops.delete_sync_record(sync_id-1)
    sync_table_ops.delete_sync_record(sync_id-2)
    print("Retrieved deleted sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))
    print("Retrieved deleted sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id-1))
    print("Retrieved deleted sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id-2))

def logging_demo():
    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')
    logging.error('error')

# Links two items in the database by 1.) Adding both items to the table, 2.) setting jira_linked_id = jama_id (and vice versa)
# 3.) adding each field to the database, and linking with corresponding field in opposite array (ie: jama_field[0].lin)
def link_items(jira_item, jama_item, jira_fields, jama_fields, num_fields):
    # Variables for readability
    id_ = 0
    title = 1
    type_ = 2
    id_to_link = 0
    project_id = 3
    field_name = 0
    field_service_id = 1

    # Get path. NOTE: due to how the flask server is set up, if you want to run this locally instead, use  os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    items_ops = ItemsTableOps(db_path)
    fields_ops = FieldsTableOps(db_path)
    last_updated = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    # Add Jira item to the database. Jama item's ID is passed to LinkedID column.
    items_ops.insert_into_items_table(jira_item[id_], jira_item[title], jama_item[id_to_link], "Jira", jira_item[type_], jira_item[project_id], last_updated)
    # Add Jama item to the database. Jira item's ID is passed to LinkedID column.
    items_ops.insert_into_items_table(jama_item[id_], jama_item[title], jira_item[id_to_link], "Jama", jama_item[type_], jama_item[project_id], last_updated)
    # Get the current largest ID in the fields table. Use this to generate the next unique ID for the fields table.
    field_id = fields_ops.get_next_field_id()[0]
    # Assume success initially. If something goes wrong during syncing process, set this to 0.
    success = 1
    for i in range(0, num_fields):
        try:
            # Update next field ID and insert current jira field into the table, passing the corresponding jama FieldID to the LinkedID column.
            # The Jama FieldID will be field_id + 1.
            field_id += 1
            last_updated = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            fields_ops.insert_into_fields_table(field_id, jira_item[id_], last_updated, jira_fields[i][field_name], jira_fields[i][field_service_id], field_id + 1)
            # Update next field ID.
            field_id += 1
            # Update next field ID and insert current jama field into the table, passing the corresponding jira FieldID to the LinkedID column.
            # The Jira FieldID will be field_id - 1, since it was calculated above and 1 has been added to it since.
            fields_ops.insert_into_fields_table(field_id, jama_item[id_], last_updated, jama_fields[i][field_name], jama_fields[i][field_service_id], field_id - 1)
        except:
            # If something goes wrong, write to the error log and indicate failure to calling routine by setting success to 0.
            logging.exception(f"Something went wrong when linking {jama_fields[i][0]} with {jira_fields[i][0]}")
            success = 0
    return success


# Main method to demo functionality. Uncomment blocks to observe how they function.
if __name__ == '__main__':
    jira_id = 12349
    jama_id = 12361
    #link_items([jira_id, "title", "issue", 7], [jama_id, "title2", "bug", 6], [[jira_id, "name"], [jira_id, "name2",]], [[jama_id,"name3"], [jama_id, "name4"]], 2)
    
    fields_table = "Fields"
    items_table = "Items"
    fields_column = "FieldID"
    items_column = "ID"
    item_id = 527
    field_id = 59
    # Gets absolute path to root folder and appends database file. Should work on any machine.
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")
    db_ops = DatabaseOperations(db_path)
    items_table_ops = ItemsTableOps(db_path)
    fields_table_ops = FieldsTableOps(db_path)
    sync_table_ops = SyncInformationTableOps(db_path)


    # Demo create Items table. Define list of types and columns to pass in to method.
    #columns = ["ID", "Title", "LinkedID", "Service", "Type", "ProjectID", "LastSyncTime"]
    #types = ["INT PRIMARY KEY NOT NULL", "STRING", "INT", "STRING", "STRING", "INT", "DATETIME"]
    #db_ops.create_table("Items", columns, types)

    # Demo create Fields table WITH FOREIGN KEY enforced.
    #curr_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    #string_to_execute = "CREATE TABLE Fields ( FieldID INTEGER PRIMARY KEY, ItemID INT NOT NULL, LastUpdated DATETIME, Name STRING, FieldServiceID STRING, LinkedID INT, FOREIGN KEY (ItemID) REFERENCES Items (ID));"
    #conn = db_ops.connect_to_db()
    #c = conn.cursor()
    #c.execute("PRAGMA foreign_keys = ON;")
    #c.execute(string_to_execute)
    #conn.commit()
    #db_ops.close_connection(conn)

    # Demo rename column. Takes the table name, current column name and updated column name as args.
    #db_ops.rename_column(items_table, "Project", "LastSyncTime")

    # Demo delete table. ***USE WITH CAUTION***
    # # # # db_ops.delete_table("Fields")
    # # # # db_ops.delete_table("Items")
    # # # db_ops.delete_table("SyncInformation")
    # Demo add column to existing table.
    #db_ops.add_column(items_table, "LastSyncTime", f"DATETIME {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')}")

    # Demo INSERT query. NOTE: field id and item id must be unique in order to be added.
    time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    items_table_ops.insert_into_items_table(item_id, 'bug1', '100', 'Jama', 'bug', "3", time)
    # This one should pass
    fields_table_ops.insert_into_fields_table(field_id, item_id, time, 'Issue', 'Ticket', "None")

    # This one should FAIL
    #fields_table_ops.insert_into_fields_table(field_id+1, -100, time, 'Issue', 'Ticket', "None")
    #field_row1 = fields_table_ops.retrieve_by_field_id(field_id+1)
    #print("IF RETRIEVED FOREIGN KEY NOT WORKING: ", field_row1)

    # Demo SELECT query.
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Retrieved from items table: ", item_row)
    field_row = fields_table_ops.retrieve_by_field_id(field_id)
    print("Retrieved from fields table: ", field_row)

    # Demo UPDATE query.
    items_table_ops.update_linked_id(item_id, "1002")
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Updated items row: ", item_row)

    fields_table_ops.update_name(field_id, "FancyIssue")
    field_row = fields_table_ops.retrieve_by_field_id(field_id)
    print("Updated fields row: ", field_row)

    # # Demo DELETE query.
    # fields_table_ops.delete_fields_in_item(item_id)
    # fields_table_ops.delete_field(field_id)
    # print("Deleted field id (expect none or empty): ", fields_table_ops.retrieve_by_item_id(item_id))
    # print("Deleted fields that match item id (expect none or empty): ", fields_table_ops.retrieve_by_field_id(field_id))

    items_table_ops.delete_item(item_id)
    print("Deleted item (expect none or empty): ", items_table_ops.retrieve_by_item_id(item_id))
    

    #print("Retrieved sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    #sync_table_ops.update_completion_status(sync_id, "0")

    #sync_table_ops.delete_sync_record(sync_id)
    #print("Retrieved deleted sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    #last_sync_data = sync_table_ops.get_most_recent_sync()
    #print("Last sync information added: ", last_sync_data)

    #demo_sync_methods(db_path)

    #print("Length of time of last sync:", sync_table_ops.get_last_sync_time()[0], sync_table_ops.get_last_sync_time()[1])
    print("Number of fields ready to sync:", fields_table_ops.get_fields_to_sync(items_table_ops, sync_table_ops)[0])
    print("Field(s) ready for syncing:", fields_table_ops.get_fields_to_sync(items_table_ops, sync_table_ops)[1])

    #demo_sync_methods(db_path)
    #logging_demo()
    