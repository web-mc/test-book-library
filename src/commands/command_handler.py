from typing import Callable

from src.database import Database, JsonDB

from .add_book import add_book
from .show_all_books import show_all_books
from .delete import delete_book
from .search_book import search
from .change_status import change_book_status


class Command:
    """Класс, представляющий одну команду."""

    def __init__(self, title: str, function: Callable) -> None:
        """
        Инициализация команды.
        :param title: Описание команды.
        :param function: Функция, выполняющая действие.
        """
        self.title = title
        self.run_function = function

    def execute(self, db) -> None:
        """Выполнение команды."""
        self.run_function(db)


class CommandHandler:
    """Класс для управления командами."""

    def __init__(self, db: type[Database]) -> None:
        """Инициализация обработчика команд."""
        self.db = db()
        self.cmd_number = "0"
        self.commands: dict[str, Command] = {}

    def prepare(self) -> None:
        """
        Сдесь можно выполнить всю подготовительную работу
        для корректного выполнения комманд.
        """
        self.db.prepare_db()

    def register_command(self, cmd_number: str, command: Command) -> None:
        """Регистрация новой команды."""
        self.commands[cmd_number] = command

    def execute(self, cmd_number: str) -> None:
        """Выполнение команды по её ключу."""
        self.commands[cmd_number].execute(self.db)
        self.cmd_number = cmd_number

    def show_commands(self) -> None:
        """Вывод меню команд."""
        print("\nВыбирите команду указав соответствующую цифру: ")
        for cmd_number, command in self.commands.items():
            print(f"{cmd_number}: {command.title}")

    def is_valid_command(self, cmd_number: str) -> bool:
        if not cmd_number or not cmd_number.isdigit():
            print(f'Выражение "{cmd_number}" не является цифрой.\n')
            return False

        if cmd_number not in self.commands:
            print(f"Команды с номером {cmd_number} не существует.\n")
            return False

        return True

    def exit(self) -> bool:
        if self.cmd_number == "0":
            return True

        return False


def init_handler() -> CommandHandler:
    handler = CommandHandler(JsonDB)
    handler.register_command("0", Command("Завершить работу", lambda db: False))
    handler.register_command("1", Command("Добавить книгу", add_book))
    handler.register_command("2", Command("Удалить книгу", delete_book))
    handler.register_command("3", Command("Изменить статус книги", change_book_status))
    handler.register_command("4", Command("Найти книгу", search))
    handler.register_command("5", Command("Показать все книги", show_all_books))
    return handler
