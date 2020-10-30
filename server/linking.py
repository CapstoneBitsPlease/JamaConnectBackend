import json
from py_jama_rest_client.client import JamaClient
import database
class linker:
	def find_items(self, type, id):
		names=__find_items(type, id)
		return names
	def find_fields(self, type, id):
		return __find_fields(type, id)
	def find_links(self, name):
		return __findmappings(name)

	def store_item_linking(self, jama_id, jama_type, jira_id, jira_type):
		if present_in_table("Items", jama_id):
			update_linked_id(jama_id,jira_id)
		else:
			insert_into_items_table(jama_id, jama_title, jama_type, jama_service, jira_id)
		if present_in_table("Items", jira_id):
			update_linked_id(jira_id,jama_id)
		else:
			insert_into_items_table(jira_id, jira_title, jira_type, jira_service, jama_id)
	def map_field(self, jama_item_id, jama_field_id, jira_item_id, jira_field_id):
