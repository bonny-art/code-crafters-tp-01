"""
This module provides functions to save and load a NoteBook object using
the pickle library.

Functions:
- save_data(book: NoteBook, filename: str = "notebook.pkl") -> None:
  Saves the NoteBook object to a file using pickle.
- load_data(filename: str = "notebook.pkl") -> NoteBook:
  Loads the NoteBook object from a file using pickle.

Usage:
This module can be imported and used in other Python scripts to persist and retrieve
NoteBook objects. Each function handles specific operations related to saving and loading
the NoteBook data.
"""

import pickle
import os

from bot.models.note_book import NoteBook

file_path = os.path.abspath("tmp/notebook.pkl")

def save_data(book: NoteBook, filename: str = file_path) -> None:
    """
    Saves the NoteBook object to a file using pickle.

    Args:
    - book (NoteBook): The NoteBook object to be saved.
    - filename (str): The name of the file to save the object to. Defaults to "notebook.pkl".

    Returns:
    - None: This function does not return a value.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: str = file_path) -> NoteBook:
    """
    Loads the NoteBook object from a file using pickle.

    Args:
    - filename (str): The name of the file to load the object from. Defaults to "notebook.pkl".

    Returns:
    - NoteBook: The loaded NoteBook object. If the file is not found,
    a new NoteBook object is created.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()
