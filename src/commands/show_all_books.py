from src.database import Database
from src.utils import get_field

from .utils import Paginator


def show_all_books(db: Database) -> None:
    paginator = Paginator(db)
    while True:
        paginator.get_page_data()

        if not paginator.page_data:
            print("Библиотека пуста.")
            return

        paginator.show_page_data()

        choice = _get_choice_from_user()
        if not choice:
            return

        paginator.set_page(choice)
        print("----------------------")
        continue


def _get_choice_from_user() -> int:
    print("----------------------")
    print("--- Меню пагинации ---")
    while True:
        print("--- 0. В главное меню | 1. Назад | 2. Вперед")
        choice = get_field("--- Введите цифру: ")
        if choice not in ["0", "1", "2"]:
            print("Некорректный ввод. Пожалуйста, введите 0, 1 или 2.")
            continue
        return int(choice)
