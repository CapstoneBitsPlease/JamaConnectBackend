from flask import g
import sqlite3
from sqlite3 import Error
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
    def insert_into_db(self, table_name, primary_key, c2, c3, c4, c5=None):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            if c5 == None:
                c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?)", (primary_key, c2, c3, c4))
            else:
                c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")

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
    def retrieve_by_column_value(self, table_name, column_to_search, value):
        row = None
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("SELECT * FROM "+table_name+" WHERE "+column_to_search+" = ?", (value,))
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


# Operations for the Items table. When columns are added or updated, make sure to update them in
# the __init__ method.
class ItemsTableOps:

    def __init__(self, path):
        self.item_id_col = "ID" # TYPE: PRIMARY KEY INT
        self.title_col = "Title" # TYPE: STRING
        self.linked_id_col = "LinkedID" # TYPE: INT
        self.service_col = "Service" # TYPE: STRING
        self.type_col = "Type" # TYPE: STRING
        self.table_name = "Items"
        self.db_ops = DatabaseOperations(path)
    
    # # # RETRIEVE METHODS FOR ITEMS TABLE # # #

    def retrieve_by_item_id(self, item_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, item_id)

    def retrieve_by_title(self, name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.title_col, name)

    def retrieve_by_linked_id(self, linked_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.linked_id_col, linked_id)

    def retrieve_by_service(self, service):
        return self.db_ops.retrieve_by_service(self.table_name, self.service_col, service)
    
    def retrieve_by_type(self, type_):
        return self.db_ops.retrieve_by_service(self.table_name, self.type_col, type_)


     # # # UPDATE METHODS FOR ITEMS TABLE # # #

     # Updates item title based on unique integer id.
    def update_item_title(self, unique_id, new_title):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.title_col, unique_id, new_title)

    # Takes unique integer ID and updates corresponding entry's linked id value.
    def update_linked_id(self, unique_id, new_linked_id):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.linked_id_col, unique_id, new_linked_id)

    def update_type(self, unique_id, new_type):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.type_col, unique_id, new_type)

    def update_service(self, unique_id, new_service):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.service_col, unique_id, new_service)

    def update_item_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.item_id_col, self.item_id_col, unique_id, new_unique_id)

    # # # INSERT METHODS FOR ITEMS TABLE # # #
    
    # Inserts one item into the Items table.
    def insert_into_items_table(self, id, title, type, service, linked_id):
        self.db_ops.insert_into_db(self.table_name, id, title, type, service, linked_id)

    # # # DELETE METHODS FOR ITEMS TABLE # # #
    def delete_item(self, item_id):
        self.db_ops.delete_entry(self.table_name, self.item_id_col, item_id)

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

    # Retrieves service of a given item. Queries the items table and returns the service as a string
    def get_service_of_item_id(self, item_id):
        id, title, linked_id, service, type = self.retrieve_by_item_id(item_id)[0]
        return service

    # Retrieves linked ID of a given item. Queries the items table and returns the linked_id as an integer
    def get_linked_id_of_item_id(self, item_id):
        id, title, linked_id, service, type = self.retrieve_by_item_id(item_id)[0]
        return linked_id


# Operations for the fields table. When columns are added or updated, make sure to update them in
# the __init__ method.
class FieldsTableOps:
    # field_id is primary key (unique identifier in table.)
    def __init__(self, path):
        self.field_id_col = "FieldID" # TYPE: PRIMARY KEY INT
        self.item_id_col = "ItemID" # TYPE: INT
        self.last_updated_col = "LastUpdated" # TYPE: DATETIME, ms precision.
        self.jama_name_col = "JamaName" # TYPE: STRING
        self.jira_name_col = "JiraName" # TYPE: STRING
        self.table_name = "Fields"
        self.db_ops = DatabaseOperations(path)

    # # # RETRIEVE METHODS FOR FIELDS TABLE # # #

    def retrieve_by_field_id(self, field_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.field_id_col, field_id)

    def retrieve_by_item_id(self, item_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, item_id)

    def retrieve_by_last_updated(self, last_updated):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.last_updated_col, last_updated)

    def retrieve_by_jama_name(self, jama_name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.jama_name_col, jama_name)

    def retrieve_by_jira_name(self, jira_name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.jira_name_col, jira_name)


    # # # UPDATE METHODS FOR FIELDS TABLE # # #

    def update_field_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.field_id_col, unique_id, new_unique_id)

    def update_item_id(self, unique_id, new_item_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.item_id_col, unique_id, new_item_id)

    def update_last_updated_time(self, unique_id, new_time_updated):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.last_updated_col, unique_id, new_time_updated)
    
    def update_jama_name(self, unique_id, new_jama_name):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.jama_name_col, unique_id, new_jama_name)
            
    def update_jira_name(self, unique_id, new_jira_name):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.jira_name_col, unique_id, new_jira_name)

    # # # INSERT METHODS FOR FIELDS TABLE # # #

    # Inserts one item into the Fields table.
    def insert_into_fields_table(self, field_id, item_id, last_updated, jama_name, jira_name):
        self.db_ops.insert_into_db(self.table_name, field_id, item_id, last_updated, jama_name, jira_name)

    # # # DELETE METHODS FOR FIELDS TABLE # # #
    def delete_fields_in_item(self, item_id):
        self.db_ops.delete_entry(self.table_name, self.item_id_col, item_id)

    def delete_field(self, field_id):
        self.db_ops.delete_entry(self.table_name, self.field_id_col, field_id)

    # OTHER SPROCS #

    # Retrieves time of last update of a given field. Queries the fields table and returns the date as a datetime object
    def get_last_update_of_field(self, field_id):
        id, item_id, last_update, jama_name, jira_name = self.retrieve_by_field_id(field_id)[0]
        date_obj = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%f')
        last_update = date_obj
        return last_update

    # Retrieves fields ready to be synced. Queries the items and fields tables and returns an array containing the number of fields and their content.
    def get_fields_to_sync(self, items_table):
        num_fields_to_sync = 0
        fields_to_sync = []
        # get all linked items and their fields
        response = items_table.get_linked_items()
        for item in response:
            item_id = item[0]
            fields = self.retrieve_by_item_id(item_id)
            for field in fields:
                fields_to_sync.append(field)
                # if field's last_updated datetime is less than the current datetime, it needs to be synced
                if (field[2] < datetime.now().strftime('%Y-%m-%d %H:%M:%f')):
                    num_fields_to_sync += 1

        return [num_fields_to_sync, fields_to_sync]


# Operations for the SyncInformation table. When columns are added or updated, make sure to update them in
# the __init__ method.
class SyncInformationTableOps:

    def __init__(self, path):
        self.sync_id_col = "SyncID" # TYPE: PRIMARY KEY INT
        self.start_time_col = "StartTime" # TYPE: DATETIME, ms precision.
        self.end_time_col = "EndTime" # TYPE: DATETIME, ms precision.
        self.completion_status_col = "CompletedSuccessfully" # TYPE: INT, 0 or 1. (functionally a boolean)
        self.table_name = "SyncInformation"
        self.db_ops = DatabaseOperations(path)

    # # # RETRIEVE METHODS # # #

    def retrieve_by_sync_id(self, sync_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.sync_id_col, sync_id)
    
    def retrieve_by_start_time(self, start_time):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.start_time_col, start_time)

    def retrieve_by_end_time(self, end_time):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.end_time_col, end_time)

    def retrieve_by_completion_status(self, completed_successfully):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.completion_status_col, completed_successfully)

    # # # UPDATE METHODS # # #
    
    def update_sync_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.sync_id_col, unique_id, new_unique_id)
    
    def update_start_time(self, unique_id, new_start_time):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.start_time_col, unique_id, new_start_time)
    
    def update_end_time(self, unique_id, new_end_time):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.end_time_col, unique_id, new_end_time)

    def update_completion_status(self, unique_id, new_completion_status):
        self.db_ops.update_existing_entry(self.table_name, self.sync_id_col, self.completion_status_col, unique_id, new_completion_status)


    # # # INSERT METHODS # # #

    def insert_into_sync_table(self, sync_id, start_time, end_time, completed_successfully):
        self.db_ops.insert_into_db(self.table_name, sync_id, start_time, end_time, completed_successfully)

    # # # DELETE METHODS # # #

    # Deletes a record of sync. Not advised but possibly necessary.
    def delete_sync_record(self, sync_id):
        self.db_ops.delete_entry(self.table_name, self.sync_id_col, sync_id)

    # # # OTHER SPROCS # # #

    def get_recent_sync_failures(self, recent_date):
        failed_syncs = self.retrieve_by_completion_status(0)
        length = len(failed_syncs)
        for i in range(0, length):
            sync_id, start_time, end_time, completion_status, description = failed_syncs[i]
            end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%f')
            date = datetime.strptime(recent_date, '%Y-%m-%d %H:%M:%f')
            print("#########################")
            print("CURRENT DATE", date)
            print("#########################")
            if date <= end:
                failed_syncs.append((sync_id, start_time, end_time, completion_status, description))
        return failed_syncs

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

    # Retrieves length of time of last sync. Queries the SyncInformation table and returns an array containing the last sync time and the time units (currently in seconds)
    def get_last_sync_time(self):
        # get most recent sync entry
        id, start_time, end_time, completed = self.get_most_recent_sync()[0]
        start_time = functions.convert_to_seconds(start_time)
        end_time = functions.convert_to_seconds(end_time)
        # format difference and add units
        last_sync_time = format(end_time - start_time, '.2f')
        units = "seconds"

        return [last_sync_time, units]

    # Main method to demo functionality. Uncomment blocks to observe how they function.
if __name__ == '__main__':
    fields_table = "Fields"
    items_table = "Items"
    fields_column = "FieldID"
    items_column = "ID"
    item_id = 100000
    field_id = 20023
    sync_id = 2
    # Gets absolute path to root folder and appends database file. Should work on any machine.
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")
    db_ops = DatabaseOperations(db_path)
    items_table_ops = ItemsTableOps(db_path)
    fields_table_ops = FieldsTableOps(db_path)
    sync_table_ops = SyncInformationTableOps(db_path)

    # Demo create table. Define list of types and columns to pass in to method.
    '''columns = ["SyncID", "StartTime", "EndTime", "CompletedSuccessfully"]
    types = ["INT PRIMARY KEY NOT NULL", "DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))", "DATETIME DEFAULT(NULL)", "INT"]
    db_ops.create_table("SyncInformation", columns, types)'''

    # Demo rename column. Takes the table name, current column name and updated column name as args.
    '''db_ops.rename_column(fields_table, "Item", "ItemID")'''

    # Demo INSERT query. NOTE: field id and item id must be unique in order to be added.
    #time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')
    #items_table_ops.insert_into_items_table(item_id, 'ticketx', 'ticket', 'Jama', 'NULL')
    #fields_table_ops.insert_into_fields_table(field_id, "1", time, 'Issue', 'Ticket')

    # Demo SELECT query.
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Retrieved from items table: ", item_row)
    field_row = fields_table_ops.retrieve_by_item_id(field_id)
    print("Retrieved from fields table: ", field_row)

    # Demo UPDATE query.
    items_table_ops.update_linked_id(item_id, "1002")
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Updated items row: ", item_row)

    fields_table_ops.update_jama_name(field_id, "FancyIssue")
    field_row = fields_table_ops.retrieve_by_field_id(field_id)
    print("Updated fields row: ", field_row)

    # Demo DELETE query.
    fields_table_ops.delete_fields_in_item(item_id)
    fields_table_ops.delete_field(field_id)
    print("Deleted field id (expect none or empty): ", fields_table_ops.retrieve_by_item_id(item_id))
    print("Deleted fields that match item id (expect none or empty): ", fields_table_ops.retrieve_by_field_id(field_id))

    items_table_ops.delete_item(item_id)
    print("Deleted item (expect none or empty): ", items_table_ops.retrieve_by_item_id(item_id))

    sync_start_time = time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')
    sync_table_ops.insert_into_sync_table(sync_id, sync_start_time, "NULL", "1")

    print("Retrieved sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    sync_table_ops.update_completion_status(sync_id, "0")

    sync_table_ops.delete_sync_record(sync_id)
    print("Retrieved deleted sync entry: ", sync_table_ops.retrieve_by_sync_id(sync_id))

    last_sync_data = sync_table_ops.get_most_recent_sync()
    print("Last sync information added: ", last_sync_data)

    # testing linked_items
    item_id = 53
    items_table_ops.delete_item(item_id)
    items_table_ops.insert_into_items_table(item_id, 'ticketx', 'ticket', 'Jama', 10)
    linked_items = items_table_ops.get_linked_items()
    print("Current linked items: ", linked_items)

    # testing get_last_update_of_field
    field_id = 12
    fields_table_ops.delete_field(field_id)
    fields_table_ops.insert_into_fields_table(field_id, 15, datetime.now().strftime('%Y-%m-%d %H:%M:%f'), 'defect', 'bug')
    last_update = fields_table_ops.get_last_update_of_field(field_id)
    print("Last update of fieldID " + str(field_id) + ": " + str(last_update))