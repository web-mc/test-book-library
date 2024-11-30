from typing import Callable

from src.database import Database
from src.utils import get_field

from .utils import SearchEngine


def search_book(db: Database) -> None:
    print("Начат поиск книги.")

    engine = SearchEngine(db)
    while engine.stay_in_menu:
        option = _get_search_option_from_user(engine.search_options)

        if not option:
            return

        engine.search(option)


def _get_search_option_from_user(options: dict[int, tuple[str, Callable]]) -> int:
    options_list = []
    menu_numbers = ["0"]
    for number, value in options.items():
        options_list.append(f"{number}. {value[0]}")
        menu_numbers.append(str(number))

    menu = f"0. В главное меню | {' | '.join(options_list)}"
    while True:
        print("\nПоиск книги. Выбирите нужную команду введя цифру:")
        print(menu)
        choice = get_field("Введите цифру: ")
        if choice not in menu_numbers:
            print("Некорректный ввод. Пожалуйста, введите цифру из меню.\n")
            continue
        return int(choice)
