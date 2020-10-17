from flask import Flask
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

from server import connections
from server import routes

