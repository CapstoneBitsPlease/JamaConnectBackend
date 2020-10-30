import json
from py_jama_rest_client.client import JamaClient
class linker:
	def link(self, jira_item_id, jama_item_id):
		jql_request = 'project = '+project_id+' AND status NOT IN (Closed, Resolved) AND Issue Key = ' + jira_item_id
		jira_item = jira.jql(jql_request)
		print(jira_item)
		jama_item = jama_connection.get_item(jama_id)
		jama_fields=json.load(jama_item.fields)
		jira_fields=json.load(jira_item.data)
	def find_items(self, type, id):
		names=find_items_database(type, id)
		return names
	def find_fields(self, type, id):
		return find_fields_database(type, id)
#	def find_links(self, name):
#		return __findmappings(name)

	def store_item_linking(self, jama_id, jama_type, jira_id, jira_type):
		if present_in_table("Items", jama_id):
			update_linked_id(jama_id,jira_id)
		else:
			insert_into_items_table(jama_id, jama_title, jama_type, jama_service, jira_id)
		if present_in_table("Items", jira_id):
			update_linked_id(jira_id,jama_id)
		else:
			insert_into_items_table(jira_id, jira_title, jira_type, jira_service, jama_id)
	#def map_field(self, jama_item_id, jama_field_id, jira_item_id, jira_field_id):
