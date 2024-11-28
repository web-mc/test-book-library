from logging import getLogger
from logging.config import dictConfig

from commands import is_valid_command, show_commands
from config import LOGGERS
from manager import Manager
from utils import prepare_app


def main() -> None:
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
        print("\nПрограмма остановлена.")
    except Exception as error:
        logger.exception(error)
        print(f"\nНепредвиденная ошибка: {error}. Детали смотрите в логах.")
    finally:
        print("Книжный менеджер завершил работу.")