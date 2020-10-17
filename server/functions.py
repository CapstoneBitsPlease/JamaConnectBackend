import json
from py_jama_rest_client.client import JamaClient
import database
import connections


# function fo defining Jama and Jira user authentications
# as well as session creation. 
def authenticate_user(organization, username, password):

    session = connections.cur_connections.new_connection()
    
    if(session.initiate_jama(organization, username, password, False) == "invalid"):
        return "invalid"
    
    projects = session.jama_connection.get_projects()
    #user = session.jama_connection.jama_client.g
    print("user has been authenticated")
    return session.id

#give this function a session UUID and get the session object returned
def get_session(token):
    session = connections.cur_connections.get_session(token)
    return session

#gets the number of current users
def get_cur_users():
    connection_list = connections.cur_connections.all_connections
    number = len(connection_list)
    return {"number of users": number}

def get_all_jira_items(session):
    jira_client = connections.jira_connection('capstone2020teamb', 'sduncan@pdx.edu', 'z7ChqFTNfhm1fBcmX9yIDF4E')
    return jira_client.get_item_types()

def jira_item_types(session):
    response = session.jira_connection.get_item_types()
    return response