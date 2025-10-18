import json
import telebot

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

    TOKEN = config['TOKEN']
    DATA_FILE = config['DATA_FILE']
    CONFIG_FILE = 'config.json'

    bot = telebot.TeleBot(TOKEN)


# ============================== БД ==============================
def get_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении '{file_name}': {e}")
        return {}


def set_data(data, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Ошибка при записи в '{file_name}': {e}")


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

    arguments = code_obj.co_varnames[:code_obj.co_argcount]

    def wrapper(message):
        try:
            data = get_data(DATA_FILE)
            allowed_args = []

            if 'chat_id' in arguments:
                try:
                    chat_id = str(message.chat.id if 'chat_id' in arguments else None)
                except AttributeError:
                    chat_id = str(message.from_user.id if 'chat_id' in arguments else None)
                allowed_args.append(chat_id)
            if 'username' in arguments:
                username = message.from_user.username
                allowed_args.append(username)
            if 'first_name' in arguments:
                first_name = message.from_user.first_name if 'first_name' in arguments else None
                allowed_args.append(first_name)
            if 'message' in arguments:
                allowed_args.append(message.text)
            if 'user_data' in arguments:
                try:
                    chat_id = str(message.chat.id if 'chat_id' in arguments else None)
                except AttributeError:
                    chat_id = str(message.from_user.id if 'chat_id' in arguments else None)
                user_data = data[chat_id] if chat_id in data else None
                allowed_args.append(user_data)
            if 'data' in arguments:
                allowed_args.append(data)


            func(*allowed_args)

            set_data(data, DATA_FILE)

        except TypeError as e:
            print(e)
            bot.send_message(message.chat.id, "Ошибка, введите /start\nЕсли проблема повторится, опишите её в /report")

    return wrapper


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
    data = get_data(DATA_FILE)

    for username, user_data in data.items():
        if any(value == float(key) for value in user_data.values()):
            return username


def get_next_user_id(file_name: str) -> int:
    """
    Получает и обновляет ID пользователя в конфигурационном файле.

    Args:
        file_name: Путь к конфигурационному файлу

    Returns:
        int: Новый уникальный ID пользователя
    """
    # Чтение данных с обработкой ошибок
    config_data = get_data(file_name)

    # Получение и валидация текущего ID
    current_id = config_data.get("last_id", 0)

    # Вычисление нового ID
    new_id = int(current_id) + 1

    # Атомарное обновление конфига
    updated_config = {**config_data, "last_id": new_id}
    set_data(updated_config, file_name)

    return new_id


def find_user_key(users_data: dict, search_value):
    for user_id, user_info in users_data.items():
        if any(str(v) == str(search_value) for v in user_info.values()):
            return user_id
    return None



# ============================== Команды ==============================
@bot.message_handler(commands=['start'])
@process_user_data
def start(chat_id, username, first_name, data):
    # Регистрация
    if chat_id not in data:
        user_id = get_next_user_id(CONFIG_FILE)

        data[chat_id] = {
            "username": username,
            "name": first_name,
            "id": user_id,
            "connect": -1,
            "options": {}
        }

        print(f"{username} зарегистрирован")

        # Сообщение
        output_msg = f"<b>{first_name}</b>, привет!\nСписок команд тут > /s"
    else:
        output_msg = "Список команд тут > /s"

    bot.send_message(chat_id, output_msg, parse_mode='html')


@bot.message_handler(commands=['connect'])
@process_user_data
def connect(chat_id, message: str, user_data, data):
    try:
        other_id = message.split()[1]
        other_id = find_user_key(data, other_id)

        user_data["connect"] = other_id

        output_msg = ('Подключено к ' + data[other_id]["name"])

    except (AttributeError, IndexError):
        output_msg = ('Введите "/connect <id пользователя> к которому вы хотите подключится"\n'
                      'или "/connect_rand", что бы подключится к случайному  пользователю')
        print("Ошибка в connect")
    bot.send_message(chat_id, output_msg)


@bot.message_handler(func=lambda message: True)
@process_user_data
def handle_message(chat_id, first_name, message, user_data: dict, data):

    recipient_id = user_data.get("connect")
    recipient_name = data[recipient_id]["name"]
    output_msg = f'[{first_name} -> {recipient_name}]: ' + message

    print(output_msg)
    bot.send_message(chat_id, f"Отправлено -> {recipient_name}")
    bot.send_message(int(recipient_id), output_msg)


if __name__ == '__main__':
    bot.polling()
