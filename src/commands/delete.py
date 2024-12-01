from src.database import Database
from src.utils import get_field


def delete_book(db: Database) -> None:
    print("Начато удаление книги.")
    title = "Удаление книги"

    while True:
        book_id = get_field(
            f"{title}. Введите ID книги или '0' для выхода в главное меню: "
        )
        if book_id == "0":
            return

        book = db.get_book_by_id(book_id)
        if not book:
            print(f"{title}. Книги с ID '{book_id}' нет в библиотеке.")
            continue

        confirmation = _get_del_confimation(title)
        if confirmation:
            db.del_book_by_id(book_id)
            print(f"{title}. Книга удалена: {book.dump()}")
        else:
            print(f"{title}. Отмена удаления.")


def _get_del_confimation(title: str) -> bool:
    while True:
        confirm = get_field(f"{title}. Подтверждаете удаление книги? [1-Да/2-Нет]: ")
        if confirm not in ["1", "2"]:
            print(f"{title}. Некорректный ввод. Пожалуйста, введите 1 или 2.")
            continue

        if confirm == "1":
            return True
        return False
