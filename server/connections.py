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
