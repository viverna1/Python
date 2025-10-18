import re
import random
# import matplotlib.pyplot as plt
# import numpy as np


# webbrowser.open("http://www.example.com")  # Открытие URL в браузере

def ctext_param(r1, g1, b1, r2, g2, b2, text):
    return f"\033[38;2;{r1};{g1};{b1};48;2;{r2};{g2};{b2}m{text}\033[0m"


def ctext(text: any, color: str = 'reset', style: str = 'reset') -> str:
    """Описание:
        Функция позволяет выводить текст определенным цветом и стилем в терминале.

    Аргументы:
        text (any): Текст, который нужно вывести с определенным цветом и стилем
        color (str): Цвет текста. Может принимать следующие значения:
            - 'black': черный
            - 'red': красный
            - 'green': зеленый
            - 'yellow': желтый
            - 'blue': синий
            - 'purple': фиолетовый
            - 'cyan': голубой
            - 'white': белый
            - 'reset': сбросить цвет на стандартный (по умолчанию)
        style (str): Стиль текста. Может принимать следующие значения:
            - 'bold': жирный
            - 'italic': курсивный
            - 'underline': подчеркнутый
            - 'strikethrough': зачёркнутый
            - 'frame': текст в рамке
            - 'reset': сбросить стиль на стандартный (по умолчанию)

    Возвращает:
        str: Строка с примененным к ней цветом и стилем.
    """
    styles = {
        'bold': '\033[1m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'strikethrough': '\033[9m',
        'frame': '\033[51m',
        'reset': '\033[0m'
    }
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'grey': '\033[37m',
        'darkgrey': '\033[90m',
        'reset': '\033[0m'
    }

    if color not in colors or style not in styles:
        return str(text)  # Вывести текст без изменений, если цвет не определён
    else:
        return f"{styles[style]}{colors[color] if color != 'reset' else ''}{str(text)}\033[0m"


def cursor_shift(code: str):
    """
    Управляет движением курсора:
    u - вверх
    l - влево
    r - вправо
    Формат ввода: команда и шаг через пробел, например: '4u 1l'.
    """
    move_map = {
        "u": "A",  # Вверх
        "l": "D",  # Влево
        "r": "C",  # Вправо
    }

    # Разделение входной строки на команды
    commands = code.split()

    # Проходим по каждой команде
    for command in commands:
        step, direction = command[:-1], command[-1]

        # Получаем нужный код из move_map
        if direction in move_map:
            print(f"\033[{step}{move_map[direction]}")
        else:
            print(f"Неверная команда: {command}")


def format_readable_count(count, option1, option2, option3):
    """
    Форматирует число с правильным окончанием существительного, зависящего от числа.

    Аргументы:
    - count (int): Число, к которому применяется форматирование.
    - Option1 (str): Опция для существительного с окончанием при числе 1.
    - Option2 (str): Опция для существительного с окончанием при числах 2, 3, 4.
    - Option3 (str): Опция для существительного с окончанием при остальных числах.

    Возвращает:
    str: Строка, содержащая отформатированное число и соответствующее существительное с правильным окончанием.
    """
    last_digit = count % 10
    last_two_digits = count % 100

    if last_digit == 1 and last_two_digits != 11:
        suffix = option1
    elif 2 <= last_digit <= 4 and (last_two_digits < 10 or last_two_digits >= 20):
        suffix = option2
    else:
        suffix = option3

    return f"{count} {suffix}"


if __name__ == '__main__':
    # Пример использования
    print(ctext("Этот наклонённый текст красного цвета!", 'red', 'italic'))
    print(ctext("Этот текст зелёного цвета!", 'green'))


def remove_unnecessary_spaces():
    with open('main.py', 'r', encoding='utf-8') as f:
        res = []
        spaces_num = 0
        for line in f:
            if line == '\n':
                spaces_num += 1
            if not line.startswith('    ') and line != '\n':
                res.append(line)
                spaces_num = 0  # Обнуляем счетчик пустых строк при добавлении непустой строки
            elif line == '\n' and spaces_num < 3:  # Изменено условие на spaces_num < 2
                res.append(line)
    return res


def ansi_to_html(text):
    """
    Преобразует ANSI Escape-коды в HTML-теги для цвета текста.

    Args:
        text (str): Исходный текст с ANSI Escape-кодами.

    Returns:
        str: Текст с HTML-тегами для цвета текста.
    """
    # Заменяем ANSI Escape-коды на HTML-теги
    text = re.sub(r'\033\[(\d+)m(.*?)\033\[0m',
                  lambda
                      match: f'<span style="color: {ansi_to_html_color(int(match.group(1)))}">{match.group(2)}</span>',
                  text)
    return text


def ansi_to_html_color(ansi_code):
    """
    Преобразует ANSI Escape-коды цветов в их эквиваленты для HTML.

    Args:
        ansi_code (int): ANSI Escape-код цвета.

    Returns:
        str: Строка с названием цвета для HTML стилей.
    """
    # Маппинг ANSI Escape-кодов на соответствующие цвета HTML
    color_map = {
        30: 'black',
        31: 'red',
        32: 'green',
        33: 'yellow',
        34: 'blue',
        35: 'magenta',
        36: 'cyan',
        37: 'white'
    }
    # Если анси код не соответствует цвету, возвращаем черный цвет
    return color_map.get(ansi_code, 'white')


if __name__ == '__main__':
    # Пример использования
    ansi_text = "\033[32mThis is red text\033[0m"
    html_text = ansi_to_html(ansi_text)
    print(html_text)


def generate_random_key():
    basic = [1, 2, 3]
    result = [(random.choice(basic), random.choice(basic))]
    for i in range(random.randint(3, 8)):
        result.append((random.choice(basic), random.choice(basic)))
    return zip(*result)


def generate_points():
    # Определение диапазона значений
    range_values = np.arange(1, 4)
    # Создание координатной сетки
    X, Y = np.meshgrid(range_values, range_values)
    # Объединение координат в один массив и преобразование к нужной форме
    points = np.vstack([X.ravel(), Y.ravel()]).T
    return points[:, 0], points[:, 1]


def ai_list_generator():
    x, y = generate_random_key()
    x_point, y_point = generate_points()
    plt.scatter(x_point, y_point)
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    ai_list_generator()
