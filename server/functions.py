import json
from py_jama_rest_client.client import JamaClient
import connections
import os
from datetime import datetime


# Utility functions

# Convert datetime string to Unix time
def convert_to_seconds(date):
    if date == "NULL":
        return 0
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp()

# Convert Unix time to datetime string
def convert_to_datetime(seconds):
    if seconds == "NULL":
        return 0
    return datetime.fromtimestamp(seconds).strftime('%Y-%m-%dT%H:%M:%S.%f%z')