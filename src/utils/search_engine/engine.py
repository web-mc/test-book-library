import re
from itertools import islice
from typing import Any, Callable, Generator

from src.database import Database
from src.utils import Paginator, get_field

from .text import calculate_similarity


class Command:
    """Класс, представляющий одну команду."""

    def __init__(self, title: str, function: Callable) -> None:
        """
        Инициализация команды.
        :param title: Описание команды.
        :param function: Функция, выполняющая действие.
        """
        self.title: str = title
        self.run_function = function

    def execute(self) -> tuple[Any, ...]:
        """Выполнение команды."""
        return self.run_function()


class SearchEngine:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.stay_in_menu = True
        self.commands: dict[str, Command] = {}
        self._init_commands()

    def run_search(self, cmd_number: str) -> tuple[Any, ...]:
        if cmd_number == "0":
            self.stay_in_menu = False
            return ()

        return self.commands[cmd_number].execute()

    def _init_commands(self) -> None:
        self._register_command("1", Command("Справка по поиску", self._show_help))
        self._register_command("2", Command("Поиск по названию", self._search_by_title))
        self._register_command("3", Command("Поиск по автору", self._search_by_author))
        self._register_command("4", Command("Поиск по году", self._search_by_year))

    def list_commands(self) -> list[tuple[str, str]]:
        list_commands = []
        for cmd_number, cmd in self.commands.items():
            list_commands.append((cmd_number, cmd.title))

        return list_commands

    def _register_command(self, cmd_number: str, command: Command) -> None:
        """Регистрация новой команды."""
        self.commands[cmd_number] = command

    def execute(self, cmd_number: str) -> None:
        """Выполнение команды по её ключу."""
        self.commands[cmd_number].execute()
        self.cmd_number = cmd_number

    def _show_help(self) -> None:
        year_help = (
            "=== 1. Доступные условия для поиска по году:\n"
            "=== '>year' от года включительно.\n"
            "=== '<year' до года включительно.\n"
            "=== '=year' год равен.\n"
            "=== '-start,end' между годами включительно.\n"
            "=== Примеры:\n"
            "=== '>1990' - Искать книги с годом от 1990.\n"
            "=== '-1990,2000' - Искать книги с годом между 1990 и 2000.\n"
            "======================================================\n"
        )

        text_help = (
            "=== 2. Поиск по автору или названию книги.\n"
            "=== Для поиска по автору или названию книги достаточно ввести текст.\n"
            "=== В результатах поиска будут показаны наиболее подходящие книги.\n"
            "=== Более похожие книги к вашему запросу будут выше в списке.\n"
            "=== Всего в результатах поиска показывается до 15 книг.\n"
            "======================================================"
        )

        print("**** [Справка по поиску] ****")
        print(year_help)
        print(text_help)

    def _search_by(self, search_type: str) -> tuple[Any, ...]:
        title = f"Поиск по {search_type}"

        while True:
            msg = f"{title}. Введите условие поиска или '0' для выхода в меню поиска: "
            request = get_field(msg)

            if request == "0":
                return ()

            books = self.db.get_all_books()
            if not books:
                print("В библиотеке нет книг.")
                return ()

            result = self._sort_by_similarity(request, search_type, books)
            return result

    def _search_by_author(self) -> tuple[Any, ...]:
        return self._search_by("author")

    def _search_by_title(self) -> tuple[Any, ...]:
        return self._search_by("title")

    def _sort_by_similarity(
        self,
        request: str,
        attribute: str,
        books: Generator[Any, None, None],
    ) -> tuple[Any, ...]:
        # 1 - проходимся по книгам и сортируем по убыванию похожести по нужным атрибутам
        # 2 - возвращаем 15 первых результатов
        result = []
        attributes = {"title": 1, "author": 2}
        for book in books:
            request = self._clean_string(request)

            # получаем из книги указаный атрибут по индексу
            book_atr_value = self._clean_string(book[attributes[attribute]])

            book += (calculate_similarity(request, book_atr_value),)
            result.append(book)

        result = self._quick_sort(result)
        return tuple(book for book in result[:15])

    def _clean_string(self, string: str) -> str:
        result = ""
        for char in string:
            if char.isalnum():
                result += char
        return result.lower()

    def _quick_sort(self, books: list[tuple[Any, ...]]) -> list[tuple[Any, ...]]:
        # Сортируем по убыванию похожести

        if len(books) <= 1:
            return books

        pivot = books[len(books) // 2][5]  # Сравниваем по второму элементу в кортеже

        left = [x for x in books if x[5] > pivot]
        middle = [x for x in books if x[5] == pivot]
        right = [x for x in books if x[5] < pivot]

        return self._quick_sort(left) + middle + self._quick_sort(right)

    def _search_by_year(self) -> tuple[Any, ...]:
        title = "Поиск по году"

        while True:
            msg = f"{title}. Введите условие поиска или '0' для выхода в меню поиска: "
            condition = get_field(msg)

            if condition == "0":
                return ()

            condition_data = self._parse_year_condition(title, condition)
            if not condition_data:
                print(f"{title}. Некорректное условие для поиска. Смотрите справку.")
                continue

            books = self.db.get_books_by_year(condition_data)
            if not books:
                print(f"{title}. Не нашлось книг по условию '{condition}'.")
                continue

            return books

    def show_results(self, search_results: tuple[Any, ...]) -> None:
        paginator = Paginator()
        while True:
            page_data = self._set_page_data(search_results, paginator)
            paginator.show_page_to_user(page_data)

            if not paginator.keep_running:
                return

    def _parse_year_condition(
        self,
        title: str,
        condition: str,
    ) -> None | tuple[str, *tuple[int, ...]]:
        pattern = r"^[=<>-]\d+,?[\d+]?"
        res = re.match(pattern, condition)
        if not res:
            return

        symbol = re.match(r"^[<>=-]", condition).group()  # type: ignore
        years = condition.replace(symbol, "").split(",")

        # Для проверки правильности введённого диапазона
        if symbol == "-":
            start, end = years[0], years[1]
            if int(start) > int(end):
                print(
                    f"\n{title}. Ошибка. {start} не меньше {end}. "
                    f"Может хотели '-{end},{start}'?"
                )
                return

        return (symbol, *[int(year) for year in years])

    def _set_page_data(
        self,
        books: tuple[Any, ...],
        paginator: Paginator,
    ) -> tuple[Any, ...]:
        """
        Проверяет, совпадает ли текущая страница с предыдущей,
        чтобы избежать повторного извлечения данных. Если страница изменилась,
        он вычисляет смещение на основе текущей страницы и размера страницы,
        извлекает данные из базы данных и обновляет кэш и длину данных.
        """
        if paginator.previous_page == paginator.page:
            return paginator.page_data

        offset = (paginator.page * paginator.page_size) - paginator.page_size
        data = tuple(islice(books, offset, offset + paginator.page_size))

        if data:
            paginator.page_data = data
            paginator.len_data = len(data)
            paginator.previous_page = paginator.page

        return data
