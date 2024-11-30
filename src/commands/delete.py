from ..database import Database
from ..utils import get_field


def delete_book(db: Database) -> None:
    print("Начато удаление книги.")
    book_id = get_field("Введите ID книги для удаления: ")

    book = db.get_book_by_id(book_id)
    if not book:
        print(f"Книги с ID '{book_id}' нет в библиотеке. Пропускаем удаление.")
        return

    confirmation = _get_del_confimation()
    if confirmation:
        db.del_book_by_id(book_id)
        print(f"Удалена книга: {book.dump()}")
    else:
        print("Удаление книги отменено.")


def _get_del_confimation() -> bool:
    while True:
        confirm = get_field("Подтверждаете удаление книги? [1-Да/2-Нет]: ")
        if confirm not in ["1", "2"]:
            print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
            continue

        if confirm == "1":
            return True
        return False
