from funcktions import rand_name, print_slow, ctext, time, Config, TargetMode


# Определение базового класса персонажа
class Character:
    """Родительский класс для определения базовых функций персонажа"""

    # Атрибуты:
    #   имя
    #   здоровье
    #   сила
    #   коофициент усиления
    #   поднят ли щит | если поднят, то сила понижается в два раза и урон по нему проходит в два раза меньше
    #   список огня (каждый ход из этого списка берётся урон и наносится себе)
    #   кд невидимости для того, что бы нельзя было накладывать невидимость каждый ход
    #   невидимый ли персонаж

    # Методы:
    #   атака - в этот метод передаётся цель и урон по желанию, если цели нет, это считается за пропуск хода
    #   получение урона
    #   проработка хода - этот метод должен реализовываться в дочерних классах, где описывается его действия
    #   статический ход - должен вызываться после каждого хода и отвечает за второстепенные действия
    #       (вроде получения урона от огня)
    #   поднять/опустить щит

    def __init__(self, name: str = None, hp: int = None,
                 power: int = None, class_name: str = '', class_name2: str = '', class_name3: str = ''):
        if class_name2 == '':
            class_name2 = class_name + "а"
        if class_name3 == '':
            class_name3 = class_name + "у"

        # если имя не передано, то поставить случайное
        if name is None:
            name = rand_name()
        self.name = ctext('BLUE', class_name) + ' ' + ctext('LIGHTBLUE_EX', name)
        self.name2 = ctext('BLUE', class_name2) + ' ' + ctext('LIGHTBLUE_EX', name)
        self.name3 = ctext('BLUE', class_name3) + ' ' + ctext('LIGHTBLUE_EX', name)

        # если сила/здоровье не указано, поставить по умолчанию
        self._hp = Config.start_hp if hp is None else hp
        self._power = Config.start_power if power is None else power
        self.max_hp = self.hp

        self.power_multiple = 1
        self.is_shield_up = False
        self.flame_list = []
        self.invisibility_cd = -1
        self.is_visible = True

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def power(self):
        return self._power * self.power_multiple

    @power.setter
    def power(self, value):
        self._power = value

    def __str__(self):
        additionally = []
        if not self.is_visible:
            additionally.append(ctext("BLUE", "Невидимый"))
        if self.power_multiple != 1:
            additionally.append(ctext("BLUE", "Усиление - " + str(self.power_multiple)))
        if len(self.flame_list) > 0:
            additionally.append(ctext('RED', f'Горит ещё {len(self.flame_list)} хода'))

        result = f"{self.name} - Здоровье: {ctext('GREEN', self.hp)} | Сила: " + ctext('RED', self.power)
        if additionally:
            result += f" ({', '.join(additionally)})"
        return result

    def attack(self, target, damage: int = None):
        if target is None:
            print(f"{self.name} пропускает ход")
            return

        # если урон не указан установить свою силу
        if damage is None:
            damage = self.power
        if self.is_shield_up:
            damage //= 2
        print(f"{self.name} атакует {target.name2}, нанося {ctext('RED', damage)} урона")
        # <имя> атакует <имя врага>, нанося 10 урона
        target.take_damage(damage)  # у врага вызывается этот метод, в который передаётся урон

        # если игрок был усилен, усиление пропадает
        if self.power_multiple != 1:
            self.power_multiple = 1
            print(f"    усиление {self.name2} установлено на:", ctext('RED', '1'), "| урон:", ctext("RED", self.power))

        if target.flame_list:
            print(f"    {self.name} поджёгся от горящего {target.name2}")
            self.flame_list.append(10)

    def take_damage(self, damage):
        hp = self.hp
        if self.is_shield_up:
            self._hp -= round(damage / 2)
        else:
            self.hp -= damage
        print(f"    {self.name} получает {ctext('RED', hp - self.hp)} урона |"
              f" здоровье: {ctext('GREEN', max(0, self.hp))}")
        #     <имя> получает 10 урона, | здоровье: 140
        # если <= 0 то погибает
        if self.hp <= 0:
            print(f"    {self.name} погибает")
            time.sleep(Config.delay["death"])
            return

    # абстрактный метод хода
    def make_a_move(self, friends, enemies):
        raise Exception("не определена функция 'make a move'")

    def make_a_move_static(self):

        if self.flame_list:
            print(f"    {self.name} получает {ctext('RED', self.flame_list[0])} урона от горения ", end="")
            self.hp -= self.flame_list.pop(0)
            if len(self.flame_list) != 0:
                print(f"(он будет ещё гореть {ctext('RED', len(self.flame_list))} ходов)", end="")
            else:
                print("(он больше не горит)", end="")
            print(f" | здоровье: {ctext('GREEN', max(0, self.hp))}")

        if not self.is_visible:
            self.is_visible = True
            print(f"невидимость {self.name2} пропадает")
        self.invisibility_cd = max(self.invisibility_cd - 1, -1)

    def shield_up(self):
        print(f"{self.name} поднял щит")
        self.is_shield_up = True

    def shield_down(self):
        print(f"        {self.name} опустил щит")
        self.is_shield_up = False


# класс, в котором хранятся способности
class Abilities:
    # Методы:
    #   подлечить союзника
    #   усилить союзника - его сила увеличивается в 2 раза
    #   поджигание врага (или союзника)
    #   невидимость - враги не могут атаковать невидимого персонажа
    #   создание скелета

    def heal(self: Character, target=None, power: float = None):
        if power is None:
            power = self.power
        if isinstance(target, list):
            names_list = [char.name3 for char in target]
            print(self.name, "восстановил", ', '.join(names_list), ctext('GREEN', power), "здоровья")
            for char in target:
                char.health = min(char.health + power, char.max_hp)
            return
        # если цель не указана установить себя
        if target is None:
            target = self
        target.hp = min(target.hp + power, target.max_hp)

        if target == self:
            print(self.name, "восстановил себе", ctext('GREEN', power),
                  "здоровья", end=" ")
            # <имя> восстановил себе 10 здоровья
        else:
            print(self.name, "восстановил", target.name3, ctext('GREEN', power),
                  "здоровья", end=" ")
            # <имя> восстановил <имя друга> 10 здоровья
        print(f"| текущее: {ctext('GREEN', self.hp)}")

        # если персонаж был усилен, убрать усиление
        if self.power_multiple != 1 and power == self.power:
            print(f"    сила {self.name2} установлена на:", ctext('RED', power))
            super().power_multiple = 1

    def enhance(self: Character, targets=None):
        # если цель не указана установить себя
        if targets is None:
            targets = self
        elif isinstance(targets, list):
            for char in targets:
                char.power_multiple *= 2
            names = [name.name2 for name in targets]
            names = ", ".join(names)
            print(f"{self.name} усилил {names} в 2 раза")

        if targets == self:
            targets.power_multiple *= 2
            print(f"{self.name} усилился в 2 раза | сила: {ctext('RED', targets.power)}")
            # <имя> усилился в 2 раза | сила: 20
        elif isinstance(targets, Character):
            targets.power_multiple *= 2
            print(f"{self.name} усилил {targets.name2} в 2 раза | сила:",
                  ctext('RED', targets.power * self.power_multiple))
            # <имя> усилил <имя друга> в 2 раза | сила: 20

    def light_up(self: Character, target: Character = None, count: int = 3, fire_damage: int = None):
        if fire_damage is None:
            fire_damage = self.power // 2
        print(f"{self.name} поджигает {target.name2} на {ctext('RED', count)} дня |"
              f" сила огня: {ctext('RED', fire_damage)}")
        for _ in range(count):
            target.flame_list.append(fire_damage)
        self.power_multiple = 1
        print(f"    усиление {self.name2} установлено на:", ctext('RED', '1'), "| урон:", ctext("RED", self.power))

    def set_invisibility(self: Character, target: Character = None, mode=None):
        """Персонаж становится невидимым (можно применять раз в два хода)"""
        if self.invisibility_cd >= 0 and mode != "force":
            raise Exception("Невидимость ещё не откатилась")

        if target is None:
            target = self
            print(f"{self.name} применяет невидимость на 1 ход")
        else:
            print(f"{self.name} применяет невидимость к {target.name3} на 1 ход")
        target.is_visible = False
        self.invisibility_cd = 1

    def summon_skeleton(self: Character, friend_team: list):
        name = rand_name()
        print(f"{self.name} призывает скелета {ctext('BLUE', name)}")
        friend_team.append(Skeleton(name=name))


# ======== Классы персонажей ========
class Player(Character, Abilities):
    # игрок может использовать любые способности
    def __init__(self, name: str = None, hp: int = 150, power: int = 10,
                 can_use_abilities: bool = True, allowed_abilities: list = None):
        if name == '':
            name = None
        super().__init__(name=name, hp=hp, power=power, class_name="Игрок")

        self.max_hp = self.hp
        self.can_use_abilities = can_use_abilities
        # список всех способностей
        all_abilities_list = [method for method in dir(Abilities) if not method.startswith("__")]
        names_abilities_list = ['Лечение', "Усиление", "Поджечь", "Невидимость", "Призвать"]
        if len(names_abilities_list) != len(all_abilities_list):
            raise Exception("Способности показываются не правильно игроку |",
                            f"есть: {len(names_abilities_list)}, нужно: {len(all_abilities_list)}")
        self.allowed_abilities = allowed_abilities if allowed_abilities else names_abilities_list

        self.items = []

    def add_item(self, item):
        print(f"{self.name3} добавлен предмет: {ctext('Blue', item)}")
        self.items.append(item)

    def make_a_move(self, friends, enemies):
        enemies = [enemy for enemy in enemies if enemy.is_visible]

        # цикл, пока игрок не выберет
        while True:
            try:
                print(f"\nВаш ход {self.name} (на поле {ctext('RED', len(enemies))} врагов | у вас"
                      f" {ctext('GREEN', self.hp)} здоровья):")

                # выводит информацию о выборе
                show_choice = ['Пропустить', 'Атаковать']
                if self.can_use_abilities:
                    show_choice.append('Способности')
                if self.items:
                    show_choice.append('Вещи')
                for idx, move in enumerate(show_choice):
                    print(f"{ctext('YELLOW', idx)}. {move}")

                # выбор игрока собственно
                choice = int(input(f"Введите {ctext('YELLOW', 'номер действия: ')}"))

                if choice == 0:
                    print_slow(ctext("lightblack_ex", "Пропуск"), 0.1)
                    return "Пропуск"

                # атака
                elif choice == 1:
                    # показывает список врагов
                    print(f"    Выберите цель для атаки (ваш урон: {ctext('RED', self.power)}):")
                    for idx, friend in enumerate(enemies):
                        print(f"    {ctext('YELLOW', idx + 1)}. {friend}")

                    # выбор игрока
                    target_choice = int(input(f"    Введите {ctext('YELLOW', 'номер цели')}: ")) - 1

                    if target_choice == -1:
                        continue

                    # игрок атакует
                    target = enemies[target_choice]
                    self.attack(target, self.power)
                    return "Атака"

                # способности
                elif choice == 2 and self.can_use_abilities:
                    # Список доступных способностей
                    abilities_list = self.allowed_abilities

                    print(f"    {ctext('YELLOW', '0')}. Назад")
                    for idx, ability in enumerate(abilities_list, 1):
                        print(f"    {ctext('YELLOW', idx)}. {ability}")

                    # Выбор способности
                    choice_ability = int(input(f"Введите {ctext('YELLOW', 'номер действия: ')}"))
                    if choice_ability == 0:
                        continue
                    elif choice_ability > len(self.allowed_abilities):
                        raise IndexError

                    target = None
                    if choice_ability != 5:
                        # Вывод списка персонажей
                        print("    Союзники:")
                        for idx, friend in enumerate(friends, 1):
                            print(f"    {ctext('YELLOW', idx)}. {friend.name} - Здоровье: {ctext('GREEN', friend.health)}")
                        print("    Враги:")
                        for idx, enemy in enumerate(enemies, len(friends) + 1):
                            print(f"    {ctext('YELLOW', idx)}. {enemy.name} - Здоровье: {ctext('GREEN', enemy.health)}")

                        target = int(input(f"Введите {ctext('YELLOW', 'номер цели')}: ")) - 1
                        target = (friends + enemies)[target]

                    # Использование выбранной способности
                    if choice_ability <= len(abilities_list):
                        ability_name = abilities_list[choice_ability - 1]
                        if ability_name == "Лечение":
                            self.heal(target)
                        elif ability_name == "Усиление":
                            self.enhance(target)
                        elif ability_name == "Поджечь":
                            self.light_up(target)
                        elif ability_name == "Невидимость":
                            self.set_invisibility(target)
                        elif ability_name == "Призвать":
                            self.summon_skeleton(friends)

                elif choice == 3 and self.items:
                    items_list = self.items

                    print(f"    {ctext('YELLOW', '0')}. Назад")
                    for idx, item in enumerate(items_list, 1):
                        print(f"    {ctext('YELLOW', idx)}. {item}")

                    target = int(input(f"Введите {ctext('YELLOW', 'номер предмета')}: ")) - 1
                    if target == -1:
                        continue
                    target = self.items[target]

                    if target == "Аптечка":
                        self.hp = self.max_hp
                        print(self.name, f"использует {ctext('yellow', 'аптечку')} | здоровье:", end=" ")
                        print(ctext('green', f'{self.hp} из {self.max_hp}'))
                    elif target == "Мантия":
                        self.hp = self.max_hp
                        print(self.name, f"использует {ctext('yellow', 'мантию')}")
                        self.set_invisibility(mode="force")
                    elif target == "Стеклянный нож":
                        self.hp = self.max_hp
                        print(self.name, f"использует {ctext('yellow', 'нож')}")
                        self.attack(TargetMode.first_in_order(enemies), damage=self.power*3)

                    self.items.remove(target)

                    continue

                else:
                    print("Недопустимый номер действия")
                    time.sleep(Config.delay["mistake"])
                    continue

                break  # завершение хода игрока

            except IndexError:
                print("Не допустимый номер")
                time.sleep(Config.delay["mistake"])
            except ValueError:
                print("Введите целое число")
                time.sleep(Config.delay["mistake"])
            except Exception as exc:
                print(exc)
                time.sleep(Config.delay["mistake"])

        print()


class Skeleton(Character):
    # он слабый
    def __init__(self, name=None):
        if name is None:
            name = rand_name()
        super().__init__(name=name, hp=10, power=5, class_name="Скелет")

    def make_a_move(self, friends, enemies):
        enemies = [enemy for enemy in enemies if enemy.is_visible]

        target = TargetMode.random_target(enemies)
        self.attack(target)


class Tank(Character):
    def __init__(self, name: str = None, hp: int = 300, power: int = 10):
        self.start_hp = hp
        super().__init__(name=name, hp=hp, power=power, class_name="Танк")

    def make_a_move(self, friends, enemies):
        enemies = [enemy for enemy in enemies if enemy.is_visible]
        if self.hp <= self.start_hp // 2 and not self.is_shield_up:
            self.shield_up()
        elif self.hp >= self.start_hp // 2 + 10 and self.is_shield_up:
            self.shield_down()
        else:
            target = TargetMode.first_in_order(enemies)
            self.attack(target)


class GainTower(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 30):
        super().__init__(name=name, hp=hp, power=0, class_name="Башня усиления")

    def make_a_move(self, friends, enemies):
        friends = [char for char in friends if not isinstance(char, (GainTower, TreatmentTower))]
        self.enhance(friends)


class TreatmentTower(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 30):
        super().__init__(name=name, hp=hp, power=10, class_name="Башня лечения")

    def make_a_move(self, friends, enemies):
        friends = [char for char in friends if not isinstance(char, (GainTower, TreatmentTower))]
        self.heal(friends)


class Archer(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 80, power: int = 10):
        self.start_hp = hp
        super().__init__(name=name, hp=hp, power=power, class_name="Лучник")

    def make_a_move(self, friends, enemies):
        # отделяем скелетов от остальной команды
        enemies_chars = [enemy for enemy in enemies if enemy.is_visible and not isinstance(enemy, Skeleton)]
        enemies_skeletons = [enemy for enemy in enemies if isinstance(enemy, Skeleton)]

        friends = [friend for friend in friends if not isinstance(friend, (Skeleton, TreatmentTower, GainTower))]
        lowest_friend = TargetMode.lowest_hp(friends)

        if self.hp <= self.start_hp // 2 and self.invisibility_cd < 0:
            self.set_invisibility()
        elif lowest_friend.health <= 60 and self.invisibility_cd < 0 and lowest_friend.is_visible:
            self.set_invisibility(lowest_friend)
        else:
            if enemies_chars:
                target = TargetMode.lowest_hp(enemies_chars)
            else:
                target = TargetMode.random_target(enemies_skeletons)
            self.attack(target)


class Summoner(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 50, power: int = 10):
        super().__init__(name=name, hp=hp, power=power, class_name="Призыватель", class_name2="Призывателя",
                         class_name3="Призывателю")

    def make_a_move(self, friends, enemies):
        friend_skeleton_count = len([skeleton for skeleton in friends if skeleton is Skeleton])
        if friend_skeleton_count < 3:
            self.summon_skeleton(friends)


class Mage(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 100, power: int = 30):
        super().__init__(name=name, hp=hp, power=power, class_name="Маг")

    def make_a_move(self, friends, enemies):
        friends = [char for char in enemies if char.is_visible and not isinstance(char, Skeleton)
                   and isinstance(char, GainTower)]

        target_friend = TargetMode.lowest_hp(friends)
        target_enemy = TargetMode.highest_power(enemies)

        if target_friend is not None and target_friend.health <= 50:
            self.heal(target_friend)
        else:
            self.light_up(target_enemy)


class Boss(Character, Abilities):
    def __init__(self, name: str = None, hp: int = 900, power: int = 15):
        super().__init__(name=name, hp=hp, power=power, class_name="Босс")

    def make_a_move(self, friends, enemies):
        for _ in range(2):
            self.enhance(self)
            self.attack(TargetMode.highest_power(enemies))


if __name__ == "__main__":
    tank = Tank(power=20)
    test = Player(hp=60, power=50, allowed_abilities=['Лечение'])
    test2 = Player(can_use_abilities=False)
    sk = Skeleton()
    arc = Archer()
    gr = GainTower()
    tr = TreatmentTower()

    test.add_item('Аптечка')
    test.add_item('Мантия')
    test.add_item('стеклянный нож')

    team1 = [test]
    team2 = [sk]

    for i in range(10):
        for i in team1:
            i.make_a_move(team1, team2)
        for i in team2:
            i.make_a_move(team2, team1)
        for i in team1 + team2:
            i.make_a_move_static()
