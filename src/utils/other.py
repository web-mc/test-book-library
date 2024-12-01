def get_field(prompt: str) -> str:
    """
    Запрашивает у пользователя ввод данных с помощью input()
    и возвращает непустую строку.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Вы не ввели значение.")
