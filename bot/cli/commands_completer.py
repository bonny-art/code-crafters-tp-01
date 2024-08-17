"""
This module provides a custom command-line auto-completer for the bot's CLI.

Classes:
- CommandCompleter: A custom completer for command-line input that provides
  auto-completion suggestions for the first word (command) in the input.

Functions:
- show_help: Retrieves the list of available commands and their descriptions.

Usage:
- The CommandCompleter class is used to provide suggestions for the available
  commands in the bot's CLI as the user types.
"""

from prompt_toolkit.completion import Completer, Completion

from bot.cli.handlers import show_help

class CommandCompleter(Completer):
    """
    A custom completer for command-line input, providing auto-completion
    suggestions only for the first word (the command).

    Methods:
        get_completions: Yields possible completions for the input text if it matches
        available commands and is the first word in the input.
    """
    def get_completions(self, document, complete_event):
        """
        Generates command completions based on the text before the cursor.

        Args:
            document (Document): An object containing information about the input text.
            complete_event (CompleteEvent): An event triggered by the completion system.

        Yields:
            Completion: A possible completion suggestion for the command.
        """
        # Get the current input text before the cursor
        text_before_cursor = document.text_before_cursor.strip()

        # If more than one word is entered, don't provide any completions
        if " " in text_before_cursor:
            return

        # Provide completions only for the first word (command)
        commands, _ = show_help()
        for command in commands:
            if command.startswith(text_before_cursor):
                completion_text = command.split(':', maxsplit=1)[0]
                start_pos = -len(text_before_cursor)
                yield Completion(completion_text, start_position=start_pos)



# Initialize the CommandCompleter
completer = CommandCompleter()

# Save the history file on exit
HISTORY_FILE = '.console_bot_history'
try:
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = f.read().splitlines()
except FileNotFoundError:
    history = []
