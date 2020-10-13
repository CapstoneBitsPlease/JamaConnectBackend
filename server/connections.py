# This document illustrated the strustures of an open connection
# the server has a list of all connections
# each connection consists of an authenticated Jira and Jama interface
# we use the connections to authenticate a user who has logged in with 
# either service.


from py_jama_rest_client.client import JamaClient

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
            raise ConnectionError()

class jira_connection:
    def __init__(self, organization, username, password):
        self.organization = organization
        self.username = username
        self.password = password

class connection:
    def __init__(self):
        self.token = []
        self.jama_connection = None
        self.jira_connection = None
        self.token = "Thisisarandomtoke...probably"
    
    def initiate_jama(self, org, name, password, oauth):
        self.jama_connection = jama_connection(org, name, password, oauth)
        return self.jama_connection


class connections:
    def __init__(self):
        self.all_connections=[]
    
    def new_connection(self):
        new_connection = connection()
        self.all_connections.append(new_connection)
        return new_connection

cur_connections = connections()