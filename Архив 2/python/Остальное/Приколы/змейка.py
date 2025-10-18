import random


def key():
    return input()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_x(self, value):
        self.x -= value

    def move_y(self, value):
        self.y -= value

    def get_position(self):
        return self.x, self.y


class Tail:
    def __init__(self, start_x, start_y):
        self.tail = []

    def get(self):
        return self.tail


    def update(self, player_pos, curr_score):
        self.tail.append(player_pos)  # добавляем новую позицию в хвост
        if len(self.tail) > curr_score + 1:  # если хвост длиннее счета
            self.tail.pop(0)  # удаляем старую позицию из хвоста



def show_field(size_x, size_y, player_pos):
    for y in range(1, size_y):
        for x in range(1, size_x):
            if x == 1 or x == size_x-1 or y == 1 or y == size_y-1:
                print('#', end='')  # отрисовка стен
            elif (player_pos[0] == x and player_pos[1] == y) or ((x, y) in tail.get()):
                print('^', end='')  # отрисовка игрока
            elif apple_x == x and apple_y == y:
                print('*', end='')  # отрисовка яблока
            else:
                print(' ', end='')  # отрисовка пробелов
        print()


def spawn_apple():
    global apple_x, apple_y
    while (apple_x, apple_y) in tail.get():
        apple_x = random.randrange(2, 17, 2)  # x яблока
        apple_y = random.randint(2, 8)  # y яблока


def move_player(player_obj):
    # Получаем следующую позицию игрока
    move = key()
    while True:
        if move == "w":  # w
            player_obj.move_y(1)
        elif move == "a":  # a
            player_obj.move_x(2)
        elif move == "s":  # s
            player_obj.move_y(-1)
        elif move == "d":  # d
            player_obj.move_x(-2)
        else:
            move = key()
            continue
        break


field_size_x, field_size_y = 20, 10  # размер поля
player_x, player_y = 10, 5  # игрок
apple_x = random.randrange(2, 17, 2)  # x яблока
apple_y = random.randint(2, 8)  # y яблока
score = 0

player = Player(player_x, player_y)
tail = Tail(player_x, player_y)  # инициализация хвоста
while True:
    print('очки:', score)

    show_field(field_size_x, field_size_y, player.get_position())

    print()

    tail.update(player.get_position(), score)
    move_player(player)

    if player.get_position() in tail.get():  # игрок наткнулся на свой хвост
        print('игра окончена')
        break

    if player.get_position() == (apple_x, apple_y):  # проверка на сбор яблока
        score += 1
        spawn_apple()
