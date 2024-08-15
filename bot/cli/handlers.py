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

from rich.prompt import Prompt
from rich.console import Console

from bot.models import AddressBook, Record
from bot.cli.input_error import input_error


console = Console()

def show_help() -> tuple:
    """
    Returns a list of available commands and a formatted string for displaying them.

    Returns:
    tuple: A tuple containing:
        - A list of command strings.
        - A formatted string listing all commands with descriptions.
    """
    commands = [
        "hello: Greet the user.",
        "help: Display this help message.",
        "add: Add a new contact with phone or a phone to existing contact. Usage: add <name> <phone>",
        "change: Update an existing field with a new value, guided by user input flow.",
        "phone: Display a contact's phone number/numbers. Usage: phone <name>",
        "show-birthday: Display a contact's birthday. Usage: show-birthday <name>",
        "birthdays: Display upcoming birthdays within 7 days.",
        "all: Display all contacts.",
        "search: Display contacts that start with the entered input. Usage: search <input>",
        "delete: Delete contact by name.",
        "close or exit: Exit the program.",
        "add-email: Add an email to an existing contact. Usage: add-email <name> <email>",
        "edit-email: Edit an existing email for a contact. Usage: edit-email <name> <old_email> <new_email>"
    ]

    commands_str = (
        "Available commands:\n"
        "- 'hello':             Greet the user.\n"
        "- 'help':              Display this help message.\n"
        "- 'add':               Add a new contact with phone or a phone to existing contact.\n"
        "                       Usage: add <name> <phone>\n"
        "- 'change':            Update an existing field with a new value through a guided process.\n"
        "- 'phone':             Display a contact's phone number/numbers. Usage: phone <name>\n"
        "- 'show-birthday':     Display a contact's birthday. Usage: show-birthday <name>\n"
        "- 'birthdays':         Display upcoming birthdays within 7 days.\n"
        "- 'all':               Display all contacts.\n"
        "- 'search':            Display contacts that start with the entered input.\n"
        "                       Usage: search <input>\n"
        "- 'delete':            Delete contact by name.\n"
        "- 'close' or 'exit':   Exit the program.\n"
        "- 'add-email':         Add an email to an existing contact."
        "                       Usage: add-email <name> <email>\n"  
        "- 'edit-email':        Edit an existing email for a contact."
        "                       Usage: edit-email <name> <old_email> <new_email>\n" 
        "- 'all-notes':         Display all notes.\n"        
        "- 'add-note':          Add a new note\n"
        "                       Usage: add-note <note text>\n"
        "- 'search-note':       Display notes that contains input.\n"
        "                       Usage by text: search-note <input>\n"
        "                       Usage by tags: search-note #<tag> #<tag2>\n"    
        "                       Usage by tags example: search-note #fire #quotation #art\n"             
        "- 'delete-note':       Delete note by Id.\n"
        "                       Usage: delete-note <id>\n"
        "- 'change-note':       Update an existing note with new text.\n"
        "                       Usage: change-note <id> <new_text>\n"
        "- 'add-note-tag':      Add new note tag by Id and tag name.\n"
        "                       Usage: add-note-tag <id> <tag>\n"
        "- 'delete-note-tag':   Delete an existing note tag\n"
        "                       Usage: delete-note-tag <id> <tag>\n"
    )
    
    return commands, commands_str


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
    Add a new contact to the address book with a name and prompt for additional details.

    Parameters:
    args (List[str]): List of arguments containing parts of the name.
    address_book (AddressBook): The address book where the contact will be added.

    Returns:
    str: Success or error message indicating the result of the operation.
    """
    # Об'єднання всіх аргументів в одне ім'я
    name_str = " ".join(args)

    record = address_book.find(name_str)

    if record:
        return f"Contact '{name_str}' already exists. If you want to update it, use the command: change <contact_name>."

    # Створення нового запису
    record = Record(name_str)

    # Введення телефонних номерів
    while True:
        phone_str = Prompt.ask("\n[cyan]Enter phone number (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]", console=console)
        if phone_str.lower() == "n":
            break
        if not phone_str.strip():  # Перевірка на порожній рядок
            console.print("[red]Phone number cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        if phone_str in [phone.value for phone in record.phones]:
            console.print("[yellow]This phone number already exists in the contact. Please enter a different one.[/yellow]")
            continue
        try:
            record.add_phone(phone_str)
        except ValueError as e:
            console.print(f"[red]Error adding phone number:[/red] {e}")
            continue

    # Введення електронних адрес з повторним запитом у разі помилки
    while True:
        email = Prompt.ask("\n[cyan]Enter email (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]", console=console)
        if email.lower() == "n":
            break
        if not email.strip():  # Перевірка на порожній рядок
            console.print("[red]Email cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        if email in [email.address for email in record.emails]:
            console.print("[yellow]This email already exists in the contact. Please enter a different one.[/yellow]")
            continue
        try:
            record.add_email(email)
        except ValueError as e:
            console.print(f"[red]Error adding email:[/red] {e}")
            continue

    # Введення адреси з повторним запитом у разі помилки
    while True:
        address = Prompt.ask("\n[cyan]Enter address (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]", console=console)
        if address.lower() == "n":
            break
        if not address.strip():  # Перевірка на порожній рядок
            console.print("[red]Address cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        try:
            record.add_address(address)
            break
        except ValueError as e:
            console.print(f"[red]Error adding address:[/red] {e}")

    # Введення дня народження з повторним запитом у разі помилки
    while True:
        birthday = Prompt.ask("\n[cyan]Enter birthday (DD.MM.YYYY) (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]", console=console)
        if birthday.lower() == "n":
            break
        if not birthday.strip():  # Перевірка на порожній рядок
            console.print("[red]Birthday cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        try:
            record.add_birthday(birthday)
            break  # Вихід з циклу, якщо введення успішне
        except ValueError as e:
            console.print(f"[red]Error adding birthday:[/red] {e}")

    # Додавання запису до адресної книги
    address_book.add_record(record)
    return "Contact added successfully."


@input_error
def change_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Change the details of an existing contact in the address book.

    Parameters:
    args (List[str]): List of arguments containing parts of the name.
    address_book (AddressBook): The address book where the contact will be updated.

    Returns:
    str: Success or error message indicating the result of the operation.
    """
    name_str = " ".join(args)

    record = address_book.find(name_str)

    if not record:
        return f"Contact '{name_str}' not found. Please check the name."

    while True:
        field_to_edit = Prompt.ask(
            "[cyan]Which field would you like to edit? (name, phones, emails, address, birthday, 'exit' to stop)[/cyan]",
            console=console
        )

        if field_to_edit.lower() == 'exit':
            break

        if field_to_edit.lower() in ["name", "phones", "emails", "address", "birthday"]:
            old_value = None
            if field_to_edit in ["phones", "emails"]:
                should_edit_existing = Prompt.ask(
                    f"Would you like to edit an existing {field_to_edit[:-1]} or add a new one? (edit/add)", 
                    default="add"
                ).lower()
                
                if should_edit_existing == "edit":
                    old_value = Prompt.ask(f"Enter the current {field_to_edit[:-1]} to be replaced")

            new_value = Prompt.ask(f"Enter the new value for {field_to_edit} (or leave empty to remove)", default="")

            if new_value.strip() == "" and old_value:
                result = record.edit_field(field_to_edit, old_value, None)
                console.print(f"[green]The {field_to_edit[:-1]} '{old_value}' has been removed.[/green]")
            elif new_value.strip() != "":
                result = record.edit_field(field_to_edit, old_value, new_value)
                console.print(f"[green]{result}[/green]")
            else:
                console.print(f"[yellow]No action taken.[/yellow]")
        else:
            console.print("[red]Invalid option. Please enter 'name', 'phones', 'emails', 'address', 'birthday', or 'exit' to stop.")

    return "Contact updated successfully."

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
    search_term = args[0]
    matches = address_book.search_in_fields(search_term.lower())

    if not matches:
        return "No matches found."
    return str(matches)
