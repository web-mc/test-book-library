import re

from src.book import Book
from src.database import Database
from src.utils import get_field


def add_book(db: Database) -> None:
    """
    Добавляет новую книгу в базу данных после получения данных от юзера.

    Функция запрашивает у пользователя данные для новой книги,
    генерирует уникальный ID книги. Если книга не является дубликатом,
    она сохраняется в базе данных.
    """
    print("\nНачато добавление книги.")
    title = "Добавление книги"
    book = _get_new_book_from_user(title)

    if _is_duplicate(db, book.id):
        print(f"{title}. Такая книга уже добавлена. Её ID '{book.id}'.")
        return

    db.save_book(book)
    print(f"\n{title}. Книга добавлена в библиотеку.\nID книги '{book.id}'")


def _get_new_book_from_user(title: str) -> Book:
    """
    Запрашивает у пользователя данные для новой книги и
    возвращает объект Book.
    """
    book = Book()
    book.title = get_field(f"{title}. Введите название: ").capitalize()
    book.author = _get_author_from_user(title)
    book.year = _get_year_from_user(title)

    book.generate_book_id()
    return book


def _get_year_from_user(title: str) -> int:
    while True:
        year = get_field(f"{title}. Введите год(только цифры): ")
        if year.isdigit():
            return int(year)
        print(f'{title}. Выражение "{year}" не является цифрой.\n')


def _get_author_from_user(title: str) -> str:
    while True:
        author = get_field(
            f"{title}. Укажите автора в формате 'Фамилия И. О.'. регистр и точки не важены: "
        )
        author = author.lower().strip()
        pattern = r"^[a-zа-яё \.]+ [a-zа-яё]\.? [a-zа-яё]\.?$"
        if not re.match(pattern, author):
            print(f"{title}. Значение '{author}' не соответсвтует шаблону 'Фамилия И. О.'\n")
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
