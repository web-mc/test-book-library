import json

from book import Book
from config import app_config

from .database import Database


class JsonDB(Database):
    def __init__(self) -> None:
        self.file = app_config.data_file

    def get_book_by_id(self, id: str) -> None | Book:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        if book := books.get(id):
            return Book.parse(book)
        return None

    def save_book(self, book: Book) -> None:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        books[book.id] = book.__dict__
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)

    def del_book_by_id(self, book_id: str) -> Book | None:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        del books[book_id]
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)

    def update_book_status(self, book_id: str, new_status: str) -> None:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        books[book_id]["status"] = new_status
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)
