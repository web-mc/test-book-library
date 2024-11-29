from src.database import Database


class Paginator:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.page_size = 5
        self.page = 1
        self.len_data = 0
        self.previos_page = 0
        self.page_data = ()

    def get_page_data(self) -> None:
        # Чтобы не вызывать заново функцию листая назад на 1 странице
        # и вперед на последней странице
        # Отслеживаем номер предыдущей страницы
        if self.previos_page == self.page:
            data = self.page_data
        else:
            offset = (self.page * self.page_size) - self.page_size
            data = self.db.get_part_data(offset, self.page_size)

            self.previos_page = self.page
            self.page_data = data
            self.len_data = len(data)

    def set_page(self, choice: int) -> None:
        if choice == 1:
            self.page = max(1, self.page - 1)

        if choice == 2:
            self.page = self.page if self.len_data < self.page_size else self.page + 1

    def show_page_data(self) -> None:
        print(f"\nСтраница {self.page}:")
        for index, book in enumerate(self.page_data, start=1):
            self.db
            msg = (
                f"{index}. id: {book[0]}, title: {book[1]}, "
                f"author: '{book[2]}', year: {book[3]}, "
                f"status: '{book[4]}'"
            )
            print(msg)
