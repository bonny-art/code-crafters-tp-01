import re
from .field import Field

class Address(Field):
    """
    A class representing a street address with basic validation.

    Inherits:
        Field: The base class representing a simple data field.

    Attributes:
        value (str): The street address stored in the field.

    Methods:
        __init__(value: str) -> None:
            Initializes a new Address instance with validation.
    """

    def __init__(self, address: str) -> None:
        """
        Initializes a new Address instance with a given value, ensuring it is a valid street address format.
        A simple validation will be performed to check if the address contains alphanumeric characters, spaces, commas, and numbers, which is a very basic form of validation.
        More complex validation rules can be added based on specific requirements.

        Args:
            address (str): The street address to be stored in the field.

        Raises:
            ValueError: If the address does not match the pattern for a basic street address format.
        """
        
        address_pattern = r'^[\w\s,]*$'
        
        if not re.fullmatch(address_pattern, address):
            raise ValueError('Invalid address format')
        self.value = address