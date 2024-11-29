from src.database import Database
from src.utils import get_field


def show_all_books(db: Database) -> None:
    all_books = db.get_all_books()
    if not all_books:
        print("Библиотека пуста.")
        return

    print(f"Книг найдено: {len(all_books)}.")
    PER_PAGE = 2
