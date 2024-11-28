from pathlib import Path
from typing import Final

# COMMANDS: Final[dict[str, str]] = {
#     "0": "Завершить работу",
#     "1": "Добавить книгу",
#     "2": "Удалить книгу",
#     "3": "Найти книгу",
#     "4": "Показать все книги",
#     "5": "Изменить статус книги",
# }


class AppConfig:
    def __init__(self) -> None:
        self.app_dir = Path(__file__).parents[1]
        self.log_dir = self.app_dir / "logs"
        self.data_dir = self.app_dir / "data"
        self.data_file = self.data_dir / "books.json"


app_config = AppConfig()
