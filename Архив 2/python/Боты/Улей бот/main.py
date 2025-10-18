import math
import telebot
import json
import time
from telebot import types
import hives
import re
import datetime

from .....MiniProjects.config import TELEGRAM_BOT_TOKEN 

with open('config.json', 'r', encoding='utf-8') as config_file_json:
    config = json.load(config_file_json)
    # Инициализация бота
    TOKEN = config['TOKEN']
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

    # Ключ к кодированию айди
    encryption_key = int(config['encryption_key'])
    # Путь к файлу с данными пользователей
    DATA_FILE = config['DATA_FILE']
    LOG_FILE = config['LOG_FILE']
    config_file = config_file_json.name

    # Время на которое будет поднят щит у игрока (в секундах) (1 час = 3600 секунд)
    fixed_shield_raising_time = config['fixed_shield_raising_time']
    # Время на перезарядку ловли пчелы
    bee_catch_cooldown = config['bee_catch_cooldown']
    # Время на перезарядку рейда
    raid_cooldown = config['raid_cooldown']

    # Айди разработчика
    developer_id = config['developer_id']


class NotFound(Exception):
    pass


def save_data(func):
    """
    Декоратор для сохранения данных в файл JSON.
    """
    def wrapper(*args, **kwargs):
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Вызываем функцию и передаем данные
        func(data, *args, **kwargs)

        # Сохраняем обновленные данные обратно в файл JSON
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=4)  # Используем json.dump для сохранения с отступами

    return wrapper


@save_data
def process_data(data):
    today = datetime.date.today()

    # Проверяем и устанавливаем последний день, если он еще не установлен
    if 'last_day' not in data:
        data['last_day'] = today.isoformat()  # Преобразуем дату в строку формата ISO
    last_day = data['last_day']

    # Проверяем, был ли новый день, и если да, то записываем его в файл логов
    if today.isoformat() != last_day:
        try:
            with open(LOG_FILE, 'a') as f:
                f.write(f'{today.isoformat():-^40}\n')
            data['last_day'] = today.isoformat()  # Преобразуем дату в строку формата ISO
        except IOError as e:
            print(f"Ошибка при записи в файл логов: {e}")


def get_data():
    """
    Получает данные из JSON файла.

    :return: Содержимое файла в формате словаря.
    """
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{DATA_FILE}' не найден.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        return {}


def set_data(data):
    """
    Записывает данные в JSON файл.

    :param data: Данные для записи.
    """
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Ошибка при записи данных в файл '{DATA_FILE}': {e}")


def encrypt_code(code):
    """
    Шифрует/дешифрует числовой код с использованием ключа.

    :param code: Числовой код для шифрования.
    :return: Зашифрованный/расшифровывает код.
    """
    encrypted_code = int(code) ^ encryption_key
    return encrypted_code


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


def format_readable_time(seconds):
    """
    Функция преобразует количество секунд в читаемый формат (часы, минуты, секунды)
    с правильными окончаниями для русского языка.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    # Формируем читаемую строку времени
    if hours > 0:
        # Определяем правильные окончания для часов
        return format_readable_count(math.floor(hours+1), 'час', 'часа', 'часы')
    elif minutes > 0:
        # Определяем правильные окончания для минут
        return format_readable_count(math.floor(minutes+1), 'минута', 'минуты', 'минут')
    else:
        # Определяем правильные окончания для секунд
        return format_readable_count(round(remaining_seconds), 'секунда', 'секунды', 'секунд')


def format_user_data(sorted_data):
    """
    Форматирует данные о пользователях для отображения.

    :param sorted_data: Отсортированные данные о пользователях.
    :return: Список отформатированных строк.
    """
    formatted_data = []

    for username, user_data in sorted_data:
        name = user_data['name']
        bee_count = user_data['bee_count']
        id_value = user_data['id']

        # Вычисляем количество точек для выравнивания имени
        dots_count = max(0, 12 - len(name) - len(str(bee_count)))

        # Формируем строку с точным выравниванием
        formatted_name = f"{name} {'...' * dots_count} {bee_count}   <code>{id_value}</code>"
        formatted_data.append(formatted_name)

    return formatted_data


def display_user_data(sort_method='name'):
    """
    Отображает данные о пользователях, отсортированные по указанному методу.

    :param sort_method: Метод сортировки данных (по умолчанию 'name'). Возможные значения: 'name', 'count', 'id'.
    :return: Отформатированные данные о пользователях в виде строки.
    """
    data = get_data()

    if not data:
        return "Ошибка при загрузке данных. Не удалось отобразить пользователей."

    sort_methods = {
        'count': lambda item: item[1]['bee_count'],
        'id': lambda item: item[1]['id'],
        'name': lambda item: item[1]['name']
    }

    sorted_data = sorted(data.items(), key=sort_methods[sort_method], reverse=True if sort_method == 'count' else False)

    formatted_data = format_user_data(sorted_data)

    return '\n'.join(formatted_data)


def find(key):
    """
    Ищет в данных пользователя по ключу.

    Args:
        key (str): Ключ, по которому производится поиск.

    Returns:
        str: Имя пользователя, у которого найдено значение, соответствующее ключу.

    Raises:
        NotFound: Если не найдено ни одного пользователя с заданным значением.
    """
    data = get_data()

    for username, user_data in data.items():
        if any(value == float(key) for value in user_data.values()):
            return username

    raise NotFound("Не найдено")


def find_values_by_key(key):
    """
    Ищет значения по ключу во вложенных словарях JSON-объекта.

    Args:
        key (str): Ключ, значения по которому нужно найти.

    Returns:
        list: Список значений, соответствующих ключу.
    """
    json_obj = get_data()
    results = []

    # Функция для рекурсивного поиска значений по ключу
    def search_values(obj, key2, cur_level=0, level=-1):
        cur_level += 1
        if isinstance(obj, dict) and (cur_level == level or level == -1):
            if key2 in obj:
                results.append(obj[key2])
                level = cur_level
            for v in obj.values():
                search_values(v, key2, cur_level=cur_level, level=level)

    # Начинаем поиск значений по ключу
    search_values(json_obj, key)

    return results


def extract_command_and_descriptions(return_type='tuple'):
    """
    Извлекает команды и их описания из файла main.py.

    Args:
        return_type (str, optional): Тип возвращаемых данных. Возможные значения:
         'tuple', 'commands', 'descriptions', 'string'. По умолчанию 'tuple'.

    Returns:
        tuple or list or str: В зависимости от значения return_type:
            - 'tuple': список кортежей (команда, описание)
            - 'commands': список команд
            - 'descriptions': список описаний
            - 'string': строка с перечислением команд и описаний
    """
    commands_list = []  # Список для хранения найденных команд
    descriptions_list = []
    commands_and_descriptions = []

    # Открываем файл для чтения
    with open('main.py', 'r', encoding='utf-8') as file:
        # Перебираем строки файла
        for line in file:
            # Ищем строки, содержащие 'commands='
            if 'commands=' in line:
                # Используем регулярное выражение для извлечения информации
                sample = r"@bot\.message_handler\(commands=\['(\w+)'\]\)\s*#\s*(.*)"
                match = re.search(sample, line)
                if match:
                    commands_list.append(match.group(1))  # Добавляем команду и описание в список
                    descriptions_list.append(match.group(2))
                    commands_and_descriptions.append((match.group(1), match.group(2)))

    if return_type == 'tuple':
        return commands_and_descriptions
    elif return_type == 'commands':
        return commands_list
    elif return_type == 'descriptions':
        return descriptions_list
    elif return_type == 'string':
        return '\n'.join([f'/{command[0]} {command[1]}' for command in commands_and_descriptions])


def print_and_log(*args, **kwargs):
    """
    Выводит информацию на экран и записывает её в файл журнала.

    Args:
        *args: Позиционные аргументы для вывода.
        **kwargs: Именованные аргументы для вывода.

    Returns:
        None
    """
    if list(args)[0] == 'viverna_1':
        return
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as file:
            process_data()
            current_time = datetime.datetime.now().time()
            formatted_time = '[' + str(current_time)[:-7] + ']'
            print(formatted_time, *args, **kwargs)
            print(formatted_time, *args, **kwargs, file=file)
    except Exception as e:
        print("Произошла ошибка при записи в файл (в функции print_and_log):", e)


def format_info(info_dict):
    """
    Форматирует информацию из словаря info_dict.

    Args:
        info_dict (dict): Словарь с информацией о пользователе.

    Returns:
        str: Строка с отформатированной информацией.
    """
    modified_data = {key: val for key, val in info_dict.items() if key in ['name', 'id', 'bee_count']}
    data_str = ''

    for key, value in modified_data.items():
        if key == 'id':
            data_str += f"{key}: <code>{value}</code>\n"
        else:
            data_str += f"{key}: {value}\n"

    data_str += 'действие щита: '
    data_str += format_shield_info(info_dict)

    return data_str


def format_shield_info(info_dict):
    """
    Форматирует информацию о щите.

    Args:
        info_dict (dict): Словарь с информацией о пользователе.

    Returns:
        str: Строка с информацией о щите.
    """
    time_time_events_dict = info_dict['time_events']
    if 'shield_raising_time' in time_time_events_dict:
        user_shield_raising_time = time_time_events_dict['shield_raising_time']
        is_shield_raised = time.time() - user_shield_raising_time < fixed_shield_raising_time
        if is_shield_raised:
            return (format_readable_time(fixed_shield_raising_time - (time.time() - user_shield_raising_time)) +
                    ' осталось')
        else:
            return 'отсутствует'
    else:
        return 'отсутствует'


# Функция-декоратор для обновления данных в JSON-файле
def process_user_data(func):
    """chat_id, username, first_name, message/call, user_data, data

    - chat_id (int): id чата.
    - username (str): username пользователя.
    - first_name (str): ник пользователя.
    - message/call (cls): объект сообщения.
    - user_data (dict): данные пользователя.
    - data (dict): все данные.
    """
    # Получаем объект кода функции
    code_obj = func.__code__

    # Получаем имена аргументов из атрибута co_varnames кода функции
    arguments = code_obj.co_varnames[:code_obj.co_argcount]

    def wrapper(message):
        try:
            data = get_data()

            username = message.from_user.username
            first_name = message.from_user.first_name if 'first_name' in arguments else None
            user_data = data[username] if username in data else None
            try:
                chat_id = message.chat.id if 'chat_id' in arguments else None
            except AttributeError:
                chat_id = message.from_user.id if 'chat_id' in arguments else None

            allowed_args = [arg for arg in [
                chat_id,
                username if 'username' in arguments else None,
                first_name,
                message if 'message' in arguments or 'call' in arguments else None,
                user_data if 'user_data' in arguments else None,
                data if 'data' in arguments else None
            ] if arg is not None]

            func(*allowed_args)

            set_data(data)

        except TypeError as e:
            print(e)
            bot.send_message(message.chat.id, "Ошибка, введите /start\nЕсли проблема повторится, опишите её в /report")

    return wrapper


# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
@process_user_data
def handle_start(chat_id, username, first_name, data):
    # Формирование сообщения
    out_message = "список команд тут > /s"

    # Если пользователь не зарегистрирован, создаем новую запись
    if username not in data:
        if len(first_name) > 12 and len(first_name.split()) > 1:
            update_first_name = ''
            for i in range(len(first_name.split())):
                if len(update_first_name) + len(first_name.split()[i]) < 12:
                    update_first_name += ' ' + first_name.split()[i]
            first_name = update_first_name

        data[username] = {
            "name": first_name,
            "bee_count": 0,
            "id": encrypt_code(chat_id),
            "time_events": {},
            "hives": {},
            "options": {}
        }

        print_and_log(username, 'зарегистрирован')
        out_message = f"<b>{first_name}</b>, привет!\nсписок команд тут > /s"

    # Отправка первого сообщения
    bot.send_message(chat_id, out_message, parse_mode='html')


# Показывает пользователю список команд
@bot.message_handler(commands=['s'])  # - список команд
@process_user_data
def handle_s(chat_id, username):
    print_and_log(username, 'смотрит /s')
    out_message = 'Список команд:\n'
    out_message += extract_command_and_descriptions(return_type='string')

    # Отправка сообщения
    bot.send_message(chat_id, out_message, parse_mode='html')


def generate_keyboard(button_id, button_text, keyboard: types.InlineKeyboardMarkup = None)\
        -> types.InlineKeyboardMarkup:
    """
    Генерирует клавиатуру.

    Args:
        button_id (str): Идентификатор кнопки.
        button_text (str): Текст кнопки.
        keyboard (list): Клавиатура.

    Returns:
        list: Клавиатура.
    """
    if keyboard is None:
        keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(button_text, callback_data=button_id))

    return keyboard


# Обработчик команды "info"
@bot.message_handler(commands=['info'])  # <b>(id, опционально)</b> - информация об игроке
@process_user_data
def handle_info(chat_id, username, message, data):
    username2 = ''

    # Формирование сообщения с информацией о пользователе
    user_message = message.text.split()
    if len(user_message) >= 2:
        try:
            username2 = find(user_message[1])
            print_and_log(username, 'смотрит /info о', username2)
        except NotFound:
            bot.send_message(chat_id, "Пользователь не найден")
            return
    else:
        print_and_log(username, 'смотрит /info о себе')

    # Формируем сообщение с информацией о пользователе
    out_message = format_info(data[username2 if username2 else username])
    keyboard = generate_keyboard('info_hives ' + username2, 'Показать ульи')

    bot.send_message(chat_id, out_message, parse_mode='html', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('info_'))
@process_user_data
def handle_info_addition(call, data):
    if call.data.startswith('info_hives'):
        out_message = call.message.text
        out_message += '\nУльи:\n'
        out_message += format_hives_info(data[call.data.split()[1]]['hives'])
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=out_message, parse_mode="HTML")


# Обработчик команды "/bee"
@bot.message_handler(commands=['bee'])  # - ловить пчелу
@process_user_data
def handle_bee(chat_id, username, user_data):

    last_catch_time = user_data.get('time_events').get('last_catch_time', 0)
    current_time = time.time()

    if current_time - last_catch_time < bee_catch_cooldown:
        # Если не прошло определённое время с последней пойманной пчелы
        remaining_time = int(bee_catch_cooldown - (current_time - last_catch_time))
        formated_remaining_time = format_readable_time(remaining_time)
        message_text = f"Ты не можешь поймать пчелу сейчас. Попробуй через {formated_remaining_time}."
        print_and_log(f'{username} не поймал /bee')
    else:
        # Пользователь может поймать пчелу
        user_data['bee_count'] += 1
        user_data['time_events']['last_catch_time'] = current_time

        formated_bee_count_str = format_readable_count(user_data['bee_count'], 'пчела', 'пчелы', 'пчёл')
        message_text = f"Ты поймал пчелу! Теперь у тебя {formated_bee_count_str}"
        print_and_log(f'{username} поймал /bee: (всего: {user_data["bee_count"]})')

    bot.send_message(chat_id, message_text)


hives_dict = {
        'hive': hives.Hive()
    }


def format_hives_info(user_hives_dict):
    if user_hives_dict == {}:
        return 'Их пока нет.'
    return '\n\n'.join(map(str, [hives_dict[name].from_dict(value)
                           for name, value in user_hives_dict.items()]))


@bot.message_handler(commands=['hives'])  # - просмотр ульев
@process_user_data
def handle_hives(chat_id, username, user_data):
    print_and_log(username, 'смотрит /hives')

    # берем информацию об ульях пользователя
    user_hives = user_data.get('hives', {})

    out_message = 'Ваши ульи:\n'

    out_message += format_hives_info(user_hives)

    # если у пользователя нет ульев, сообщить об этом
    if user_hives == {}:
        out_message += 'Их пока нет.'

    bot.send_message(chat_id, out_message)


@bot.message_handler(commands=['add_hive'])
@process_user_data
def handle_add_hive(chat_id, username, message, user_data):
    user_request = ''
    user_hives = user_data['hives']

    try:
        user_request: str = message.text.split()[1].lower()
    except IndexError:
        bot.send_message(message.chat.id, 'ошибка, введите /add_hive <название>')

    if hives_dict[user_request].name in user_hives:
        bot.send_message(chat_id, 'Этот улей уже у вас есть')

    else:
        user_hives[user_request] = hives_dict[user_request].to_dict()

        print_and_log(username, 'добавил улей', user_request)
        bot.send_message(chat_id, 'добавлено ' + user_request)


SORT_BY_NAME = 'name'
SORT_BY_ID = 'id'
SORT_BY_COUNT = 'count'


def create_sorting_keyboard(without):
    """
    Создает клавиатуру для сортировки данных.

    Args:
        without (str): Значение, которое не должно быть добавлено в клавиатуру.

    Returns:
        InlineKeyboardMarkup: Созданная клавиатура для сортировки.
    """
    keyboard = types.InlineKeyboardMarkup()

    # Создаем кнопки для сортировки по разным критериям
    sorting_options = [
        (SORT_BY_NAME, "Сортировать по имени"),
        (SORT_BY_ID, "Сортировать по айди"),
        (SORT_BY_COUNT, "Сортировать по количеству пчёл")
    ]

    for option, text in sorting_options:
        if option != without:
            keyboard.add(types.InlineKeyboardButton(text, callback_data='sort_by_' + option))

    return keyboard


@bot.message_handler(commands=['players_list'])  # - показывает список игроков
@process_user_data
def handle_players_list(chat_id, username):
    print_and_log(username, 'смотрит /players_list')

    keyboard = create_sorting_keyboard('name')
    out_message = display_user_data()  # Отправляем сообщение и сохраняем его объект

    message = bot.send_message(chat_id, out_message, parse_mode="HTML", reply_markup=keyboard)
    return message  # Возвращаем объект сообщения для использования в обратном вызове


@bot.callback_query_handler(func=lambda call: call.data.startswith('sort_by_'))
def handle_sorting_callback(call):
    sort_method = call.data.split('_')[-1]  # Получаем метод сортировки из callback_data

    out_message = display_user_data(sort_method)
    keyboard = create_sorting_keyboard(sort_method)

    try:
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=out_message, parse_mode="HTML", reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException as e:
        print(e)


# Обработчик команды "/raid"
@bot.message_handler(commands=['raid'])  # <b>(id)</b> - рейд
@process_user_data
def handle_raid(chat_id, username, first_name, message, user_data, data):
    try:
        # Проверяем наличие аргумента с ID цели
        if len(message.text.split()) < 2:
            bot.send_message(chat_id, 'Используйте команду в формате: /raid <ID цели>\n'
                                      'Id игроков можно посмотреть в /players_list')
            print_and_log(username, "не написал id при /raid")
            return

        target_id = message.text.split()[1]
        target = find(target_id)

        if target == username:
            print_and_log(username, 'начинает /raid на себя')
            bot.send_message(chat_id, 'Нельзя рейдить себя')
            return

        # Проверяем наличие кулдауна для рейда
        user_last_raid_time = user_data.get('time_events').get('last_raid_time', 0)
        remaining_raid_cooldown = user_last_raid_time + raid_cooldown - time.time()
        if time.time() - user_last_raid_time <= raid_cooldown:
            bot.send_message(chat_id, f'Вы можете рейдить только через'
                                      f' {format_readable_time(remaining_raid_cooldown)}')
            print_and_log(username, 'не /raid по кд')
            return

        # Проверяем возможность рейдить игрока, если у него не поднят щит
        user_shield_raising_time = data[target].get('time_events').get('shield_raising_time', 0)
        can_raid = time.time() - user_shield_raising_time > fixed_shield_raising_time

        if can_raid:
            print_and_log(username, 'начинает /raid на', target)
            # Поднимаем щит у атакованного игрока
            data[target]['time_events']['shield_raising_time'] = time.time()
            # Устанавливаем время последнего рейда атакующего
            user_data['time_events']['last_raid_time'] = time.time()

            bot.send_message(chat_id, f"Рейд на {data[target]['name']}")
            bot.send_message(encrypt_code(int(target_id)), f"Вас рейдит {first_name}")
        else:
            bot.send_message(
                chat_id,
                f"Вы не можете атаковать этого игрока, его щит действует ещё "
                f"{format_readable_time(fixed_shield_raising_time - (time.time() - user_shield_raising_time))}")

    except NotFound:
        bot.send_message(chat_id, 'Ошибка: неверный id пользователя')


@bot.message_handler(commands=['shield_down'])  # - Опустить свой щит
@process_user_data
def handle_shield_down(chat_id, user_data):
    user_shield_raising_time = user_data.get('time_events').get('shield_raising_time', 0)
    is_shield_raised = time.time() - user_shield_raising_time < fixed_shield_raising_time

    if is_shield_raised:
        keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton("Подтвердить", callback_data='shield_lower_the_shield'))
        # keyboard.add(types.InlineKeyboardButton("Отмена", callback_data='shield_cancel'))
        keyboard = generate_keyboard('shield_lower_the_shield', 'Подтвердить', keyboard=keyboard)
        keyboard = generate_keyboard('shield_cancel', 'Отмена', keyboard=keyboard)
        bot.send_message(chat_id, "Вы действительно хотите опустить свой щит?", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Ваш щит и так опущен")


@bot.callback_query_handler(func=lambda call: call.data.startswith('shield_'))
@process_user_data
def handle_sorting_callback(chat_id, call, user_data):
    if call.data == 'shield_lower_the_shield':
        user_data['time_events']['shield_raising_time'] = 0
        bot.send_message(chat_id, "Вы опустили щит")
    bot.delete_message(chat_id, call.message.message_id)


# Обработчик команды "/send"
@bot.message_handler(commands=['send'])
@process_user_data
def handle_send(chat_id, first_name, message, data):
    try:
        # Проверяем наличие аргументов
        args = message.text.split()
        if len(args) < 3:
            bot.send_message(chat_id, 'Ошибка: недостаточно аргументов. '
                                      'Используйте команду в формате: /send <ID получателя> <сообщение>')
            return

        recipient = args[1]
        message_text = ' '.join(args[2:])

        if recipient == 'all':
            # Проверяем отправителя, если он не админ, то выдаем ошибку
            if message.from_user.username != 'viverna_1':
                bot.send_message(chat_id, 'Ошибка: вы не являетесь администратором')
                return

            for user_id in find_values_by_key('id'):
                try:
                    can_send = data[find(user_id)].get('options', {}).get('advertisements_is_allowed', True)
                except KeyError:
                    data[find(user_id)]['options'] = {'advertisements_is_allowed': True}
                    can_send = True

                if can_send:
                    bot.send_message(encrypt_code(user_id), f'[{first_name} -> всем]: {message_text}')
        else:
            recipient_id = int(recipient)
            if recipient_id not in find_values_by_key('id'):
                bot.send_message(chat_id, 'Ошибка: неверный ID получателя')
                return
            bot.send_message(encrypt_code(recipient_id),
                             f"[{first_name} -> {data[find(recipient)]['name']}]: {message_text}")

        recipient = data[find(recipient)]['name'] if recipient != "all" else "всем"
        print_and_log(f'[{first_name} -> {recipient}]: {message_text}')
        bot.send_message(chat_id, 'Отправлено')

    except Exception as e:
        print("Ошибка при обработке команды /send:", e)
        bot.send_message(chat_id, 'Произошла ошибка при выполнении команды /send')


@bot.message_handler(commands=['report'])  # <b>(сообщение)</b> - сообщить об ошибке
def handle_report(message):
    chat_id = message.from_user.id
    username = message.from_user.username
    out_message = username + ' сообщил об ошибке: '
    if len(message.text.split()) < 2:
        bot.send_message(chat_id, 'Правильный формат: /report <сообщение>')
        return

    out_message += ' '.join(message.text.split()[1:])
    print_and_log(out_message)
    bot.send_message(developer_id, out_message)

    bot.send_message(chat_id, 'Отправлено')


def create_options_keyboard(user_data):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    options = user_data.get('options', {})
    notifications_enabled = options.get('advertisements_is_allowed', True)
    button1 = types.KeyboardButton(f"Уведомления: {'вкл' if notifications_enabled else 'выкл'}")
    button2 = types.KeyboardButton("скрыть")
    keyboard.add(button1, button2)
    return keyboard


@bot.message_handler(commands=['options'])  # - настройки
@process_user_data
def handle_options(chat_id, user_data):
    try:
        keyboard = create_options_keyboard(user_data)
        bot.send_message(chat_id, "Выберите настройку", reply_markup=keyboard)
    except Exception as e:
        print("Ошибка при обработке команды /options:", e)
        bot.send_message(chat_id, "Произошла ошибка при выполнении команды /options")


@bot.message_handler(commands=['test'])
@process_user_data
def handle_test(chat_id, username, user_data):
    bot.send_message(chat_id, f'test')
    if username == 'viverna_1':
        user_data['time_events']['shield_raising_time'] = time.time()


@bot.message_handler(func=lambda message: True)
@process_user_data
def handle_message(chat_id, first_name, message, user_data):
    try:
        if message.text.startswith('Уведомления: '):
            value = message.text.split()[1].lower() == 'выкл'
            user_data.setdefault('options', {})['advertisements_is_allowed'] = value
            bot.send_message(chat_id, f"Уведомления {'включены' if value else 'выключены'}",
                             reply_markup=create_options_keyboard(user_data))
        elif message.text == 'скрыть':
            bot.send_message(chat_id, "Клавиатура скрыта", reply_markup=types.ReplyKeyboardRemove())

        else:
            if message.text.startswith('/'):
                if message.text[1:] not in extract_command_and_descriptions(return_type='commands'):
                    response_message = 'Такой команды не существует\n\nАктуальный список команд:\n'
                    response_message += extract_command_and_descriptions(return_type='string')
                    bot.send_message(chat_id, response_message)
        print_and_log(f'[{first_name}]:', message.text)
    except Exception as e:
        print("Ошибка при обработке сообщения:", e)


if __name__ == '__main__':
    bot.infinity_polling()
