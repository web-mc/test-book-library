from .commands import COMMANDS
from .database import Database
from .utils import get_field


class Manager:
    def __init__(self, db: type[Database]) -> None:
        self.db = db

    def prepare(self) -> None:
        """
        Сдесь можно выполнить всю подготовительную работу
        для корректной работы приложения.
        """
        self.db.prepare_db()

    def execute_command(self, nubmer: str) -> None:
        """
        Извлекает команду, связанную с данным номером,
        из словаря COMMANDS и выполняет её, используя экземпляр базы данных.

        nubmer (str): Номер команды, которую необходимо выполнить.
        """
        self.cmd_number = nubmer
        COMMANDS[nubmer][1](self.db())

    def exit(self) -> bool:
        if self.cmd_number == "0":
            return True

        return False
