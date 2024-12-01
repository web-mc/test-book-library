from logging import getLogger
from logging.config import dictConfig

from src.command_handler import init_handler
from src.config import LOGGERS, app_config


def main() -> None:
    """
    Точка входа для приложения.

    Создает экземпляр CommandHandler, выводит список доступных команд,
    получает ввод от пользователя, обрабатывает команды и
    останавливает приложение, если пользователь выбрал соответствующую команду.
    """
    handler = init_handler()
    handler.prepare()

    print("\nКнижный менеджер запущен.")
    while True:
        handler.show_commands()
        command = input("\nВведите номер команды: ").strip()

        if not handler.is_valid_command(command):
            continue

        handler.execute(command)
        if not handler.exit():
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
        print(f"\nНепредвиденная ошибка:\n{error}\nДетали смотрите в логах.")
    finally:
        print("\nКнижный менеджер завершил работу.")
