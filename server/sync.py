from connections import connection
from database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)
import os


def last_sync_period():
    """
    returns the amount of time the last sync took and when it was completed
    """
    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    sync_table = SyncInformationTableOps(db_path)
    sync_info = sync_table.get_last_sync_time()
    sync_time =  {"Completed on": sync_info[2], "Total Sync Time": sync_info[0]}
    return sync_time