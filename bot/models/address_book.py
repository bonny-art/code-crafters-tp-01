"""
This module provides the AddressBook class, which is used to manage a collection of contact records.

Classes:
- AddressBook: A class that extends UserDict to manage a collection of contact records.
It supports adding, finding, and deleting contacts.

Imports:
- UserDict from collections: A dictionary-like class that allows extension and customization.
- Record from .record: A class representing a contact record, which includes contact name
and phone numbers.

Usage:
- The AddressBook class provides methods to add new contact records, find existing records
by name, and delete records by name.
- Each record in the address book is identified by the contact's name, which is used as
the key in the underlying dictionary.

Example:
    address_book = AddressBook()
    record = Record("John Doe")
    address_book.add_record(record)
    found_record = address_book.find("John Doe")
    address_book.delete("John Doe")
"""

from datetime import datetime, timedelta, date
from typing import Optional
from collections import UserDict
from io import StringIO
from rich.table import Table
from rich.console import Console

from bot.models.birthday import Birthday

from .record import Record

class AddressBook(UserDict):
    """
    AddressBook is a collection of contact records that allows adding,
    finding, and deleting contacts.

    Methods:
        add_record(record: Record) -> None:
            Adds a new record to the address book.

        find(name: str) -> Optional[Record]:
            Finds and returns a record by the contact's name.

        delete(name: str) -> None:
            Deletes a record from the address book by the contact's name.

        get_upcoming_birthdays() -> List[Dict[str, str]]:
            Returns a list of upcoming birthdays within the next 7 days.
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
    
    def search_in_fields(self, input: str) -> Optional[list[str]]:
        """
        Search through name, phones, birthday fields and returns a list of matching records

        Args:
            input(str): the str value to search through all fields.
            
        Returns:
            Optional[List[Record]]: The found records list or None if not found.
        """
        matching_records = []
        for record in self.data.values():
            matches = [record.name and record.name.value.lower().startswith(input),
                       record.phones and any(phone.value.lower().startswith(input) for phone in record.phones),
                       record.emails and any(email.address.lower().startswith(input) for email in record.emails),
                       record.address and record.address.value.lower().startswith(input),
                       type(record.birthday) == Birthday and record.birthday.value.strftime('%d.%m.%Y').startswith(input)]
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
                table.add_row(
                    record.name.value,
                    record.birthday.value.strftime('%d.%m.%Y') if record.birthday else '---',
                    ', '.join([phone.value for phone in record.phones]) if len(record.phones) > 0 else '---',
                    ', '.join([email.address for email in record.emails]) if len(record.emails) > 0 else '---',
                    record.address.value if record.address else '---'
                    )
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

        Returns:
            str: A formatted string containing the name and birthday date of contacts
                with upcoming birthdays, displayed as a table.
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
        table.add_column("Congratulation Date", style="sky_blue3", justify="center", width=15)
        table.add_column("Phone\n", style="sky_blue3", justify="center", width=15)


        today_date = datetime.now().date()

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
                        phone_number = record.phones[0].value if record.phones else '---'

                        table.add_row(
                            record.name.value,
                            congratulation_date.strftime('%d.%m.%Y'),
                            phone_number
                        )

                except ValueError:
                    pass

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
