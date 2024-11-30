import json
from itertools import islice
from pathlib import Path
from typing import Any

from src.book import Book
from src.config import app_config

from .database import Database


class JsonDB(Database):
    """
    JsonDB - это конкретная реализация абстрактного класса Database,
    использующая JSON-файл для хранения и управления данными о книгах.
    Она взаимодействует с JSON-файлом, указанным в конфигурации приложения.
    """

    def __init__(self) -> None:
        self.file: Path = app_config.data_file

    @staticmethod
    def prepare_db() -> None:
        """
        Подготавливает БД, создавая необходимые директории и файлы.
        """
        app_config.data_dir.mkdir(exist_ok=True)

        if not app_config.data_file.exists():
            with open(app_config.data_file, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4, ensure_ascii=False)

    def get_book_by_id(self, id: str) -> None | Book:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        if book := books.get(id):
            return Book.parse(book)
        return None

    def save_book(self, book: Book) -> None:
        with open(self.file, "r+", encoding="utf-8") as file:
            books = json.load(file)

            books[book.id] = book.dump()
            file.seek(0)
            json.dump(books, file, indent=4, ensure_ascii=False)
            file.truncate()

    def del_book_by_id(self, book_id: str) -> Book | None:
        with open(self.file, "r+", encoding="utf-8") as file:
            books = json.load(file)

            del books[book_id]

            file.seek(0)
            json.dump(books, file, indent=4, ensure_ascii=False)
            file.truncate()

    def update_book_status(self, book_id: str, new_status: str) -> None:
        with open(self.file, "r+", encoding="utf-8") as file:
            books = json.load(file)

            books[book_id]["status"] = new_status
            file.seek(0)
            json.dump(books, file, indent=4, ensure_ascii=False)
            file.truncate()

    def get_part_data(self, offset: int, limit: int) -> tuple[Any, ...]:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        # Итерация по значениям словаря в диапазоне
        books_iterator = islice(books.values(), offset, offset + limit)

        # Преобразуем только выбранные элементы в кортежи
        books_tuple = tuple(tuple(value.values()) for value in books_iterator)
        return books_tuple

    def get_books_by_year(
        self, condition: tuple[str, *tuple[int, ...]]
    ) -> tuple[Any, ...]:
        with open(self.file, "r", encoding="utf-8") as file:
            books = json.load(file)

        operator, *years = condition
        filters = {
            "=": lambda book: book["year"] == years[0],
            ">": lambda book: book["year"] >= years[0],
            "<": lambda book: book["year"] <= years[0],
            "-": lambda book: years[0] <= book["year"] <= years[1],
        }

        # делаем генератор с уже нужными нам рещультатми поиска
        result = (book for book in books.values() if filters[operator](book))
        return tuple(tuple(value.values()) for value in result)
