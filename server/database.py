from flask import g
import sqlite3
from sqlite3 import Error
from datetime import datetime
import os

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("database.db")
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# # # INSERT METHODS # # #

# Inserts one item into the Fields table.
def insert_into_fields_table(table_name, item_id, field_id, last_updated, jira_name, jama_name, db_file):
    insert_into_db(table_name, item_id, field_id, last_updated, jira_name, jama_name, db_file)

# Inserts one item into the Items table.
def insert_into_items_table(table_name, id, title, type, service, linked_id, db_file):
    insert_into_db(table_name, id, title, type, service, linked_id, db_file)

# Inserts one item into a given table and verifies that values added to table match expected.
def insert_into_db(table_name, primary_key, c2, c3, c4, c5, db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

# # # UPDATE METHODS # # #

# Updates an existing entry. Column to search should probably be some unique identifier.
def update_existing_entry(table_name, column_to_search, column_to_update, value_to_search, value_to_update, db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("UPDATE "+table_name+" SET "+column_to_update+" = ? WHERE "+column_to_search+" = ?", (value_to_update, value_to_search))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

# Updates item title based on unique integer id.
def update_item_title(unique_id, new_title, db_file):
    update_existing_entry("Items", "ID", "Title", unique_id, new_title, db_file)

# Takes unique integer ID and updates corresponding entry's linked id value.
def update_linked_id(unique_id, new_linked_id, db_file):
    update_existing_entry("Items", "ID", "LinkedID", unique_id, new_linked_id, db_file)

# # # RETRIEVE METHODS # # #

# Retrieves all items that match the value in the specified column.
def retrieve_by_column_value(table_name, column_to_search, value, db_file):
    conn = None
    row = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
       # c.execute("SELECT * FROM "+table_name+" WHERE "+column_to_search+" == '"+id+"'")
        c.execute("SELECT * FROM "+table_name+" WHERE "+column_to_search+" = ?", (value,))
        row = c.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return row

'''def retrieve_by_unique_id():

def retrieve_by_name():

def retrieve_by_linked_id():

def retrieve_by_item_id()

def retrieve_by_service()

def retrieve_by_type()'''

def create_table(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("CREATE TABLE Fields(ITEM ID INT PRIMARY KEY, FieldID INT NOT NULL, LastUpdated DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), JiraName TEXT, JamaName TEXT);")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    fields_table = "Fields"
    items_table = "Items"
    fields_column = "FieldID"
    items_column = "ID"
    item_id = 32
    field_id = 26
    # Gets absolute path to root folder and appends database file. Should work on any machine.
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")
    #create_table(db_path)

    # Demo INSERT query
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')
    insert_into_fields_table(fields_table, field_id, '6', time, 'Issue', 'Ticket', db_path)
    insert_into_items_table(items_table, item_id, 'ticketx', 'ticket', 'Jama', 'NULL', db_path)

    # Demo SELECT query
    item_row = retrieve_by_column_value(items_table, items_column, item_id, db_path)
    print("Retrieved from table: ", item_row)
    field_row = retrieve_by_column_value(fields_table, fields_column, field_id, db_path)
    print("Retrieved from table: ", field_row)

    # Demo UPDATE query
    #update_existing_entry(items_table, 'ID', 'Title', item_id, 'Updated Ticket', db_path)
    update_linked_id(item_id, "1002", db_path)
    item_row = retrieve_by_column_value(items_table, items_column, item_id, db_path)
    print("Updated row: ", item_row)