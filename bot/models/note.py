import uuid
from datetime import datetime
from typing import List

class Note:
	def __init__(self, text, tags: List[str]=None):
		self.id = str(uuid.uuid4())
		self.create_date = datetime.now()
		self.text = text
		self.tags = tags if tags else []

	def add_tag(self, tag):
		if tag not in self.tags:
			self.tags.append(tag)

	def remove_tag(self, tag):
		if tag in self.tags:
			self.tags.remove(tag)

	def __str__(self):
		s = f"{self.id} | {self.create_date.strftime("%Y-%m-%d %H:%M:%S")} | {self.text}"
		if self.tags:
			s += f" ({', '.join(self.tags)})"
		return s