from flask import Flask

server = Flask(__name__)

from server import connections
from server import routes

