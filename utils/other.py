import json

from config import app_config


def get_field(prompt: str) -> str:
    """
    Запрашивает у пользователя ввод данных с помощью input()
    и возвращает непустую строку.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Вы не ввели значение.\n")


def prepare_app() -> None:
    """
    Подготавливает окружение приложения, создавая необходимые директории
    и файлы, если они отсутствуют. В частности, обеспечивает наличие
    директорий для данных и логов, а также инициализирует пустой JSON-файл
    для данных, если он отсутствует.
    """
    app_config.data_dir.mkdir(exist_ok=True)
    app_config.log_dir.mkdir(exist_ok=True)

    if not app_config.data_file.exists():
        with open(app_config.data_file, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4, ensure_ascii=False)
