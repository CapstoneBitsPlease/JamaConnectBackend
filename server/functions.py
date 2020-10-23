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
    # get start and times, convert to seconds
    start_time_object = datetime.strptime(last_sync_data[0][1], '%Y-%m-%d %H:%M:%f')
    start_time = start_time_object.timestamp()
    end_time_object = datetime.strptime(last_sync_data[0][2], '%Y-%m-%d %H:%M:%f')
    end_time = end_time_object.timestamp()
    # format difference and add units
    last_sync_time = format(end_time - start_time, '.2f')
    units = "seconds"
    response = [last_sync_time, units]
    return response

# Retrieves number of fields ready to be synced
def get_fields_ready_to_sync():
    items_table = database.ItemsTableOps(db_path)
    fields_table = database.FieldsTableOps(db_path)
    fields_to_sync = 0

    # for testing
    #fields_table.delete_field(13)
    #fields_table.delete_field(14)
    #items_table.delete_item(45)
    #items_table.insert_into_items_table(45, "test", "Story", "Jira", 2)
    #fields_table.insert_into_fields_table(14, 45, datetime.now().strftime('%Y-%m-%d %H:%M:%f'), "assigned", "assignee")
    #fields_table.insert_into_fields_table(13, 45, datetime.now().strftime('%Y-%m-%d %H:%M:%f'), "description", "description")

    # get all linked items and their fields
    response = items_table.get_linked_items()
    for item in response:
        print()
        print("Item: ", item)
        item_id = item[0]
        fields = fields_table.retrieve_by_item_id(item_id)
        for field in fields:
            print("Field: ", field)
            # if field's last_updated datetime is less than the current datetime, it needs to be synced
            if(field[2] < datetime.now().strftime('%Y-%m-%d %H:%M:%f')):
                fields_to_sync += 1

    return fields_to_sync