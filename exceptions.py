class ValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"\n===========\nОшибка ввода команды: {self.message}\n==========="
