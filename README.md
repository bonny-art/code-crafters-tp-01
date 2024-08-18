# Overview

Contacts Bot is a Python-based terminal application for managing your contacts efficiently. With this bot, you can add, delete, and edit contacts, as well as keep track of birthdays and additional notes for each contact. It’s an ideal tool for anyone looking to organize their contacts directly from the command line.

# Features

- hello: Greet the user.
- help: Display this help message.
- add-contact: Add a new contact. Usage: `add-contact <name>`
- change-contact: Update an existing contact. Usage: `change-contact <name>`
- delete-contact: Remove a contact by name. Usage: `delete-contact <name>`
- all-contacts: Display all contacts.
- search-contact: Display contacts that match the entered input. Usage: `search-contact <input>`
- show-phones: Display a contact's phone number(s). Usage: `show-phones <name>`
- show-birthday: Display a contact's birthday. Usage: `show-birthday <name>`
- birthdays: List upcoming birthdays. By default, lists birthdays within 7 days. Usage: `birthdays [<number_of_days>]`
- add-note: Add a new note. Usage: `add-note <note text>`
- change-note: Update an existing note with new text. Usage: `change-note <id> <new_text>`
- delete-note: Remove a note by ID. Usage: `delete-note <id>`
- all-notes: Display all notes.
- search-note: Search for notes. Usage by text: `search-note <input>`. Usage by tags: `search-note #<tag> #<tag2>`
- add-note-tag: Add a tag to a note. Usage: `add-note-tag <id> <tag1> [<tag2> ... <tagN>]`
- delete-note-tag: Remove a tag from a note. Usage: `delete-note-tag <id> <tag>`
- close or exit: Exit the program.

# Installation
## Prerequisites
- Python 3.8+
- pip (Python package installer)

## Installation Steps
1. Clone the repository:

    ```
    git clone https://github.com/bonny-art/code-crafters-tp-01
    cd code-crafters-tp-01
    ```

### Option 1: Install as a package

2. Install the package:

    ```
    pip install .
    ```

3. Run the bot with the command:

    ```
    run-bot
    ```

### Option 2: Run from `main.py`
2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Run the bot:

    ```
    python main.py
    ```

# Usage example

## Adding a Contact

Add a new contact by providing the necessary details such as name, phone numbers, emails, birthday, and address:

    ```
    python main.py
    add Name
    1234567890
    n
    example@email.com
    n
    address
    01.01.1999
    ```

## Listing Contacts

View all your contacts:

    ```
    all
    ```

For other commands details please run 'help' command

# Contributors
- https://github.com/bonny-art - TeamLead
- https://github.com/Serhii-Palamarchuk - Developer
- https://github.com/AndyGrigs - ScrumMaster
- https://github.com/AndriiRohovenko - Developer
- https://github.com/MarynaKip - Developer
