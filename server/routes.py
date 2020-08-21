from server import server

@server.route('/')
@server.route('/index')
def index():
    return "hello world"