from connections import connection
from database import (SyncInformationTableOps, ItemsTableOps, FieldsTableOps)
from atlassian import Jira
import os
from datetime import datetime, timezone
import logging


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

    #session = connection()
    #session.initiate_jama(os.environ["JAMA_SYNC_ORG"], os.environ["JAMA_SYNC_USERNAME"], os.environ["JAMA_SYNC_PASSWORD"])
    #session.initiate_jira(os.environ["JIRA_SYNC_ORG"], os.environ["JIRA_SYNC_USERNAME"], os.environ["JIRA_SYNC_PASSWORD"])

    #initialize the table interfaces
    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    items_table = ItemsTableOps(db_path)
    fields_table = FieldsTableOps(db_path)

    #look up the items to sync in the item table
    sync_item1 = items_table.retrieve_by_item_id(item_id)[0]
    sync_item2 = items_table.retrieve_by_item_id(sync_item1[2])[0]

    # check to see which item was updated most recently. 
    # and compare that with internal sync log to see if
    # the item has been updated in the time since last sync
    time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    if sync_item1[6] == 'NULL':
        items_table.update_last_sync_time(sync_item1[0], time)
        sync_item1 = items_table.retrieve_by_item_id(sync_item1[0])[0]
        
    if sync_item2[6] == 'NULL':
        items_table.update_last_sync_time(sync_item2[0], time)
        sync_item2 = items_table.retrieve_by_item_id(sync_item2[0])[0]
    last_sync = max([sync_item1[6],sync_item2[6]])
    last_sync = datetime.strptime(last_sync, '%Y-%m-%dT%H:%M:%S.%f%z')
    pos, src_id, dst_id, most_recent_change = session.most_recent_update(sync_item1[3],sync_item1[0], sync_item2[3], sync_item2[0])
    
    if most_recent_change <= last_sync:
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
        dst_field = fields_table.retrieve_by_field_id(str(src_field[5]))[0]
        dst_fields.append(dst_field)

    #put the names of the fields into two corresponding lists
    src_field_names = []
    for field in src_fields:
        src_field_names.append(field[4])
    
    dst_field_names = []
    for field in dst_fields:
        dst_field_names.append(field[4])
    
    # get the data to be passed to the other service
    if src_item[3] == "jama" or src_item[3] == "Jama":
        src_data = session.get_jama_item(src_id, src_field_names)
        dst_data = session.get_jira_item(dst_id, dst_field_names)
    else:
        src_data = session.get_jira_item(src_id, src_field_names)
        dst_data = session.get_jama_item(dst_id, dst_field_names)

    #convert src data to same type as dst data

    dst_field_values = {} #destination list with source values
    for i in range(len(src_data)):
        src_data_i = src_data[src_field_names[i]]
        dst_data_i = dst_data[dst_field_names[i]]
        if(type(dst_data_i) == int):
            src_data_i = int(src_data_i)
        if(type(dst_data_i) == str):
            src_data_i = str(src_data_i)
        dst_field_values[dst_field_names[i]] = src_data_i

    #send the data
    if src_item[3] == "jama" or src_item[3] == "Jama":
        print(dst_field)
        session.set_jira_item(dst_field[1], dst_field_values)
    else:
        print(dst_field)
        session.set_jama_item(dst_field[1], dst_field_values)

    #update the last sync time with the current time. 
    sync_end_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    for field in dst_fields:
        fields_table.update_last_updated_time(field[0], sync_end_time)
    items_table.update_last_sync_time(dst_id, sync_end_time)
    return True

#function for getting the list of items to be synced and passing them off to the sync function
def sync_all(session):
    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    items_table = ItemsTableOps(db_path)
    success = True
    linked_items = items_table.get_linked_items()
    for item in linked_items:
        try:
            sync_one_item(item[0], session)
        except:
            logging.error("Something failed when syncing item ID:" + str(item[0]))
            success = False
    return success


def admin_sync():
    print("starting all item sync")
    session = connection()
    session.initiate_jama(os.environ["JAMA_SYNC_ORG"], os.environ["JAMA_SYNC_USERNAME"], os.environ["JAMA_SYNC_PASSWORD"])
    session.initiate_jira(os.environ["JIRA_SYNC_ORG"], os.environ["JIRA_SYNC_USERNAME"], os.environ["JIRA_SYNC_PASSWORD"])
    db_path = os.path.join(os.path.dirname(os.getcwd()), "C2TB/JamaJiraConnectDataBase.db")
    items_table = ItemsTableOps(db_path)
    success = True
    linked_items = items_table.get_linked_items()
    for item in linked_items:
        try:
            sync_one_item(item[0], session)
        except:
            logging.error("Something failed when syncing item ID:" + str(item[0]))
            success = False
    return success


# update scheduler to run at specified sync interval
def update_scheduler():
    success = True
    return success


def set_linked_url(jira_id, jama_id):

    #initiate the admin sync user 
    session = connection()
    session.initiate_jama(os.environ["JAMA_SYNC_ORG"], os.environ["JAMA_SYNC_USERNAME"], os.environ["JAMA_SYNC_PASSWORD"])
    session.initiate_jira(os.environ["JIRA_SYNC_ORG"], os.environ["JIRA_SYNC_USERNAME"], os.environ["JIRA_SYNC_PASSWORD"])

    jira_res = session.jira_connection.get_issue(jira_id)

    #Build up the Jira URL
    jira_url = "https://"+ os.environ["JIRA_SYNC_ORG"] + ".atlassian.net/browse/" + jira_res["key"]


    #build up the jama item URL because the jama API doesn't provide it
    jama_project_id = session.get_jama_item(jama_id, ["project"])
    jama_url = "https://" + os.environ["JAMA_SYNC_ORG"] +".jamacloud.com/perspective.req#/items/"
    jama_url = jama_url + str(jama_id) + "?projectId=" + str(jama_project_id["project"])

    #set the Jira URL field in the jama item
    session.set_jama_item(jama_id, {"Jira_URL$29":jira_url})

    #set the jama URL field in the jama item
    session.set_jira_item(jira_id,{"customfield_10029":jama_url})

    return True


if __name__ == '__main__':

    session = connection()
    session.initiate_jama(os.environ["JAMA_SYNC_ORG"], os.environ["JAMA_SYNC_USERNAME"], os.environ["JAMA_SYNC_PASSWORD"])
    session.initiate_jira(os.environ["JIRA_SYNC_ORG"], os.environ["JIRA_SYNC_USERNAME"], os.environ["JIRA_SYNC_PASSWORD"])

    sync_one_item("10040", session)
    sync_all(session)
