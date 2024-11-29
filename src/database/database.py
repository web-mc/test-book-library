from abc import ABC, abstractmethod
from typing import Any

from ..book import Book


class Database(ABC):
    @staticmethod
    @abstractmethod
    def prepare_db() -> None:
        """
        Подготавливает БД, создавая объекты, необходимые для
        хранения данных приложения.
        """

    @abstractmethod
    def get_book_by_id(self, id: str) -> Book | None:
        pass

    @abstractmethod
    def del_book_by_id(self, id: str) -> Book | None:
        pass

    @abstractmethod
    def save_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def update_book_status(self, book_id: str, new_status: str) -> None:
        pass

    @abstractmethod
    def get_all_books(self) -> dict[str, dict[str, Any]]:
        pass
