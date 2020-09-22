from .calling import get_projects
from server import server


@server.route('/')
@server.route('/index')
def index():
    return "hello world"

@server.route('/all')
def all():
    projects = get_projects('sduncan', "Fuck0ffJama")
    return "Number of Projects:" + str(projects)