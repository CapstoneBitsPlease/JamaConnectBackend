import base64
from flask import Flask
from flask import request
from flask import Response
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token , get_jwt_identity)
from flask import jsonify
from flask_cors import CORS, cross_origin
import json
import os
from set_up_log import json_log_setup
import connections
import functions
import database
from database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)

app = Flask(__name__)

# setup for the JWT
app.config['JWT_SECRET_KEY']= 'Change this' #replace with a real secret?
jwt = JWTManager(app)

#create the active connection list
cur_connections = connections.connections()

#set the CORS headrer to allow all access
CORS(app, supports_credentials=True)

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
        username = cred["username"]
        password = cred["password"]
        organization = cred["organization"]
        
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

@app.route('/user', methods=['GET'])
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

@app.route('/users', methods=['GET'])
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

@app.route('/jama/projects', methods=['GET'])
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

@app.route('/jama/item_types', methods=['GET'])
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

@app.route('/jama/items_by_type', methods=['GET'])
@jwt_required
def get_items_of_type():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    
    args = request.values
    type_id = int(args["type_id"])
    project_id = int(args["project_id"])
    
    if type_id == "" or project_id == "":
        return jsonify("Must specify an item type ID and Project ID"), 422
    
    if session.jama_connection:
        items = jsonify(session.get_items_by_type(project_id, type_id))
        return items
    else:
        return Response(401)

@app.route('/capstone/item_types_jira')
def get_capstone_item_types_jira():
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    itemsTableOps = ItemsTableOps(db_path)
    types = itemsTableOps.get_all_jira_types()
    print(types)
    return jsonify(types = types), 200

@app.route('/capstone/item_types_jama')
def get_capstone_item_types_jama():
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    itemsTableOps = ItemsTableOps(db_path)
    types = itemsTableOps.get_all_jama_types()
    print(types)
    return jsonify(types = types), 200

@app.route('/capstone/items_of_type')
def get_capstone_items_of_type():
    type_ = request.values("type")
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    itemsTableOps = ItemsTableOps(db_path)
    items = itemsTableOps.retrieve_by_type(type_)
    return jsonify(items = items), 200

@app.route('/jama/item_by_id', methods=['GET'])
@jwt_required
def get_item_of_id():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    
    args = request.values
    item_id = int(args["item_id"])
    
    if item_id == "":
        return jsonify("Must specify an item ID"), 422
    
    if session.jama_connection:
        item = jsonify(session.get_item_by_id(item_id))
        return item
    else:
        return Response(401)

@app.route('/Jira_item_types')
@jwt_required
def item_types():
    identity = get_jwt_identity()
    token = identity.get("connection_id")
    print(token)
    session = cur_connections.get_session(token)
    return session

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

# Retrieves item by ID
@app.route('/capstone/item_of_id')
def get_capstone_item_of_id():
    print(request)
    id_ = request.values["id"]
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    itemsTableOps = ItemsTableOps(db_path)
    items = itemsTableOps.retrieve_by_item_id(id_)
    return jsonify(items = items), 200

# Retrieves the length of time of the last sync
@app.route('/capstone/last_sync_time')
def last_sync_time():
    if request.method == 'GET':
        db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
        sync_table = SyncInformationTableOps(db_path)
        last_sync_time = sync_table.get_last_sync_time()
        return jsonify(last_sync_time)
    else:
        return Response(401)

# Retrieves fields ready to sync
@app.route('/capstone/fields_to_sync')
def fields_to_sync():
    if request.method == 'GET':
        db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
        fields_table = FieldsTableOps(db_path)
        items_table = ItemsTableOps(db_path)
        sync_table = SyncInformationTableOps(db_path)
        response = fields_table.get_fields_to_sync(items_table, sync_table)
        num_fields = response[0]
        fields_to_sync = response[1]
        return jsonify(num_fields=num_fields, fields_to_sync=fields_to_sync)
    else:
        return Response(401)

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

@app.route('/post_link_item', methods=['POST'])
def post_link_item():#returns false if the item called for does not exist in the Items table, does not check to see if the linked item exists in the items table
    if request.method == 'POST':
        input = request.values
        id_primary=input["primary_ID"]#This is the id that remains the same whose linked_id is being updated
        id_update=input["update_ID"]#this is the new linked_id
        db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
        print(db_path)
        itemsTableOps = ItemsTableOps(db_path)
        databaseOperations = DatabaseOperations(db_path)
        if databaseOperations.present_in_table("Items", id_primary):
            itemsTableOps.update_linked_id(id_primary, id_update)
            return jsonify("Success"), 200
        return jsonify("The Item does not exist in the Items table"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
