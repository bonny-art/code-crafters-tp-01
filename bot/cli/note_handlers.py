"""
This module provides functions to manage notes using NoteBook and Note classes.

Functions:
- add_note(args: List[str], note_book: NoteBook) -> str:
  Adds a new note with the given text to the NoteBook.
- delete_note(args: List[str], note_book: NoteBook) -> str:
  Deletes a note from the NoteBook by its ID.
- change_note(args: List[str], note_book: NoteBook) -> str:
  Changes the text of an existing note in the NoteBook.
- show_all_notes(note_book: NoteBook) -> str:
  Retrieves all notes stored in the NoteBook.
- search_note(args: List[str], note_book: NoteBook) -> str:
  Searches for notes in the NoteBook by keyword.
- add_note_tag(args: List[str], note_book: NoteBook) -> str:
  Adds tags to a note in the NoteBook.
- delete_note_tag(args: List[str], note_book: NoteBook) -> str:
  Deletes tags from a note in the NoteBook.

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
    """
    Adds a new note with the given text to the NoteBook.

    Args:
    - args (List[str]): The text of the note.
    - note_book (NoteBook): The NoteBook to add the note to.

    Returns:
    - str: A message indicating the note was added.
    """
    if len(args) == 0:
        raise ValueError("No note text provided. Usage: add-note <note text>")
    note = Note(" ".join(args))
    note_book.add_note(note)
    return "Note added."

@input_error
def delete_note(args: List[str], note_book: NoteBook) -> str:
    """
    Deletes a note from the NoteBook by its ID.

    Args:
    - args (List[str]): The ID of the note to be deleted.
    - note_book (NoteBook): The NoteBook to delete the note from.

    Returns:
    - str: A message indicating the note was deleted.
    """
    if len(args) == 0:
        raise ValueError("No note ID provided. Usage: delete-note <id>")
    if len(args) > 1:
        raise ValueError("More than one note ID provided. Usage: delete-note <id>")
    note_book.delete_note(args[0])
    return "Note deleted."

@input_error
def change_note(args: List[str], note_book: NoteBook) -> str:
    """
    Changes the text of an existing note in the NoteBook.

    Args:
    - args (List[str]): The ID of the note and the new text.
    - note_book (NoteBook): The NoteBook containing the note.

    Returns:
    - str: A message indicating the note was changed.
    """
    if len(args) == 0:
        raise ValueError("No note ID provided. Usage: change-note <id> <new_text>")
    if len(args) == 1:
        raise ValueError("No text provided. Usage: change-note <id> <new_text>")
    note_id = args[0]
    text = " ".join(args[1:])
    note_book.change_note(note_id, text)
    return "Note changed."

@input_error
def show_all_notes(note_book: NoteBook) -> str:
    """
    Retrieves all notes stored in the NoteBook.

    Args:
    - note_book (NoteBook): The NoteBook containing notes.

    Returns:
    - str: All notes in the NoteBook or a message indicating it's empty.
    """
    if not note_book.data:
        return "No notes."
    return str(note_book)

@input_error
def search_note(args: List[str], note_book: NoteBook) -> str:
    """
    Searches for notes in the NoteBook by keyword.

    Args:
    - args (List[str]): The keyword to search for.
    - note_book (NoteBook): The NoteBook to search in.

    Returns:
    - str: A formatted table string of the found notes or a message if no notes are found.
    """
    search = " ".join(args)
    return note_book.search_notes(search)

@input_error
def add_note_tag(args: List[str], note_book: NoteBook) -> str:
    """
    Adds tags to a note in the NoteBook.

    Args:
    - args (List[str]): The ID of the note and the tags to be added.
    - note_book (NoteBook): The NoteBook containing the note.

    Returns:
    - str: A message indicating the tags were added.
    """
    if len(args) == 0:
        raise ValueError(
            "No note ID and tag provided. "
            "Usage: add-note-tag <id> <tag1> [<tag2> ... <tagN>]"
        )
    if len(args) == 1:
        raise ValueError("No tag provided. Usage: add-note-tag <id> <tag1> [<tag2> ... <tagN>]")
    note_id = args[0]
    tags = args[1:]
    note_book.add_tag(note_id, tags)
    return "Tag added."

@input_error
def delete_note_tag(args: List[str], note_book: NoteBook) -> str:
    """
    Deletes tags from a note in the NoteBook.

    Args:
    - args (List[str]): The ID of the note and the tags to be deleted.
    - note_book (NoteBook): The NoteBook containing the note.

    Returns:
    - str: A message indicating the tags were deleted.
    """
    if len(args) == 0:
        raise ValueError("No note ID and tag provided. delete-note-tag <id> <tag>")
    if len(args) == 1:
        raise ValueError("No tag provided. delete-note-tag <id> <tag>")
    note_id = args[0]
    tags = args[1:]
    note_book.delete_tag(note_id, tags)
    return "Tag deleted."
