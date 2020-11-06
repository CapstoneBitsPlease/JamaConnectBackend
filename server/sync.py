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

    #look up the items to sync in the item table
    sync_item1 = items_table.retrieve_by_item_id(item_id)[0]
    sync_item2 = items_table.retrieve_by_item_id(sync_item1[2])


    # check to see which item was updated most recently. 
    # and compare that with internal sync log to see if
    # the item has been updated in the time since last sync
    last_sync = max([sync_item1[6],sync_item2[6]])
    pos, src_id, most_recent_change = session.most_recent_update(sync_item1[0], sync_item2[0])
    if(most_recent_change <= last_sync):
        # the last sync time was the same or newer than the last modified time
        return False

    # define src as the item that was most recently updated
    if pos == 0:
        src_item = sync_item1
    else:
        src_item = sync_item2

    #look up the src and destination fields for the synced item
    #field_id = src_item[0][2] #(LinkedID)
    src_fields = fields_table.retrieve_by_item_id(str(src_id))
    dst_fields = []
    for src_field in src_fields:
        dst_field = fields_table.retrieve_by_field_id(str(src_field[5]))
        dst_fields.append(dst_field)

    #put the names of the fields into two corresponding lists
    src_field_names = []
    for field in src_field:
        src_field_names.append(field[3])
    
    dst_field_names = []
    for field in dst_fields:
        dst_field_names.append(field[3])
    
    # get the data to be passed to the other service
    if src_item[3] == "jama":
        src_data = session.get_jama_item(src_id, src_field_names)
    else:
        src_data = session.get_jira_item(src_id, src_field_names)

    dst_fields = {} #destination list with source values
    for i in range(len(src_data)):
        dst_fields[dst_field_names[i]]=src_data[i][1]

    #send the data
    if src_item[3] == "jama":
        session.set_jira_item(dst_field[0], dst_fields)
    else:
         session.set_jama_item(dst_field[0], dst_fields)

    #update the last sync time with the current time. 

    return True

#function for getting the list of items to be synced and passing them off to the sync function


if __name__ == '__main__':
    session = connection()
    session.initiate_jama("capstone2020", "sduncan", "Fuck0ffJama")
    session.initiate_jira("capstone2020teamb", "sduncan@pdx.edu", "hgTbykR23f57YxsYYgRY84F3")

    sync_one_item("100", session)


