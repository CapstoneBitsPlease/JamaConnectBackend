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
		jama_primary=find_primary_key(jama_type, jama_id)
		jira_primary=find_primary_key(jira_type, jira_id)
		update_linked_id(jama_id,jira_id)