from commands import COMMANDS
from database import JsonDB
from utils import get_field


class Manager:
    def execute_command(self, nubmer: str) -> None:
        self.cmd_number = nubmer
        COMMANDS[nubmer][1](JsonDB())

    def keep_running(self) -> bool:
        if self.cmd_number == "0":
            return False

        while True:
            user_input = get_field("\nЗавершить работу? [1-Да/2-Вернуться в меню]: ")
            if user_input.isdigit():
                if user_input == "1":
                    return False
                elif user_input == "2":
                    return True
                else:
                    print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
            else:
                print(f'Выражение "{user_input}" не является цифрой.\n')
