"""
Модуль для збереження та відновлення об'єкта адресної книги за допомогою
бібліотеки pickle.

Функції:
- save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None
- load_data(filename: str = "addressbook.pkl") -> AddressBook
"""

import pickle
from bot.models.address_book import AddressBook
import os


file_path = os.path.abspath("tmp/addressbook.pkl")

def save_data(book: AddressBook, filename: str = file_path) -> None:
    """
    Зберігає об'єкт адресної книги у файл за допомогою pickle.

    Параметри:
    - book (AddressBook): Об'єкт адресної книги, який потрібно зберегти.
    - filename (str): Назва файлу, в який буде збережено об'єкт. За замовчуванням "addressbook.pkl".

    Повертає:
    - None: Функція не повертає значення.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(book, f)
    except Exception as ex:
        print(f"An error occurred while saving data: {ex}")

def load_data(filename: str = file_path) -> AddressBook:
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
    except Exception as ex:
            print(f"An error occurred while loading data: {ex}")
