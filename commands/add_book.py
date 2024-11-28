from book import Book
from utils import get_field
from database import Database


def add_book(db: Database) -> None:
    print("\nНачато добавление книги.")
    book = _get_new_book_from_user()
    book.generate_book_id()
    if _is_duplicate(db, book.id):
        print(f"Такая книга уже добавлена. Её ID '{book.id}'.")
        return
    db.save_book(book)
    print(f"\nКнига добавлена в библиотеку.\nID книги '{book.id}'")


def _get_new_book_from_user() -> Book:
    book = Book()
    book.title = get_field("Введите название книги: ")
    book.author = get_field("Введите автора книги: ")
    while True:
        year = get_field("Введите год книги(только цифры): ")
        if not year or not year.isdigit():
            print(f'Выражение "{year}" не является цифрой.\n')
            continue

        book.year = int(year)
        return book


def _is_duplicate(db: Database, book_id: str) -> bool:
    book = db.get_book_by_id(book_id)
    if book:
        return True
    return False
