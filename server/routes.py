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
from server.connections import connections
import functions
import database
from database import (ItemsTableOps, FieldsTableOps, SyncInformationTableOps)
import sync
import datetime



app = Flask(__name__)

# setup for the JWT
app.config['JWT_SECRET_KEY']= 'Change this' #replace with a real secret?
jwt = JWTManager(app)

#create the active connection list
cur_connections = connections()

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
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity={"connection_id":session.id}, expires_delta=expires)
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
        
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity={"connection_id":session.id},expires_delta=expires)
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
        item = jsonify(session.get_jama_item_by_id(item_id))
        return item
    else:
        return Response(401)

@app.route('/jira/item_by_id', methods=['GET'])
@jwt_required
def get_jira_item_of_id():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)

    args = request.values
    item_id = args["id"]
    
    if item_id == "":
        return jsonify("Must specify an item ID."), 422
    
    if session.jira_connection:
        item = jsonify(session.get_jira_item_by_id(item_id))
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

# Unlinkes a pair of linked Jira and Jama items from the JamaJira Connect DataBase
@app.route('/capstone/unlink_with_id')
def get_capstone_unlink_with_id():
    print(request)
    id_ = request.values["id"]
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
    itemsTableOps = ItemsTableOps(db_path)
    items = itemsTableOps.retrieve_by_item_id(id_)
    if not items:
        return "Unlinking did not occure. This item was not found.", 200

    item = items[0]
    if str(item[2]).lower() == "none" or str(item[2]).lower() == "null":
        return "Unlinking did not occure. This item is not linked.", 200

    fieldsTableOps = FieldsTableOps(db_path)
    fields = fieldsTableOps.retrieve_by_item_id(id_)
    IDs_to_unlink = []
    for field in fields:
        IDs_to_unlink.append(field[5])

    fields_to_unlink = []
    for ID in IDs_to_unlink:
        fields_to_unlink += fieldsTableOps.retrieve_by_linked_id(ID)

    for field in fields_to_unlink:
        fieldsTableOps.update_linked_id(field[0], "None") 
        fieldsTableOps.delete_field(field[0])

    item_ID_to_unlink = item[2]
    items_to_unlink = itemsTableOps.retrieve_by_linked_id(item_ID_to_unlink)
    for item in items_to_unlink:
        itemsTableOps.update_linked_id(item[0], "None")
        itemsTableOps.delete_item(item[0])
    return "Unlinking successful.", 200

# Retrieves the length of time of the last sync
@app.route('/capstone/last_sync_time', methods=['GET'])
def last_sync_time():
    # get the length of time of the last sync from our database 
    time = sync.last_sync_period()
    if time:
        return jsonify(time)
    else:
        Response(401)

# Retrieves the length of time of the last sync from capstone database
@app.route('/capstone/last_successful_sync_time')
def last_successful_sync_time():
    if request.method == 'GET':
        db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaConnectBackend/JamaJiraConnectDataBase.db")
        sync_table = SyncInformationTableOps(db_path)
        last_sync_time = sync_table.get_last_sync_time()
        return jsonify(last_sync_time)
    else:
        return Response(500)

# Retrieves fields ready to sync from capstone database
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
        return Response(500)

@app.route('/sync/single', methods=['POST'])
@jwt_required
def sync_one():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)

    item_id = request.values["item_id"]

    response = sync.sync_one_item(item_id, session)

    if response:
        return Response(200)
    else:
        return Response(500)


@app.route('/sync_all', methods=['POST'])
@jwt_required
def sync_all():
    token = get_jwt_identity()
    uuid = token.get("connection_id")
    session = cur_connections.get_session(uuid)
    if session.jama_connection and session.jira_connection:
        response = sync.sync_all(session)
        if response:
            return ["Synced all items successfully.", Response(200)]
        else:
            return Response(500)
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

# Links two items. Accepts 4 arrays: jama_item, jira_item, jama_fields, and jira_fields, and 1
# integer parameter which indicates the total number of fields in each fields array.
@app.route('/link_items', methods=['POST'])
def link_items():
    json_log_setup()
    if request.method == "POST":
        # Get all items in array that correspond to jira_item[].
        jira_item = request.form.getlist("jira_item[]")
        print(jira_item)
        # Get all items in array that correspond to jama_item[].
        jama_item = request.form.getlist("jama_item[]")
        print(jama_item)
        # Get number of fields that will be linked.
        num_fields = request.form.get("num_fields")
        print(num_fields)
        jira_fields = []
        jama_fields = []
        num = int(num_fields)
        for i in range(0, num):
            val_to_get = "jira_fields[{}]".format(i)
            print(val_to_get)
            jira_field = request.form.getlist(val_to_get)
            print(jira_field)
            jira_fields.append(jira_field)
        for i in range(0, num):
            val_to_get = "jama_fields[{}]".format(i)
            print(val_to_get)
            jama_field = request.form.getlist(val_to_get)
            jama_fields.append(jama_field)
        print(jira_fields)
        print(jama_fields)
        num_jira_fields = len(jira_fields)
        num_jama_fields = len(jama_fields)
        if num_jira_fields != num_jama_fields:
            print("array len is different")
            return {"error": "The number of Jama fields to link does not match the number of Jira fields."}, 500
        success = database.link_items(jira_item, jama_item, jira_fields, jama_fields, num_jama_fields)
        if success == 0:
            print("something went wrong with linking")
            return {"error": "Linking unsuccessful"}, 500
        return {"success": "Linking was successful"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
