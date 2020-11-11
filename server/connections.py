# This document illustrated the strustures of an open connection
# the server has a list of all connections
# each connection consists of an authenticated Jira and Jama interface
# we use the connections to authenticate a user who has logged in with 
# either service.

#from py_jama_rest_client.client import JamaClient
import uuid
import requests
from requests.auth import HTTPBasicAuth
import json
from atlassian import Jira
from atlassian.errors import ApiError
from py_jama_rest_client.client import *
from datetime import datetime


class connection:
    def __init__(self):
        self.jama_connection = None
        self.jira_connection = None
        self.id = str(uuid.uuid4())
    
    def initiate_jama(self, org, username, password, oauth=False):
        #build the URL with the org name
        jama_url = "https://" + org +".jamacloud.com"
        
        #initialize a jama connection and test to see if it valid
        jama_connection = JamaClient(host_domain=jama_url, credentials=(username, password), oauth=False)
        try:
            jama_connection.get_projects()
            
        except APIException as error:
            return error.status_code
        
        #if it was valid save it and return a 200 status code
        self.jama_connection = jama_connection
        return 200
    
    def initiate_jira(self, org, username, password):
        #build the URL with the org name
        url = "https://" + org +".atlassian.net"
        #initalize the jira connection
        jira_connection = Jira(url=url, username=username, password=password)

        try:
            jira_connection.get_all_projects()
        except:
            return 401


        self.jira_connection = jira_connection
        return 200

    def get_project_list(self):
        response = self.jama_connection.get_projects()
        projects =[]

        for project in response:
            item = {"name":project["fields"]["name"], "id":project["id"]}
            projects.append(item)
        return projects
    
    def get_type_list(self):
        response = self.jama_connection.get_item_types()
        types=[]
        for j_type in response:
            item = {"name":j_type["display"], "id":j_type["id"]}
            types.append(item)
        return types

    def get_items_by_type(self, project_id, type_id):
        """
        get a list of items and item_id's given a project and an item type
        """
        response = self.jama_connection.get_abstract_items(project=project_id, item_type=type_id)
        items=[]
        for item_chunk in response:
            item = {"name":item_chunk["fields"]["name"], "id":item_chunk["id"]}
            items.append(item)
        return items
    
    # gets a jama item and returns only the fields specified in the array
    def get_jama_item(self, item_id, fields):
        jama_object = self.jama_connection.get_item(item_id)
        item={}
        for field in fields:
            if jama_object.get(field):
                item[field] = jama_object[field]
            else:
                 item[field] = jama_object["fields"][field]
        return item

    # gets a Jira item and returns only the fields specified in the array
    def get_jira_item(self, item_key, fields):
        item = {}
        for field in fields:
            jira_object = self.jira_connection.issue_field_value(item_key, field)
            item[field] = jira_object
        return item
    
    # updates the fields of the jama item specified by the item_key
    # and fields in the form {"field":"value", "field":"value",..}
    def set_jira_item(self, item_key, fields):
        #jira.edit_issue("C2TB-41",{"customfield_10016":[{"set":14.0}]})
        json_fields ={}
        for field in fields:
            json_fields[field] = [{"set":fields[field]}]
        self.jira_connection.edit_issue(item_key, json_fields, False)
        return True

    def set_jama_item(self, item_id, fields):
        for field in fields:
            path = "/fields/" + field
            patch = { "op":"replace", "path": path, "value":fields[field]}
            self.jama_connection.patch_item(item_id, patch)
        return True

    #this function returns the id and last update time of the item last updated.
    # return format (pos of src, src_id, dst_id, most recent update)
    def most_recent_update(self,item_1_service, item_1_id, item_2_service, item_2_id):

        if item_1_service == "jama":
            item1 = self.get_jama_item(item_1_id, ["modifiedDate"])
            item2 = self.get_jira_item(item_2_id, ["updated"])
            item1_time = datetime.strptime(item1["modifiedDate"], '%Y-%m-%dT%H:%M:%S.%f%z')
            item2_time = datetime.strptime(item2["updated"], '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            item2 = self.get_jama_item(item_2_id, ["modifiedDate"])
            item1 = self.get_jira_item(item_1_id, ["updated"])
            item2_time = datetime.strptime(item2["modifiedDate"], '%Y-%m-%dT%H:%M:%S.%f%z')
            item1_time = datetime.strptime(item1["updated"], '%Y-%m-%dT%H:%M:%S.%f%z')
        
        #time comparison
        if(item1_time >= item2_time):
            return [0, item_1_id, item_2_id, item1_time]
        return  [1,item_2_id, item_1_id, item2_time]


    def get_jama_item_by_id(self, item_id):
        try:
            response = self.jama_connection.get_item(item_id = item_id)
        except ResourceNotFoundException:
            response = "Item ID not found."

    def get_jira_item_by_id(self, key):
        try:
            response = self.jira_connection.issue(key = key)
        except requests.exceptions.HTTPError:
            response = "Item key not found."
        return response    

    def match_token(self, token):
        if self.id == token:
            return True
        else:
            return False

class connections:
    def __init__(self):
        self.all_connections=[]
    
    #creates a new session and returns a UUID,
    #this does NOT log the user into Jama or Jira
    #make sure to validate that 
    def new_connection(self):
        new_connection = connection()
        self.all_connections.append(new_connection)
        return new_connection

    #takes a session UUID and return the session object
    #if there is no token then it returns none
    def get_session(self, token):
        if not token:
            return None
        num_sessions = len(self.all_connections)
        for session in range(0,num_sessions):
            connection = self.all_connections[session]
            if(connection.match_token(token)):
                return connection
        return None
