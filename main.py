from logging import getLogger
from logging.config import dictConfig

from book_manager import Manager
from config import LOGGERS
from exceptions import ValidationError
from utils.other import prepare_app, show_menu, validate_number


def main() -> None:
    manager = Manager()

    print("\nКнижный менеджер запущен.\n")
    while True:
        show_menu()
        number = input("\nВведите номер команды: ").strip()

        try:
            validate_number(number)
        except ValidationError as error:
            print(error)
            continue

        if not manager.run_command(number):
            return

        keep_running = input("\nЗавершить работу? [1-Да/2-Нет]: ").strip()
        if keep_running == "1":
            return


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
