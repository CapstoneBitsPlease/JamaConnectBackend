from .calling import get_projects
from server import server
import base64
from flask import request
from flask import Response

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
@server.route('/projects/basic/<credentials>')
def all(credentials):
    credentials = base64.b64decode(credentials)
    print (credentials)
    credentials = credentials.decode().split(':')
    username = credentials[0]
    password = credentials[1]
    projects = get_projects(username, password, False)
    return "Number of Projects:" + str(projects)

#Oauth using clientID:clientSecret as credentials (not good)
@server.route('/projects/oath/<credentials>')
def all_projects(credentials):
    credentials = credentials.split(':')
    username = credentials[0]
    password = credentials[1]
    projects = get_projects(username, password, True)
    return "Number of Projects:" + str(projects)

#Login validation interface
@server.route('/login/basic', methods=['GET', 'POST'])
def verify_login():
    if request.method == "POST":
        cred = request.values
        print(cred)
        if(cred.get("username")):
            if(cred.get("username") == "FakeUser"):
                status = Response(status=200)
                return status
            else:
                status = Response(status=401)
                return status