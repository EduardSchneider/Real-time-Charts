import requests
import pandas as pd


'''
This python file is intended for use alongside the realtimecharts module.
This file is used to create a connector to an external server of the realtimecharts Dashboard.
Each function in this file is added to a list of functions below.

Want to create your own connector? Create a new function below.

CONNECTOR MAKE-UP
The connector should be able to request data to the server.
The return must contain a dataframe object with a standard index.
The timestamp index isc created within Connection.data_to_timestamp()
This is necessary because Periodic dataframes don't function otherwise.
'''


def get_http_connector(connection):
    jsonlist = []
    data_request = requests.get(connection.address)
    jsonlist.append(data_request.json())
    df = pd.DataFrame(jsonlist)

    return df


def get_http_connector2(connection):
    jsonlist = []
    data_request = requests.get(connection.address)
    jsonlist.append(data_request.json())
    df = pd.DataFrame(jsonlist)

    return df


# *-------------------------------------------------------------------------------------------------------*

# Add your connector function here, as a tuple.
# Tuple item 1: name of your connecctor
# Tuple item 2: your connector function

connector_functions = [
    ('HTTP connector', get_http_connector),
    ('HTTP connector2', get_http_connector2)
]