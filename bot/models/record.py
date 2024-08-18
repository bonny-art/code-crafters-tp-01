"""
This module provides classes for managing contact records, including names and phone numbers.

Classes:
- Name: Represents a contact's name.
- Phone: Represents a contact's phone number.
- Record: Represents a contact record with a name and a list of phone numbers.
"""

from typing import List, Optional

from .name import Name
from .phone import Phone
from .birthday import Birthday
from .email import Email
from .address import Address

class Record:
    """
    Represents a contact record with a name and a list of phone numbers.
    
    Attributes:
    - name (Name): The contact's name.
    - phones (List[Phone]): A list of the contact's phone numbers.
    - emails (List[Email]): A list of the contact's email addresses.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new Record instance with a name.
        
        Args:
        - name (str): The name of the contact.
        """
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.emails: List[Email] = []
        self.birthday = None
        self.address = None

#------------------------------------------------------------------

    def add_email(self, email_address: str) -> None:
        """
        Adds an email address to the contact's list of emails.

        If the emails list does not exist, it initializes it first.

        Args:
        - email_address (str): The email address to add.
        """
        if not hasattr(self, 'emails'):
            self.emails = []

        email = Email(email_address)
        self.emails.append(email)

#------------------------------------------------------------------

    def remove_email(self, email_address:str) -> None:
        """
        Removes an email address from the contact's list of email addresses.

        Args:
        - email_address (str): The email address to remove.

        Returns:
        - None
        """
        self.emails = [e for e in self.emails if e.address != email_address]

#------------------------------------------------------------------

    def edit_email(self, old_email:str, new_email:str) -> None:
        """
        Replaces an old email address with a new one in the contact's list of emails.

        Args:
        - old_email (str): The email address to replace.
        - new_email (str): The new email address to add.
        """
        self.add_email(new_email)
        self.remove_email(old_email)

#------------------------------------------------------------------

    def add_address(self, address_str: str) -> None:
        """
        Adds an address to the contact record.
        
        Args:
        - address_str (str): The address to set.
        """
        self.address = Address(address_str)

#------------------------------------------------------------------

    def edit_address(self, new_address_str: str) -> None:
        """
        Edits the contact's address.
        
        Args:
        - new_address_str (str): The new address to set.
        """
        self.address = Address(new_address_str)

#------------------------------------------------------------------

    def get_address(self) -> Optional[str]:
        """
        Gets the contact's address.
        
        Returns:
        - str or None: The address string if set, otherwise None.
        """
        return self.address.value if self.address else None

#------------------------------------------------------------------

    def add_phone(self, phone_number: str) -> None:
        """
        Adds a phone number to the contact's list of phone numbers.

        Args:
        - phone_number (str): The phone number to add.
        """
        phone = Phone(phone_number)
        self.phones.append(phone)

#------------------------------------------------------------------

    def remove_phone(self, phone_number: str) -> None:
        """
        Removes a phone number from the contact's list of phone numbers.

        Args:
        - phone_number (str): The phone number to remove.
        """
        self.phones = [p for p in self.phones if p.value != phone_number]

#------------------------------------------------------------------

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        """
        Replaces an old phone number with a new phone number in the contact's list.

        Args:
        - old_phone_number (str): The phone number to replace.
        - new_phone_number (str): The new phone number to add.
        """

        self.add_phone(new_phone_number)
        self.remove_phone(old_phone_number)

#------------------------------------------------------------------

    def show_formated_phones(self) -> str:
        """
        Returns a formatted string of the contact's name and phone numbers.
        
        Returns:
        - str: A string in the format 'name: phone1, phone2, ...'.
        """
        phones = ", ".join(f"[cyan]{phone.value}[/cyan]" for phone in self.phones)
        return f"[dark_orange]{self.name.value}:[/dark_orange] {phones}"

#------------------------------------------------------------------

    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthday to the contact record. Raises an exception if the birthday is invalid.

        Args:
        - birthday (str): The birthday to add.
        """
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday is already set")

#------------------------------------------------------------------

    def show_birthday(self) -> str:
        """
        Returns a string representation of the contact's birthday.

        Returns:
        - str: A string describing the contact's birthday.
        """
        if self.birthday is None:
            return "No birthday set"
        return f"{self.name.value}'s birthday is on {self.birthday.value.strftime('%d.%m.%Y')}"

#------------------------------------------------------------------

    def edit_field(self, field: str, old_value: str, new_value: str, address_book=None):
        """
        Edits or removes a specific field of the contact record.

        Args:
        - field (str): The field to edit. Options include 'name', 'phones', 'emails',
        'address', and 'birthday'.
        - old_value (str): The current value to be replaced or removed. This is required
        when editing.
        - new_value (str): The new value to set for the field. If None, the old value will
        be removed.
        - address_book (AddressBook, optional): An instance of AddressBook, required only
        when changing the contact's name to update the AddressBook accordingly.

        Returns:
        - str: A message indicating the result of the edit. Describes what changes were made
        or if no change was applied.
        """
        if field == 'name':
            if not address_book:
                raise ValueError("AddressBook is required to change the contact's name.")

            if new_value:
                # Remove the contact under the old name from the AddressBook
                old_name = self.name.value
                address_book.delete(old_name)

                # Update the contact's name in the Record
                self.name = Name(new_value)

                # Add the contact back to the AddressBook with the new name
                address_book.add_record(self)

                return f"Name updated from '{old_name}' to '{new_value}'."
            return "No name change applied."

        elif field == 'phones':
            if new_value:
                if old_value:
                    self.edit_phone(old_value, new_value)
                    return f"Phone number '{old_value}' updated to '{new_value}'."
                else:
                    self.add_phone(new_value)
                    return f"Phone number '{new_value}' added."
            elif old_value:
                self.remove_phone(old_value)
                return f"Phone number '{old_value}' removed."

        elif field == 'emails':
            if new_value:
                if old_value:
                    self.edit_email(old_value, new_value)
                    return f"Email '{old_value}' updated to '{new_value}'."
                else:
                    self.add_email(new_value)
                    return f"Email '{new_value}' added."
            elif old_value:
                self.remove_email(old_value)
                return f"Email '{old_value}' removed."

        elif field == 'address':
            if new_value:
                self.edit_address(new_value)
                return f"Address updated to '{new_value}'."
            else:
                self.address = None
                return "Address removed."

        elif field == 'birthday':
            if new_value:
                self.birthday = Birthday(new_value)
                return f"Birthday updated to '{new_value}'."
            else:
                self.birthday = None
                return "Birthday removed."

        return "Unknown action."

#------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Returns a string representation of the contact record.

        Returns:
        - str: A string describing the contact's name and phone numbers.
        """
        phones_str = '; '.join(str(p) for p in self.phones)
        if not phones_str:
            phones_str = "----------"

        if hasattr(self, 'emails'):
            emails_str = '; '.join(e.address for e in self.emails)
        else:
            emails_str = "----------"

        address_str = self.get_address() or "----------"

        if self.birthday:
            birthday_str = self.birthday.value.strftime("%d.%m.%Y")
        else:
            birthday_str = "----------"

        return (
            f"Contact name: {self.name.value}, "
            f"birthday: {birthday_str}, "
            f"phones: {phones_str}, "
            f"emails: {emails_str}, "
            f"address: {address_str}"
        )
