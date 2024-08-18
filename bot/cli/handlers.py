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

from bot.models.phone import Phone
from bot.models.email import Email
from bot.models.address import Address
from bot.models.birthday import Birthday

from bot.utils import print_with_newlines

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
        "close",
        "exit",
        "hello",
        "add-contact",
        "change-contact",
        "delete-contact",
        "all-contacts",
        "search-contact",
        "show-phones",
        "show-birthday",
        "birthdays",
        "add-note",
        "change-note",
        "delete-note",
        "all-notes",
        "search-note",
        "add-note-tag",
        "delete-note-tag",
        "help"
    ]

    commands_str = (
        "Available commands:\n"
        "- 'close' or 'exit':   Exit the program.\n"
        "- 'hello':             Greet the user.\n"
        "- 'add-contact':       Add a new contact. Guided by user input flow.\n"
        "                       Usage: add-contact <name>\n"
        "- 'change-contact':    Update an existing contact. Guided by user input flow.\n"
        "                       Usage: change-contact <name>\n"
        "- 'delete-contact':    Remove a contact by name.\n"
        "                       Usage: delete-contact <name>\n"
        "- 'all-contacts':      Display all contacts.\n"
        "- 'search-contact':    Display contacts that match the entered input.\n"
        "                       Usage: search-contact <input>\n"
        "- 'show-phones':       Display a contact's phone number/numbers.\n"
        "                       Usage: show-phones <name>\n"
        "- 'show-birthday':     Display a contact's birthday.\n"
        "                       Usage: show-birthday <name>\n"
        "- 'birthdays':         List upcoming birthdays."
        "                       By default, lists birthdays within 7 days.\n"
        "                       Usage: birthdays [<number_of_days>]\n"
        "- 'add-note':          Add a new note.\n"
        "                       Usage: add-note <note text>\n"
        "- 'change-note':       Update an existing note with new text.\n"
        "                       Usage: change-note <id> <new_text>\n"
        "- 'delete-note':       Remove a note by ID.\n"
        "                       Usage: delete-note <id>\n"
        "- 'all-notes':         Display all notes.\n"
        "- 'search-note':       Search for notes.\n"
        "                       Usage by text: search-note <input>\n"
        "                       Usage by tags: search-note #<tag> [#<tag2> ... #<tagN>]\n"
        "- 'add-note-tag':      Add a tag to a note.\n"
        "                       Usage: add-note-tag <id> <tag1> [<tag2> ... <tagN>]\n"
        "- 'delete-note-tag':   Remove a tag from a note.\n"
        "                       Usage: delete-note-tag <id> <tag>\n"
        "- 'help':              Display this help message.\n"
    )

    return commands, commands_str

#------------------------------------------------------------------

@input_error
def add_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Adds a new contact to the address book with the specified details.

    This method prompts the user for phone numbers, emails, addresses, and birthdays. 
    It validates the input, ensuring that each piece of information is unique within 
    the contact. If the contact already exists in the address book, the method informs 
    the user and provides instructions for updating the contact.

    Args:
        args (List[str]): A list where the first element is the contact's name.
        address_book (AddressBook): The address book instance to which the contact is added.

    Returns:
        str: A message indicating whether the contact was added successfully or if it 
             already exists.
    """
    name_str = " ".join(args)

    record = address_book.find(name_str)

    if record:
        return (
            f"Contact '{name_str}' already exists. "
            "If you want to update it, use the command: change <contact_name>."
        )

    record = Record(name_str)

    while True:
        phone_str = Prompt.ask(
            "\n[cyan]Enter phone number (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]",
            console=console
        )
        if phone_str.lower() == "n":
            break
        if not phone_str.strip():
            console.print(
                "[red]Phone number cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]"
            )
            continue
        if phone_str in [phone.value for phone in record.phones]:
            console.print(
                "[yellow]This phone number already exists in the contact.[/yellow]"
            )
            console.print(
                "[yellow]Please enter a different one.[/yellow]"
            )
            continue
        try:
            record.add_phone(phone_str)
        except ValueError as e:
            console.print(f"[red]Error adding phone number:[/red] {e}")
            continue

    while True:
        email = Prompt.ask(
            "\n[cyan]Enter email (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]",
            console=console
        )
        if email.lower() == "n":
            break
        if not email.strip():
            console.print(
                "[red]Email cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]"
            )
            continue
        if email in [email.address for email in record.emails]:
            console.print(
                "[yellow]This email already exists in the contact.[/yellow]"
            )
            console.print(
                "[yellow]Please enter a different one.[/yellow]"
            )
            continue
        try:
            record.add_email(email)
        except ValueError as e:
            console.print(f"[red]Error adding email:[/red] {e}")
            continue

    while True:
        address = Prompt.ask(
            "\n[cyan]Enter address (or '[dark_orange]n[/dark_orange]' to skip)[/cyan]",
            console=console
        )
        if address.lower() == "n":
            break
        if not address.strip():
            console.print("[red]Address cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        try:
            record.add_address(address)
            break
        except ValueError as e:
            console.print(f"[red]Error adding address:[/red] {e}")

    while True:
        birthday = Prompt.ask(
            "\n[cyan]Enter birthday (DD.MM.YYYY) "
            "(or '[dark_orange]n[/dark_orange]' to skip)[/cyan]",
            console=console
        )
        if birthday.lower() == "n":
            break
        if not birthday.strip():
            console.print("[red]Birthday cannot be empty. Enter '[cyan]n[/cyan]' to skip.[/red]")
            continue
        try:
            record.add_birthday(birthday)
            break
        except ValueError as e:
            console.print(f"[red]Error adding birthday:[/red] {e}")

    address_book.add_record(record)
    return "Contact added successfully."

#------------------------------------------------------------------

@input_error
def change_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Updates the details of an existing contact in the address book.

    This method allows users to change various fields of an existing contact, including 
    the name, phone numbers, emails, address, and birthday. It prompts the user to select 
    which field they wish to edit and provides options to edit or add new values. The 
    method also handles input validation and provides appropriate feedback if the contact 
    does not exist or if errors occur during editing.

    Args:
        args (List[str]): A list where the first element is the contact's name to be updated.
        address_book (AddressBook): The address book instance containing the contact to be updated.

    Returns:
        str: A message indicating the result of the update operation, including success or 
             errors encountered during the process.
    """
    name_str = " ".join(args)
    record = address_book.find(name_str)

    if not record:
        return f"Contact '{name_str}' not found. Please check the name."

    # Map the numbers to fields
    field_map = {
        "1": "name",
        "2": "phones",
        "3": "emails",
        "4": "address",
        "5": "birthday"
    }

    # Function to extract the underlying value from the object
    def extract_value(obj):
        if isinstance(obj, Phone):
            return obj.value
        elif isinstance(obj, Email):
            return obj.address
        elif isinstance(obj, Address):
            return obj.value
        elif isinstance(obj, Birthday):
            return obj.value.strftime("%d.%m.%Y")
        else:
            return str(obj)

    while True:
        print_with_newlines(
            address_book.show_single_contact(record),
            lines_before=0,
            lines_after=0,
            use_rich_print=False
        )
        field_to_edit = Prompt.ask(
            """[cyan]
            Which field would you like to edit?
            [green]Just enter the number next to the field.[/green]
            1: Name
            2: Phones
            3: Emails
            4: Address
            5: Birthday

            Type 'exit' to stop
            [/cyan]""",
            console=console
        )

        if field_to_edit.lower() == 'exit':
            break

        if field_to_edit not in field_map:
            console.print(
                "[red]Invalid option. "
                "Please choose a valid number or 'exit' to stop.[/red]"
            )
            continue

        selected_field = field_map[field_to_edit]

        # Show all contact information before editing
        console.print("[cyan]Current contact information:[/cyan]")
        print_with_newlines(
            address_book.show_single_contact(record),
            lines_before=0,
            lines_after=0,
            use_rich_print=False
        )

        # Handle Name Editing
        if selected_field == "name":
            while True:
                new_value = Prompt.ask("Enter the new name (or type 'back' to cancel)")
                if new_value.lower() == 'back':
                    break
                try:
                    result = record.edit_field(selected_field, None, new_value, address_book)
                    console.print(f"[green]{result}[/green]")
                    name_str = new_value  # Update the name if changed
                    break
                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}. Please try again.[/red]")

        else:
            old_value = None
            current_values = getattr(record, selected_field, None)

            # Handle fields that store lists (Phones, Emails)
            if selected_field in ["phones", "emails"]:
                extracted_values = (
                    [extract_value(value) for value in current_values]
                    if current_values else []
                )

                if not extracted_values:
                    console.print(
                        f"[yellow]No current {selected_field} found. "
                        "Switching to add mode.[/yellow]"
                    )
                    action = "add"
                else:
                    prompt_message = (
                        f"Would you like to edit an existing {selected_field[:-1]} or "
                        "add a new one? (edit/add or type 'back' to cancel)"
                    )
                    action = Prompt.ask(prompt_message, default="add").lower()

                # Handle exit action
                if action == "back":
                    continue  # Return to the field selection menu

                if action == "edit":
                    console.print(f"[cyan]Current {selected_field}:[/cyan] {extracted_values}")
                    old_value = Prompt.ask(
                        f"Enter the current {selected_field[:-1]} to be replaced "
                        "(or type 'back' to cancel)"
                    )
                    if old_value.lower() == 'back':
                        continue

                    if old_value not in extracted_values:
                        console.print(
                            f"[red]The {selected_field[:-1]} '{old_value}' "
                            "does not exist.[/red]"
                        )
                        continue

                # Editing or adding loop with exception handling
                while True:
                    if action == "add":
                        prompt_message = (
                            f"Enter the new value for {selected_field[:-1]} "
                            "(or type 'back' to cancel)"
                        )
                    else:  # Режим редагування
                        prompt_message = (
                            f"Enter the new value for {selected_field[:-1]} "
                            "(leave empty to remove or type 'back' to cancel)"
                        )

                    new_value = Prompt.ask(prompt_message, default="")
                    if new_value.lower() == 'back':
                        break

                    try:
                        if new_value.strip() == "" and old_value:
                            result = record.edit_field(selected_field, old_value, None)
                            console.print(
                                f"[green]{selected_field[:-1].capitalize()} "
                                f"'{old_value}' has been removed.[/green]"
                            )
                            break

                        # Handle duplication check
                        elif new_value.strip() != "":
                            if new_value in extracted_values:
                                console.print(
                                    f"[red]The {selected_field[:-1]} '{new_value}' "
                                    "is already in the list.[/red]"
                                )
                                continue

                            result = record.edit_field(selected_field, old_value, new_value)
                            console.print(f"[green]{result}[/green]")
                            break
                    except ValueError as e:
                        console.print(f"[red]Error: {str(e)}. Please try again.[/red]")

            # Handle fields (Address, Birthday) with exception handling
            elif selected_field in ["address", "birthday"]:
                current_value = extract_value(current_values) if current_values else None

                if current_value:
                    console.print(f"[cyan]Current {selected_field}:[/cyan] {current_value}")

                # Editing loop for Address and Birthday with exception handling
                while True:
                    new_value = Prompt.ask(
                        f"Enter the new value for {selected_field} "
                        "(this will overwrite the existing value, or type 'back' to cancel)"
                    )
                    if new_value.lower() == 'back':
                        break

                    try:
                        result = record.edit_field(selected_field, None, new_value)
                        console.print(f"[green]{result}[/green]")
                        break
                    except ValueError as e:
                        console.print(f"[red]Error: {str(e)}. Please try again.[/red]")

    return "Contact updated successfully."

#------------------------------------------------------------------

@input_error
def delete_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Deletes a contact from the address book.

    This method removes a contact based on the provided name. If the contact exists in 
    the address book, it will be deleted. If the contact does not exist, an appropriate 
    message will be returned.

    Args:
        args (List[str]): A list where the elements are parts of the contact's name to be deleted.
        address_book (AddressBook): The address book instance from which the contact will
        be deleted.

    Returns:
        str: A message indicating whether the contact was successfully deleted or not found.
    """
    if len(args) < 1:
        return "Please provide the name of the contact to delete."

    contact_name = " ".join(args)

    if contact_name in address_book:
        address_book.delete(contact_name)
        return f"Contact '{contact_name}' has been deleted."

    return f"Contact '{contact_name}' not found."

#------------------------------------------------------------------

@input_error
def show_all(address_book: AddressBook) -> str:
    """
    Retrieve a string representation of all contacts stored in the address book.

    Parameters:
    address_book (AddressBook): The address book instance containing contacts.

    Returns:
    str: A string listing all contacts in the address book. 
         Returns "No contacts." if the address book is empty.
    """
    if not address_book.data:
        return "No contacts."

    return address_book.show_all_contacts()
    # return str(address_book)

#------------------------------------------------------------------

@input_error
def search_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Search for contacts in the address book based on the provided search input.

    This function searches through all the fields of each contact in the address book
    for matches with the search input. The search input is provided as a list of strings,
    where each string is used as a search criterion. The function returns a string listing
    all contacts that match the search criteria or a message indicating no matches were found.

    Parameters:
    args (List[str]): A list of strings where each string represents a search criterion.
    address_book (AddressBook): An instance of the AddressBook class containing contacts
    to be searched.

    Returns:
    str: A string with the matching contacts, or a message indicating no matches were found.
    
    Raises:
    ValueError: If no search input is provided in the `args` list.
    """
    if len(args) == 0:
        raise ValueError("No search input provided.")

    matches = address_book.search_in_fields(args)

    if matches is None:
        return "No matches found."
    return matches

#------------------------------------------------------------------

@input_error
def show_phones(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve the phone number(s) of a contact from the address book.

    Parameters:
    args (List[str]): A list of arguments containing the name of the contact.
    address_book (AddressBook): The address book containing the contact.

    Returns:
    str: A string containing the phone number(s) of the contact if found; otherwise,
    a message indicating
    that the contact was not found or if there are insufficient arguments.
    """
    if len(args) < 1:
        return "Insufficient arguments. Usage: phone <name>"

    name_str = " ".join(args)
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    return record.show_formated_phones()

#------------------------------------------------------------------

@input_error
def show_birthday(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve the birthday of a contact from the address book.

    This function takes a list of arguments where the first argument should be
    the name of the contact whose birthday is to be retrieved. It searches for
    the contact in the provided address book and returns the contact's birthday 
    if found. If the contact is not found or if insufficient arguments are provided, 
    it returns an appropriate error message.

    Parameters:
    args (List[str]): List of arguments containing the name of the contact.
    address_book (AddressBook): The address book where the contact records are stored.

    Returns:
    str: The birthday of the contact if found, otherwise a message indicating
    the contact was not found or if the arguments are insufficient.
    """
    if len(args) < 1:
        return "Insufficient arguments. Usage: show-birthday <name>"

    name_str = " ".join(args)
    record = address_book.find(name_str)

    if not record:
        return f"No contact found with name {name_str}."

    return record.show_birthday()

#------------------------------------------------------------------

@input_error
def birthdays(args: List[str], address_book: AddressBook) -> str:
    """
    Retrieve a list of upcoming birthdays from the address book.

    Parameters:
    args (List[str]): Command-line arguments where the first argument specifies the number
    of days to look ahead for upcoming birthdays.
    address_book (AddressBook): The address book containing contacts.

    Returns:
    str: A message listing upcoming birthdays within the specified number of days, or an
    error message if arguments are incorrect, or if there are no contacts in the address book.

    Error Cases:
    - If no arguments are provided, the default is 7 days.
    - If more than one argument is provided, an error message is returned indicating too
    many arguments.
    - If the provided argument is not an integer, an error message is returned indicating
    that the number of days must be an integer.
    - If the address book is empty, a message indicating there are no contacts is returned.
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
