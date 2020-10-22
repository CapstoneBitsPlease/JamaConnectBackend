import json
from py_jama_rest_client.client import JamaClient
import database
import connections

def get_project_list(self):
    response = self.jama_connection.get_projects()
    projects = []
    for project in response:
        item = {"name":project["fields"]["name"], "id":project["id"]}
        projects.append(item)
    return projects

def get_last_sync_time(self):
    # SELECT rows FROM SyncInfo WHERE completed_successfully = 0
    response = database.retrieve_by_column_value(SyncInfo, completed_successfully, 0)
   
    
    return 1

