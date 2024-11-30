def calculate_levenshtein_distance(string1: str, string2: str) -> int:
    """
    Вычисляет расстояние Левенштейна между двумя строками.
    Возвращает минимальное количество операций
    для преобразования одной строки в другую.
    """
    length1, length2 = len(string1), len(string2)

    # Создаём матрицу для хранения результатов
    distance_table = [[0 for _ in range(length2 + 1)] for _ in range(length1 + 1)]

    # Инициализируем первую строку и первый столбец таблицы
    for row in range(length1 + 1):
        for col in range(length2 + 1):
            if row == 0:
                # Если первая строка пустая, нужно вставить все символы второй строки
                distance_table[row][col] = col
            elif col == 0:
                # Если вторая строка пустая, нужно удалить все символы первой строки
                distance_table[row][col] = row
            elif string1[row - 1] == string2[col - 1]:
                # Символы совпадают, операция не требуется
                distance_table[row][col] = distance_table[row - 1][col - 1]
            else:
                # Символы не совпадают, выбираем минимальную стоимость операции
                insert_cost = distance_table[row][col - 1]  # Вставка
                delete_cost = distance_table[row - 1][col]  # Удаление
                replace_cost = distance_table[row - 1][col - 1]  # Замена
                distance_table[row][col] = 1 + min(
                    insert_cost, delete_cost, replace_cost
                )

    return distance_table[length1][length2]


def str_similarity_percent(str_1: str, str_2: str) -> float:
    """
    Определяет процент похожести между строками на основе расстояния Левенштейна.
    """
    max_len = max(len(str_1), len(str_2))
    distance = calculate_levenshtein_distance(str_1, str_2)
    percent = (1 - distance / max_len) * 100
    return round(percent, 2)
