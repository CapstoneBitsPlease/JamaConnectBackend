from flask import Flask

server = Flask(__name__)

from server import initalize
from server import routes

