"""
This module provides an Email class to represent and validate email addresses.

Classes:
- Email: A class representing an email address with validation.

Example usage:
    email = Email("example@domain.com")
"""

import re
from .field import Field

class Email(Field):
    """
    A class representing an email address with validation.

    Inherits:
        Field: The base class representing a simple data field.

    Attributes:
        address (str): The email address stored in the field.

    Methods:
        __init__(address: str) -> None:
            Initializes a new Email instance with validation.
    """

    def __init__(self, address: str) -> None:
        """
        Initializes a new Email instance with a given value, ensuring it is a valid email address.

        Args:
            address (str): The email address to be stored in the field.

        Raises:
            ValueError: If the email address does not match the pattern.
        """
        super().__init__(address)
        self.address = address

        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

        if not re.fullmatch(email_pattern, address):
            raise ValueError("Invalid email format. Expected format: example@domain.com")
