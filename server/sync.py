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

    #initialize the table interfaces
    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    items_table = ItemsTableOps(db_path)
    fields_table = FieldsTableOps(db_path)

    #look up the item to sync in the item table
    sync_item = items_table.retrieve_by_item_id(item_id)

    #look up the src and destination fields for the synced item
    field_id = sync_item[0][2]
    
    src_field = fields_table.retrieve_by_field_id(str(field_id))
    dst_field = fields_table.retrieve_by_field_id(str(src_field[0][5]))

    # get the data from jama to be handed off to jira
    src_id = src_field[0][1]
    jama_item = session.jama_connection.get_item(src_id)
    
    field_value = jama_item["fields"][src_field[0][3]]
    fields = {"story point estimate":field_value}

    #send the data to jira
    session.jira_connection.update_issue_field("C2TB-41", fields)

    return True