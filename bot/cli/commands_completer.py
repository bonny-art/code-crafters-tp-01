from bot.cli.handlers import show_help
from prompt_toolkit.completion import Completer, Completion

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
                yield Completion(command.split(":")[0], start_position=-len(text_before_cursor))


# Initialize the CommandCompleter
completer = CommandCompleter()

# Save the history file on exit
HISTORY_FILE = '.console_bot_history'
try:
    with open(HISTORY_FILE, 'r') as f:
        history = f.read().splitlines()
except FileNotFoundError:
    history = []
