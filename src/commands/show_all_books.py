from typing import Any, Never
from src.database import Database
from src.utils import get_field

from .utils import Paginator


def show_all_books(db: Database) -> None:
    paginator = Paginator()
    while True:
        data = _get_page_data(paginator, db)
        if not data:
            print("Библиотека пуста.")
            return

        paginator.show_page_data(data)

        choice = _get_choice_from_user()
        if not choice:
            return

        paginator.set_page(choice)
        print("----------------------")
        continue


def _get_page_data(paginator: Paginator, db: Database) -> tuple[()] | tuple[Any, ...]:
    """
    Проверяет, совпадает ли текущая страница с предыдущей,
    чтобы избежать повторного извлечения данных. Если страница изменилась,
    он вычисляет смещение на основе текущей страницы и размера страницы,
    извлекает данные из базы данных и обновляет кэш и длину данных.
    """
    if paginator.previous_page == paginator.page:
        data = paginator.page_data
    else:
        offset = (paginator.page * paginator.page_size) - paginator.page_size
        data = db.get_part_data(offset, paginator.page_size)

        paginator.previous_page = paginator.page
        paginator.page_data = data
        paginator.len_data = len(data)

    return data


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
