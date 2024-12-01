from typing import Any

from src.database import Database

from src.utils import Paginator


def show_all_books(db: Database) -> None:
    paginator = Paginator()
    while True:
        page_data = _get_page_data(paginator, db)
        if not page_data:
            print("Библиотека пуста.")
            return

        paginator.show_page_to_user(page_data)
        if not paginator.keep_running:
            return

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
