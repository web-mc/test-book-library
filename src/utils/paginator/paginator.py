from typing import Any

from src.utils import get_field


class Paginator:
    def __init__(self) -> None:
        self.page_size = 5
        self.page = 1
        self.len_data = 0
        self.previous_page = 0
        self.offset = 0
        self.page_data = ()
        self.keep_running = True

    def set_page(self, choice: int) -> None:
        """
        Обновляет атрибут `page`,
        чтобы он оставался в пределах допустимых значений.

        Args:
            choice (int): Выбор пользователя для навигации по страницам:
                        1 - для перехода на предыдущую страницу
                        2 - для перехода на следующую
        """

        if choice == 1:
            self.page = max(1, self.page - 1)

        if choice == 2:
            self.page = self.page if self.len_data < self.page_size else self.page + 1

    def show_page_data(self, page_data: tuple[Any, ...]) -> None:
        """
        Отрисовывает в консоли содержание страницы.
        """
        print(f"\nСтраница {self.page}:")
        for index, book in enumerate(page_data, start=1):
            msg = (
                f"{index}. id: {book[0]}, title: {book[1]}, "
                f"author: '{book[2]}', year: {book[3]}, "
                f"status: '{book[4]}'"
            )
            print(msg)

    def get_choice_from_user(self) -> int:
        print("----------------------")
        print("--- Меню пагинации ---")
        while True:
            print("--- 0. Выход | 1. Назад | 2. Вперед")
            choice = get_field("--- Введите цифру: ")
            if choice not in ["0", "1", "2"]:
                print("Некорректный ввод. Пожалуйста, введите 0, 1 или 2.")
                continue
            print("----------------------")
            return int(choice)

    def show_page_to_user(self, data: tuple[Any, ...]) -> None:
        self.show_page_data(data)

        choice = self.get_choice_from_user()
        if not choice:
            self.keep_running = False
            return

        self.set_page(choice)
