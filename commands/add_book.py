import re

from book import Book
from database import Database
from utils import get_field


def add_book(db: Database) -> None:
    """
    Добавляет новую книгу в базу данных после получения данных от юзера.

    Функция запрашивает у пользователя данные для новой книги,
    генерирует уникальный ID книги. Если книга не является дубликатом,
    она сохраняется в базе данных.
    """
    print("\nНачато добавление книги.")
    book = _get_new_book_from_user()

    if _is_duplicate(db, book.id):
        print(f"Такая книга уже добавлена. Её ID '{book.id}'.")
        return

    db.save_book(book)
    print(f"\nКнига добавлена в библиотеку.\nID книги '{book.id}'")


def _get_new_book_from_user() -> Book:
    """
    Запрашивает у пользователя данные для новой книги и
    возвращает объект Book.
    """
    book = Book()
    book.title = get_field("Введите название книги: ").capitalize()
    book.author = _get_author_from_user()
    book.year = _get_year_from_user()

    book.generate_book_id()
    return book


def _get_year_from_user() -> int:
    while True:
        year = get_field("Введите год книги(только цифры): ")
        if year.isdigit():
            return int(year)
        print(f'Выражение "{year}" не является цифрой.\n')


def _get_author_from_user() -> str:
    while True:
        author = get_field(
            "Укажите автора в формате 'Фамилия И. О.'. регистр и точки не важены: "
        )
        author = author.lower().strip()
        pattern = r"^[a-zа-яё \.]+ [a-zа-яё]\.? [a-zа-яё]\.?$"
        if not re.match(pattern, author):
            print(f"Значение '{author}' не соответсвтует шаблону 'Фамилия И. О.'")
            continue

        lst = author.split()
        lst[-1] = lst[-1] if lst[-1].endswith(".") else lst[-1] + "."
        lst[-2] = lst[-2] if lst[-2].endswith(".") else lst[-2] + "."
        author = " ".join(lst)
        return author.title()


def _is_duplicate(db: Database, book_id: str) -> bool:
    book = db.get_book_by_id(book_id)
    if book:
        return True
    return False
