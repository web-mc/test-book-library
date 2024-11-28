import json

from book_manager import Manager
from config import app_config
from exceptions import ValidationError


def show_menu() -> None:
    print("Выбирите команду указав соответствующую цифру:")
    for key, value in Manager.commands.items():
        print(f"{key}. {value}")


def prepare_app() -> None:
    app_config.data_dir.mkdir(exist_ok=True)
    app_config.log_dir.mkdir(exist_ok=True)

    init_data = {
        "books": {},
        "unique_book_index": {}, # hash и ID книги в словаре
    }
    if not app_config.data_file.exists():
        with open(app_config.data_file, "w", encoding="utf-8") as json_file:
            json.dump(init_data, json_file, indent=4, ensure_ascii=False)


def validate_number(number: str | None) -> None:
    if not number:
        raise ValidationError("Вы ввели пустую строку!")

    if number.isalpha():
        raise ValidationError(f'Выражение "{number}" не является цифрой.')

    if number not in Manager.commands:
        raise ValidationError(f"Команды с номером {number} не существует.")
