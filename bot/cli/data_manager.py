"""
Модуль для збереження та відновлення об'єкта адресної книги за допомогою
бібліотеки pickle.

Функції:
- save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None
- load_data(filename: str = "addressbook.pkl") -> AddressBook
"""

import pickle
from bot.models.address_book import AddressBook

def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Зберігає об'єкт адресної книги у файл за допомогою pickle.

    Параметри:
    - book (AddressBook): Об'єкт адресної книги, який потрібно зберегти.
    - filename (str): Назва файлу, в який буде збережено об'єкт. За замовчуванням "addressbook.pkl".

    Повертає:
    - None: Функція не повертає значення.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Завантажує об'єкт адресної книги з файлу за допомогою pickle.

    Параметри:
    - filename (str): Назва файлу, з якого буде завантажено об'єкт. За замовчуванням
    "addressbook.pkl".

    Повертає:
    - AddressBook: Завантажений об'єкт адресної книги. Якщо файл не знайдено,
    створюється новий об'єкт AddressBook.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
