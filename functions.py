import json
import os
import re
from typing import Callable, Optional

import keyboard

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
            - 'grey': серый
            - 'dark_grey': тёмно-серый
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
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'grey': '\033[37m',
        'dark_grey': '\033[90m',
        'darkgrey': '\033[90m',
        'reset': '\033[0m'
    }

    if color not in colors or style not in styles:
        return str(text)  # Вывести текст без изменений, если цвет не определён
    else:
        return f"{styles[style]}{colors[color] if color != 'reset' else ''}{str(text)}\033[0m"


def remove_ansi_codes(text: str) -> str:
    """Удаляет ANSI-коды из текста

    :return текст без ANSI-кодов
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def supports_ansi() -> bool:
    """Проверяет поддержку ANSI-кодов в этой консоли.

    :return bool: True, если поддерживает ANSI-коды, иначе False.
    """
    # Проверяем версию Windows и наличие поддержки ANSI
    from ctypes import windll, byref
    from ctypes.wintypes import DWORD

    # Проверяем, поддерживает ли консоль ANSI-коды
    kernel32 = windll.kernel32
    stdout = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    mode = DWORD()
    if kernel32.GetConsoleMode(stdout, byref(mode)):
        # Проверяем, включена ли поддержка ANSI-кодов
        return (mode.value & 0x0004) != 0  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    return False


def format_readable_count(count: int, option1: str, option2: str, option3: str) -> str:
    """
    Форматирует число с правильным окончанием существительного, зависящего от числа.

    Аргументы:
    - count (int): Число, к которому применяется форматирование.
    - Option1 (str): Опция для существительного с окончанием при числе 1.
    - Option2 (str): Опция для существительного с окончанием при числе 2.
    - Option3 (str): Опция для существительного с окончанием при числе 5.

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

    return f"{suffix}"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def update_console(*args):
    clear_console()
    print(*args)


def choose_menu(options: list[str], title: str = "Выберите опцию:", start_index: int = 0,
                select_count: int = 1, centered: bool = False, descriptions: list[str] = None,
                default_input: bool = False) -> int | list[int]:
    """
    Функция для выбора одного или нескольких пунктов из меню.

    :param options: Список строк, представляющих пункты меню.
    :param title: Заголовок меню (по умолчанию "Выберите вариант:").
    :param start_index: Индекс пункта, который будет выбран по умолчанию (по умолчанию 0).
    :param select_count: Количество пунктов, которые можно выбрать (по умолчанию 1).
    :param centered: Если True, меню будет центрировано (по умолчанию False).
    :param descriptions: Список описаний пунктов меню (по умолчанию пустой).
    :param default_input: Вместо интерактивного списка, будет обычный с цифрами (по умолчанию False).
    :return: Индекс выбранного пункта или список индексов, если select_count > 1.
             Возвращает -1, если пользователь нажал esc.
    """
    # Режим отладки: использование текстового ввода вместо интерактивного меню
    if default_input:
        report = ""
        choiced_indexes = []
        select_count = min(select_count, len(options))
        select_count_remaining = select_count

        while select_count_remaining > 0:
            # Отображаем меню
            output2 = f"{title}\n"
            for i2, option2 in enumerate(options):
                output2 += f"{i2 + 1}. {option2}\n"
            output2 += report
            update_console(output2)

            # Запрашиваем ввод пользователя
            prompt = ("Введите номер варианта (0 - Назад): " if not choiced_indexes else
                      f"{title}\nВыбрано: {', '.join(map(lambda x: str(x + 1), choiced_indexes))}, : ")
            str_option = input(prompt)

            # Проверяем корректность ввода
            if not str_option.isdigit():
                report = ctext("Некорректный ввод. Пожалуйста, введите число.", "red")
                continue

            choiced_index = int(str_option)

            # Проверяем, что введённый номер находится в допустимом диапазоне
            if not -1 <= choiced_index <= len(options):
                report = ctext(f'Некорректный ввод. Пожалуйста, введите число в диапазоне от 1 до {len(options)}',
                               'red')
                continue

            # Проверяем, что пункт ещё не выбран
            if choiced_index - 1 in choiced_indexes:
                report = ctext("Вы уже выбрали этот вариант.", "red")
                continue

            # Добавляем выбранный пункт в список
            choiced_indexes.append(choiced_index - 1)
            select_count_remaining -= 1

        # Возвращаем результат
        return choiced_indexes[0] if select_count == 1 else choiced_indexes

    # Основной режим: интерактивное меню с использованием стрелочек
    else:
        select_count = min(select_count, len(options))
        choiced_indexes = [i for i in range(start_index, start_index + select_count)]

        # Находим строку с максимальной длиной для центрирования
        longest_option = len(max(map(remove_ansi_codes, options), key=len)) + 10

        def display_menu():
            """Отображает текущее состояние меню."""
            nonlocal choiced_indexes
            if centered:
                output = f"\n{f'{title}':^{longest_option}}\n"
            else:
                output = title + "\n"

            for i, option in enumerate(options):
                prefix = "> " if i in choiced_indexes else "  "
                suffix = " <" if i in choiced_indexes else "  "
                formatted_option = f"{prefix}{option}{suffix}"

                # Выравниваем пункт меню, если нужно
                if centered:
                    clean_option = remove_ansi_codes(formatted_option)
                    padding = (longest_option - len(clean_option)) // 2
                    formatted_option = " " * padding + formatted_option

                output += formatted_option + "\n"

            formated_output = output + ("\n" + descriptions[choiced_indexes[0]]
                                        if descriptions and choiced_indexes[0] + 1 <= len(descriptions) else "")
            update_console(formated_output)

        def up():
            """Перемещает выбор на пункт вверх."""
            nonlocal choiced_indexes
            choiced_indexes = [(idx - 1) % len(options) for idx in choiced_indexes]
            display_menu()

        def down():
            """Перемещает выбор на пункт вниз."""
            nonlocal choiced_indexes
            choiced_indexes = [(idx + 1) % len(options) for idx in choiced_indexes]
            display_menu()

        def wait_for_keys(*keys):
            """Ожидает нажатия одной из указанных клавиш."""
            while True:
                key_event = keyboard.read_event()
                if key_event.event_type == keyboard.KEY_DOWN and key_event.name in keys:
                    return key_event

        # Отображаем меню впервые
        display_menu()

        # Привязываем клавиши
        keyboard.add_hotkey('up', up)
        keyboard.add_hotkey('down', down)

        # Ждём подтверждения или выхода
        event = wait_for_keys('esc', 'space', 'enter')

        # Чистим клавиши после выбора
        keyboard.unhook_all_hotkeys()

        # Возвращаем результат
        if event.name == 'esc':
            return -1  # Пользователь выбрал "Назад"

        if select_count == 1:
            return choiced_indexes[0]  # Возвращаем один выбранный индекс
        return choiced_indexes  # Возвращаем список выбранных индексов



def validated_input(
        prompt: str = "",
        parse_func: Callable[[str], any] = str,
        allow_blank: bool = False
    ) -> Optional[any]:
    """
    Запрашивает и проверяет пользовательский ввод.

    :param prompt: (str): Сообщение-приглашение для ввода.
    :param parse_func: (Callable): Функция для преобразования и валидации ввода.
    :param allow_blank: (bool): Разрешить пустой ввод.

    :return Результат ввода, преобразованный parse_func, или None если разрешен пустой ввод.
    """
    while True:
        try:
            user_input = input(prompt).strip()

            # Обрабатываем пустой ввод
            if not user_input:
                if allow_blank:
                    return None
                print("Поле не может быть пустым. Пожалуйста, введите значение.")
                continue

            # Пытаемся преобразовать и проверить ввод
            result = parse_func(user_input)
            return result

        except ValueError:
            print(f"Неверный формат. Ожидается: {parse_func.__name__}. Попробуйте еще раз.")
        except KeyboardInterrupt:
            print("\nОперация отменена.")
            return None
        except Exception as error:
            print(f"Произошла ошибка: {error}. Попробуйте еще раз.")

# Примеры использования validated_input:
if __name__ == "__main__":
    # Запрос числа (обязательный)
    age = validated_input("Сколько вам лет? ", parse_func=int)
    print(f"Возраст: {age}")

    # Запрос числа с плавающей точкой (необязательный)
    weight = validated_input("Ваш вес (кг, можно пропустить): ", parse_func=float, allow_blank=True)
    print(f"Вес: {weight}")

    # Запрос обычной строки
    name = validated_input("Ваше имя: ")
    print(f"Имя: {name}")

    # Запрос булевого значения
    def parse_bool(text: str) -> bool:
        if text.lower() in ['да', 'yes', 'true', '1', 'y']:
            return True
        elif text.lower() in ['нет', 'no', 'false', '0', 'n']:
            return False
        raise ValueError("Введите 'да' или 'нет'")

    is_active = validated_input("Активен? (да/нет): ", parse_func=parse_bool)
    print(f"Активен: {is_active}")


# Проверка через __module__
def is_builtin_function(func):
    """Проверяет, является ли функция встроенной или из стандартной библиотеки"""
    if not hasattr(func, '__module__'):
        return True  # Встроенные функции типа len, print не имеют __module__

    module_name = func.__module__

    # Встроенные функции и функции из стандартной библиотеки
    builtin_modules = {
        None,  # Встроенные функции (C implementation)
        'builtins',  # Встроенные функции
        'math', 'os', 'sys', 're', 'json',  # Стандартные модули
        'datetime', 'collections', 'itertools'  # и другие...
    }

    return module_name in builtin_modules or module_name.startswith('_') or module_name is None
