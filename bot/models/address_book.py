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
from typing import List, Dict, Optional
from collections import UserDict

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
        Returns a formatted string of upcoming birthdays within the next 7 days.

        Returns:
            str: A formatted string containing the name and birthday date of contacts
                with upcoming birthdays.
        """
        upcoming_birthdays_list = []

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
                        # email = record.email.value if record.email else '---'

                        upcoming_birthdays_list.append(
                            f"Contact name: {record.name.value}, birthday: {congratulation_date.strftime('%d.%m.%Y')}, Phone: {phone_number}"
                        )

                except ValueError:
                    pass

        return "\n".join(upcoming_birthdays_list)

    # from datetime import datetime, date
    # from rich.table import Table
    # from rich.console import Console
    # from io import StringIO

    # def get_upcoming_birthdays(self, days: int) -> str:
    #     """
    #     Returns a formatted string of upcoming birthdays within the next specified number of days.

    #     Returns:
    #         str: A formatted string containing the name and birthday date of contacts
    #             with upcoming birthdays, displayed as a table.
    #     """
    #     # Створюємо таблицю з інтеграцією значення days в заголовок
        # table = Table(
        #     title=f"Upcoming Birthdays within {days} Days",
        #     title_style="bold orange1",
        #     border_style="gray50",
        #     padding=(0, 2),
        #     show_header=True,
        #     show_lines=True,
        #     header_style="bold cyan",
        #     row_styles=["dim", "none"],
        # )

    #     # Додаємо стовпці
        # table.add_column("Name", style="dark_orange", width=20)
        # table.add_column("Birthday", style="sky_blue3", style="green")
        # table.add_column("Phone", style="sky_blue3", width=15)


    #     today_date = datetime.now().date()

    #     for record in self.data.values():
    #         if record.birthday:
    #             try:
    #                 user_birthday = record.birthday.value

    #                 if self._is_date_within_days(user_birthday, days):
    #                     month = user_birthday.month
    #                     day = user_birthday.day
    #                     birthday_this_year = date(today_date.year, month, day)

    #                     if birthday_this_year < today_date:
    #                         congratulation_date = date(today_date.year + 1, month, day)
    #                     else:
    #                         congratulation_date = birthday_this_year

    #                     congratulation_date = self._adjust_to_weekday(congratulation_date)

    #                     table.add_row(
    #                         record.name.value,
    #                         congratulation_date.strftime('%d.%m.%Y')
    #                     )

    #             except ValueError:
    #                 pass

    #     # Створюємо консоль для захоплення виходу таблиці
    #     console = Console()
    #     with StringIO() as buf:
    #         console.file = buf
    #         console.print(table)
    #         table_output = buf.getvalue()

    #     return table_output


    def __str__(self) -> str:
        """
        Returns a string representation of all records in the address book.

        Returns:
            str: A string representing all records in the address book.
        """
        return "\n".join(str(record) for record in self.data.values())