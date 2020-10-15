# This document illustrated the strustures of an open connection
# the server has a list of all connections
# each connection consists of an authenticated Jira and Jama interface
# we use the connections to authenticate a user who has logged in with 
# either service.

from py_jama_rest_client.client import JamaClient
import string
import random
import uuid

secret = "Change me plz"

class jama_connection:
    def __init__(self, org, name, password, oauth):
        self.organization = org
        self.username = name
        self.password = password
        self.oauth = oauth

        jama_url = "https://" + self.organization +".jamacloud.com"
        try:
            self.jama_client = JamaClient(host_domain=jama_url, credentials=(self.username, self.password), oauth=self.oauth)
        except:
            print("Invalid credentials")

class jira_connection:
    def __init__(self, organization, username, password):
        self.organization = organization
        self.username = username
        self.password = password

class connection:
    def __init__(self):
        self.jama_connection = None
        self.jira_connection = None
        self.id = uuid.uuid4()
    
    def initiate_jama(self, org, name, password, oauth):
        self.jama_connection = jama_connection(org, name, password, oauth)
        return self.jama_connection
    
    def match_token(self, token):
        if self.id == token:
            return True
        else:
            return False

class connections:
    def __init__(self):
        self.all_connections=[]
    
    def new_connection(self):
        new_connection = connection()
        self.all_connections.append(new_connection)
        return new_connection

    def get_session(self, token):
        num_sessions = len(self.all_connections)
        for session in range(num_sessions):
            connection = self.all_connections[session]
            if(connection.match_token(token)):
                return connection
            else:
                return None
cur_connections = connections()