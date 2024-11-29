from logging import getLogger
from logging.config import dictConfig

from src.commands import is_valid_command, show_commands
from src.config import LOGGERS
from src.manager import Manager
from src.utils import prepare_app


def main() -> None:
    """
    Точка входа для приложения.

    Создает экземпляр Manager, выводит список доступных команд,
    получает ввод от пользователя, обрабатывает команды и
    останавливает приложение, если пользователь выбрал соответствующую команду.
    """
    manager = Manager()

    print("\nКнижный менеджер запущен.\n")
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
    prepare_app()

    dictConfig(LOGGERS)
    logger = getLogger()
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        logger.exception(error)
        print(f"\nНепредвиденная ошибка: {error}. Детали смотрите в логах.")
    finally:
        print("\nКнижный менеджер завершил работу.")
