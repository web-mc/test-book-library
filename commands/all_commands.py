from typing import Final, Callable
from .add_book import add_book
from .delete import delete_book


COMMANDS: Final[dict[str, tuple[str, Callable]]] = {
    "0": ("Завершить работу", lambda db: False),
    "1": ("Добавить книгу", add_book),
    "2": ("Удалить книгу", delete_book),
    # "3": ("Найти книгу", None),
    # "4": ("Показать все книги", None),
    # "5": ("Изменить статус книги", None),
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
