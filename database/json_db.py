from typing import Literal
from config import app_config
import json
from .database import Database
from book import Book


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
