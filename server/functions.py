import json
from py_jama_rest_client.client import JamaClient
import connections
import os
from datetime import datetime


# Utility functions

# Convert datetime string to Unix time
def convert_to_seconds(date):
    if(date == "NULL"):
        return 0
    else:
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%f').timestamp()

# Convert Unix time to datetime string
def convert_to_datetime(seconds):
    if(seconds == "NULL"):
        return 0
    else:
        return datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%f')