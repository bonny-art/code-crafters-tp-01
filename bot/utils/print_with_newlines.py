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
    >>> print_with_newlines("Hello, World!", lines_before=2, lines_after=1)
    
    Output:
    
    (empty line)
    (empty line)
    Hello, World!
    (empty line)
"""

def print_with_newlines(content: str, lines_before: int = 1, lines_after: int = 1) -> None:
    """
    Prints content with a specified number of empty lines before and after the content.

    Parameters:
    - content (str): The content to be printed.
    - lines_before (int): Number of empty lines to print before the content. Default is 1.
    - lines_after (int): Number of empty lines to print after the content. Default is 1.

    Returns:
    None

    Example:
        >>> print_with_newlines("Hello, World!", lines_before=2, lines_after=1)
        
        Output:
        
        (empty line)
        (empty line)
        Hello, World!
        (empty line)
    """
    print("\n" * lines_before + content + "\n" * lines_after)
