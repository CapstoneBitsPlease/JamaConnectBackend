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

class jira_connection:
    def __init__(self, org, username, password):
        self.username = username
        self.token = password
        self.url = "https://"+org+".atlassian.com/rest/api/3/"
    
    def get_item_types(self):

        auth = HTTPBasicAuth(self.username, self.token)

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            self.url,
            headers=headers,
            auth=auth
        )

        return response


class connection:
    def __init__(self):
        self.jama_connection = None
        self.jira_connection = None
        self.id = uuid.uuid4()
    
    def initiate_jama(self, org, username, password, oauth=False):
        #build the URL with the org name
        jama_url = "https://" + org +".jamacloud.com"
        
        #initialize a jama connection and save it.
        self.jama_connection = JamaClient(host_domain=jama_url, credentials=(username, password), oauth=False)
        return self.jama_connection
    
    def initiate_jira(self, org, username, password):
        url = "https://" + org +".atlassian.net"
        self.jira_connection = Jira(url=url, username=username, password=password)
        return self.jira_connection

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
    def get_session(self, token):
        num_sessions = len(self.all_connections)
        for session in range(num_sessions):
            connection = self.all_connections[session]
            if(connection.match_token(token)):
                return connection
            else:
                return None


cur_connections = connections()