import json
from py_jama_rest_client.client import JamaClient

def get_projects(clientID, ClientPass):
    
    jama_url = "https://capstone2020.jamacloud.com"
    jama_api_username = clientID
    jama_api_password = ClientPass

    jama_client = JamaClient(host_domain=jama_url, credentials=(jama_api_username, jama_api_password))

    project_list = jama_client.get_projects()
    projects = 0
    
    for project in project_list:
        project_name = project['fields']['name']
        print('\n---------------' + project_name + '------------------')



    # Print each field
    for field_name, field_data in project.items():

        projects +=1

        # If one of the fields(i.e. "fields") is a dictionary then print it's sub fields indented.
        if isinstance(field_data, dict):
            print(field_name + ':')
            # Print each sub field
            for sub_field_name in field_data:
                sub_field_data = field_data[sub_field_name]
                print('\t' + sub_field_name + ': ' + str(sub_field_data))

        # If this field is not a dictionary just print its field.
        else:
            print(field_name + ': ' + str(field_data))

    return projects