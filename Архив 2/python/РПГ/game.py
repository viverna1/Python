import keyboard
from funcktions import print_slow, time, Config, ctext, set_text_color, reset_text_color
from characters import Player, Skeleton, Tank, Archer, Summoner, GainTower, Mage, TreatmentTower, Boss


def print_day(day):
    """
    Выводит в консоль номер дня и информацию об игроках
    """
    global team1, team2
    print("="*50)
    print("День", day)
    print("="*50)

    print(f"команда 1 ({ctext('LIGHTBLUE_EX', len(team1))} персонажей):")
    for char1 in team1:
        print(char1)
    print("-"*50)
    print(f"команда 2 ({ctext('LIGHTBLUE_EX', len(team2))} персонажей):")
    for char2 in team2:
        print(char2)
    print("-"*50)


def update_teams():
    """Обновляет состояние команд, если кто-то умер, то он выйдет из команды"""
    # Создание новых списков, содержащих только живых персонажей
    global team1, team2
    alive_team_2 = [char2 for char2 in team2 if char2.health > 0]
    alive_team_1 = [char1 for char1 in team1 if char1.health > 0]
    # Обновление исходных списков
    team1 = alive_team_1
    team2 = alive_team_2


def create_team(character_classes):
    """
    Создает команду из экземпляров персонажей заданных классов.

    Returns:
    - list: Список экземпляров персонажей, сформированных в команду.
    """
    team = []
    for character_class in character_classes:
        team.append(character_class())
    return team


# Главный игровой цикл
def game():
    day = 1  # :З
    while True:
        print_day(day)
        time.sleep(Config.delay["start_day"])
        print("зона действий")

        # Действия команды 1
        print(f"\nход команды 1:\n")
        if len(team1) == 0:
            print_slow(ctext('LIGHTBLACK_EX', "... но никто не пришёл"), 0.2)
        for char in team1:
            char.make_a_move(team1, team2)
            update_teams()
            time.sleep(Config.delay["move"])
        for char in team2:
            char.make_a_move_static()
            update_teams()

        time.sleep(Config.delay["turn_completed"])

        # Действия команды 2
        print(f"\nход команды 2:\n")
        if len(team2) == 0:
            print_slow(ctext('LIGHTBLACK_EX', "... но никто не пришёл"), 0.2)
        for char in team2:
            char.make_a_move(team2, team1)
            update_teams()
            time.sleep(Config.delay["move"])
        for char in team1:
            char.make_a_move_static()
            update_teams()

        # Проверка условия завершения игры
        if len(team2) == 0:
            res = 1
            print(f'команда 1 победила')
            break
        elif len(team1) == 0:
            res = 2
            print(f'команда 2 победила')
            break

        print("\nход завершён")
        time.sleep(Config.delay["day_completed"])

        # Увеличение счетчика дня
        day += 1

    print("\nИтоги битвы:")
    print_day(day)
    return res


text = True
win = None

reset_text_color()

player = Player()
player.add_item('Стеклянный нож')
player.add_item('Стеклянный нож')
player.add_item('Аптечка')
player.add_item('Аптечка')
player.add_item('Мантия')
player.add_item('Стеклянный нож')
player.add_item('Стеклянный нож')

team1 = create_team([GainTower, GainTower, GainTower, GainTower, GainTower, GainTower, Archer, TreatmentTower])
team2 = create_team([Boss])
game()
