import random
import copy

# TODO:
# ИИ для бота
# Больше персонажей
# Нормальный показ характеристик, это короче - (can_move: True, shield: 0)


config = {
    "default_hp": 50,
    "default_damage": 10,
    "shield_protection_multiplier": 2
}


class Character:
    def __init__(self):
        self._health = config["default_hp"]
        self._damage = config["default_damage"]
        self._name = "default name"
        self._level = 1
        self._max_level = 3

        self.class_titles = ["DEFAULT_CLASS", "DEFAULT_CLASS", "DEFAULT_CLASS"]

        self.abilities = {
            "can_move": True,
            "shield": 0,
            "power_multiplier": 1
        }

    def __call__(self, num, cross=False):
        if cross:
            return ctext(f"{self.class_titles[num]} {self.name}", "cyan", "strikethrough")
        return ctext(f"{self.class_titles[num]} {self.name}", "cyan")

    def __str__(self):
        additionally = [ctext(f"{key}: {val}", "blue") for key, val in self.abilities.items()]

        character_info = f"{self.name} - Здоровье: {ctext(self.health, 'green')} | Сила: " + ctext(self.damage, 'red')
        character_info += ctext(f"  {self.level} ур", "grey")
        if additionally:
            character_info += f" ({', '.join(additionally)})"
        return character_info

    def move(self, action_type, target, report=True):
        """Выбор того, что будет делать персонаж.
        Сначала выбор, потом цель.
        0: атака
        1, 2, 3: способность"""
        if not self.abilities["can_move"]:
            raise ValueError("Пешка уже сделала ход, или не может делать ход.")

        if action_type == 0:
            self.attack(target, report=report)
        elif action_type == 1:
            self.special(target, report=report)
        elif action_type == 2:
            self.special2(target, report=report)
        elif action_type == 3:
            self.special3(target, report=report)
        self.abilities["can_move"] = False

    def take_damage(self, damage, report=True):
        hp = self.health
        if self.abilities["shield"] > 0:
            self.health -= damage // config["shield_protection_multiplier"]
        else:
            self.health -= damage
        if report:
            print(f"    {self(0, cross=False)} получает {ctext(hp - self.health, 'red')} урона |"
                  f" здоровье: {ctext(max(0, self.health), 'green')}")
        if self.health <= 0:
            if report:
                print(f"    {self(0)} погибает")

    def attack(self, target, report=True):
        total_damage = self.damage * self.abilities["power_multiplier"]
        if report:
            print(f"{self(0)} атакует {target(1)}, нанося {ctext(total_damage, 'red')} урона")
            if self.abilities["power_multiplier"] > 1:
                print(f"усиление {self(1)} обнулилось")

        print(self.abilities["power_multiplier"])
        target.take_damage(total_damage, report=report)
        if self.abilities["power_multiplier"] > 1:
            self.abilities["power_multiplier"] = 1

    def special(self, *args, **kwargs):
        raise NotImplementedError("Метод способности не реализован")

    def special2(self, *args, **kwargs):
        raise NotImplementedError("Метод третей способности не реализован")

    def special3(self, *args, **kwargs):
        raise NotImplementedError("Метод третей способности не реализован")

    def get_abilities_list(self):
        raise NotImplementedError("Метод get_abilities_list не реализован у", self(1))

    def after_move(self):
        self.abilities["can_move"] = True

    def is_positive_ability(self, num):
        raise NotImplementedError("get_positive_abilities не реализован у", self.class_titles[1])

    @property
    def name(self) -> str:
        if self.abilities["can_move"]:
            return ctext(self._name, "blue")
        else:
            return ctext(self._name, "blue", "strikethrough")

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
    def damage(self) -> int:
        return self._damage

    @damage.setter
    def damage(self, value: int):
        self._damage = value


# ПЕРСОНАЖИ
class Dagger(Character):
    def __init__(self):
        super().__init__()
        self.class_titles = ["воин", "воина", "воину"]
        self._name = "Дагер"

    def special(self, target: Character, report=True):
        if report:
            print(f"{self(0)} поднял щит {target(2)} на 3 хода")
        target.abilities["shield"] = 3

    def special2(self, target: Character, report=True):
        if report:
            print(f"{self(0)} усилил {target(1)} на х2")
        target.abilities["power_multiplier"] *= 2

    def special3(self, target: Character, report=True):
        if report:
            print(f"{self(0)} нанёс {ctext('1000', 'red')} урона {target(2)} и умер")
        target.take_damage(1000)
        self.take_damage(self.health)

    def get_abilities_list(self):
        return ["щит", "усиление", "мега удар"][:self.level]

    @staticmethod
    def is_positive_ability(num, **kwargs):
        return {0: False, 1: True, 2: True, 3: False}[num]


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
        for char in targets:
            if char.health < target.health:
                target = char
        return target

    @staticmethod
    def highest_power(targets: list):
        """Возвращает цель с самой высокой силой"""
        if not targets:
            return None
        target = targets[0]
        for char in targets:
            if char.power > target.power:
                target = char
        return target


# ФУНКЦИИ
def rand_name():
    """:return: Возвращает случайное имя"""
    names = ['Лока', 'Кирик', 'Цикада', 'Мотылек', 'Иви', 'Пинт', 'Азура', 'Зефир', 'Сирин', 'Элейн', 'Вайт', 'Лорен',
             'Зара', 'Фин', 'Эмеральд', 'Айрис', 'Скарлет', 'Найт', 'Оливия', 'Амбер', 'Зенит', 'Феликс', 'Сабина',
             'Андромеда', 'Тайга', 'Пентагон']
    return random.choice(names)


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


def update_team(team):
    """Обновляет состояние команды, если кто-то умер, то он выйдет из команды"""
    # Создание новых списков, содержащих только живых персонажей
    team = [char for char in team if char.health > 0]
    for char in team:
        char.after_move()
    return team




def player_move(current_team, enemy_team):
    while any([char.abilities["can_move"] for char in current_team]):
        print("\nВаша команда:")
        for i, char in enumerate(current_team):
            if char.abilities["can_move"]:
                print(ctext(i + 1, "yellow") + ":", char(0))
            else:
                print(ctext(i + 1, "yellow") + ":", char(0, cross=True))

        # Выбор персонажа игроком
        char = input("Персонаж: ")
        while not char:
            char = input("Персонаж: ")
        player_choice_char_index = int(char) - 1
        if 0 <= player_choice_char_index >= len(current_team):
            print(ctext("Выберите персонажа из списка", "red"))
            continue

        # Если игрок выбрал персонажа, который не может ходить
        if not current_team[player_choice_char_index].abilities["can_move"]:
            print(ctext("Вы выбрали персонажа, который не может ходить", "red"))
            continue

        player_choice_char = current_team[player_choice_char_index]

        # Ход игрока
        player_choice = player_selected_action(current_team, enemy_team, player_choice_char)

        # Отмена
        if not player_choice:
            continue
        # Сам ход пешкой
        player_choice_char.move(player_choice[0], player_choice[1])


def format_readable_count(count, option1, option2, option3):
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


def print_day(current_team, enemy_team, day):
    """
    Выводит в консоль номер дня и информацию об игроках
    """
    print("\n")
    print("=" * 50)
    print("День", day)
    print("=" * 50)

    print(f"команда 1 ({ctext(len(current_team), 'blue')} "
          f"{format_readable_count(len(current_team), 'персонаж', 'персонажа', 'персонажей')}):")
    for char1 in current_team:
        print(char1)
    print("-" * 50)
    print(f"команда 2 ({ctext(len(enemy_team), 'blue')} "
          f"{format_readable_count(len(enemy_team), 'персонаж', 'персонажа', 'персонажей')}):")

    for char2 in enemy_team:
        print(char2)
    print("=" * 50)


def minimax_bot_move(current_team, enemy_team):
    """Сначала команду бота, потом противоположную"""
    for char in current_team:
        selected_action = random.randint(0, 1)
        if selected_action == 0:
            char.move(0, TargetMode.random_target(enemy_team))
        else:
            char.move(1, TargetMode.random_target(current_team))


def random_bot_move(current_team, enemy_team):
    """Сначала команду бота, потом противоположную"""
    for char in current_team:
        selected_action = random.randint(0, 1)
        if selected_action == 0:
            char.move(0, TargetMode.random_target(enemy_team))
        else:
            char.move(1, TargetMode.random_target(current_team))


def is_team_empty(team):
    return len(team) == 0


def create_team(unit_list):
    """[(класс, имя, уровень), (класс), ...]"""
    team = []
    for char_set in unit_list:
        char = char_set[0]()

        if len(char_set) > 1:
            char.name = char_set[1]

        if len(char_set) > 2:
            char.level = char_set[2]

        team.append(char)
    return team


def set_units_level(current_team: list[Character], upgrades_count):
    upgrades_count_remained = upgrades_count
    while upgrades_count_remained > 0:
        upgrades_count_remained = upgrades_count
        print()
        for index, unit in enumerate(current_team):
            print(f'{index + 1}: {unit(0)} {ctext("ур: " + str(unit.level), "grey")}')
            unit.level = 1
        print("выберите кому присвоить +1 уровень (0 - заново):")
        while upgrades_count_remained > 0:
            player_input = input(f"осталось {upgrades_count_remained}: ")

            if not player_input.isdigit():  # Проверяем, состоит ли строка только из цифр
                print(ctext("Некорректный ввод", "red"))
                continue

            player_input = int(player_input)  # Преобразуем в число

            choice = int(player_input)

            if choice == 0:
                break

            selected_unit = current_team[choice - 1]

            if selected_unit.level > 2:
                print("максимальный уровень - 3")
                continue

            selected_unit.level += 1
            print(f'{choice}: {selected_unit(0)} {ctext("ур: " + str(selected_unit.level), "grey")}')

            upgrades_count_remained -= 1
        continue


def debug(a):
    """Можно удалить"""
    team = []
    for i in a:
        if i[0] == 1:
            char = Dagger()
        else:
            char = i[0]()
        char.name = i[1]
        team.append(char)
    return team


# ИИ
def team_indexing(team):
    return list(range(len(team)))


def generate_permutations(input_list):
    if len(input_list) == 1:
        return [input_list]

    permutations = []
    for current_index in range(len(input_list)):
        current_element = input_list[current_index]
        remaining_elements = input_list[:current_index] + input_list[current_index + 1:]
        for sub_permutation in generate_permutations(remaining_elements):
            permutations.append([current_element] + sub_permutation)
    return permutations


def evaluation(team) -> int:
    score = 0
    for char in team:
        score += char.health
    score += len(team) * 100
    return score


def minimax(current_team, enemy_team, is_maximizing):
    if is_team_empty(current_team):
        return evaluation(current_team)

    if is_maximizing:
        best_score = float('-inf')
        for char_permutation in generate_permutations(team_indexing(current_team)):
            print("\n\n\nпоследовательность союзников:")
            for char_index in char_permutation:
                for action in [0, 1]:
                    # Атака
                    if action == 0:
                        for enemy_permutation in generate_permutations(team_indexing(enemy_team)):
                            print("\nпоследовательность атаки:")
                            for enemy_index in enemy_permutation:
                                print(current_team[char_index].name,
                                      "способность" if action else "атакует",
                                      enemy_team[enemy_index].name)
                                copy_current_team = copy.deepcopy(current_team)
                                copy_enemy_team = copy.deepcopy(enemy_team)
                                copy_current_team[char_index].move(action, copy_enemy_team[enemy_index])

                    # Способность
                    else:
                        for current_permutation in generate_permutations(team_indexing(current_team)):
                            print("\nпоследовательность способности:")
                            for current_index in current_permutation:
                                print(current_team[char_index].name,
                                      "способность" if action else "атакует",
                                      current_team[current_index].name)
                                copy_current_team = copy.deepcopy(current_team)
                                copy_current_team[char_index].move(action, copy_current_team[current_index])
            print("Eval:", evaluation(current_team), evaluation(enemy_team))

    else:
        best_score = float('inf')


def game(team1: list[Character], team2: list[Character]):
    rounds = 1
    while True:
        print_day(team1, team2, rounds)
        rounds += 1

        # Ход игрока
        player_move(team1, team2)

        team2 = update_team(team2)
        if is_team_empty(team2):
            return 1

        print("\n")
        # Ход бота
        random_bot_move(team2, team1)

        team1 = update_team(team1)
        if is_team_empty(team1):
            return 2

        print("\n")


if __name__ == "__main__":
    print(ctext("ВЕРСИЯ 2.1 СКОРО БУДЕТ ДОБАВЛЕН УМНЫЙ СЛОЖНЫЙ БОТ\nпустой ввод означает отмена", "red"))

    team_1: list[Character] = create_team([(Dagger, "первый"), (Dagger, "nhtnbq")])
    team_2: list[Character] = create_team([(Dagger, "11"), (Dagger, "12")])

    set_units_level(team_1, 3)
    # minimax(team_1, team_2, True)

    winner = game(team_1, team_2)
    input(f"КОМАНДА {winner} ПОБЕДИЛА, НАЖМИ ЕНТЕР, и у тебя выключится комп")
