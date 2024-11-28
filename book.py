from hashlib import md5
from typing import Any, Literal, Self


class Book:
    def __init__(self) -> None:
        self.id: str = ""
        self.title: str = ""
        self.author: str = ""
        self.year: int | None = None
        self.status: Literal["в наличии", "выдана"] = "в наличии"

    def generate_book_id(self) -> None:
        str_to_hash = f"{self.title}{self.author}{self.year}"
        str_to_hash = "".join(char for char in str_to_hash if char.isalnum())
        self.id = md5(str_to_hash.encode("utf-8")).hexdigest()

    @staticmethod
    def parse(book_data: dict[str, Any]) -> "Book":
        book = Book()
        book.id = book_data.get("id", "")
        book.title = book_data.get("title", "")
        book.author = book_data.get("author", "")
        book.year = book_data.get("year", None)
        book.status = book_data.get("status", "в наличии")
        return book
