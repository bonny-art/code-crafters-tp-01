"""
Модуль для збереження та відновлення об'єкта нотаток за допомогою
бібліотеки pickle.

Функції:
- save_data(book: NoteBook, filename: str = "notebook.pkl") -> None
- load_data(filename: str = "notebook.pkl") -> NoteBook
"""

import pickle
from bot.models.note_book import NoteBook
import os

file_path = os.path.abspath("tmp/notebook.pkl")

def save_data(book: NoteBook, filename: str = file_path) -> None:
    """
    Зберігає об'єкт адресної книги у файл за допомогою pickle.

    Параметри:
    - book (NoteBook): Об'єкт адресної книги, який потрібно зберегти.
    - filename (str): Назва файлу, в який буде збережено об'єкт. За замовчуванням "notebook.pkl".

    Повертає:
    - None: Функція не повертає значення.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: str = file_path) -> NoteBook:
    """
    Завантажує об'єкт адресної книги з файлу за допомогою pickle.

    Параметри:
    - filename (str): Назва файлу, з якого буде завантажено об'єкт. За замовчуванням
    "notebook.pkl".

    Повертає:
    - NoteBook: Завантажений об'єкт адресної книги. Якщо файл не знайдено,
    створюється новий об'єкт NoteBook.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()
