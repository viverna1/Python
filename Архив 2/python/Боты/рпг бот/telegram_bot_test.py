data = {
    'a': [1, 2, 3],
    'b': [4, 5, 6]
}


def get_users(find, opposite=False, return_type='value'):
    """
    Извлекает информацию о пользователях из глобального словаря `data` на основе заданных параметров.

    Args:
        find (str): Искомое значение (ключ или значение), которое нужно найти в словаре `data`.
        opposite (bool, опционально): При значении True меняет целевое значение на противоположное (первое или второе значение из пары).
                                   По умолчанию False.
        return_type (str, опционально): Определяет тип данных, который нужно вернуть.
                                    Возможные значения:
                                    - 'value': Возвращает значение из пары (по умолчанию).
                                    - 'key': Возвращает ключ из пары.

    Returns:
        object: Значение или ключ из пары в словаре `data` в зависимости от заданных параметров.
                    Если искомый элемент не найден, возвращает None.
    """
    global data
    # Распаковываем элементы словаря
    (key1, values1), (key2, values2) = data.items()

    # Проверяем наличие искомого значения или ключа в значениях или ключах
    if find in values1 or find in values2:
        if return_type == 'value':
            return values1 if not opposite else values2
        elif return_type == 'key':
            return key1 if not opposite else key2
    else:
        if find in [key1, key2]:
            if return_type == 'value':
                return values1 if not opposite else values2
            elif return_type == 'key':
                return key1 if not opposite else key2


print(get_users('a', return_type='key', opposite=True))
