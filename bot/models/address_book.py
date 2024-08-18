"""
This module provides the AddressBook class, which is used to manage a collection of contact records.

Classes:
- AddressBook: A class that extends UserDict to manage a collection of contact records. 
  It supports adding, finding, searching, deleting contacts, and displaying information about them.

Imports:
- UserDict from collections: A dictionary-like class that allows extension and customization.
- Record from .record: A class representing a contact record, which includes contact name and
phone numbers.
- Birthday from bot.models.birthday: A class representing a birthday.

Usage:
- The AddressBook class provides methods to add new contact records, find existing records by name, 
  search through various fields, delete records by name, and display upcoming birthdays and
  contact details.
- Each record in the address book is identified by the contact's name, which is used as the key
in the underlying dictionary.

Example:
    address_book = AddressBook()
    record = Record("John Doe")
    address_book.add_record(record)
    found_record = address_book.find("John Doe")
    address_book.delete("John Doe")
    upcoming_birthdays = address_book.get_upcoming_birthdays(7)
    single_contact_info = address_book.show_single_contact(record)
    all_contacts_info = address_book.show_all_contacts()
"""

from datetime import datetime, timedelta, date
from typing import Optional, List
from collections import UserDict

from io import StringIO
from rich.table import Table
from rich.console import Console

from bot.models.birthday import Birthday
from .record import Record

class AddressBook(UserDict):
    """
    AddressBook is a collection of contact records that allows adding,
    searching, deleting contacts, and displaying information about them.

    Methods:
        add_record(record: Record) -> None:
            Adds a new record to the address book.

        find(name: str) -> Optional[Record]:
            Finds and returns a record by the contact's name.

        search_in_fields(args: list[str]) -> Optional[list[Record]]:
            Searches through name, phones, emails, address, and birthday fields 
            and returns a list of matching records.

        delete(name: str) -> None:
            Deletes a record from the address book by the contact's name.

        get_upcoming_birthdays(days: int) -> str:
            Returns a formatted string of upcoming birthdays within the next specified
            number of days.

        show_single_contact(record: Record) -> str:
            Returns a formatted string of a single contact in the address book.

        show_all_contacts() -> str:
            Returns a formatted string of all contacts in the address book.

        __str__() -> str:
            Returns a string representation of all records in the address book.
    """

    def add_record(self, record: Record) -> None:
        """
        Adds a new record to the address book.

        Args:
            record (Record): The record to be added.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """
        Finds and returns a record by the contact's name.

        Args:
            name (str): The name of the contact to find.

        Returns:
            Optional[Record]: The found record or None if not found.
        """
        return self.data.get(name, None)

    def search_in_fields(self, args: list[str]) -> Optional[List[Record]]:
        """
        Searches through name, phones, emails, address, and birthday fields 
        and returns a list of matching records.

        Args:
            args (list[str]): The search terms to look for in the contact fields.
            
        Returns:
            Optional[List[Record]]: The found records list or None if no matches are found.
        """
        if not self.data:
            return "No contacts found."
        search = [arg.lower() for arg in args]
        matching_records = []
        for record in self.data.values():
            name_check = (
                record.name and
                record.name.value.lower().startswith(tuple(search))
            )

            phones_check = (
                record.phones and
                any(phone.value.lower().startswith(tuple(search)) for phone in record.phones)
            )

            emails_check = (
                record.emails and
                any(email.address.lower().startswith(tuple(search)) for email in record.emails)
            )

            address_check = (
                record.address and
                record.address.value.lower().startswith(tuple(search))
            )

            birthday_check = (
                isinstance(record.birthday, Birthday) and
                record.birthday.value.strftime('%d.%m.%Y').startswith(tuple(search))
            )

            matches = [
                name_check,
                phones_check,
                emails_check,
                address_check,
                birthday_check
            ]

            if any(matches):
                matching_records.append(record)

        if len(matching_records) > 0:
            table = Table(
                "Name",
                "Birthday",
                "Phones",
                "Emails",
                "Address",
                title="Search Results",
                title_style="bold orange1",
                border_style="gray50",
                padding=(0, 2),
                show_header=True,
                show_lines=True,
                header_style="bold cyan"
            )
            for record in matching_records:
                name = record.name.value
                birthday = (
                    record.birthday.value.strftime('%d.%m.%Y')
                    if record.birthday
                    else '---'
                )
                phones = (
                    ', '.join(phone.value for phone in record.phones) 
                    if record.phones
                    else '---'
                )
                emails = (
                    ', '.join(email.address for email in record.emails) 
                    if record.emails
                    else '---'
                )
                address = record.address.value if record.address else '---'

                table.add_row(name, birthday, phones, emails, address)

            console = Console()
            console.print(table)
            return ""
        else:
            return None

    def delete(self, name: str) -> None:
        """
        Deletes a record from the address book by the contact's name.

        Args:
            name (str): The name of the contact to delete.
        """
        if name in self.data:
            del self.data[name]

    def _is_date_within_days(self, target_date: datetime, days: int) -> bool:
        """
        Checks if the target date falls within the given number of days from today.

        Args:
            target_date (datetime): The target date to check.
            days (int): The number of days to check within.

        Returns:
            bool: True if the target date is within the range, False otherwise.
        """
        today_date = datetime.now().date()
        date_this_year = date(today_date.year, target_date.month, target_date.day)

        if date_this_year < today_date:
            target_date = date(today_date.year + 1, target_date.month, target_date.day)
        else:
            target_date = date_this_year

        return today_date <= target_date <= (today_date + timedelta(days=days))

    def _adjust_to_weekday(self, date_obj: date) -> date:
        """
        Adjusts the date to the next weekday if it falls on a weekend.

        Args:
            date_obj (date): The date to adjust.

        Returns:
            date: The adjusted date.
        """
        if date_obj.weekday() == 5:  # Saturday
            return date_obj + timedelta(days=2)

        if date_obj.weekday() == 6:  # Sunday
            return date_obj + timedelta(days=1)

        return date_obj

    def get_upcoming_birthdays(self, days: int) -> str:
        """
        Returns a formatted string of upcoming birthdays within the next specified number of days.

        Args:
            days (int): The number of days within which to find upcoming birthdays.

        Returns:
            str: A formatted string containing the name and birthday date of contacts
                with upcoming birthdays, displayed as a table. If no upcoming birthdays are found,
                returns a message indicating this.
        """
        table = Table(
            title=f"Upcoming Birthdays within {days} Days",
            title_style="bold orange1",
            border_style="gray50",
            padding=(0, 2),
            show_header=True,
            show_lines=True,
            header_style="bold cyan"
        )

        table.add_column("Name\n", style="dark_orange", width=20)
        table.add_column("Congratulation Date", style="green", justify="center", width=16)
        table.add_column("Phones\n", style="green", justify="center", width=16)
        table.add_column("Emails\n", style="green", justify="center", width=30)

        today_date = datetime.now().date()
        has_birthdays = False

        for record in self.data.values():
            if record.birthday:
                try:
                    user_birthday = record.birthday.value

                    if self._is_date_within_days(user_birthday, days):
                        month = user_birthday.month
                        day = user_birthday.day
                        birthday_this_year = date(today_date.year, month, day)

                        if birthday_this_year < today_date:
                            congratulation_date = date(today_date.year + 1, month, day)
                        else:
                            congratulation_date = birthday_this_year

                        congratulation_date = self._adjust_to_weekday(congratulation_date)
                        phone_numbers = (
                            '\n'.join(phone.value for phone in record.phones)
                            if record.phones
                            else '---'
                        )
                        emails = (
                            '\n'.join(email.address for email in record.emails)
                            if record.emails
                            else '---'
                        )

                        table.add_row(
                            record.name.value,
                            congratulation_date.strftime('%d.%m.%Y'),
                            phone_numbers,
                            emails
                        )
                        has_birthdays = True

                except ValueError:
                    pass

        if not has_birthdays:
            return f"There are no upcoming birthdays within {days} days."

        console = Console()
        with StringIO() as buf:
            console.file = buf
            console.print(table)
            table_output = buf.getvalue()

        return table_output

    def show_single_contact(self, record: Record) -> str:
        """
        Returns a formatted string of a single contact in the address book.

        Args:
            record (Record): The contact record to be displayed.

        Returns:
            str: A formatted string containing the contact information displayed as a table.
        """
        table = Table(
            title="Contact Details",
            title_style="bold orange1",
            border_style="gray50",
            padding=(0, 2),
            show_header=True,
            show_lines=True,
            header_style="bold cyan"
        )

        table.add_column("Name\n", style="dark_orange", width=20)
        table.add_column("Phones\n", style="green", justify="center", width=16)
        table.add_column("Emails\n", style="green", justify="center", width=30)
        table.add_column("Address\n", style="green", justify="center")
        table.add_column("Birthday\n", style="green", justify="center", width=16)

        phone_numbers = (
            '\n'.join(phone.value for phone in record.phones)
            if record.phones
            else '---'
        )
        emails = '\n'.join(email.address for email in record.emails) if record.emails else '---'
        address = record.get_address() if record.get_address() else '---'
        birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else '---'

        table.add_row(
            record.name.value,
            phone_numbers,
            emails,
            address,
            birthday
        )

        console = Console()
        with StringIO() as buf:
            console.file = buf
            console.print(table)
            table_output = buf.getvalue()

        return table_output

    def show_all_contacts(self) -> str:
        """
        Returns a formatted string of all contacts in the address book.

        Returns:
            str: A formatted string containing all contacts in the address book,
                displayed as a table.
        """
        if not self.data:
            return "No contacts found."

        table = Table(
            title="All Contacts",
            title_style="bold orange1",
            border_style="gray50",
            padding=(0, 2),
            show_header=True,
            show_lines=True,
            header_style="bold cyan"
        )

        table.add_column("Name\n", style="dark_orange", width=20)
        table.add_column("Phones\n", style="green", justify="center", width=16)
        table.add_column("Emails\n", style="green", justify="center", width=30)
        table.add_column("Address\n", style="green", justify="center")
        table.add_column("Birthday\n", style="green", justify="center", width=16)

        for record in self.data.values():
            phone_numbers = (
                '\n'.join(phone.value for phone in record.phones)
                if record.phones
                else '---'
            )
            emails = '\n'.join(email.address for email in record.emails) if record.emails else '---'
            address = record.get_address() if record.get_address() else '---'
            birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else '---'

            table.add_row(
                record.name.value,
                phone_numbers,
                emails,
                address,
                birthday
            )

        console = Console()
        with StringIO() as buf:
            console.file = buf
            console.print(table)
            table_output = buf.getvalue()

        return table_output

    def __str__(self) -> str:
        """
        Returns a string representation of all records in the address book.

        Returns:
            str: A string representing all records in the address book.
        """
        return "\n".join(str(record) for record in self.data.values())
