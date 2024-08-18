"""
This module provides a utility function to print content with specified
numbers of empty lines before and after the content.

Function:
- print_with_newlines: Prints content with a specified number of empty lines
  before and after the content to improve readability.

Usage:
- Import the function and call it to print content with customizable spacing
  around it.

Example:
    >>> print_with_newlines("Hello, World!", lines_before=2, lines_after=1, use_rich_print=True)
    
    Output:
    
    (empty line)
    (empty line)
    Hello, World!
    (empty line)
"""

from rich import print as rich_print

def print_with_newlines(
    content: str,
    lines_before: int = 1,
    lines_after: int = 1,
    use_rich_print: bool = True
) -> None:
    """
    Prints content with a specified number of empty lines before and after the content.

    Parameters:
    - content (str): The content to be printed.
    - lines_before (int): Number of empty lines to print before the content. Default is 1.
    - lines_after (int): Number of empty lines to print after the content. Default is 1.
    - use_rich_print (bool): Whether to use rich print for output. Default is False.

    Returns:
    None

    Example:
        >>> print_with_newlines("Hello, World!", lines_before=2, lines_after=1, use_rich_print=True)
        
        Output:
        
        (empty line)
        (empty line)
        Hello, World!
        (empty line)
    """
    output = "\n" * lines_before + content + "\n" * lines_after
    if use_rich_print:
        rich_print(output)
    else:
        print(output)
