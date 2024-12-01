from typing import Literal

from src.database import Database
from src.utils import get_field


def change_book_status(db: Database) -> None:
    title = "Изменение статуса"
    while True:
        msg = f"{title}. Введите ID книги или '0' для выхода в главное меню: "
        book_id = get_field(msg)
        if book_id == "0":
            return

        book = db.get_book_by_id(book_id)
        if not book:
            msg = f"{title}. Книги с ID '{book_id}' нет в библиотеке. Пропускаем."
            print(msg)
            continue

        new_status = _get_status_from_user(title, book.status)
        if new_status == book.status:
            msg = f"{title}. Новый статус({new_status}) совпадает с текущим({book.status})."
            print(msg)
            print(f"{title}. Пропускаем обновление статуса книги.")
            continue

        db.update_book_status(book_id, new_status)
        print(f"{title}. Статус книги(ID '{book_id}') изменён на '{new_status}'.")


def _get_status_from_user(
    title: str,
    old_status: Literal["В наличии", "Выдана"],
) -> str:
    statuses = {
        "1": "В наличии",
        "2": "Выдана",
    }
    while True:
        print(f"{title}. Текущий статус книги: '{old_status}'.")
        new_status = get_field(
            f"{title}. Введите новый статус [1-В наличии/2-Выдана]: "
        )
        if new_status not in ["1", "2"]:
            print(f"{title}. Некорректный ввод. Пожалуйста, введите 1 или 2.")
            continue

        return statuses[new_status]
