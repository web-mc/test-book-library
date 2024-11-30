from typing import Callable, Final

from .add_book import add_book
from .change_status import change_book_status
from .delete import delete_book
from .search_book import search_book
from .show_all_books import show_all_books

COMMANDS: Final[dict[str, tuple[str, Callable]]] = {
    "0": ("Завершить работу", lambda db: False),
    "1": ("Добавить книгу", add_book),
    "2": ("Удалить книгу", delete_book),
    "3": ("Изменить статус книги", change_book_status),
    "4": ("Найти книгу", search_book),  # TODO: Найти книгу
    "5": ("Показать все книги", show_all_books),
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
    print("\nВыбирите команду указав соответствующую цифру: ")
    for key, value in COMMANDS.items():
        print(f"{key}. {value[0]}")
