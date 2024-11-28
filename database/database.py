from abc import ABC, abstractmethod

from book import Book


class Database(ABC):
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
