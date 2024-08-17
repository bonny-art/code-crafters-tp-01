"""
This module provides functions to save and load an AddressBook object using
the pickle library.

Functions:
- save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
  Saves the AddressBook object to a file using pickle.
- load_data(filename: str = "addressbook.pkl") -> AddressBook:
  Loads the AddressBook object from a file using pickle.

Usage:
This module can be imported and used in other Python scripts to persist and retrieve
AddressBook objects. Each function handles specific operations related to saving and loading
the AddressBook data.
"""

import pickle
import os

from bot.models.address_book import AddressBook

file_path = os.path.abspath("tmp/addressbook.pkl")

def save_data(book: AddressBook, filename: str = file_path) -> None:
    """
    Saves the AddressBook object to a file using pickle.

    Args:
    - book (AddressBook): The AddressBook object to be saved.
    - filename (str): The name of the file to save the object to. Defaults to "addressbook.pkl".

    Returns:
    - None: This function does not return a value.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(book, f)
    except OSError as os_error:
        print(f"An error occurred while accessing the file system: {os_error}")
    except pickle.PickleError as pickle_error:
        print(f"An error occurred while pickling the data: {pickle_error}")


def load_data(filename: str = file_path) -> AddressBook:
    """
    Loads the AddressBook object from a file using pickle.

    Args:
    - filename (str): The name of the file to load the object from. Defaults to "addressbook.pkl".

    Returns:
    - AddressBook: The loaded AddressBook object. If the file is not
    found, a new AddressBook object is created.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    except OSError as os_error:
        print(f"An error occurred while accessing the file system: {os_error}")
    except pickle.PickleError as pickle_error:
        print(f"An error occurred while unpickling the data: {pickle_error}")
