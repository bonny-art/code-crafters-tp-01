"""
This module provides functions to manage notes using NoteBook, Note,
Name, and Phone classes.

Functions:
- add_note(args: List[str], note_book: NoteBook) -> str:
  Adds a new note with the given name and phone number to the Note book.

Usage:
This module can be imported and used in other Python scripts to manage a collection
of notes. Each function handles specific operations related to adding, updating,
and retrieving note information.
"""

from typing import List
from bot.models import NoteBook, Note
from bot.cli.input_error import input_error

@input_error
def add_note(args: List[str], note_book: NoteBook) -> str:
    if len(args) < 2:
        return "Insufficient arguments. Usage: add <name> <phone>"

    name_str, phone_str = args

    note = note_book.find(name_str)

    if note:
        if note.find_phone(phone_str):
            return f"Note {name_str} already has this note."
        note.add_phone(phone_str)
        return f"Phone number added to existing note {name_str}."

    note = Note(name_str)
    note.add_phone(phone_str)
    note_book.add_note(note)
    return "Note added."

@input_error
def show_all_notes(note_book: NoteBook) -> str:
    """
    Retrieve all notes stored in the Note book.

    Parameters:
    note_book (NoteBook): The Note book containing notes.

    Returns:
    str: All notes in the Note book or a message indicating it's empty.
    """
    if not note_book.data:
        return "No notes."

    return str(note_book)

if __name__ == "__main__":
    print()

    note_list = NoteBook()

    # Test show_all
    # Should show all notes
    print(show_all_notes(note_list))
    print()

    # Test add_note
    print('Test add_note >>>')
    # Should add note successfully
    print(add_note(["John", "123456789"], note_list))
    # Should indicate note already exists
    print(add_note(["John", "987654321"], note_list))
    # Should indicate invalid arguments
    print(add_note(["John"], note_list))
    # Should indicate invalid arguments
    print(add_note([], note_list))
    print()

    # Test change_note
    print('Test change_note >>>')

    print()

    # Test show_all
    # Should show all notes
    print(show_all_notes(note_list))
    print()
