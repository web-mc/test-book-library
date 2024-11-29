from typing import Callable, Final

from .add_book import add_book
from .change_status import change_book_status
from .delete import delete_book
from .show_all_books import show_all_books

COMMANDS: Final[dict[str, tuple[str, Callable]]] = {
    "0": ("Завершить работу", lambda db: False),
    "1": ("Добавить книгу", add_book),
    "2": ("Удалить книгу", delete_book),
    # "3": ("Найти книгу", None), #TODO: Найти книгу
    "4": ("Показать все книги", show_all_books),
    "5": ("Изменить статус книги", change_book_status),
}


def is_valid_command(number: str) -> bool:
    if not number or not number.isdigit():
        print(f'Выражение "{number}" не является цифрой.\n')
        return False

    if number not in COMMANDS:
        print(f"Команды с номером {number} не существует.\n")
        return False

    return True


def show_commands() -> None:
    print("Выбирите команду указав соответствующую цифру: ")
    for key, value in COMMANDS.items():
        print(f"{key}. {value[0]}")
