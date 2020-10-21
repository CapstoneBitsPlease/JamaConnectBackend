from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import base64
from flask import request
from flask import Response

import functions
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token , get_jwt_identity)
from flask import jsonify 
import connections

# setup for the JWT
app.config['JWT_SECRET_KEY']= 'Change this' #replace with a real secret?
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

@app.route('/jama_item')
@jwt_required
def jama_item():
    return 1

@app.route('/Jira_item_types')
@jwt_required
def item_types():
    identity = get_jwt_identity()
    token = identity.get("connection_id")
    print(token)
    session = functions.get_session(token)
    return session

# retrieves all Jama projects 
@app.route('/jama_projects')
@jwt_required
def jama_projects():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    if session.jama_connection:
        projects = session.get_project_list()
        return jsonify(projects)
    else:
        return Response(401)

# retrieves all Jama items in a given project
@app.route('/jama_items')
@jwt_required
def jama_items():
    # validate the user
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    # get the Jama items in the given project
    if session.jama_connection and request.method == 'GET':
        arguments = request.values
        project_id = arguments.get("projectid")
        items = session.get_item_list(project_id)
        return jsonify(items)
    else:
        return Response(401)
    
# retrieves all Jama item types of a given project 
@app.route('/item_types_of_project')
@jwt_required
def item_types_of_project():
    # validate the user
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    # get the Jama item types of a given project
    if session.jama_connection and request.method == 'GET':
        arguments = request.values
        project_id = arguments.get("projectid")
        item_types = session.get_item_types_of_project_list(project_id)
        return jsonify(item_types)
    else:
        return Response(401)

# retrieves all Jama item types across all projects 
@app.route('/jama_item_types')
@jwt_required
def jama_item_types():
    # validate the user
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    # get the Jama item types across all projects
    if session.jama_connection:
        item_types = session.get_item_type_list()
        return jsonify(item_types)
    else:
        return Response(401)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
