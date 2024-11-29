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

    def keep_running(self) -> bool:
        if self.cmd_number == "0":
            return False

        while True:
            print("\nВыберите действие:\n   1-Завершить работу\n   2-В главное меню")
            user_input = get_field("Ваш выбор: ")
            if user_input.isdigit():
                if user_input == "1":
                    return False
                elif user_input == "2":
                    return True
                else:
                    print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
            else:
                print(f'Выражение "{user_input}" не является цифрой.\n')
