from server import server
import base64
from flask import request
from flask import Response
import functions
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token , get_jwt_identity)
from flask import jsonify
import connections

# setup for the JWT
server.config['JWT_SECRET_KEY']= 'Change_at_some_point' #replace with a real secret?
jwt = JWTManager(server)

# "@server.route('...')" indicates the URL path
# the function that follows is called when requesting 
# the indicated URL.
@server.route('/')
@server.route('/index')
def index():
    return "hello world"

#send the credentials to the server in base64 encoding of the string "username:password"
#putting something in the <> like <foo> creates a variable that can be passed into the 
#function call.

#Login validation interface
@server.route('/login/basic', methods=['GET', 'POST'])
def verify_login():
    if request.method == "POST":
        #request.values converts form items AND URLstring encoded items into a dict
        cred = request.values
        username = cred.get("username")
        password = cred.get("password")
        organization = cred.get("organization")
        
        #authenticate the Jama user
        connection_id = functions.authenticate_user(organization, username, password)
        if(connection_id == "invalid"):
            status = Response(status=400)
            return status
        
        #generate the JWT to use as uthentication for future transactions
        access_token = create_access_token(identity={"username":username,"connection_id":connection_id})
        return jsonify(access_token=access_token), 200

@server.route('/login/jira/basic', methods=['POST'])
def initialize_jira():
    cred = request.values
    org = cred["organization"]
    username = cred["username"]
    password = cred["password"]

    token = request.values.get("Authorization")
    session = None
    
    if(token):
        session = functions.get_session(token)
    else:
        session = connections.cur_connections.new_connection()
    
    session.initiate_jira(org, username, password)

    access_token = create_access_token(identity={"connection_id":session.id})
    return jsonify(access_token=access_token), 200

@server.route('/user')
@jwt_required
def user():
    current_connection = get_jwt_identity()
    return jsonify(Jama_Login=current_connection), 200

@server.route('/users')
def get_all_user():
    if request.method == "GET":
        arg = request.values
        token = arg.get("Authorization")
        session = functions.get_session(token)
        if session == None:
            status = Response(500)
            return status
        return functions.get_cur_users()

@server.route('/jama_item')
@jwt_required
def jama_item():
    return 1

@server.route('/Jira_item_types')
@jwt_required
def item_types():
    identity = get_jwt_identity()
    token = identity.get("connection_id")
    print(token)
    session = functions.get_session(token)
    return functions.jira_item_types(session)
