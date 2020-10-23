import json
from py_jama_rest_client.client import JamaClient
import database
import connections
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")

# Retrieves length of time of last sync from sqlite database table SyncInformation
def get_last_sync_time():
    sync_table = database.SyncInformationTableOps(db_path)
    # get most recent sync entry
    last_sync_data = sync_table.get_most_recent_sync()
    # get start time, convert to seconds
    start_time_string = last_sync_data[0][1]
    start_time_object = datetime.strptime(start_time_string, '%Y-%m-%d %H:%M:%f')
    start_time = start_time_object.timestamp()
    # get end time, convert to seconds
    end_time_string = last_sync_data[0][2]
    end_time_object = datetime.strptime(end_time_string, '%Y-%m-%d %H:%M:%f')
    end_time = end_time_object.timestamp()
    # format difference and return
    last_sync_time = format(end_time - start_time, '.2f')
    units = "seconds"
    response = [last_sync_time, units]
    print(response)
    return response

def get_items_ready_to_sync():
    num_items = 0
    items_table = database.ItemsTableOps(db_path)
    # for testing
    items_table.delete_item(45)
    items_table.insert_into_items_table(45, "test", "Story", "Jira", 2)
    print(items_table)
    response = items_table.get_linked_items()
    for item in response:
        print(item)
        num_items += 1

    print(num_items)
    return num_items


get_last_sync_time()
get_items_ready_to_sync()