import json

from config import app_config


def get_field(prompt: str) -> str:
    """
    Получает данные от пользователя и помощью input().
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Вы не ввели значение.\n")


def prepare_app() -> None:
    """
    Создает необходимые для работы приложения файлы и папки,
    если их нет.
    """
    app_config.data_dir.mkdir(exist_ok=True)
    app_config.log_dir.mkdir(exist_ok=True)

    if not app_config.data_file.exists():
        with open(app_config.data_file, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4, ensure_ascii=False)
