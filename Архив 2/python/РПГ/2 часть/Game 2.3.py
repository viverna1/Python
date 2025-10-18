try:
    import math
    import copy
    import re
    import os
    import random
    import sys
    import threading
    import time
    import keyboard
    from typing import Self, Callable, Any
    from collections import Counter
    from types import MethodType
except ModuleNotFoundError as e:
    module_name = re.search(r"'(.*?)'", str(e)).group(1)
    print(f"Не установлена библиотека '{module_name}'")
    input()
    sys.exit(1)

# TODO:
# Код:
#   ❌ Написать документацию!!!
#   🟰 Сделать испытания, там будет фиксированная команда, и её нельзя будет изменять, или это будут пазлы
#   ❌ Сохранения.
#   ❌ Год мод не работает. Добавить обратно is_ally. Оно есть также в generate_team
#   ✅ Карту с уровнями.
#   ✅ Пауза и перезапуск.
#   ✅ Сделать ценность юнитов и автоматический сбор команды
#   ✅ дать игроку возможность самому собирать команду
#   ✅ доработать centered в choose_from_menu
#   ✅ Переделать код так, чтобы при каждом запуске очищалась консоль.
#   ✅ Добавить меню

# Недописанная документация:
#   ❌ player_move
#   ❌ set_units_level
#   ❌ set_units_in_team
#   ❌ set_units_names
#   ❌ set_team
#   ❌ GameConfig
#   ❌ TargetMode
#   ❌ Challenges
#   ✅ Ai
#   ❌ new_game
#   ❌ continue_game
#   ❌ debug
#   ❌ UnitBehaviour
#   ❌ UnitBehaviour.Actions

# Бот:
#   ❌ Сделать Minimax 👑
#   ✅ Реализовать метод script_move в классе Ai
#   ✅ Создать класс Ai
#   ✅ Переделать evaluation для Ai

# Баги:
#   ✅ После последнего хода игрока обновлялась консоль
#   ✅ Баг с 0 урона
#   ✅ На esc пропускается ход
#   ✅ после смерти пешка остаётся в целях для игрока
#   ✅ Вылет игры, при игре без anci, после первого дня
#   ✅ При выходе в меню сбрасывается потраченные очки улучшений.
#   ✅ Переделать get_all_moves

# Юниты:
#   ❌ Добавить больше персонажей
#   ❌ ? Турелям можно менять способ нахождения цели.
#   ✅ Реализовать КД для третьей способности.
#   ✅ Реализовать нормальный показ характеристик, а не (can_move: True, shield: 0)
#   ✅ Добавить кнопку для перехода на следующий день (в интерфейсе)
#   ✅ Добавить инициализацию уровней персонажей

# Идеи
#   ❌ 🖤 Проклятье: если пешка делает ход, она получает урон
#   ❌ Шипы: поражают только милеров
#   ❌ 🎲 Рандом: может произойти что угодно
#   ❌ 📀 Турель, которая принимает весь урона нв себя
#   ❌ ✨ Турель, восстанавливающая ходы.
#   ❌ Турель с одним хп, которая ставит усиление каждого минимум на 2
#   ❌ 🪞 Невидимость
#   ❌ Возможность забирать возможность хода юнита.
#   ❌ Сбивать усиления противника
...


# Юниты и турели:
class Character:
    """
    Атрибуты:
        - name: Имя, по умолчанию выдается случайное имя
        - max_health: Максимальное здоровье
        - health: Текущее здоровье
        - power: сила, урон и возможно не только
        - cost: стоимость юнита, зависит от его силы и уровня и используется для генерации команды
        - level: Уровень персонажа, чем больше уровень, тем больше ему доступно действий
        - alive: bool жив ли персонаж
        - can_move: может ли персонаж делать ход

        - specials: словарь в котором описаны особенности юнита такие, как поднят ли щит или усиление
        - class_titles: список заголовков класса персонажа [кто, кого, кому]
        - positive_actions: список, элементы которого означают какие действия положительные [True, False, True]
        - targets_count: список чисел, в котором количество целей может быть разным для каждого действия [1, 1, 2]
        - moves_names: список названий способностей
        - actions_info: список описаний способностей
        - initial_abilities_cooldown: список с максимальным количеством ходов до отката способности
        - abilities_cooldown:список с количеством ходов до отката способности

    Методы:
        - __call__(num, cross=False, raw): Возвращает строковое представление персонажа с учетом класса.
        - __str__(): Возвращает полную информацию о персонаже.
        - move(action_type, target, report=True): Выполняет действие персонажа.
        - action1(targets, report=True): Первое действие персонажа (переопределяется в подклассе).
        - action2(targets, report=True): Второе действие персонажа (переопределяется в подклассе).
        - action3(targets, report=True): Третье действие персонажа (переопределяется в подклассе).
        - algorithm(ally_team, enemy_team): алгоритм по которому будет следовать юнит при скриптовом ходе бота (переопределяется в подклассе).
        - take_damage(damage, report=True): Применяет урон к персонажу.
        - after_move(): Восстанавливает возможность персонажа ходить.

        - info(): Возвращает полную информацию о персонаже и его способностях.
        - get_move_names(): Возвращает названия доступных способностей в зависимости от уровня.
        - get_targets_count(action_index): Возвращает количество целей для выбранного действия.
        - is_positive_action(action_index): Проверяет, является ли действие положительным.
        - can_make_this_move(action_index, target): проверка на возможность совершить это действие с учётом кд.
        - can_make_move(action_index, target): проверка на возможность совершить это действие (переопределяется в подклассе).
        - has_specials(): Определяет, есть ли у персонажа активные особенности (щит, усиление, ...).
    """

    # Базовые:
    def __init__(self,
                 max_health: int = None,
                 power: int = None,
                 name: str = None,
                 level: int = None,
                 max_level: int = None,
                 cost: int = None,
                 behaviors: list[str] = None,
                 class_titles: list[str] = None,
                 algorithm: Callable = None):
        self._max_health: int = max_health or GameConfig.config["default_hp"]
        self._health: int = self._max_health
        self._power: int = power or GameConfig.config["default_damage"]
        self._name: str = name or rand_name()
        self._level: int = level
        self.alive: bool = True
        self.can_move: bool = True

        self.specials: dict = {
            "shield": 0,
            "power_multiplier": 1
        }

        self.behaviors: list[str] = behaviors

        self.class_titles: list[str] = class_titles or ["default_class", "default_class", "default_class"]
        self._max_level: int = max_level or 3
        self._level = level or 1
        self._cost: int = cost or 0

        self.initial_abilities_cooldown: list[int] = [0, 0, 0]
        self.abilities_cooldown: list[int] = [0, 0, 0]
        self.can_attack = None

        if algorithm:
            self.algorithm = MethodType(algorithm, self)
        else:
            self.algorithm = self.algorithm

    def initial(self):
        self.initial_abilities_cooldown: list[int] = [UnitBehaviour.Actions.get_code(behaviour)[4] for behaviour in
                                                      self.behaviors]
        self.can_attack = any(not UnitBehaviour.Actions.get_code(action)[0] for action in self.behaviors)

    def __call__(self, num: int, cross=False, raw=False):
        """
        Возвращает класс и имя юнита текстом.

        :param num: Индекс класса персонажа.
        :param cross: Если True, возвращает имя серым цветом.
        :param raw: Если True, возвращает имя, хп, уровень, и особенности.
        :return: Форматированная строка с именем и классом персонажа.
        """
        text = ""
        if cross:
            text += ctext(self.class_titles[num], "dark_grey")
            text += " " + ctext(self._name, "grey")
        else:
            text += ctext(self.class_titles[num], "cyan") + " " + self.name

        if raw:
            text += (f" | {ctext(self.health, 'green')} {ctext(f'{self.level} ур', 'grey')} | "
                     f"{self.format_specials()}")

        return text

    def __str__(self):
        """
        :return: Форматированная строка с информацией о персонаже (класс, имя, хп, сила, уровень, свойства).
        """
        character_info = ctext(self.class_titles[0], "cyan")
        character_info += f" {self.name} | HP: {ctext(self.health, 'green')} | Сила: " + ctext(self.power, 'red')
        character_info += ctext(f"  {self.level} ур", "grey")
        character_info += " " + self.format_specials()
        return character_info

    # Ходы:
    def move(self, action_type: int, target: Self | list[Self] | None, report=True):
        """
        Выполняет действие персонажа.

        :param action_type: Тип действия (0, 1, 2).
        :param target: Цель действия (объект Character).
        :param report: Если True, добавляет информацию о действии в консоль.
        :raises ValueError: Если персонаж не может выполнить действие.
        """
        if not self.can_move:
            raise ValueError(self(0), "уже сделал ход, или не может делать ход.")
        elif not self.alive:
            raise ValueError(self(0), "мертв и не может делать ход.")

        UnitBehaviour.Actions.perform(self.behaviors[action_type], self, target, report)
        self.can_move = False

    def take_damage(self, damage, report=True):
        """
        Наносит урон персонажу, если у юнита поднят щит, урон снижается на коэффициент щита.

        :param damage: Количество урона.
        :param report: Если True, добавляет информацию о действии в консоль.
        """
        damage_taken = damage // GameConfig.config["shield_protection_multiplier"] if self.specials[
                                                                                          "shield"] > 0 else damage
        self.health -= damage_taken

        if self.health <= 0:
            self.alive = False
        if report:
            text = (f"    {self(0)} получает {ctext(damage_taken, 'red')} урона |"
                    f" здоровье: {ctext(max(0, self.health), 'green')}")
            if self.health <= 0:
                text += f"\n    {self(0)} погибает"
            GameConfig.move_history.append(text)

    def algorithm(self, ally_team: list[Self], enemy_team: list[Self]):
        raise NotImplementedError(self(0), "| algorithm не реализован")

    def after_move(self):
        """
        Сбрасывает флаг возможности хода после завершения хода.
        """
        self.can_move = True
        for i in range(3):
            self.abilities_cooldown[i] = max(self.abilities_cooldown[i] - 1, 0)

    # Свойства:
    def info(self) -> str:
        """
        Возвращает информацию о персонаже и его действиях.

        :return: Форматированная строка с информацией о персонаже и его действиях.
        """
        info_list = [UnitBehaviour.Actions.get_code(behaviour)[3] for behaviour in self.behaviors]
        cooldown_list = [UnitBehaviour.Actions.get_code(behaviour)[4] for behaviour in self.behaviors]
        names_list = self.get_move_names()
        result = "\n".join(
            f"  {ctext(idx + 1, 'yellow')}: {names_list[idx]} - {ability
            if cooldown_list[idx] == 0 else ctext(remove_ansi_codes(ability), 'dark_grey')}"
            for idx, ability in enumerate(info_list))
        return ctext('Информация:\n', 'yellow') + str(self) + f"\nДействия:\n{result}"

    def get_move_names(self) -> list[str]:
        """
        Возвращает названия действий персонажа.

        :return: Список названий действий.
        """
        moves_names = [UnitBehaviour.Actions.get_code(behavior)[2] for behavior in self.behaviors]
        result = [moves_names[move_idx] if self.abilities_cooldown[move_idx] == 0
                  else ctext(remove_ansi_codes(moves_names[move_idx]), 'dark_grey')
                  for move_idx in range(len(moves_names[:self.level]))]
        return result

    def is_positive_action(self, action_index: int) -> bool:
        """
        Определяет, является ли действие положительным (атака, лечение и т.д.).

        :param action_index: Индекс действия.
        :return: True, если действие положительное, иначе False.
        """
        return UnitBehaviour.Actions.get_code(self.behaviors[action_index])[0]

    def get_targets_count(self, action_index: int) -> int:
        """
        Возвращает количество целей для указанного действия.

        :param action_index: Индекс действия.
        :return: Количество целей.
        """
        return UnitBehaviour.Actions.get_code(self.behaviors[action_index])[1]

    def can_make_this_move(self, action_index: int, target: Self | list[Self] | None):
        if self.abilities_cooldown[action_index] != 0:
            return False
        return UnitBehaviour.Actions.can_make_move(self.behaviors[action_index], target)

    def format_specials(self):
        """
        Форматирует специальные эффекты (спецэффекты) для отображения.

        Возвращает строку с описанием активных спецэффектов, таких как "Под щитом" и "Усиление".
        Если спецэффектов нет, возвращает пустую строку.

        Returns:
            str: Строка с описанием спецэффектов в формате "(эффект1, эффект2)" или "".
        """
        # Словарь для хранения описаний спецэффектов и их условий
        specials_mapping = {
            "shield": ("Под щитом", "blue"),
            "power_multiplier": (f"Усиление: {ctext(str(self.specials["power_multiplier"]) + 'x', 'red')}", None),
        }

        # Создаем список для хранения активных спецэффектов
        active_specials = []

        # Проходим по словарю и проверяем, активен ли каждый спецэффект
        for key, (description, color) in specials_mapping.items():
            if self.specials.get(key) and self.specials[key] != 1:
                if color:
                    active_specials.append(ctext(description, color))
                else:
                    active_specials.append(description)

        # Если есть активные спецэффекты, объединяем их в строку и добавляем скобки
        if active_specials:
            return f"({active_specials[0]})" if len(active_specials) == 1 else f"({', '.join(active_specials)})"

        # Если спецэффектов нет, возвращаем пустую строку
        return ""

    def has_specials(self) -> bool:
        """
        Определяет, есть ли у персонажа активные особенности (щит, усиление, ...).

        Returns:
            bool: True, если есть активные особенности, иначе False.
        """
        return any(self.specials.get(key) and self.specials[key] != 1 for key in self.specials)

    # Сеттеры, гетеры:
    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def name(self) -> str:
        return ctext(self._name, "blue")

    @property
    def raw_name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: int):
        self._name = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value

    @property
    def max_level(self) -> int:
        return self._max_level

    @max_level.setter
    def max_level(self, value: int):
        self._max_level = value

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def power(self) -> int:
        return self._power * self.specials["power_multiplier"]

    @power.setter
    def power(self, value: int):
        self._power = value


class Turret(Character):
    """
    Базовый класс турели, наследуемы от Character.

            Атрибуты:
                - все атрибуты класса Character

            Методы:
                - move(action_type, target, report=True): Выполняет действие персонажа.
                - action(targets, report=True): Единственное действие персонажа (переопределяется в подклассе).
                - get_target(targets): Способ по которому турель выбирает цель (переопределяется в подклассе).
            """

    # Базовые:
    def __init__(self,
                 max_health: int = None,
                 power: int = None,
                 name: str = None,
                 level: int = None,
                 cost: int = None,
                 class_titles: list[str] = None,
                 positive_actions: list[bool] = None,
                 targets_count: list[int] = None):
        super().__init__(max_health=max_health,
                         power=power,
                         name=name,
                         level=level,
                         max_level=5,
                         cost=cost,
                         class_titles=class_titles)
        self.level = level or 1

    # Ходы:
    def move(self, action_type: int, targets: Character | list[Character] | None, report=True):
        """
        Выполняет действие персонажа.

        :param action_type: Ничего не делает.
        :param targets: Вражеская команда (объект Character).
        :param report: Если True, добавляет информацию о действии в консоль.
        :raises ValueError: Если персонаж не может выполнить действие.
        """
        if not self.can_move:
            raise ValueError(self(0), "уже сделала ход, или не может делать ход.")

        target = self.get_target(targets)

        self.action(target, report=report)
        self.can_move = False

    def action(self, targets: Character | list[Character] | None, report=True):
        """
        Первое действие персонажа. Должно быть переопределено в дочерних классах.

        :param targets: Цель или список целей.
        :param report: Если True, добавляет информацию о действии в историю.
        :raises NotImplementedError: Если метод не переопределен.
        """
        raise NotImplementedError("Метод первого действия не реализован")

    def get_target(self, targets: list[Character]) -> Character:
        """Способ по которому турель выбирает цель."""
        raise NotImplementedError(self(0) + " Метод получения цели не реализован")


class Duo(Turret):
    def __init__(self, name=None, level=None):
        super().__init__(
            name=name,
            level=level,
            power=15,
            cost=15,
            class_titles=["турель", "турель", "турели"],
            positive_actions=[False],
            targets_count=[1])

        self._actions_info = [f"Стреляет в цель, у которой больше всего здоровья"
                              f", нанося {ctext(self.power, 'red')} урона"
                              f"\n{ctext('Улучшения', 'yellow')} - увеличивают силу экспоненциально"]

    def action(self, target: Character, report=True):
        if report:
            text = f"{self(0)} стреляет в {target(0)}, нанося {ctext(self.power, 'red')} урона"
            GameConfig.move_history.append(text)
        target.take_damage(self.power, report=report)

    def get_target(self, targets: list[Character]) -> Character:
        return UnitBehaviour.TargetMode.highest_power(targets)

    def can_make_this_move(self, action_index: int, target: Self | list[Self] | None):
        return True

    # У этой турели урон зависит от уровня
    @property
    def power(self) -> int:
        """Сила атаки персонажа с учетом множителя и уровня."""
        return self._power * self.specials["power_multiplier"] * self.level


class Dagger(Character):
    """
    Класс персонажа "Воин" (Dagger).

    Наследует базовый класс Character и реализует уникальные действия:
    - Атака (action1)
    - Поднятие щита (action2)
    - Мощный удар с самопожертвованием (action3)
    """

    def __init__(self, name=None, level=None, algorithm=None):
        super().__init__(
            name=name,
            level=level,
            algorithm=algorithm,
            behaviors=["attack", "shield_up", "mega_blow"],
            cost=10,
            class_titles=["воин", "воина", "воину"]
        )
        self.initial()


class Archer(Character):
    """
    Класс персонажа "Лучник" (Archer).

    Наследует базовый класс Character и реализует уникальные действия:
    - Обычный выстрел (action1)
    - Усиленный выстрел (action2)
    - Залп стрел по нескольким целям (action3)
    """

    def __init__(self, name=None, level=None, algorithm=None):
        super().__init__(
            name=name,
            level=level,
            algorithm=algorithm,
            max_health=20,
            power=12,
            max_level=None,
            behaviors=["attack", "accurate_shot", "volley_of_arrows"],
            cost=10,
            class_titles=["лучник", "лучника", "лучнику"])
        self.initial()


# Прочие классы:
class Ai:
    """
    Класс Ai предоставляет методы для управления действиями команды бота в игре.

    Методы:
    - random_move: Выполняет случайные действия для команды бота.
    - script_move: Выполняет действия команды бота на основе заданных алгоритмов.
    - minimax_move: Метод-заглушка для реализации алгоритма минимакс.
    - generate_permutations: Генерирует все возможные перестановки заданного списка.
    - generate_all_moves: Генерирует все возможные действия для всех персонажей или конкретного юнита.
    - evaluation: Оценивает текущую команду на основе здоровья и размера команды.
    """

    @staticmethod
    def random_move(ally_team: list[Character], enemy_team: list[Character], update_progress=None) -> None:
        """
        Делает случайные действия команды.

        :param update_progress: Ничего такого, игнорировать.
        :param ally_team: Команда бота.
        :param enemy_team: Команда противника.
        """
        while True:
            update_progress(len(list(filter(lambda char: not char.can_move, ally_team))) / len(ally_team) * 100)

            moves = Ai.generate_all_moves(ally_team, enemy_team)
            if not moves:
                return
            move_pack = random.choice(moves)
            unit, action_index, target = move_pack
            unit.move(action_index, target)
            time.sleep(0.25)
            update_console("")
            time.sleep(0.25)

    @staticmethod
    def script_move(ally_team: list[Character], enemy_team: list[Character], update_progress=None) -> None:
        """
        все пешки выполняют метод algorithm, он определяется в отдельных функциях.

        :param update_progress: Ничего такого, игнорировать.
        :param ally_team: Команда бота.
        :param enemy_team: Команда противника.
        """
        for unit in [unit for unit in ally_team if unit.alive and unit.can_move]:
            update_progress(len(list(filter(lambda char: not char.can_move, ally_team))) / len(ally_team) * 100)
            unit.algorithm(ally_team, enemy_team)
        update_console("")

    @staticmethod
    def minimax_move(current_team, enemy_team, depth, is_maximizing) -> None:
        """Легенда"""
        pass

    @staticmethod
    def generate_permutations(lst: Any) -> list[list[Any]]:
        """
        Генерирует все перестановки списка

        :param lst: Список для перестановки

        :return: Список списков во всех перестановках
        """
        if len(lst) == 1:
            return [lst]
        result = []

        for item in range(len(lst)):
            first_item = lst[item]
            remaining_items = lst[:item] + lst[item + 1:]
            for permutation in Ai.generate_permutations(remaining_items):
                result.append([first_item] + permutation)
        return result

    @staticmethod
    def generate_all_moves(ally_team: list[Character], enemy_team: list[Character], unit: Character = None) \
            -> list[tuple[Character, int, Character | list[Character] | None]]:
        """
        Генерирует все возможные действия для всех персонажей или конкретного юнита.

        Args:
            ally_team: Список союзных юнитов
            enemy_team: Список вражеских юнитов
            unit: Конкретный юнит, для которого нужно сгенерировать ходы. Если None, генерирует для всех

        Returns:
            Список кортежей вида (юнит, индекс действия, цель/цели).
        """
        result = []
        enemy_team = [enemy for enemy in enemy_team if enemy.alive]

        def generate_unit_moves(current_unit, current_ally_team, current_enemy_team) -> list[
            tuple[Character, int, Character | list[Character] | None]]:
            """
            Генерирует все возможные действия для конкретного юнита.

            Args:
                current_unit: Юнит, для которого генерируются ходы
                current_ally_team: Список союзных юнитов
                current_enemy_team: Список вражеских юнитов

            Returns:
                Список кортежей вида (юнит, индекс действия, цель/цели).
            """
            intermediate_result = []

            for action_index, action_name in enumerate(current_unit.get_move_names()):
                targets_count = current_unit.get_targets_count(action_index)
                target_team = current_ally_team if current_unit.is_positive_action(action_index) else current_enemy_team

                if not current_unit.can_make_this_move(action_index, target_team if targets_count != 0 else None):
                    continue

                if targets_count == -1:  # Действие на всю команду
                    intermediate_result.append((current_unit, action_index, target_team))

                elif targets_count == 0:  # Действие без цели
                    intermediate_result.append((current_unit, action_index, None))

                elif targets_count == 1:  # Действие на одного
                    intermediate_result.extend((current_unit, action_index, target) for target in target_team if
                                               current_unit.can_make_this_move(action_index, target))

                elif targets_count > 1:  # Действие на нескольких
                    targets_count = min(targets_count, len(target_team))

                    if targets_count == len(target_team):
                        intermediate_result.append((current_unit, action_index, target_team))
                        continue

                    for i in range(len(target_team)):
                        targets = [target_team[(i + j) % len(target_team)] for j in range(targets_count)]
                        if current_unit.can_make_this_move(action_index, targets):
                            intermediate_result.append((current_unit, action_index, targets))

            return intermediate_result

        if unit:
            result.extend(generate_unit_moves(unit, ally_team, enemy_team))
        else:
            for unit in ally_team:
                # Проверка на то, может ли персонаж делать ходы и это не турель
                if not unit.can_move or not unit.alive or isinstance(unit, Turret):
                    continue

                moves = generate_unit_moves(unit, ally_team, enemy_team)
                result.extend(moves)

        return result

    @staticmethod
    def evaluation(team: list[Character]) -> int:
        """
        Оценка текущей команды по здоровью и размеру

        :param team: Команда

        :return: Оценка команды
        """
        score = 0
        for char in team:
            score += (char.health / char.max_health) * 100
        score += len(team) * 100
        return score


class UnitBehaviour:
    class TargetMode:
        """Способы выделения целей"""

        @staticmethod
        def random_target(targets: list[Character]) -> Character | None:
            """Случайная цель"""
            return random.choice(targets) if targets else None

        @staticmethod
        def lowest_hp(targets: list[Character]) -> Character | None:
            """Цель с самым низким здоровьем"""
            return None if not targets else min(targets, key=lambda x: x.health)

        @staticmethod
        def highest_hp(targets: list[Character]) -> Character | None:
            """Цель с самым большим здоровьем"""
            return None if not targets else max(targets, key=lambda x: x.health)

        @staticmethod
        def highest_power(targets: list[Character]) -> Character | None:
            """Цель с самой высокой силой"""
            return None if not targets else max(targets, key=lambda x: x.power)

    class Actions:
        @staticmethod
        def perform(action_name: str, unit: Character, target: Character, report: bool) -> None:
            getattr(UnitBehaviour.Actions, action_name)(unit, target, report)

        @staticmethod
        def get_code(action: str) -> list:
            """
            Возвращает код действия

            index:
                0. bool: позитивное действие
                1. кол-во целей
                2. название
                3. инфо
                4. кд

            :param action: Название действия
            :return: Код действия
            """
            return {
                "attack": [False, 1, "⚔ Атака", "Атакует цель", 1],
                "shield_up": [True, 2, "🛡 щит", f"Поднимает {ctext('щит', 'blue')}", 1],
                "mega_blow": [False, 1, "💀 мега удар",
                              f"Наносит {ctext('1000', 'red')} урона и {ctext('умирает', 'red')}", 2],
                "accurate_shot": [False, 1, "🎯 Точный выстрел",
                                  f"с вероятностью 75% наносит х3 урона, или промахивается", 1],
                "volley_of_arrows": [False, 3, "🌧 Залп стрел", "наносит {ctext('x2', 'red')} урона всем врагам", 2]
            }[action]

        # Ходы:
        @staticmethod
        def can_make_move(action: str, target: Character | list[Character]) -> bool:
            """
            Проверяет, может ли юнит выполнить указанное действие для цели.

            Args:
                action (str): Название действия (например, "attack", "shield_up")
                target (Character | list[Character]): Цель действия (одиночный юнит или группа)

            Returns:
                bool: True, если действие может быть выполнено, иначе False.

            Raises:
                ValueError: Если действие не поддерживается.
            """

            # Логика проверки для действия "shield_up"
            def is_shield_up(targets) -> bool:
                if isinstance(targets, Character):
                    return targets.specials.get("shield", 1) == 0  # 1 — значение по умолчанию, если ключа нет
                else:
                    return any(unit.specials.get("shield", 1) == 0 for unit in targets)

            # Словарь с логикой проверки для каждого действия
            ACTION_CHECKS = {
                "attack": True,  # Атака всегда доступна
                "shield_up": is_shield_up(target),  # Проверка щита
                "mega_blow": True,  # Мега-удар всегда доступен
                "accurate_shot": True,  # Точный выстрел всегда доступен
                "volley_of_arrows": True,  # Залп стрел всегда доступен
            }

            # Проверяем, поддерживается ли действие
            if action not in ACTION_CHECKS:
                raise ValueError(f"Действие '{action}' не поддерживается.")

            # Возвращаем результат проверки
            return ACTION_CHECKS[action]

        @staticmethod
        def attack(unit: Character, target: Character, report=True) -> None:
            """
            Атака цели. Наносит урон, равный силе персонажа.

            :param unit: Персонаж, который атакует.
            :param target: Цель атаки.
            :param report: Если True, добавляет информацию о действии в консоль.
            """
            text = f"{unit(0)} атакует {target(1)}, нанося {ctext(unit.power, 'red')} урона"

            if unit.specials["power_multiplier"] > 1:
                unit.specials["power_multiplier"] = 1
                text += f"\n    усиление {unit(1)} обнулилось"

            if report:
                GameConfig.move_history.append(text)
            target.take_damage(unit.power, report=report)

        @staticmethod
        def shield_up(unit: Character, targets: list[Character], report=True) -> None:
            for target in targets:
                if report:
                    text = f"{unit(0)} поднял щит {target(2)} на 3 хода"
                    GameConfig.move_history.append(text)
                target.specials["shield"] = 3

        @staticmethod
        def mega_blow(unit: Character, target: Character, report=True) -> None:
            if report:
                text = f"{unit(0)} нанёс {ctext('1000', 'red')} урона {target(2)} и умер"
                GameConfig.move_history.append(text)
            unit.specials["shield"] = 0
            target.take_damage(1000)
            unit.take_damage(unit.health)

        @staticmethod
        def accurate_shot(unit: Character, target: Character, report=True) -> None:
            is_lucky = random.randint(1, 100) <= 75
            if report:
                text = f"{unit(0)} стреляет в {target(1)}, и "
                if is_lucky:
                    text += f"наносит {ctext(unit.power * 3, 'red')} урона"
                else:
                    text += ctext("промахивается", 'red')
                GameConfig.move_history.append(text)

            if is_lucky:
                target.take_damage(unit.power * 3, report=report)

        @staticmethod
        def volley_of_arrows(unit: Character, targets: list[Character], report=True) -> None:
            if report:
                text = f"{unit(0)} выпускает залп стрел, нанося {ctext(unit.power * 2, 'red')} урона трём врагам"
                GameConfig.move_history.append(text)
            for enemy in targets:
                enemy.take_damage(unit.power * 2, report=report)


class GameConfig:
    version = "2.3"
    updates_history = """Обновления:
    1.0 Создана игра, добавлены классы.

    2.0 Оптимизирован код

    2.1 Переделан вывод в консоль, теперь нет спама
        А так же добавлена система уровней юнитов

    2.2 Переделана механика выбора опций

    2.21 
        Добавлено:
        - Меню   
        - Загрузка, пока бот делает ход  
        - Смайлики в выборе
        - История обновлений
        - Рандомные фразы в конце боя
        - Баги

    2.22 
        Исправлены баги:
        - Баг с 0 урона
        - На esc пропускался ход

        Добавлено:
        - Проверка на поддержку цветного кода
        - Возможность атаковать нескольких одновременно

    2.23
        Исправлено:
        - Вылет игры, при игре без anci, после первого дня
        - после смерти пешка остаётся в целях для игрока
        - При выходе в меню сбрасывается потраченные очки улучшений
        - Баг с кривым меню

        Добавлено:
        - Читы
        - Редактирование команды
        - Генератор вражеской команды
        - Уровни сложности
        - Кнопки "продолжить" и "новая игра" теперь делают не одно и то же

        всё, что угодно, только не делать что то полезное

    2.3
        Добавлено:
        - Уровни

    2.4 Добавлен сложный ИИ бот

    3.0 Переделан интерфейс, добавлено поле
    3.1 Добавлены анимации"""

    phrases = ["и у тебя выключится комп",
               "и иди потрогай траву",
               "что бы забыть этот успех навсегда",
               "что бы эта команда проиграла",
               "хотя не, не жми"]
    config = {
        "default_hp": 30,
        "default_damage": 10,
        "shield_protection_multiplier": 2
    }
    settings = {
        "vertical_unit_table": False,
    }
    debug_mode = {
        "ally_god_mode": False,
        "enemy_god_mode": False,
        "playable_enemy_team": False,
        "infinity_moves": False,
        "skip_move": False,
        "default_input": False,
        "infinity_upgrade_points": False,
        "infinity_upgrades": False,
    }
    data = {
        "player_team": [],
        "current_ally_team": [],
        "current_enemy_team": [],
        "upgrade_points": 2,
        "remaining_upgrade_points": 2,
    }

    classes_list = [Dagger, Archer, Duo]
    custom_classes = []

    current_bot_mode = None
    show_day = False
    current_day = ""
    move_history = []


# Обычные функции:
def choose_from_menu(options: list[str], title: str = "Выберите вариант:", start_index: int = 0,
                     select_count: int = 1, centered: bool = False, descriptions: list[str] = None) -> int | list[int]:
    """
    Функция для выбора одного или нескольких пунктов из меню.

    :param options: Список строк, представляющих пункты меню.
    :param title: Заголовок меню (по умолчанию "Выберите вариант:").
    :param start_index: Индекс пункта, который будет выбран по умолчанию (по умолчанию 0).
    :param select_count: Количество пунктов, которые можно выбрать (по умолчанию 1).
    :param centered: Если True, меню будет центрировано (по умолчанию False).
    :param descriptions: Список описаний пунктов меню (по умолчанию пустой).
    :return: Индекс выбранного пункта или список индексов, если select_count > 1.
             Возвращает -1, если пользователь нажал esc.
    """
    # Режим отладки: использование текстового ввода вместо интерактивного меню
    if GameConfig.debug_mode["default_input"]:
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


def rand_name() -> str:
    """:return: Возвращает случайное имя"""
    names = ['Лока', 'Кирик', 'Цикада', 'Мотылек', 'Иви', 'Пинт', 'Азура', 'Зефир', 'Сирин', 'Элейн', 'Вайт', 'Лорен',
             'Зара', 'Фин', 'Эмеральд', 'Айрис', 'Скарлет', 'Найт', 'Оливия', 'Амбер', 'Зенит', 'Феликс', 'Сабина',
             'Андромеда', 'Тайга', 'Пентагон']
    return random.choice(names)


def loading(func):
    """Декоратор, показывающий загрузку, пока выполняется декорируемая функция."""

    def wrapper(*args, **kwargs):
        def spinner():
            frames = ['-', '\\', '|', '/']
            i = 0
            while not done.is_set():
                print(f'\rЗагрузка... {frames[i % 4]}', end='', flush=True)
                i += 1
                time.sleep(0.1)
            update_console("")

        done = threading.Event()  # Event to stop the spinner
        spinner_thread = threading.Thread(target=spinner)
        spinner_thread.start()

        # Execute the wrapped function
        result = func(*args, **kwargs)

        # Stop the spinner
        done.set()
        spinner_thread.join()

        return result

    return wrapper


def progress_bar(title="Загрузка"):
    """
    Декоратор для отображения загрузки прогресс-бара, пока выполняется функция.

    :param title: Заголовок прогресс-бара (по умолчанию "Загрузка").
    """

    def decorator(decorated_func):
        def wrapper(*args, **kwargs):
            # Callback-функция для обновления прогресса
            def update_progress(progress):
                progress_bar_line = '=' * round(progress // 10)
                print(f"{title}: [{progress_bar_line.ljust(10)}]", end="\r")

            # Вызываем целевую функцию, передавая callback
            result = decorated_func(update_progress=update_progress, *args, **kwargs)
            return result

        return wrapper

    return decorator


def ignore_interrupt(function):
    """Убирает ошибку в консоли, при остановке кода"""

    def wrapper(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except KeyboardInterrupt:
            sys.exit(0)
        return result

    return wrapper


def remove_ansi_codes(text: str) -> str:
    """Удаляет ANSI-коды из текста

    :return текст без ANSI-кодов
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


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


def print_info(*info):
    """Печатает информацию в консоль, после чего код приостанавливается до нажатия клавиши."""
    clear_console()
    print(*info)
    while True:
        key_event = keyboard.read_event()
        if key_event.event_type == keyboard.KEY_DOWN and key_event.name in ['esc', 'space', 'enter']:
            break
    clear_console()


def all_match(lst: list, condition) -> bool:
    """Проверяет условие для всех элементов списка.

    :param lst: Список элементов
    :param condition: Условие для проверки каждого элемента

    :return: True, если условие выполняется для всех элементов, иначе False."""
    return all(condition(item) for item in lst)


def update_console(text: str):
    """Очищает консоль и выводит актуальную информацию.
    Сверху пишет текущий раунд, вражескую и дружескую команду.
    После историю ходов раунда.
    И в конце выводит переданное сообщение.

    :param text: Строка для вывода
    """
    clear_console()
    day_str = str(get_day_str() if not GameConfig.settings["vertical_unit_table"] else get_day_str_old() + "\n\n") \
        if GameConfig.show_day else "\n"
    moves_str = str("\n".join(GameConfig.move_history) + "\n\n") if GameConfig.show_day else ""
    print(day_str, moves_str, text)


# Игровые функции:
def get_day_str() -> str:
    """
    Возвращает таблицу с информацией о текущем дне, включая статус всех живых юнитов
    в дружеской и вражеской командах.

    Формат вывода:
    - Таблица с юнитами, их здоровьем, силой, уровнем и спецэффектами.
    - Заголовки для дружеской и вражеской команд.
    - Разделители между командами и завершение таблицы.

    Returns:
        str: Отформатированная таблица с информацией о юнитах.
    """
    ally_team = [unit for unit in GameConfig.data["current_ally_team"] if unit.alive]
    enemy_team = [unit for unit in GameConfig.data["current_enemy_team"] if unit.alive]

    def calculate_table_width(team, raw=False):
        """Возвращает ширину всех характеристик персонажа без учёта anci"""
        if not team:
            return {"longest_name": 0, "max_hp_len": 0, "max_power_len": 0, "max_specials_len": 0}

        if raw:
            metrics = {
                "longest_name": max((len(str(remove_ansi_codes(unit(0)))) for unit in team), default=0),
                "max_hp_len": max((len(str(unit.health)) for unit in team), default=0),
                "max_power_len": max((len(str(unit.power)) for unit in team), default=0)
            }
            specials = [unit.format_specials() for unit in team]
            metrics["max_specials_len"] = max((len(remove_ansi_codes(s)) for s in specials), default=0)
        else:
            metrics = {
                "longest_name": max((len(str(unit(0))) for unit in team), default=0),
                "max_hp_len": max((len(str(unit.health)) for unit in team), default=0),
                "max_power_len": max((len(str(unit.power)) for unit in team), default=0)
            }
            specials = [unit.format_specials() for unit in team]
            metrics["max_specials_len"] = max((len(s) for s in specials), default=0)

        return metrics

    def format_unit_line(unit, metrics):
        line = (
            f"{str(unit(0)).ljust(metrics['longest_name'])} | "
            f"Сила: {ctext(f'{str(unit.power).rjust(metrics['max_power_len'])}', 'red')} | "
            f"HP: {ctext(f'{str(unit.health).rjust(metrics['max_hp_len'])}', 'green')} | "
            f"{ctext(f'{unit.level} ур', 'grey')}"
        )
        if unit.has_specials():
            line += f" | {unit.format_specials():<{metrics['max_specials_len']}}"
        elif metrics['max_specials_len'] != 0:
            line += f" | {unit.format_specials():<{(metrics['max_specials_len'] // 2) - 1}}"
        return line

    def format_full_line(char_index, team, metrics, width, plus_two):
        res = ""
        if char_index < len(team):
            res += f"| {format_unit_line(team[char_index], metrics)} |"
        else:
            res += "|".ljust(width + (2 if plus_two else 0)) + "|"
        return res

    left_metrics = calculate_table_width(ally_team)
    right_metrics = calculate_table_width(enemy_team)

    raw_left_metrics = calculate_table_width(ally_team, raw=True)
    raw_right_metrics = calculate_table_width(enemy_team, raw=True)

    raw_left_table_width = sum(raw_left_metrics.values()) + (29 if raw_left_metrics["max_specials_len"] > 0 else 26)
    raw_right_table_width = sum(raw_right_metrics.values()) + (27 if raw_right_metrics["max_specials_len"] > 0 else 24)

    total_table_width = raw_left_table_width + raw_right_table_width + 4

    # Заголовок таблицы
    result = f'{"=" * total_table_width}'

    # Первая строчка
    result += ("\n| Дружеская команда".ljust(raw_left_table_width) + " || "
               + "Вражеская команда".ljust(raw_right_table_width) + "|")
    for unit_index in range(max(len(ally_team), len(enemy_team))):
        result += ("\n" +
                   format_full_line(unit_index, ally_team, left_metrics, raw_left_table_width, False) +
                   format_full_line(unit_index, enemy_team, right_metrics, raw_right_table_width, True))

    # Завершение таблицы
    result += f'\n{"=" * total_table_width}'

    return result


def get_day_str_old() -> str:
    """
    Возвращает таблицу с информацией о текущем дне, включая статус всех живых юнитов
    в дружеской и вражеской командах.

    Формат вывода:
    - Таблица с юнитами, их здоровьем, силой, уровнем и спецэффектами.
    - Заголовки для дружеской и вражеской команд.
    - Разделители между командами и завершение таблицы.

    Returns:
        str: Отформатированная строка с информацией о юнитах.
    """
    # Все живые юниты
    all_units = [unit for unit in GameConfig.data["current_ally_team"] + GameConfig.data["current_enemy_team"]]

    # Находим максимальную длину каждого столбца
    longest_name = max(len(str(unit(0))) for unit in all_units)
    max_hp_len = max(len(str(unit.health)) for unit in all_units)
    max_power_len = max(len(str(unit.power)) for unit in all_units)
    max_specials_len = max(len(unit.format_specials()) for unit in all_units)

    # Динамическая ширина таблицы
    table_width = longest_name + max_hp_len + max_power_len + max_specials_len // 2 + 13

    def format_unit_line(unit):
        """
        Форматирует строку с информацией о юните.

        Args:
            unit: Объект юнита.

        Returns:
            str: Отформатированная строка с данными о юните.
        """
        line = (
            f"|  {str(unit(0)).ljust(longest_name)} "
            f" |  Сила: {ctext(str(unit.power).rjust(max_power_len), 'red')} "
            f" |  HP: {ctext(str(unit.health).rjust(max_hp_len), 'green')} "
            f" |  {ctext(str(unit.level) + ' ур', 'grey')} "
        )
        line += f" |  {unit.format_specials().ljust(max_specials_len // 2)}" if max_specials_len else ""

        # Убираем ANSI-коды только для подсчёта длины
        clean_line = remove_ansi_codes(line)

        # Добавляем нужное количество пробелов
        line += " " * (table_width - len(clean_line) - 1) + "|"
        return line

    def format_team_section(team, team_name: str) -> str:
        """
        Форматирует секцию таблицы для одной команды.

        Args:
            team: Список юнитов команды
            team_name: Название команды (например, "Дружеская команда")

        Returns:
            str: Отформатированная секция таблицы.
        """
        section = f"\n| {team_name} "
        formated_count = ""
        if len(team) > 5:
            formated_count = f" ({ctext(len(team), 'blue')} "
            formated_count += f"{format_readable_count(len(team), 'юнит', 'юнита', 'юнитов')}):"
            section += formated_count
        section += " " * (table_width - len(team_name) - (len(formated_count) // 2) - 4) + "|"
        for unit in team:
            if unit.alive:
                section += f"\n{format_unit_line(unit)}"
        return section

    # Заголовок таблицы
    result = f'\n{"=" * table_width}'

    # Форматирование таблиц команд
    result += format_team_section(GameConfig.data["current_ally_team"], "Ваша команда")

    # Разделитель между командами
    result += f'\n|{"-" * (table_width - 2)}|'

    # Форматирование вражеской команды
    result += format_team_section(GameConfig.data["current_enemy_team"], "Вражеская команда")

    # Завершение таблицы
    result += f'\n{"=" * table_width}'

    return result


def update_team(team: list[Character]):
    """Вызывает метод after_move у всей команды.

    :param team: Команда, у которой вызывается after_move
    """
    for char in team:
        char.after_move()


def get_team_cost(team: list[Character]) -> int:
    """Возвращает стоимость всех юнитов в команде.

    :param team: Команда, стоимость которой нужно посчитать

    :return: Стоимость юнитов в команде
    """
    return sum(unit.cost + unit.level * 5 for unit in team)


def generate_team(is_ally: bool, available_cost: int) -> list[Character]:
    """Создает новую команду, соответствующую доступной цене, цена указывается в классах.

    :param is_ally: Является ли команда дружественной
    :param available_cost: Доступный бюджет для покупки юнитов

    :return: Сформированная команда
    """
    team: list[Character] = []
    while available_cost > 5:
        # Улучшение одного из юинтов
        if team and random.randint(1, 2) == 1:
            random_unit = random.choice([unit for unit in team if unit.alive])

            # Если юнит максимального уровня
            if random_unit.level == random_unit.max_level:
                continue

            random_unit.level += 1
            available_cost -= 5

        # Добавление юнитов в команду
        else:
            # Фильтруем юнитов, которые можно купить
            available_units = [unit for unit in GameConfig.classes_list if unit().cost <= available_cost]

            # Если нет доступных юнитов, выходим из цикла
            if not available_units:
                break

            # Выбираем случайный юнит из доступных
            unit = random.choice(available_units)()

            # Уменьшаем доступный бюджет
            available_cost -= unit.cost
            unit.is_ally = is_ally

            # Добавляем юнита в команду
            team.append(unit)

            if available_cost < 15:
                if random.randint(1, 4) == 1:
                    return team

    return team


def move_turrets(ally_team: list[Character], enemy_team: list[Character]):
    """Выполняет метод move у всех турельных юнитов.

    :param ally_team: Текущая команда
    :param enemy_team: Вражеская команда
    """
    for unit in ally_team:
        if isinstance(unit, Turret) and unit.can_move and unit.alive:
            unit.move(0, enemy_team)


# Функции игрока:
@ignore_interrupt
def player_move(ally_team: list[Character], enemy_team: list[Character]):
    target = None
    while any([unit.can_move and not isinstance(unit, Turret) and unit.alive for unit in ally_team]):
        if all_match(enemy_team, lambda unit: not unit.alive):
            return

        alive_ally_team = [unit for unit in ally_team if unit.alive]
        alive_enemy_team = [unit for unit in enemy_team if unit.alive]

        ally_team_names = [f'{unit(0, cross=not unit.can_move, raw=True)}' for unit in alive_ally_team]
        enemy_team_names = [unit(0, raw=True) for unit in alive_enemy_team]

        # Первый юнит, который может ходить
        first_possible = next((i for i, unit in enumerate(alive_ally_team) if
                               unit.can_move and not isinstance(unit, Turret) == True), None)

        # Если включён чит "пропустить ход" появится соответствующая опция
        if GameConfig.debug_mode["skip_move"]:
            ally_team_names.append(ctext("Debug: Закончить ход", 'red'))

        # Выбор персонажа игроком
        unit_index = choose_from_menu(ally_team_names, "Ваша команда:", first_possible)

        # Выход
        if unit_index == -1:
            menu()

        # Включён чит "пропустить ход"
        elif GameConfig.debug_mode["skip_move"] and unit_index == len(ally_team_names) - 1:
            return

        unit = alive_ally_team[unit_index]
        if not unit.can_move:
            continue

        # Цикл пока игрок не сделает ход
        while True:
            options = unit.get_move_names()
            options.append("📖 Инфо")

            title = f"{unit}\nХод:"

            action_index = choose_from_menu(options, title)

            # Назад
            if action_index == -1:
                break

            # Инфо
            elif action_index == len(options) - 1:
                print_info(unit.info())
                continue

            # Действие
            else:
                select_count = unit.get_targets_count(action_index)
                team = alive_ally_team if unit.is_positive_action(action_index) else alive_enemy_team
                team_names = ally_team_names if unit.is_positive_action(action_index) else enemy_team_names

                if select_count == 0:
                    target = 0
                    break
                elif select_count == -1:
                    target = team
                    break
                else:
                    title = f"{unit}\n{options[action_index]}:"
                    target_index = choose_from_menu(team_names, title, select_count=select_count)
                    # Назад
                    if target_index == -1:
                        target = None
                        continue

                    target = team[target_index] if select_count == 1 else [team[i] for i in target_index]
                    break

        if target is None or not unit.can_make_this_move(action_index, target) or isinstance(unit, Turret):
            continue
        unit.move(action_index, target)
        if GameConfig.debug_mode["infinity_moves"]:
            unit.can_move = True


@ignore_interrupt
def set_units_level(ally_team: list[Character]):
    unit_index = 0

    while True:
        unit_list = [f"{unit(0)} {ctext(str(unit.level) + ' ур', 'grey')}" for unit in ally_team]
        unit_list.extend(["Сброс", "Назад"])

        text = f"Выберите кому присвоить +1 уровень (осталось: {GameConfig.data["remaining_upgrade_points"]})"

        # Выбор юнита
        unit_index = choose_from_menu(unit_list, text, unit_index)

        # Назад
        if unit_index == len(unit_list) - 1 or unit_index == -1:
            return

        # Сброс уровней
        if unit_index == len(unit_list) - 2:
            GameConfig.data["remaining_upgrade_points"] = GameConfig.data["upgrade_points"]
            for unit in ally_team:
                unit.level = 1
            continue

        # Присваивание уровня
        if ((ally_team[unit_index].level < ally_team[unit_index].max_level or GameConfig.debug_mode[
            "infinity_upgrades"]) and
                (GameConfig.data["remaining_upgrade_points"] > 0 or GameConfig.debug_mode["infinity_upgrade_points"])):
            ally_team[unit_index].level += 1
            GameConfig.data["remaining_upgrade_points"] -= 1


@ignore_interrupt
def set_units_in_team(team: list[Character]):
    class_index = 0
    is_add = True
    while True:
        options = [ctext("Добавить", "green") if is_add else
                   ctext("Удалить", "red")]

        classes_names_list = [cls().class_titles[0] for cls in GameConfig.classes_list]

        # Создаём Counter с нулевыми значениями для всех классов
        team_dict = Counter({name: 0 for name in classes_names_list})
        team_dict.update(unit.class_titles[0] for unit in team)

        options.extend([str(ctext(class_title, 'blue') + f": {count}")
                        for class_title, count in team_dict.items()])
        title = "Редактирование состава:"
        class_index = choose_from_menu(options, title, class_index)  # Добавлена дополнительная строчка

        if class_index == -1:
            return
        elif class_index == 0:
            is_add = not is_add
            continue

        else:
            if is_add:
                team.append(GameConfig.classes_list[class_index - 1]())
            elif (team_dict[classes_names_list[class_index - 1]] > 0
                  and sum([count for count in team_dict.values()])) > 1:
                team.remove(next(item for item in team if isinstance(item, GameConfig.classes_list[class_index - 1])))


@ignore_interrupt
def set_units_names(team: list[Character]):
    unit_index = 0
    while True:
        options = [unit(0) for unit in team]
        title = "Редактирование имён:"
        unit_index = choose_from_menu(options, title, unit_index)

        if unit_index == -1:
            return
        else:
            # Вводим новое имя
            input()
            new_name = input(f"Введите имя для {team[unit_index](0)}: ")
            team[unit_index].name = new_name


@ignore_interrupt
def set_team():
    """
    Позволяет пользователю настраивать команды.
    """
    team = GameConfig.data["player_team"]  # Список команд для удобного доступа по индексу
    action_index = 0  # Индексы выбора игрока

    while True:
        options = ["Уровни персонажей", "Редактирование состава", "Имена"]
        title = f"Изменение команды"
        action_index = choose_from_menu(options, title, action_index, centered=True)

        if action_index == -1:
            break

        # Уровни персонажей
        elif action_index == 0:
            set_units_level(team)

        # Редактирование состава
        elif action_index == 1:
            set_units_in_team(team)

        # Имена
        elif action_index == 2:
            set_units_names(team)


# Игра:
class Challenges:
    @staticmethod
    def choose_level():
        methods = [name for name in dir(Challenges)
                   if callable(getattr(Challenges, name)) and not name.startswith('__') and name.startswith('level')]
        options = [f"уровень {method.split("_")[1]}" for method in methods]
        action = choose_from_menu(options, "Выберите уровень:")
        if action == -1:
            return
        getattr(Challenges, methods[action])(Challenges)

    @staticmethod
    def start_level(player_team, team):
        game(player_team, team, 1)

    def level_1(self):
        def dagger_algorithm(unit: Character, ally_team: list[Character], enemy_team: list[Character]) -> None:
            if unit.specials['shield'] > 0:
                unit.move(2, UnitBehaviour.TargetMode.highest_hp(enemy_team))
            elif any(unit.specials['shield'] == 0 for unit in ally_team):
                moves = Ai.generate_all_moves(ally_team, enemy_team, unit=unit)
                moves = [move for move in moves if move[1] == 1 and isinstance(move[0], Dagger)]
                unit, move, target = random.choice(moves)
                unit.move(move, target)
            else:
                unit.move(1, UnitBehaviour.TargetMode.random_target(enemy_team))

        dagger1 = Dagger(name="Даггер 1", level=3, algorithm=dagger_algorithm)

        dagger2 = Dagger(name="Даггер 2", level=3, algorithm=dagger_algorithm)

        team = [dagger1, dagger2]
        player_team = [Archer(name="Первый"), Archer(name="Gthds")]
        self.start_level(player_team, team)


def team_turn(active_team, passive_team, is_player_controlled, team_number, bot_mode: int):
    """
    Функция для выполнения хода команды.

    :param active_team: Список персонажей активной команды, которые выполняют ход.
    :param passive_team: Список персонажей пассивной команды, против которых выполняется ход.
    :param is_player_controlled: Флаг, определяющий, контролируется ли активная команда игроком.
    :param team_number: Номер команды (1 для союзников, 2 для врагов).
    :param bot_mode: Номер режима бота (0 - случайный ход, 1 - скриптовый ход, 2 - минимакс ход).

    :return: True, если команда победила, иначе False.
    """
    GameConfig.move_history.append(f"\nХод команды {team_number}:")

    # Если команда управляется игроком, то ходит игрок
    if is_player_controlled:
        player_move(active_team, passive_team)
    else:
        # Иначе ходит бот
        match bot_mode:
            case 0:
                Ai.random_move(active_team, passive_team)
            case 1:
                Ai.script_move(active_team, passive_team)

    # Действие турелей
    move_turrets(active_team, passive_team)

    # Обновление состояния пассивной команды
    update_team(passive_team)

    # Проверка, если все члены пассивной команды мертвы
    if all_match(passive_team, lambda unit: not unit.alive and unit.can_attack):
        update_console("")
        return True  # Победа активной команды

    return False


def game(ally_team: list[Character], enemy_team: list[Character], bot_mode: int):
    """
    Главная игровая функция, выполняющая игру до победы одной из команд.

    :param ally_team: Список персонажей команды союзников.
    :param enemy_team: Список персонажей команды врагов.
    :param bot_mode: Номер режима бота (0 - случайный ход, 1 - скриптовый ход, 2 - минимакс ход).
    """
    if not ally_team or not enemy_team:
        return
    GameConfig.current_bot_mode = bot_mode

    GameConfig.data["current_ally_team"] = ally_team
    GameConfig.data["current_enemy_team"] = enemy_team
    GameConfig.show_day = True
    GameConfig.move_history = []

    while True:
        update_console("")  # Очистка консоли

        # Ход первой команды (союзников)
        if team_turn(ally_team, enemy_team, True, 1, bot_mode):
            winner = 1  # Победа союзников
            GameConfig.move_history = []
            break

        update_console("")  # Очистка консоли перед ходом врагов

        # Проверка, управляется ли вражеская команда игроком
        enemy_controlled_by_player = GameConfig.debug_mode["playable_enemy_team"]

        # Ход второй команды (врагов)
        if team_turn(enemy_team, ally_team, enemy_controlled_by_player, 2, bot_mode):
            winner = 2  # Победа врагов
            GameConfig.move_history = []
            break

        # Пауза для перехода к следующему дню
        update_console("Нажмите Enter для следующего дня...")
        keyboard.wait("enter")

        # Очистка истории ходов на новый день
        GameConfig.move_history = []

    # Ожидание нажатия Enter после победы
    input(f"КОМАНДА {winner} ПОБЕДИЛА, НАЖМИ ЕНТЕР, {random.choice(GameConfig.phrases)}")
    keyboard.wait("enter")


def new_game():
    GameConfig.current_day, GameConfig.move_history = '', []
    difficulty_coefficients = [0.7, 1, 1.3, 1.75]
    # Выбор уровня сложности
    options = [ctext("Легкий", 'blue'),
               ctext("Справедливый", 'green'),
               ctext("Сложный", 'red'),
               ctext("Кошмар", 'black')]
    descriptions = [f"😀 {ctext('Слабая', 'blue')} команда противников.",
                    f"✅  {ctext('Примерно равная', 'green')} по силе команда — {ctext('честный бой', 'green')}.",
                    f"❌  {ctext('Сильная', 'red')} команда в {ctext('1.5 раза', 'red')} сильнее вашей.",
                    f"💀 {ctext('Смертельная', 'red')} команда — в больше чем {ctext('2 раза сильнее', 'red')} вашей."]

    title = "Выберите уровень сложности:"
    difficulty_index = choose_from_menu(options, title, centered=True, descriptions=descriptions)

    # Выход
    if difficulty_index == -1:
        return

    difficulty = round(get_team_cost(GameConfig.data["player_team"]) * difficulty_coefficients[difficulty_index])

    # Создаём копию списка команд
    team_1 = copy.deepcopy(GameConfig.data["player_team"])
    GameConfig.data["enemy_team"] = generate_team(False, difficulty)
    team_2 = copy.deepcopy(GameConfig.data["enemy_team"])

    # Запускаем игру
    game(team_1, team_2, 0)
    GameConfig.show_day = False


def continue_game():
    if not GameConfig.data["player_team"] or not GameConfig.data["enemy_team"]:
        new_game()
    GameConfig.current_day, GameConfig.move_history = '', []
    team1 = copy.deepcopy(GameConfig.data["player_team"])
    team2 = copy.deepcopy(GameConfig.data["enemy_team"])
    game(team1, team2, GameConfig.current_bot_mode)
    GameConfig.show_day = False


def exit_game():
    """
    Очищает консоль и останавливает код.
    """
    clear_console()
    sys.exit()


@ignore_interrupt
def menu():
    """
    Отображает главное меню игры и обрабатывает выбор пользователя.

    Меню включает следующие опции:
    - Испытания: выбор уровня сложности.
    - Быстрая игра: начать новую игру.
    - Продолжить: продолжить сохраненную игру.
    - Настройки: изменить настройки игры.
    - Команда: изменить состав команды.
    - Выход: завершить игру.
    - Отладка: режим отладки (скрытая опция).

    Использует декоратор @ignore_interrupt для игнорирования прерываний (например, Ctrl+C).
    """
    GameConfig.show_day = False  # Скрыть отображение дня при входе в меню

    # Опции меню
    MENU_OPTIONS = [
        "Испытания",
        "Быстрая игра",
        "Продолжить",
        "Настройки",
        "Команда",
        "Выход",
        "     ",  # Секретная опция для просмотра истории обновления
        ctext('отладка', 'dark_grey')  # Скрытая опция отладки
    ]

    # Действия, соответствующие опциям меню
    MENU_ACTIONS = [
        Challenges.choose_level,    # Испытания
        new_game,                   # Быстрая игра
        continue_game,              # Продолжить
        settings,                   # Настройки
        set_team,                   # Команда
        exit_game,                  # Выход
        lambda: print_info(GameConfig.updates_history),
        debug                       # Отладка
    ]

    while True:
        # Отображение меню и получение выбора пользователя
        selected_action = choose_from_menu(MENU_OPTIONS, title="Меню", centered=True)

        # Выполнение выбранного действия
        MENU_ACTIONS[selected_action]()


@ignore_interrupt
def settings():
    """
    Меню с настройками.

    Настройки:
    - Вертикальная таблица юнитов: если включено, отображается вертикальная таблица юнитов.
    """
    choiced_option = 0
    while True:
        title = "Настройки"
        options = [f"{key.capitalize().replace('_', ' ')}: {value}" for key, value in
                   GameConfig.settings.items()]

        # Выбор настройки
        choiced_option = choose_from_menu(options, title, centered=True, start_index=choiced_option)
        setting_option = list(GameConfig.settings.keys())[choiced_option]

        # Выход
        if choiced_option == -1:
            return

        # Изменения флага с False на True
        else:
            GameConfig.settings[setting_option] = not GameConfig.settings[setting_option]


@ignore_interrupt
def character_editor():
    """
    Меню с редактором персонажей.

    Редактор персонажей позволяет изменять параметры юнитов и их модификаторы.
    """


@ignore_interrupt
def debug():
    """
    Функция с опциями для пользователя, с помощью которой можно управлять читами и смотреть переменные.
    """
    action = choiced_option = 0
    while True:
        # Выбор опции отладки
        title = "Отладка"
        options = ["Читы", "Дата"]
        action = choose_from_menu(options, title, centered=True, start_index=action)

        # Выход
        if action == -1:
            return

        # Читы
        if action == 0:
            while True:
                # Форматирование интерактивного списка
                title = "Читы"
                options = [f"{key.capitalize().replace('_', ' ')}: {value}" for key, value in
                           GameConfig.debug_mode.items()]
                # Выбор чита
                choiced_option = choose_from_menu(options, title, centered=True, start_index=choiced_option)
                debug_option = list(GameConfig.debug_mode.keys())[choiced_option]

                # Выход
                if choiced_option == -1:
                    return

                # Изменения флага с False на True
                else:
                    GameConfig.debug_mode[debug_option] = not GameConfig.debug_mode[debug_option]

                # Если включен чит на бесконечные ходы включить чит на возможность пропуска ходов
                if GameConfig.debug_mode["infinity_moves"]:
                    GameConfig.debug_mode["skip_move"] = True

        # Переменные
        elif action == 1:
            while True:
                # Выбор опции пользователем
                title = "Дата"
                options = [key.capitalize() for key in GameConfig.data.keys()]
                choiced_option = choose_from_menu(options, title, centered=True, start_index=choiced_option)
                option = list(GameConfig.data.keys())[choiced_option]

                # Выход
                if choiced_option == -1:
                    return

                else:
                    # Если переменная является списком юнитов
                    if isinstance(GameConfig.data[option], list) and all(
                            isinstance(item, Character) for item in GameConfig.data[option]):
                        info_list = list(map(lambda unit: unit(0), GameConfig.data[option]))
                        info = ", ".join(info_list)
                    # Вывод переменной
                    else:
                        info = GameConfig.data[option]
                    print_info(info)


def main():
    print(ctext(f"ВЕРСИЯ {GameConfig.version}\n", "red"))
    # loading(lambda: time.sleep(1))()

    GameConfig.data["player_team"]: list[Character] = [Dagger(name="Первый", level=3), Archer("enemy", level=3)]

    menu()


if __name__ == "__main__":
    if not supports_ansi():
        print("Внимание, текущая консоль не поддерживает цветной текст.")
        input("Ентер, что бы продолжить")
        ctext = lambda text, color: str(text)
        clear_console()

    # Оборачивание функции в декоратор
    Ai.random_move = progress_bar(title="Ход бота")(Ai.random_move)
    Ai.script_move = progress_bar(title="Ход бота")(Ai.script_move)
    main()
