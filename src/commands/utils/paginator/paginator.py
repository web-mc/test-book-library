from typing import Any


class Paginator:
    def __init__(self) -> None:
        self.page_size = 5
        self.page = 1
        self.len_data = 0
        self.previous_page = 0
        self.offset = 0
        self.page_data = ()

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
