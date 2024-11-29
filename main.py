from logging import getLogger
from logging.config import dictConfig

from src.commands import is_valid_command, show_commands
from src.config import LOGGERS, app_config
from src.database import JsonDB
from src.manager import Manager


def main() -> None:
    """
    Точка входа для приложения.

    Создает экземпляр Manager, выводит список доступных команд,
    получает ввод от пользователя, обрабатывает команды и
    останавливает приложение, если пользователь выбрал соответствующую команду.
    """
    manager = Manager(JsonDB)
    manager.prepare()

    print("\nКнижный менеджер запущен.")
    while True:
        show_commands()
        number = input("\nВведите номер команды: ").strip()

        if not is_valid_command(number):
            continue

        manager.execute_command(number)
        if manager.keep_running():
            continue

        break


if __name__ == "__main__":
    app_config.log_dir.mkdir(exist_ok=True)
    dictConfig(LOGGERS)
    logger = getLogger()

    try:
        main()
    except KeyboardInterrupt:
        print("\nРучная остановка.")
    except Exception as error:
        logger.exception(error)
        print(f"\nНепредвиденная ошибка: {error}. Детали смотрите в логах.")
    finally:
        print("\nКнижный менеджер завершил работу.")
