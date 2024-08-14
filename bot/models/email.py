import re
from .field import Field

class Email(Field):
    """
    A class representing an email address with validation.

    Inherits:
        Field: The base class representing a simple data field.

    Attributes:
        value (str): The email address stored in the field.

    Methods:
        __init__(value: str) -> None:
            Initializes a new Email instance with validation.
    """

    def __init__(self, address: str) -> None:
        self.address = address
        """
        Initializes a new Email instance with a given value, ensuring it is a valid email address.

        Args:
            value (str): The email address to be stored in the field.

        Raises:
            ValueError: If the email address does not match the pattern.
        """
        
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        
        if not re.fullmatch(email_pattern, address):
            raise ValueError('Invalid email format')
        
        
        
