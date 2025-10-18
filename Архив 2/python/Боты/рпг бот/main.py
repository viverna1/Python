import telebot
from telebot import types
import characters2
from typing import Union

from .....MiniProjects.config import TELEGRAM_BOT_TOKEN 

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Словарь для отображения идентификаторов пользователей на их имена
users = {}
# Список команд с игроками
teams = {'team1': [], 'team2': []}
# Идентификатор пользователя, чей ход сейчас
current_turn_user_id = None


def switch_movers():
    global current_turn_user_id
    for user in users.keys():
        if user != current_turn_user_id:
            current_turn_user_id = user
            return


def get_users(find, opposite=False, return_type='value') -> Union[list, str, int]:
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
    global users
    # Распаковываем элементы словаря
    (key1, values1), (key2, values2) = users.items()

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


def find_team(name, opposite=False, return_type='value'):
    """
    Найти команду, в которой есть игрок с указанным именем и вернуть нужную информацию.

    Args:
        name (str): Имя игрока для поиска.
        opposite (bool, optional): Если True, вернуть противоположную команду.
                                   Если False, вернуть текущую команду. По умолчанию False.
        return_type (str, optional): Тип результата ('value', 'key', 'object').
                                     'value' - вернуть список игроков в команде.
                                     'key' - вернуть название команды.
                                     'object' - вернуть объект игрока. По умолчанию 'value'.

    Returns:
        list or str or Player: Возвращает список игроков, название команды или объект игрока.
    """
    global teams  # Используем глобальную переменную teams

    # Определяем индекс команды, с которой нужно начинать поиск
    current_index = 1 if opposite else 0

    # Перебираем команды из словаря teams
    for key, players in teams.items():
        # Проверяем наличие игрока с указанным именем в текущей команде
        if any(player.name == name or player.id == name for player in players):
            if return_type == 'key':
                return list(teams.keys())[current_index]  # Возвращаем название команды
            elif return_type == 'value':
                return list(teams.values())[current_index]  # Возвращаем список игроков в команде
            elif return_type == 'object':
                for char in players:  # Возвращаем объект класса персонажа
                    if char.id == name:
                        return char

        # Переключаемся на следующую команду (переключение между первой и второй командой)
        current_index = 1 - current_index

    # Если игрок не найден в обеих командах, возвращаем None или пустую строку
    return None


@bot.message_handler(commands=['join'])
def handle_join(message):
    if message.from_user.id in users:
        bot.send_message(message.chat.id, "Вы уже в команде")
    elif len(users) < 2:
        users[message.from_user.id] = message.from_user.first_name

        # первый игрок проходит в первую команду, второй соответственно
        if len(users) == 1:
            teams['team1'].append(characters2.Player(message.from_user.first_name))
        else:
            teams['team2'].append(characters2.Player(message.from_user.first_name))
            # ход применяется на второго игрока
            global current_turn_user_id
            current_turn_user_id = message.from_user.id

            # сообщаем первому игроку, что подключился второй
            bot.send_message(get_users(message.from_user.first_name, return_type='key'),
                             f"Вы присоединились\nИгроки: "
                             f"{', '.join([characters.name for characters in teams['team1']])} / "
                             f"{', '.join([characters.name for characters in teams['team2']])}\n")

        bot.send_message(message.chat.id, f"Вы присоединились\nИгроки: "
                                          f"{', '.join([characters.name for characters in teams['team1']])} / "
                                          f"{', '.join([characters.name for characters in teams['team2']])}\n")
        print(f"{message.from_user.first_name} подключился")

        if len(users) == 2:
            print(f"игроки: {teams['team1'][0].name}, {teams['team2'][0].name}")
    else:
        print(message.from_user.first_name, 'попытался подключится в заполненное лобби')
        bot.send_message(message.chat.id, "Мест нет")


@bot.message_handler(commands=['teams'])
def handle_teams(message):
    """Показывает пользователю информацию обо всех персонажах на поле"""
    user_name = message.from_user.first_name
    team = find_team(user_name)

    if team:
        # Находим персонажа игрока и отправляем информацию о нем
        characters_info = "Ваша команда:\n"
        characters_info += '\n\n'.join([str(character) for character in team])
        characters_info += "\n\nКоманда противника:\n"
        characters_info += '\n\n'.join([str(character) for character in find_team(user_name, opposite=True)])
        bot.send_message(message.chat.id, characters_info)

    print(message.from_user.first_name, 'смотрит персонажа')


@bot.message_handler(commands=['add'])
def handle_add(message):
    # Добавляем в команду пользователя "бублик"
    user_name = message.from_user.first_name
    team_name = find_team(user_name, return_type='key')

    try:
        user_choice = message.text.split()[1]

        characters = {
            'бублик': characters2.Bagel,
            'скелет': characters2.Skeleton
        }

        if team_name:
            teams[team_name].append(characters[user_choice]())
            bot.send_message(message.chat.id, 'В команду добавлен ' + user_choice)
            print(user_name, 'добавил в команду', user_choice)
    except IndexError:
        bot.send_message(message.chat.id, 'Введите /add <название класса>')


@bot.message_handler(commands=['move'])
def handle_move(message):
    global current_turn_user_id

    user_name = message.from_user.first_name
    if current_turn_user_id != message.from_user.id:
        bot.send_message(message.chat.id, "Сейчас не ваш ход")
        return

    # Создаем инлайн клавиатуру для действий
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Атака", callback_data='attack'))
    keyboard.add(types.InlineKeyboardButton("Действие", callback_data='action'))
    keyboard.add(types.InlineKeyboardButton("Пропустить", callback_data='skip'))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
    print(user_name, 'выбрал /move')


# Обработчик инлайн клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_name = call.from_user.first_name
    if call.data == 'attack':
        if current_turn_user_id != call.from_user.id:
            bot.send_message(call.message.chat.id, "Сейчас не ваш ход")
            return
        print('  ', call.from_user.first_name, 'выбрал атаку')

        # Создаем инлайн клавиатуру, где буду все враги
        keyboard = types.InlineKeyboardMarkup()
        # берём список всех врагов
        enemy_team = find_team(user_name, opposite=True)
        # добавляем кнопку назад
        keyboard.add(types.InlineKeyboardButton('назад', callback_data='back'))
        enemy_buttons = list()

        # формируем остальные кнопки врагов
        for enemy in enemy_team:
            enemy_buttons.append(types.InlineKeyboardButton(f'{enemy.name} - {enemy.hp}хп', callback_data=enemy.id))
        keyboard.add(*enemy_buttons)

        # отправка сформированного сообщения
        bot.send_message(call.message.chat.id, "Выбери цель:", reply_markup=keyboard)

    elif call.data in [char.id for char in find_team(user_name, opposite=True)]:
        if current_turn_user_id != call.from_user.id:
            bot.send_message(call.message.chat.id, "Сейчас не ваш ход")
            return
        # даём ходу следующему игроку
        switch_movers()

        # Получаем цель, которую выбрали
        target = find_team(call.data, return_type='object')
        # получаем того, кто атаковал
        attacker = find_team(call.data, return_type='object')
        # он атакует цель
        attacker.attack(target)

        text = 'Bы атаковали ' + target.name
        text += ' | ' + str(target.hp) + f' (-{attacker.power}) hp'
        # отправка сообщения атакующему
        bot.send_message(call.message.chat.id, text)

        # отправка цели атакующего
        attacked = get_users(target.name, return_type='key')
        bot.send_message(attacked, f"Вас атаковал {attacker.name} нанося {attacker.power} урона"
                                   f" (осталось {target.hp})")

    elif call.data == 'action':
        # Не реализовано
        user_name = call.from_user.first_name

        if current_turn_user_id != call.from_user.id:
            bot.send_message(call.message.chat.id, "Сейчас не ваш ход")
            return
        # даём ходу следующему игроку
        switch_movers()
        print('   ', user_name, 'выбрал действие')

        a = find_team(call.from_user.first_name, opposite=0)
        a = ', '.join([i.name for i in a])
        bot.send_message(call.message.chat.id, a)

    elif call.data == 'skip':
        if current_turn_user_id != call.from_user.id:
            bot.send_message(call.message.chat.id, "Сейчас не ваш ход")
            return
        # даём ходу следующему игроку
        switch_movers()

        bot.send_message(call.message.chat.id, f"Вы пропустили ход")

        player2 = get_users(call.from_user.first_name, opposite=True, return_type='key')
        bot.send_message(player2, f"Соперник пропустил ход")

    else:
        print(call.data, 'непонятно')
        print(find_team(call.from_user.first_name, opposite=1))
        print([char.id for char in find_team(user_name, opposite=True)])
        print([char.id for char in find_team(user_name, opposite=False)])
        print(call.data in [char.id for char in find_team(user_name, opposite=False)])
        bot.send_message(call.message.chat.id, 'Ошибка')


# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    current_message = f'[{message.from_user.first_name}]: ' + message.text
    opponent_id = list(users.keys())[0] if message.from_user.id == list(users.keys())[1] else list(users.keys())[1]
    bot.send_message(opponent_id, current_message)


if __name__ == '__main__':
    bot.infinity_polling()
