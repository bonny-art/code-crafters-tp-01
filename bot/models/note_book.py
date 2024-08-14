from note import Note
from datetime import datetime

class NoteBook:
	def __init__(self):
		self.notes = []

	def add_note(self, text, tags=None):
		note = Note(text, tags)
		self.notes.append(note)

	def edit_note(self, index, new_text):
		if 0 <= index < len(self.notes):
			self.notes[index].text = new_text

	def delete_note (self, index):
		if 0 <= index < len(self.notes):
			del self.notes[index]

	def search_notes(self, keyword):
		return [note for note in self.notes if keyword in note.text]

	def search_by_tag(self, tag):
		return [note for note in self.notes if tag in note.tags]

	def sort_by_tag(self):
		return sorted(self.notes, key=lambda note: note.tags)

# Example usage
if __name__ == "__main__":
	manager = NoteBook()
	manager.add_note("First note", ["work"])
	manager.add_note("Second note", ["personal"])
	manager.add_note("Third note", ["work", "urgent"])

	print("All notes:")
	for note in manager.notes:
		print(note.id, note.create_date, note.text, note.tags)

	print("\nSearch for 'work' tag:")
	for note in manager.search_by_tag("work"):
		print(note.id, note.create_date, note.text, note.tags)

	print("\nSearch for 'Second' note:")
	for note in manager.search_notes("Second"):
		print(note.id, note.create_date, note.text, note.tags)

	print("\nSort by tag:")
	for note in manager.sort_by_tag():
		print(note.id, note.create_date, note.text, note.tags)