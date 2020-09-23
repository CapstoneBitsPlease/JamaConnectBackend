from .calling import get_projects
from server import server
import base64


@server.route('/')
@server.route('/index')
def index():
    return "hello world"

#send the credentials to the server in base64 encoding of the string "username:password"
@server.route('/all/<credentials>')
def all(credentials):
    credentials = base64.b64decode(credentials)
    print (credentials)
    credentials = credentials.decode().split(':')
    username = credentials[0]
    password = credentials[1]
    projects = get_projects(username, password)
    return "Number of Projects:" + str(projects)