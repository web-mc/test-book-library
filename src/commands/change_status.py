from typing import Literal

from ..database import Database
from ..utils import get_field


def change_book_status(db: Database) -> None:
    book_id = get_field("Введите ID книги: ")

    book = db.get_book_by_id(book_id)
    if not book:
        print(f"Книги с ID '{book_id}' нет в библиотеке. Завершаем операцию.")
        return

    new_status = _get_status_from_user(book.status)
    if new_status == book.status:
        print(f"Новый статус({new_status}) совпадает с текущим({book.status}).")
        print("Пропускаем обновление статуса книги.")
        return

    db.update_book_status(book_id, new_status)
    print(f"Статус книги(ID '{book_id}') изменён на '{new_status}'.")


def _get_status_from_user(old_status: Literal["В наличии", "Выдана"]) -> str:
    statuses = {
        "1": "В наличии",
        "2": "Выдана",
    }
    while True:
        print(f"Текущий статус книги: '{old_status}'.")
        new_status = get_field("Введите новый статус [1-В наличии/2-Выдана]: ")
        if new_status not in ["1", "2"]:
            print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
            continue

        return statuses[new_status]
