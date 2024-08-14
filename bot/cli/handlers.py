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

- search(args: List[str], address_book: AddressBook) -> str:
  Searchs through contacts fields stored in the address book.

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
        "- 'search':            Display contacts that starts with entered input.\n"
        "                       Usage: search <input>\n"
        "- 'delete':            Delete contact by name.\n"
        "- 'close' or 'exit':   Exit the program.\n"
        "- 'add-email':         Add an email to an existing contact. Usage: add-email <name> <email>\n"  
        "- 'edit-email':        Edit an existing email for a contact. Usage: edit-email <name> <old_email> <new_email>\n" 
        

    )

#------------------------------------------------------------------

@input_error
def add_email_to_contacts(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 2:
        return "Wrong arguments! Use command: add-email: <name> <email>"
    
    name_str, email_str = args
    record = address_book.find(name_str)
    if not record:
        return f"No contact found with name {name_str}"
    try:
        record.add_email(email_str)
        return f"Email '{email_str}' added to contact '{name_str}'."
    except ValueError as e:
        return str(e)
    
@input_error
def edit_contact_email(args: List[str], address_book: AddressBook) -> str:
    """
    Edit an existing email address of a contact in the address book.

    Parameters:
    args (List[str]): List of arguments containing name, old email address, and new email address.
    address_book (AddressBook): The address book where the contact exists.

    Returns:
    str: Success or error message indicating whether the email was updated
    successfully, or if it was not found, or if the old email address was not found.
    """
    if len(args) < 3:
        return "Insufficient arguments. Usage: edit-email <name> <old_email> <new_email>"

    name_str, old_email_str, new_email_str = args
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    if not record.find_email(old_email_str):
        return f"No email address {old_email_str} found for contact {name_str}."

    try:
        record.edit_email(old_email_str, new_email_str)
        return f"Email address updated for contact {name_str}."
    except ValueError as e:
        return str(e)

@input_error
def remove_email_from_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Remove an email address from a contact in the address book.

    Parameters:
    args (List[str]): List of arguments containing the name and the email address to remove.
    address_book (AddressBook): The address book where the contact exists.

    Returns:
    str: Success or error message indicating whether the email was removed
    successfully, or if the contact or email address was not found.
    """
    if len(args) < 2:
        return "Insufficient arguments. Usage: remove-email <name> <email>"

    name_str, email_str = args
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    if not record.find_email(email_str):
        return f"No email address {email_str} found for contact {name_str}."

    record.remove_email(email_str)
    return f"Email address '{email_str}' removed from contact '{name_str}'."


@input_error
def add_address_to_contact(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 2:
        return "Insufficient arguments. Usage: add-address <name> <address>"
    
    name_str = args[0]
    address_str = ' '.join(args[1:])

    name_str, address_str = args
    record = address_book.find(name_str)
    
    if not record:
        return f"No contact found with name {name_str}."
    
    try:
        record.add_address(address_str)
        return f"Address '{address_str}' added to contact '{name_str}'."
    except ValueError as e:
        return str(e)

@input_error
def edit_contact_address(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 2:
        return "Insufficient arguments. Usage: edit-address <name> <new_address>"
    
    name_str, new_address_str = args
    record = address_book.find(name_str)
    
    if not record:
        return f"No contact found with name {name_str}."
    
    try:
        record.edit_address(new_address_str)
        return f"Address updated for contact {name_str}."
    except ValueError as e:
        return str(e)





#------------------------------------------------------------------
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

@input_error
def search(args: List[str], address_book: AddressBook) -> str:
    """
    Search in all the fields of each contacts stored in the address book.

    Parameters:
    args (List[str]): List of arguments containing the input.
    address_book (AddressBook): The address book containing contacts.

    Returns:
    str: All contacts that matche the passed input or a message indicating it's empty.
    """
    input = args[0]
    matches = address_book.search_in_fields(input.lower())
    if not matches:
        return "No matches found."
    return str(matches)
