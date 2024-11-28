from pathlib import Path


class AppConfig:
    def __init__(self) -> None:
        self.app_dir = Path(__file__).parents[1]
        self.log_dir = self.app_dir / "logs"
        self.data_dir = self.app_dir / "data"
        self.data_file = self.data_dir / "books.json"


app_config = AppConfig()
