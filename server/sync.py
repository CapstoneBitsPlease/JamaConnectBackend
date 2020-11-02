from server.connections import connection
from server.database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)
from atlassian import Jira
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


#are we making our own item_id for internal tracking? or should we just
#use the jama or jira item id and specify that?
def sync_one_item(item_id, session):

    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    items_table = ItemsTableOps(db_path)
    
    fields_table = FieldsTableOps(db_path)
    sync_item = items_table.retrieve_by_item_id(item_id)

    field_id = sync_item[0][2]
    
    src_field = fields_table.retrieve_by_field_id(str(field_id))
    dst_field = fields_table.retrieve_by_field_id(str(src_field[0][5]))

    src_id = src_field[0][1]
    value = session.jama_connection.get_item(src_id)

    session.jira_connection.update_issue_fields(dst_field[1])

    return True