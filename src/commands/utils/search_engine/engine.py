import re
from functools import cached_property
from itertools import islice
from typing import Any, Callable

from src.commands.utils import Paginator
from src.database import Database
from src.utils import get_field


class SearchEngine:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.stay_in_menu = True

    @cached_property
    def search_options(self) -> dict[int, tuple[str, Callable]]:
        return {
            1: ("Справка по поиску", self._show_help),
            2: ("Поиск по названию", self._search_by_title),
            3: ("Поиск по автору", self._search_by_author),
            4: ("Поиск по году", self._search_by_year),
        }

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

    # def stay_in_menu(self):
    def search(self, option: int) -> None:
        if option == 1:
            self.stay_in_menu = True
        else:
            self.stay_in_menu = False

        self.search_options[option][1]()

    def _search_by_title(self) -> None:
        pass

    def _search_by_author(self) -> None:
        pass

    def _search_by_year(self) -> None:
        print("Поиск по году начат. Введите условие поиска.")

        while True:
            msg = "Поиск по году. Введите условие поиска или '0' для выхода в меню поиска: "
            condition = get_field(msg)

            if condition == "0":
                self.stay_in_menu = True
                return

            search_results = self._get_search_results(condition)
            if not search_results:
                continue

            self._show_results(search_results)

    def _show_results(self, search_results: tuple[Any, ...]) -> None:
        paginator = Paginator()
        while True:
            page_data = self._set_page_data(search_results, paginator)
            paginator.show_page_to_user(page_data)

            if not paginator.keep_running:
                return

    def _get_search_results(self, condition: str) -> None | tuple[Any, ...]:
        condition_data = self._parse_condition(condition)
        if not condition_data:
            print("Некорректное условие для поиска. Смотрите справку.")
            return

        books = self.db.get_books_by_year(condition_data)
        if not books:
            print(f"Не нашлось книг по условию '{condition}'.\n")

        return books

    def _parse_condition(self, condition: str) -> None | tuple[str, *tuple[int, ...]]:
        pattern = r"^[=<>-]\d+,?[\d+]?"
        res = re.match(pattern, condition)
        if not res:
            return None

        symbols = re.match(r"^[<>=-]", condition).group()  # type: ignore
        years = condition.replace(symbols, "").split(",")

        if symbols == "-":
            start, end = years[0], years[1]
            if int(start) > int(end):
                print(
                    f"\nОшибка. {start} не меньше {end}. "
                    f"Может хотели '-{end},{start}'?"
                )
                return

        return (symbols, *[int(year) for year in years])

    def _set_page_data(
        self, books: tuple[Any, ...], paginator: Paginator
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
