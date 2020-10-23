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
    # retrieve most recent sync entry
    last_sync_data = sync_table.get_most_recent_sync()
    # get start time, convert to seconds
    start_time_string = last_sync_data[0][1]
    start_time_object = datetime.strptime(start_time_string, '%Y-%m-%d %H:%M:%f')
    start_time = start_time_object.timestamp()
    # get end time, convert to seconds
    end_time_string = last_sync_data[0][2]
    end_time_object = datetime.strptime(end_time_string, '%Y-%m-%d %H:%M:%f')
    end_time = end_time_object.timestamp()

    last_sync_time = format(end_time - start_time, '.3f')
    return last_sync_time



