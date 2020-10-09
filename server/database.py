from flask import g
import sqlite3
from sqlite3 import Error
from datetime import datetime

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

def insert_into_db(table_name, id, title, type, service, linked_id, db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?)", (id, title, type, service, linked_id))
        conn.commit()
        c.execute("SELECT * FROM "+table_name+" WHERE FieldID == '"+id+"'")
        x = c.fetchall()
        print("Got: ", x)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def retrieve_by_id(table_name, id, db_file):
    conn = None
    row = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM "+table_name+" WHERE ID == '"+id+"'")
        row = c.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return row

def create_connection(db_file):
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
    db_path = "/Users/ktsutter/Capstone/JamaConnectBackend/JamaJiraConnectDataBase.db"
    #create_connection(db_path)
    # Demo SELECT query
    x = retrieve_by_id("Items", '1', db_path)
    print("Retrieved from table: ", x)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')
    insert_into_db("Fields", '3', '3', time, 'Issue', 'Ticket', db_path)