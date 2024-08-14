"""
This module provides functions to manage contacts using AddressBook, Record,
Name, and Phone classes.

Functions:
- add_contact(args: List[str], address_book: AddressBook) -> str:
  Adds a new contact with the given name and phone number to the address book.

- change_contact(args: List[str], address_book: AddressBook) -> str:
  Updates the phone number of an existing contact in the address book.

- show_phone(args: List[str], address_book: AddressBook) -> str:
  Retrieves the phone number of a contact from the address book.

- show_all(address_book: AddressBook) -> str:
  Retrieves all contacts stored in the address book.

- add_birthday(args: List[str], address_book: AddressBook) -> str:
  Adds a birthday to a contact or creates a new contact with the birthday.

- show_birthday(args: List[str], address_book: AddressBook) -> str:
  Retrieves the birthday of a contact from the address book.

- birthdays(address_book: AddressBook) -> str:
  Retrieves a list of upcoming birthdays from the address book.

Usage:
This module can be imported and used in other Python scripts to manage a collection
of contacts. Each function handles specific operations related to adding, updating,
and retrieving contact information.
"""

from typing import List
from bot.models import AddressBook, Record
from bot.cli.input_error import input_error

def show_help() -> None:
    """
    Displays a list of available commands for the assistant bot.

    Returns:
    None
    """
    return (
        "Available commands:\n"
        "- 'hello':             Greet the user.\n"
        "- 'help':              Display this help message.\n"
        "- 'add':               Add a new contact with phone or a phone to existing contact.\n"
        "                       Usage: add <name> <phone>\n"
        "- 'add-birthday':      Add a new contact with birthday or a birthday to a contact.\n"
        "                       Usage: add-birthday <name> <birthday>\n"
        "- 'change':            Update an existing field with new value. Usage: change <contact_name> <field name> <old_value> <new_value>\n"
        "                       Usage: change <name> <old_phone> <new_phone>\n"
        "- 'phone':             Display a contact's phone number/numbers. Usage: phone <name>\n"
        "- 'show-birthday':     Display a contact's birthday. Usage: show-birthday <name>\n"
        "- 'birthdays':         Display upcoming birthdays within 7 days.\n"
        "- 'all':               Display all contacts.\n"
        "- 'delete':            Delete contact by name.\n"
        "- 'close' or 'exit':   Exit the program.\n"
    )

@input_error
def add_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Add a new contact with the given name and phone number to the address book.

    Parameters:
    args (List[str]): List of arguments containing name and phone number.
    address_book (AddressBook): The address book where the contact will be added.

    Returns:
    str: Success or error message indicating whether the contact was added successfully
    or if the phone number already exists for the contact.
    """
    if len(args) < 2:
        return "Insufficient arguments. Usage: add <name> <phone>"

    name_str, phone_str = args

    record = address_book.find(name_str)

    if record:
        if record.find_phone(phone_str):
            return f"Contact {name_str} already has this phone number."
        record.add_phone(phone_str)
        return f"Phone number added to existing contact {name_str}."

    record = Record(name_str)
    record.add_phone(phone_str)
    address_book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args: List[str], address_book: AddressBook) -> str:
    """
 Edits a contact's information in the address book.

    Parameters:
    args (List[str]): List of arguments containing the contact name, the field to edit 
                      (e.g., 'name', 'phone', 'birthday'), and the new value.
    address_book (AddressBook): The address book where the contact exists.

    Returns:
    str: Success or error message indicating whether the contact was updated successfully,
         or if the contact was not found, or if the specified field is unknown.
    """
    if len(args) < 3:
        return "Usage: edit <name> <field> <new_value>"

    contact_name, field, old_value, new_value = args[0], args[1], args[2], args[3]
    
    if contact_name not in address_book:
        return f"Contact '{contact_name}' not found."
    
    record = address_book[contact_name]
    result = record.edit_field(field, old_value, new_value)
    
    if field == 'name':
        # Handle renaming by updating the key in the address book
        address_book[new_value] = record
        del address_book[contact_name]
    
    return result

@input_error
def delete_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Deletes a contact from the address book.

    Args:
        args: List containing the contact name to delete.
        address_book: The AddressBook instance to delete the contact from.

    Returns:
        str: A message indicating the result of the deletion.
    """
    if len(args) < 1:
        return "Please provide the name of the contact to delete."
    
    contact_name = args[0]
    
    if contact_name in address_book:
        address_book.delete(contact_name)
        return f"Contact '{contact_name}' has been deleted."
    else:
        return f"Contact '{contact_name}' not found."

@input_error
def show_phone(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve the phone number(s) of a contact from the address book.

    Parameters:
    args (List[str]): List of arguments containing the name of the contact.
    address_book (AddressBook): The address book where the contact exists.

    Returns:
    str: Phone number(s) of the contact if found, otherwise a message indicating
    the contact was not found.
    """
    if len(args) != 1:
        return "Insufficient arguments. Usage: phone <name>"

    name_str = args[0]
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    return str(record)

@input_error
def show_all(address_book: AddressBook) -> str:
    """
    Retrieve all contacts stored in the address book.

    Parameters:
    address_book (AddressBook): The address book containing contacts.

    Returns:
    str: All contacts in the address book or a message indicating it's empty.
    """
    if not address_book.data:
        return "No contacts."

    return str(address_book)

@input_error
def add_birthday(args: List[str], address_book: AddressBook) -> str:
    """
    Add a birthday to a contact or create a new contact with the birthday.

    Parameters:
    args (List[str]): List of arguments containing name and birthday.
    address_book (AddressBook): The address book where the contact will be added or updated.

    Returns:
    str: Success or error message indicating whether the birthday was added successfully
    or if there were insufficient arguments.
    """
    if len(args) < 2:
        return "Insufficient arguments. Usage: add-birthday <name> <birthday>"

    name_str, birthday_str = args

    record = address_book.find(name_str)

    if record:
        record.add_birthday(birthday_str)
        return f"Birthday added to existing contact {name_str}."

    record = Record(name_str)
    record.add_birthday(birthday_str)
    address_book.add_record(record)
    return "Contact with birthday added."


@input_error
def show_birthday(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve the birthday of a contact from the address book.

    Parameters:
    args (List[str]): List of arguments containing the name of the contact.
    address_book (AddressBook): The address book where the contact exists.

    Returns:
    str: The birthday of the contact if found, otherwise a message indicating
    the contact was not found.
    """
    if len(args) != 1:
        return "Insufficient arguments. Usage: show-birthday <name>"

    name_str = args[0]
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    return record.show_birthday()

@input_error
def birthdays(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve a list of upcoming birthdays from the address book.

    Parameters:
    address_book (AddressBook): The address book containing contacts.

    Returns:
    str: A list of upcoming birthdays or a message indicating there are no contacts.
    """
    if len(args) == 0:
        days = 7
    elif len(args) > 1:
        return "Too many arguments. Usage: show-birthday <days>"
    else:
        try:
            days = int(args[0])
        except ValueError:
            return "The number of days must be an integer. Usage: show-birthday <days>"

    if not address_book.data:
        return "No contacts."

    return address_book.get_upcoming_birthdays(days)