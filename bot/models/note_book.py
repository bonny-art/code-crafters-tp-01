from .note import Note
from datetime import datetime
from collections import UserDict
from rich.table import Table
from rich.console import Console
from typing import List
from io import StringIO

class NoteBook(UserDict):

	def add_note(self, note: Note):
		self.data[note.id] = note

	def change_note(self, index, new_text):
		self.data[index].text = new_text

	def delete_note (self, index):
		del self.data[index]

	def search_notes(self, keyword):
		if not self.data:
			return "No notes found."
		return self.notes_to_table(f"Found Notes by Keyword '{keyword}'", [note for note in self.data.values() if keyword in note.text])

	def search_by_tag(self, tag):
		return [note for note in self.data if tag in note.tags]

	def sort_by_tag(self):
		return sorted(self.data, key=lambda note: note.tags)
	
	def notes_to_table(self, title: str, notes: List[Note]) -> str:
		table = Table(
            title=f"{title}",
            title_style="bold orange1",
            border_style="gray50",
            padding=(0, 2),
            show_header=True,
            show_lines=True,
            header_style="bold cyan"
        )
		table.add_column("Id", style="green", justify="center", width=40)
		table.add_column("Creation Date", style="green", justify="center", width=30)
		table.add_column("Text", style="green", justify="left", width=60, no_wrap=False)

		for n in notes:
			table.add_row(
                            str(n.id),
                            n.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                            str(n.text)
                        )
		console = Console()
		with StringIO() as buf:
			console.file = buf
			console.print(table)
			table_output = buf.getvalue()
		return table_output
	
	
	def __str__(self) -> str:
		if not self.data:
			return "No notes."
		return self.notes_to_table("All Notes", [note for note in self.data.values()])

		# return "\n".join(str(record) for record in self.data.values())
	
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