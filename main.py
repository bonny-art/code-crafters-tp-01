"""
This module provides the main function to run an assistant bot for managing contacts.

The assistant bot supports the following commands:
- 'close' or 'exit': Exit the program.
- 'hello': Greet the user.
- 'add': Add a new contact.
- 'change': Update an existing contact.
- 'phone': Display a contact's phone number.
- 'all': Display all contacts.
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

from bot.cli import handlers
from bot.cli.data_manager import load_data, save_data
from bot.cli.parse_input import parse_input
from bot.utils import print_with_newlines
from bot.cli.commands_completer import completer, history
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import CompleteStyle


def main() -> None:
    """
    Runs the assistant bot for managing contacts.

    The function continuously prompts the user for commands and processes them accordingly:
    - 'close' or 'exit' to exit the program
    - 'hello' to greet the user
    - 'add' to add a contact
    - 'change' to update a contact
    - 'phone' to display a contact's phone number
    - 'all' to display all contacts
    - 'help' to display available commands

    Uses handlers from the 'handlers' module for contact management.

    Returns:
    None
    """
    address_book = load_data()

    print_with_newlines("Welcome to the assistant bot!")
    print_with_newlines("Type 'help' to see a list of available commands.", lines_before = 0)
    
    while True:
        user_input: str = prompt("Enter a command: ", completer=completer, complete_style=CompleteStyle.COLUMN, history=history)

        if not user_input:
            continue

        command: str
        args: List[str]
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(address_book)
            print_with_newlines("Good bye!")
            break

        if command == "help":
            _, commands_str = handlers.show_help()
            print_with_newlines(commands_str)

        elif command == "hello":
            print_with_newlines("How can I help you?")

        elif command == "add":
            print_with_newlines(handlers.add_contact(args, address_book))

        elif command == "change":
            print_with_newlines(handlers.change_contact(args, address_book))

        elif command == "phone":
            print_with_newlines(handlers.show_phone(args, address_book))

        elif command == "all":
            print_with_newlines(handlers.show_all(address_book))

        elif command == "search":
            print_with_newlines(handlers.search(args, address_book))

        elif command == "add-birthday":
            print_with_newlines(handlers.add_birthday(args, address_book))

        elif command == "show-birthday":
            print_with_newlines(handlers.show_birthday(args, address_book))

        elif command == "birthdays":
            print_with_newlines(handlers.birthdays(args, address_book))

        elif command == "delete":
            print_with_newlines(handlers.delete_contact(args, address_book))

        else:
            print_with_newlines("Invalid command.")

if __name__ == "__main__":
    main()
