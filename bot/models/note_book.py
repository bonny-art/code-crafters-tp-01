"""
This module provides a NoteBook class to manage a collection of notes with text and optional tags.

Classes:
- NoteBook: A dictionary-like collection to store and manage Note objects.

Example usage:
    notebook = NoteBook()
    note = Note(
        text="This is a sample note.",
        tags=["sample", "note"]
    )
    notebook.add_note(note)
    print(notebook)
"""

from collections import UserDict
from typing import List
from io import StringIO

from rich.table import Table
from rich.console import Console

from .note import Note

class NoteBook(UserDict):
    """
    A dictionary-like collection to store and manage Note objects.

    Methods:
    - add_note: Adds a new note to the notebook.
    - change_note: Changes the text of an existing note.
    - delete_note: Deletes a note from the notebook.
    - search_notes: Searches for notes by keyword or tag.
    - add_tag: Adds tags to a note.
    - delete_tag: Deletes tags from a note.
    - search_by_tag: Searches for notes by a specific tag.
    - sort_by_tag: Sorts notes by their tags.
    - notes_to_table: Converts notes to a formatted table string.
    - __str__: Returns a string representation of all notes.
    """

    def add_note(self, note: Note):
        """
        Adds a new note to the notebook.

        Args:
        - note (Note): The note to be added.
        """
        self.data[note.id] = note

    def change_note(self, index, new_text):
        """
        Changes the text of an existing note.

        Args:
        - index (str): The ID of the note to be changed.
        - new_text (str): The new text for the note.
        """
        self.data[index].text = new_text

    def delete_note(self, index):
        """
        Deletes a note from the notebook.

        Args:
        - index (str): The ID of the note to be deleted.
        """
        del self.data[index]

    def search_notes(self, keyword):
        """
        Searches for notes by keyword or tag.

        Args:
        - keyword (str): The keyword or tag to search for.

        Returns:
        - str: A formatted table string of the found notes or a message if no notes are found.
        """
        if not keyword:
            return (
                "Provide at least one search word or tag! "
                "Usage by text: search-note <input> "
                "Usage by tags: search-note #<tag> [#<tag2> ... #<tagN>]"
            )

        if not self.data:
            return "No notes found."

        data = []

        if "#" in keyword:
            keys = [k for k in keyword.split(" ") if "#" in k]
            data = [note for note in self.data.values() if any(key in note.tags for key in keys)]
            data = sorted(data, key=lambda note: note.tags)
            if not data:
                return "No notes found."
            return self.notes_to_table(f"Found Notes by Tag '{' '.join(keys)}'", data)

        data = [note for note in self.data.values() if keyword in note.text]
        if not data:
            return "No notes found."
        return self.notes_to_table(f"Found Notes by Keyword '{keyword}'", data)

    def add_tag(self, note_id: str, tags: List[str]):
        """
        Adds tags to a note.

        Args:
        - note_id (str): The ID of the note.
        - tags (List[str]): A list of tags to be added.
        """
        note = self.data[note_id]
        for tag in tags:
            if tag in note.tags:
                continue
            if "#" not in tag:
                tag = f"#{tag}"
            note.tags.append(tag)

    def delete_tag(self, note_id: str, tags: List[str]):
        """
        Deletes tags from a note.

        Args:
        - note_id (str): The ID of the note.
        - tags (List[str]): A list of tags to be deleted.
        """
        note = self.data[note_id]
        for tag in tags:
            if tag in note.tags:
                continue
            if "#" not in tag:
                tag = f"#{tag}"
            note.tags.remove(tag)

    def search_by_tag(self, tag):
        """
        Searches for notes by a specific tag.

        Args:
        - tag (str): The tag to search for.

        Returns:
        - List[Note]: A list of notes that contain the tag.
        """
        return [note for note in self.data.values() if tag in note.tags]

    def sort_by_tag(self):
        """
        Sorts notes by their tags.

        Returns:
        - List[Note]: A list of notes sorted by their tags.
        """
        return sorted(self.data.values(), key=lambda note: note.tags)

    def notes_to_table(self, title: str, notes: List[Note]) -> str:
        """
        Converts notes to a formatted table string.

        Args:
        - title (str): The title of the table.
        - notes (List[Note]): A list of notes to be included in the table.

        Returns:
        - str: A formatted table string of the notes.
        """
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
        table.add_column("Text", style="dark_orange", justify="left", no_wrap=False)
        table.add_column("Tags", style="green", justify="left", width=15, no_wrap=False)

        for n in notes:
            table.add_row(
                str(n.id),
                n.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                str(n.text),
                " ".join(n.tags)
            )
        console = Console()
        with StringIO() as buf:
            console.file = buf
            console.print(table)
            table_output = buf.getvalue()
        return table_output

    def __str__(self) -> str:
        """
        Returns a string representation of all notes.

        Returns:
        - str: A formatted table string of all notes or a message if no notes are found.
        """
        if not self.data:
            return "No notes."
        return self.notes_to_table("All Notes", [note for note in self.data.values()])
