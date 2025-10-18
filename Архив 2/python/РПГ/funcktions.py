import random
import time
from colorama import init, Fore
import sys

init()


class Config:
    """Класс, в котором хранятся все настройки"""

    has_delay = False

    delay = {
        "move": 0.5,  # после чьего-то хода
        "death": 0.6,  # когда кто-то умер (суммируется с move)
        "start_day": 2,  # после объявления дня и статистики персонажей
        "turn_completed": 1,  # после хода 1 команды
        "day_completed": 1,  # после хода последней команды
        "mistake": 0.9  # except
    } if has_delay else {
        "move": 0,
        "death": 0,
        "start_day": 0,
        "turn_completed": 0,
        "day_completed": 0,
        "mistake": 0
    }

    start_hp = 150
    start_power = 10


class TargetMode:
    """Способы выделения целей"""

    @staticmethod
    def first_in_order(targets: list):
        """Возвращает первую цель из списка"""
        return targets[0] if targets else None

    @staticmethod
    def random_target(targets: list):
        """Возвращает случайную цель"""
        return random.choice(targets) if targets else None

    @staticmethod
    def lowest_hp(targets: list):
        """Возвращает цель с самым низким здоровьем"""
        if not targets:
            return None
        target = targets[0]
        for char1 in targets:
            if char1.health < target.health:
                target = char1
        return target

    @staticmethod
    def highest_power(targets: list):
        """Возвращает цель с самой высокой силой"""
        if not targets:
            return None
        target = targets[0]
        for char1 in targets:
            if char1.power > target.power:
                target = char1
        return target


def rand_name():
    """:return: Возвращает случайное имя"""
    names = ['Лока', 'Кирик', 'Цикада', 'Мотылек', 'Иви', 'Пинт', 'Азура', 'Зефир', 'Сирин', 'Элейн', 'Вайт', 'Лорен',
             'Зара', 'Фин', 'Эмеральд', 'Айрис', 'Скарлет', 'Найт', 'Оливия', 'Амбер', 'Зенит', 'Феликс', 'Сабина',
             'Андромеда', 'Тайга', 'Пентагон']
    return random.choice(names)


def ctext(color: str, text: any) -> str:
    """
    color: цвет | str\n
    text: текст | str
    :return: Цветной текст"""
    return getattr(Fore, color.upper()) + str(text) + Fore.RESET


def set_text_color(color: str = "LIGHTBLACK_EX"):
    print(getattr(Fore, color.upper()), end="")


def reset_text_color():
    print(Fore.RESET, end="")


def print_slow(text: str, delay: float = 0.1, end="\n"):
    """
    text: текст | str \n
    delay: задержка между буквами | float \n
    Медленно печатает текст"""
    for sym in text:
        if sym == '.':
            time.sleep(delay * 3)
        else:
            time.sleep(delay)
        sys.stdout.write(sym)
        sys.stdout.flush()
    sys.stdout.write(end)
    sys.stdout.flush()

