import json
from py_jama_rest_client.client import JamaClient
import connections
import os
from datetime import datetime

# Utility functions

# Convert datetime string to Unix time (seconds since 1/1/1970)
def convert_to_seconds(date):
        date_time_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%f')
        seconds = date_time_object.timestamp()
        return seconds