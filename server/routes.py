from server import server
import base64
from flask import request
from flask import Response
import functions

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
        print(cred)
        username = cred.get("username")
        password = cred.get("password")
        organization = cred.get("organization")
        #authenticate the Jama user
        jwt = functions.authenticate_user(organization,username, password)
        if(jwt == "invalid"):
            status = Response(status=400)
            return status
        return jwt

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
