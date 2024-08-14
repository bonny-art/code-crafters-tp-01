import itertools
from datetime import datetime

class Note:
	_id_counter = itertools.count(1)
	def __init__(self, text, tags=None):
		self.id = next(Note._id_counter)
		self.create_date = datetime.now()
		self.text = text
		self.tags = tags if tags else []

	def add_tag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def remove_tag(self, tag):
		if tag in self.tags:
			self.tags.remove(tag)