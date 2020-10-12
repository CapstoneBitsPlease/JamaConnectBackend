from py_jama_rest_client.client import JamaClient

class jama_connection:
    def __init__(self, org, name, passwrd, oauth):
        self.organization = org
        self.username = name
        self.password = passwrd
        self.oauth = oauth

        jama_url = "https://" + self.organization +".jamacloud.com"
        self.jama_client = JamaClient(host_domain=jama_url, credentials=(self.username, self.password), oauth=self.oauth)

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

class connections:
    def __init__(self):
        self.all_connections=[]
    
    def new_connection(self,org, name, passwrd, oauth):
        connection = jama_connection(org, name, passwrd, oauth)
        self.all_connections.append(connection)
        return connection


connections = connections()