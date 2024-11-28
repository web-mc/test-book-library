import json
from hashlib import md5
from logging import getLogger

from config import app_config
from exceptions import ValidationError

logger = getLogger()


class Book:
    def __init__(self) -> None:
        self.id: str = ""
        self.title: str = ""
        self.author: str = ""
        self.year: str = ""
        self.status: str = "в наличии"

    def generate_book_id(self) -> None:
        str_to_hash = f"{self.title}{self.author}{self.year}"
        str_to_hash = "".join(char for char in str_to_hash if char.isalnum())
        self.id = md5(str_to_hash.encode("utf-8")).hexdigest()


class Manager:
    commands = {
        "0": "Завершить работу",
        "1": "Добавить книгу",
        "2": "Удалить книгу",
        "3": "Найти книгу",
        "4": "Показать все книги",
        "5": "Изменить статус книги",
    }


    # def _load_unique_index(self):
    #     with open(app_config.data_file, "r", encoding="utf-8") as json_file:
    #         return json.load(json_file)["unique_book_index"]


    def run_command(self, nubmer: str) -> bool:
        if nubmer == "0":
            return False

        if nubmer == "1":
            _add_book()

        return True


def _add_book() -> None:
    print("\nНачато добавление книги.")
    book = _get_new_book_from_user()
    book.generate_book_id()
    # check_duplication(book.id)
    # save_book(book)
    print(f"\nКнига добавлена в библиотеку.\nID книги '{book.id}'")


def get_field(prompt) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Вы не ввели значение.\n")


def _get_new_book_from_user() -> Book:
    book = Book()
    book.title = get_field("Введите название книги: ")
    book.author = get_field("Введите автора книги: ")
    while True:
        year = get_field("Введите год книги(только цифры): ")
        if year.isdigit():
            book.year = year
            break
        print(f'Выражение "{year}" не является цифрой.\n')
    return book
