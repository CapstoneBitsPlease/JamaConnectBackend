from flask import g
import database
import os
import logging
from database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)

def link_items(jira_item, jama_item, jira_fields, jama_fields, num_fields):
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    items_ops = ItemsTableOps(db_path)
    fields_ops = FieldsTableOps(db_path)
    print(jira_item[0])
    print(jama_item[0])
    items_ops.insert_into_items_table(jira_item[0], jira_item[1], jira_item[2], "Jira", jama_item[0], jira_item[3], "NULL")
    items_ops.insert_into_items_table(jama_item[0], jama_item[1], jama_item[2], "Jama", jira_item[0], jama_item[3], "NULL")
    field_id = fields_ops.get_next_field_id()
    for i in range(0, num_fields):
        try:
            field_id += 1
            fields_ops.insert_into_fields_table(field_id, jira_item[0], "NULL", jira_fields[i][0], jira_fields[i][1], field_id + 1)
            field_id += 1
            fields_ops.insert_into_fields_table(field_id, jama_item[0], "NULL", jama_fields[i][0], jama_fields[i][1], field_id - 1)
        except:
            logging.log("Something went wrong when linking ", jama_fields[i][0], " with ", jira_fields[i][0])
            success = 0
    return success
