"""
This module provides the main function to run an assistant bot for managing contacts.

The assistant bot supports the following commands:
- 'close' or 'exit': Exit the program.
- 'hello': Greet the user.
- 'add-contact': Add a new contact.
- 'change-contact': Update an existing contact.
- 'delete-contact': Remove a contact.
- 'all-contacts': Display all contacts.
- 'search-contact': Search for contacts.
- 'show-phones': Display a contact's phone numbers.
- 'show-birthday': Show a contact's birthday.
- 'birthdays': List upcoming birthdays.
- 'add-note': Add a new note.
- 'change-note': Update an existing note.
- 'delete-note': Remove a note.
- 'all-notes': Display all notes.
- 'search-note': Search for notes.
- 'add-note-tag': Add a tag to a note.
- 'delete-note-tag': Remove a tag from a note.
- 'help': Display all available commands.

Imports:
- List from typing: Used for type annotations.
- handlers from bot.cli: Contains functions to handle various contact management commands.
- AddressBook from bot.models: Represents a collection of contact records.
- parse_input from bot.cli.parse_input: Parses user input into commands and arguments.

Functions:
- main: The entry point of the assistant bot, which continuously prompts the user
for commands and processes them accordingly.

Usage:
- Run the module as a script to start the assistant bot.
- The bot will prompt the user for commands and manage the contact records in the AddressBook.

Example:
    Run the script:
        $ python module_name.py
    Interact with the bot using the supported commands.

Main Function:
- main: Initializes the AddressBook and enters an infinite loop to handle user commands
until 'close' or 'exit' is entered.

if __name__ == "__main__":
    main()

The above block ensures that the main function runs only when the module is executed
as a script, not when it is imported as a module.
"""

from typing import List

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import CompleteStyle

from bot.cli import handlers
from bot.cli.data_manager import load_data, save_data
from bot.cli.parse_input import parse_input
from bot.cli.commands_completer import completer, history
from bot.cli import note_handlers
from bot.cli.note_data_manager import load_data as note_load_data, save_data as note_save_data

from bot.utils import print_with_newlines

def main() -> None:
    """
    Runs the assistant bot for managing contacts.

    The function continuously prompts the user for commands and processes them accordingly:
    - 'close' or 'exit' to exit the program
    - 'hello' to greet the user
    - 'add-contact' to add a contact
    - 'change-contact' to update a contact
    - 'delete-contact' to remove a contact
    - 'all-contacts' to display all contacts
    - 'search-contact' to search for contacts
    - 'show-phones' to display a contact's phone numbers
    - 'show-birthday' to show a contact's birthday
    - 'birthdays' to list upcoming birthdays
    - 'add-note' to add a note
    - 'change-note' to update a note
    - 'delete-note' to remove a note
    - 'all-notes' to display all notes
    - 'search-note' to search for notes
    - 'add-note-tag' to add a tag to a note
    - 'delete-note-tag' to remove a tag from a note
    - 'help' to display available commands

    Uses handlers from the 'handlers' module for contact and note management.

    Returns:
    None
    """
    address_book = load_data()
    note_list = note_load_data()

    logo = ""
    with open("logo.txt", "r") as file:
        logo = file.read()

    print_with_newlines(f"[blue]{logo}")
    print_with_newlines("Welcome to the assistant bot!")
    print_with_newlines("Type 'help' to see a list of available commands.", lines_before=0)

    while True:
        user_input: str = prompt(
            "Enter a command: ",
            completer=completer,
            complete_style=CompleteStyle.COLUMN,
            history=history
        )

        if not user_input:
            continue

        command: str
        args: List[str]
        command, *args = parse_input(user_input)

        #------------------------------------------------------------------
        # Command group: Core Commands
        #------------------------------------------------------------------

        if command in ["close", "exit"]:
            save_data(address_book)
            note_save_data(note_list)
            print_with_newlines("Good bye!")
            break

        if command == "help":
            _, commands_str = handlers.show_help()
            print_with_newlines(commands_str)

        elif command == "hello":
            print_with_newlines("How can I help you?")

        #------------------------------------------------------------------
        # Command group: Contact Management
        #------------------------------------------------------------------

        elif command == "add-contact":
            print_with_newlines(handlers.add_contact(args, address_book))

        elif command == "change-contact":
            print_with_newlines(handlers.change_contact(args, address_book))

        elif command == "delete-contact":
            print_with_newlines(handlers.delete_contact(args, address_book))

        elif command == "all-contacts":
            print_with_newlines(handlers.show_all(address_book), use_rich_print=False)

        elif command == "search-contact":
            print_with_newlines(handlers.search_contact(args, address_book))

        elif command == "show-phones":
            print_with_newlines(handlers.show_phones(args, address_book))

        elif command == "show-birthday":
            print_with_newlines(handlers.show_birthday(args, address_book))

        elif command == "birthdays":
            print_with_newlines(handlers.birthdays(args, address_book), use_rich_print=False)

        #------------------------------------------------------------------
        # Command group: Note Management
        #------------------------------------------------------------------

        elif command == "add-note":
            print_with_newlines(note_handlers.add_note(args, note_list))

        elif command == "change-note":
            print_with_newlines(note_handlers.change_note(args, note_list))

        elif command == "delete-note":
            print_with_newlines(note_handlers.delete_note(args, note_list))

        elif command == "all-notes":
            print_with_newlines(note_handlers.show_all_notes(note_list), use_rich_print=False)

        elif command == "search-note":
            print_with_newlines(note_handlers.search_note(args, note_list), use_rich_print=False)

        elif command == "add-note-tag":
            print_with_newlines(note_handlers.add_note_tag(args, note_list))

        elif command == "delete-note-tag":
            print_with_newlines(note_handlers.delete_note_tag(args, note_list))

        else:
            print_with_newlines("Invalid command.")

if __name__ == "__main__":
    main()
