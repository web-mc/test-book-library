from database import Database
from utils import get_field


def delete_book(db: Database) -> None:
    book_id = get_field("Введите ID книги: ")

    book = db.get_book_by_id(book_id)
    if not book:
        print(f"Книги с ID '{book_id}' нет в библиотеке. Пропускаем удаление.")
        return

    db.del_book_by_id(book_id)
    print(f"Удалена книга: {book.__dict__}")
