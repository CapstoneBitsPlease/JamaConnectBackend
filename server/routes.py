from flask import Flask
import logging

app = Flask(__name__)

import base64
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token , get_jwt_identity)
from flask import jsonify
import connections
import database
from database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)
from set_up_log import json_log_setup
import json
import os

# setup for the JWT
app.config['JWT_SECRET_KEY']= 'Change_at_some_point' #replace with a real secret?
jwt = JWTManager(app)

#create the active connection list
cur_connections = connections.connections()


# "@server.route('...')" indicates the URL path
# the function that follows is called when requesting 
# the indicated URL.
@app.route('/')
@app.route('/index')
def index():
    return "hello world"

#send the credentials to the server in base64 encoding of the string "username:password"
#putting something in the <> like <foo> creates a variable that can be passed into the 
#function call.

#Login validation interface
@app.route('/login/jama/basic', methods=['GET', 'POST'])
def initalize_jama():
    if request.method == "POST":
        #request.values converts form items AND URLstring encoded items into a dict
        cred = request.values
        username = cred["username"]
        password = cred["password"]
        organization = cred["organization"]
        
        #check to see if an authorization token is being passed in, otherwise make a new connection
        token = get_jwt_identity()
        session = None
        if token:
            uuid = token.get("connection_id")
            session = cur_connections.get_session(uuid)
        if not session:
            session = cur_connections.new_connection()

        #authenticate the Jama user
        response = session.initiate_jama(organization, username, password)

        #if it was invalid credentials respond with the error
        if(response != 200):
            status = Response(status=response)
            return status
        
        #the credentials are valid, generate a JWT and return it
        access_token = create_access_token(identity={"connection_id":session.id})
        return jsonify(access_token=access_token), 200

@app.route('/login/jira/basic', methods=['POST'])
@jwt_required
def initialize_jira():
    if request.method == "POST":
        #request.values converts form items AND URLstring encoded items into a dict
        cred = request.values
        username = cred.get("username")
        password = cred.get("password")
        organization = cred.get("organization")
        
        #check to see if an authorization token is being passed in, otherwise make a new connection
        session= None
        token = get_jwt_identity()
        if token:
            uuid = token.get("connection_id")
            session = cur_connections.get_session(uuid)
        if not session:
            session = cur_connections.new_connection()
            

        #authenticate the Jama user
        response = session.initiate_jira(organization, username, password)

        #if it was invalid credentials respond with the error
        if response != 200:
            status = Response(status=response)
            return status
        
        access_token = create_access_token(identity={"connection_id":session.id})
        return jsonify(access_token=access_token), 200

@app.route('/user')
@jwt_required
def user():
    #This is basicaly the authenticaion chunk
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)

    jama = False
    jira = False

    if session.jama_connection:
        jama = True
    if session.jira_connection:
        jira = True

    return {"jama_connected": jama, "jira_connected": jira}, 200

@app.route('/users')
@jwt_required
def get_all_user():
    if request.method == "GET":
        token = get_jwt_identity()
        uuid = token.get("connection_id")
        session = cur_connections.get_session(uuid)
        if session == None:
            status = Response(500)
            return status
        return {"Number of current connections": len(cur_connections.all_connections)}, 200

@app.route('/jama/projects')
@jwt_required
def getprojects():
    #This is basicaly the authenticaion chunk
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)

    if session.jama_connection:
        projects = session.get_project_list()
        return jsonify(projects)
    else:
        return Response(401)

@app.route('/jama/item_types')
@jwt_required
def get_item_types():
    #This is basicaly the authenticaion chunk
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)

    if session.jama_connection:
        item_types = jsonify(session.get_type_list())
        return item_types
    else:
        return Response(401)


@app.route('/jama_item_types')
def get_jama_item_types():
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    print(db_path)
    itemsTableOps = ItemsTableOps(db_path)
    types = itemsTableOps.get_all_types()
    print(types)
    return jsonify(types = types), 200

@app.route('/Jira_item_types')
@jwt_required
def item_types():
    identity = get_jwt_identity()
    token = identity.get("connection_id")
    print(token)
    session = cur_connections.get_session(token)
    return session

@app.route('/demo_logs')
def default():
    json_log_setup()
    database.logging_demo()
    return {"logging": "lit"}, 200

@app.route('/get_logs')
def get_logs():
    error_list = []
    with open('error_json.log') as f:
        for json_obj in f:
            error = json.loads(json_obj)
            error_list.append(error)
    return jsonify(error_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
