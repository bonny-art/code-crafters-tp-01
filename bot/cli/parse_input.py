"""
Module providing functions for parsing user input.

Functions:
- parse_input(user_input: str) -> tuple: Parses user input into a command and its arguments.
"""


def parse_input(user_input: str) -> tuple:
    """
    Parses user input into a command and its arguments.

    Args:
    user_input (str): The input string from the user containing the command and optional arguments.

    Returns:
    tuple: A tuple containing the command (str) and its arguments (list of str).

    Example:
    >>> parse_input("Search file.txt")
    ('search', ['file.txt'])
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
