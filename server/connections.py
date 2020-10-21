# This document illustrated the strustures of an open connection
# the server has a list of all connections
# each connection consists of an authenticated Jira and Jama interface
# we use the connections to authenticate a user who has logged in with 
# either service.

from py_jama_rest_client.client import JamaClient
import uuid
import requests
from requests.auth import HTTPBasicAuth
import json
from atlassian import Jira
from atlassian.errors import ApiError
from py_jama_rest_client.client import *


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

    # returns a dictionary with the name and id of all projects
    def get_project_list(self):
        response = self.jama_connection.get_projects()
        projects=[]
        for project in response:
            item = {"name":project["fields"]["name"], "id":project["id"]}
            projects.append(item)
        return projects

    # returns a dictionary with the name, id, and item_type of all items in a given project
    def get_item_list(self, project_id):
        response = self.jama_connection.get_items(project_id)
        items = []
        for item in response:
            entry = {"name":item["fields"]["name"], "id":item["id"], "item_type":item["itemType"]}
            items.append(entry)
        return items

    # returns a dictionary with the name and id of all item_types
    def get_item_type_list(self):
        response = self.jama_connection.get_item_types()
        item_types = []
        for item_type in response:
            entry = {"name":item_type["fields"][0]["name"], "id":item_type["id"]}
            item_types.append(entry)
        return item_types

    # returns a dictionary with the name and id of all item_types
    def get_item_types_of_project_list(self, project_id):
        response = self.jama_connection.get_item_types_of_project(project_id)
        item_types = []
        for item_type in response:
            entry = {"name":item_type["fields"][0]["name"], "id":item_type["id"]}
            item_types.append(entry)
        return item_types
    

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
