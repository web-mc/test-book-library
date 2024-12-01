from src.database import Database
from src.utils import SearchEngine, get_field


def search(db: Database) -> None:
    print("Начат поиск книги.")

    engine = SearchEngine(db)
    while engine.stay_in_menu:
        request = _get_request_from_user(engine.list_commands())

        if not request:
            return

        result = engine.run_search(request)
        if result:
            engine.show_results(result)


def _get_request_from_user(options: list[tuple[str, str]]) -> str:
    options_list = []
    menu_numbers = ["0"]
    for command in options:
        options_list.append(f"{command[0]}. {command[1]}")
        menu_numbers.append(str(command[0]))

    menu = f"0. В главное меню | {' | '.join(options_list)}"
    while True:
        print("\nПоиск книги. Выбирите нужную команду введя цифру:")
        print(menu)
        request = get_field("Поиск книги. Введите цифру: ")
        if request not in menu_numbers:
            print("Поиск книги. Некорректный ввод. Пожалуйста, введите цифру из меню.")
            continue
        return request
