import uuid


class Character:
    def __init__(self, name: str = None, hp: int = 100, power: int = 10, character_class: str = None):
        self.name = name
        self._hp = hp
        self._power = power
        self.character_class = character_class
        self.id = str(uuid.uuid4())

    def __str__(self):
        content = 'Класс: {}\nИмя: {}\nЗдоровье: {}\nСила: {}'.format(self.character_class,
                                                                      self.name, self.hp, self.power)
        return content

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    def take_damage(self, damage):
        self.hp -= damage

    def attack(self, target):
        target.take_damage(self.power)

    # абстрактный метод хода
    def make_a_move(self, friends, enemies):
        raise Exception("не определена функция 'make a move'")


class Player(Character):
    def __init__(self, name: str, hp: int = 100, power: int = 10):
        super().__init__(name, hp, power, character_class='Игрок')


class Bagel(Character):
    def __init__(self, name: str = 'Бублик', hp: int = 10, power: int = 0):

        super().__init__(name, hp, power, character_class='Бублик')


class Skeleton(Character):
    def __init__(self, name: str = 'Скелет', hp: int = 30, power: int = 5):
        super().__init__(name, hp, power, character_class='Скелет')
