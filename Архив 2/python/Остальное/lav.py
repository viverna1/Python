import random


def say(*a): print(*a)


def none(): print()


def saves():
    def launch_count():
        file = open('C:/Users/v-v/OneDrive/Рабочий стол/example.txt', 'r')
        data = file.read()
        print('эта программа запущена', data, 'раз')
        file = open('C:/Users/v-v/OneDrive/Рабочий стол/example.txt', 'w')
        file.write(str(int(data) + 1))

        none()  # количество запусков программы

    # launch_count()

    def name_generator():
        import pyperclip
        import win32con
        import win32api
        import threading

        def is_ctrl_v_pressed():
            return win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(ord('V')) < 0

        def wait_for_action():
            while not is_ctrl_v_pressed():
                pass

        a, copy_list = input('названия: ').split(), []

        while True:
            if not a:
                break

            for i in a:
                i = ' ' + i + ' '
                print(f'# {i:=^60}')
                copy_list.append(f'# {i:=^60}')

            pyperclip.copy(copy_list[0])
            for i in copy_list[1:]:
                wait_for_action()
                thread = threading.Thread(target=wait_for_action)
                thread.start()
                pyperclip.copy(i)
                thread.join()

            a, copy_list = input('названия: ').split(), []

        none()  # создать названия

    # name_generator()

    def pip_install():
        import subprocess as sb

        command = 'pip install ' + input('загрузка библиотеки: ')
        if command != 'pip install ':
            sb.run(command, shell=True)

        none()  # установка библиотеки

    # pip_install()

    def CopyLevels_to_BeatSaber():
        import os
        import tempfile
        import shutil
        import zipfile

        def main():
            temp_dir = None
            try:
                # Создаем временную папку на диске D
                temp_dir = tempfile.mkdtemp(dir='D:\\', prefix='temp_folder_')
                print(f'Создана временная папка: {temp_dir}')

                # Открываем папку
                os.startfile(temp_dir)

                # В данном месте вы можете выполнить необходимые действия, например, скопировать файлы в эту папку
                folder = input('1-бит сайбер\n2-новая папка на рабочем столе\nпуть: ')
                if folder == '1':
                    folder = r'D:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels'
                elif folder == '2':
                    folder_name = "archives"
                    folder_path = create_folder_on_desktop(folder_name)
                    folder = folder_path

                source_folder = temp_dir
                process_archives(source_folder, folder)

            finally:
                print('=' * 20)
                if temp_dir:
                    # Закрываем и удаляем временную папку вместе с файлами
                    print(f'Закрываем и удаляем временную папку: {temp_dir}')
                    try:
                        shutil.rmtree(temp_dir)  # Удаляем папку рекурсивно
                    except Exception as e:
                        print(f'Ошибка при удалении временной папки: {e}')

        def process_archives(source_folder, destination_folder):
            # Получаем список файлов в папке с архивами
            archive_files = [f for f in os.listdir(source_folder) if f.endswith('.zip')]

            print('=' * 20)
            # Обработка каждого архива
            for archive_file in archive_files:
                # Получаем полный путь к архиву
                zip_file_path = os.path.join(source_folder, archive_file)

                # Получаем имя архива без расширения
                archive_name = os.path.splitext(archive_file)[0]

                # Создаем папку в указанной директории с именем архива
                extraction_path = os.path.join(destination_folder, archive_name)

                # Если папка уже существует, добавляем числовой суффикс
                count = 1
                while os.path.exists(extraction_path):
                    extraction_path = os.path.join(destination_folder, f'{archive_name}_{count}')
                    count += 1

                os.makedirs(extraction_path)

                # Извлекаем файлы из архива
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extraction_path)

                # Копируем название архива в папку
                with open(os.path.join(extraction_path, 'archive_name.txt'), 'w') as name_file:
                    name_file.write(archive_name)

                print(f'Файлы из архива "{archive_file}" успешно извлечены и скопированы в папку: {extraction_path}\n')

        def create_folder_on_desktop(folder_name):
            desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive\Рабочий стол")
            folder_path = os.path.join(desktop_path, folder_name)

            try:
                print('=' * 20)
                # Проверяем, существует ли папка
                if not os.path.exists(folder_path):
                    # Создаем папку
                    os.makedirs(folder_path)
                    print(f'Папка "{folder_name}" создана на рабочем столе по пути: {folder_path}')

                return folder_path

            except Exception as e:
                print(f'Ошибка при создании папки: {e}')
                return None

        if __name__ == "__main__":
            main()

        none()  # копирование архивов

    # CopyLevels_to_BeatSaber()

    def corrector():
        from pyperclip import copy
        from pyperclip import paste

        letters = {'q': 'й', 'й': 'q', 'w': 'ц', 'ц': 'w', 'e': 'у', 'у': 'e', 'r': 'к', 'к': 'r', 't': 'е', 'е': 't',
                   'y': 'н', 'н': 'y', 'u': 'г', 'г': 'u', 'i': 'ш', 'ш': 'i', 'o': 'щ', 'щ': 'o', 'p': 'з', 'з': 'p',
                   '[': 'х', 'х': '[', ']': 'ъ', 'ъ': ']', 'a': 'ф', 'ф': 'a', 's': 'ы', 'ы': 's', 'd': 'в', 'в': 'd',
                   'f': 'а', 'а': 'f', 'g': 'п', 'п': 'g', 'h': 'р', 'р': 'h', 'j': 'о', 'о': 'j', 'k': 'л', 'л': 'k',
                   'l': 'д', 'д': 'l', ';': 'ж', 'ж': ';', "'": 'э', 'э': "'", 'z': 'я', 'я': 'z', 'x': 'ч', 'ч': 'x',
                   'c': 'с', 'с': 'c', 'v': 'м', 'м': 'v', 'b': 'и', 'и': 'b', 'n': 'т', 'т': 'n', 'm': 'ь', 'ь': 'm',
                   ',': 'б', 'б': ',', '.': 'ю', 'ю': '.', '/': ',', '?': '.', '`': 'ё', 'ё': '`'}

        st = str(paste()).lower()
        out = ''
        for i in st:
            if i in letters:
                out += letters[i]
            else:
                out += i

        if len(out) <= 50:
            dash = '-' * len(out)
        else:
            dash = '-' * 50

        print(f'исправленный текст:\n{dash}\n{out}\n{dash}\nскопировано...')
        copy(out)

        none()  # исправляет ghbdtn > привет

    # corrector()

    def azart():
        import random

        money = 5000  # int(input("Введите начальное количество денег: "))
        print('у вас 5 тыщ')
        stat = ''
        is_continue = 1

        while money > 0 and money < 10000 and is_continue == 1:
            win = random.randint(-30, 30) * 100
            money += win
            is_continue = int(input('продолжим? '))

            if win < 0:
                stat += '↓'
                print(f'не повезло: {money} ({win})')
            else:
                stat += '↑'
                print(f'удача: {money} (+{win})')

        print(f"Игра закончена. Ваш баланс: {money} рублей")
        print('статистика этой игры:', stat)

        none()  # азартная игра

    # azart()

    def distorter():
        from pyperclip import copy
        import random

        def distorter(string1, dist_level=30):

            distorted_text = ''
            symbols = '$%&*+=#@!"№;%:?*'

            for i in range(len(string1)):
                if random.randint(1, 100) <= dist_level:
                    distorted_text += random.choice(symbols)
                else:
                    distorted_text += string1[i]

            return distorted_text

        while True:
            string1 = input('текст для искажения: ')
            if not string1:
                break
            level = input('уровень искажения (0-100)%: ')
            if level:
                out = distorter(string1, int(level))
            else:
                out = distorter(string1)

            print(out)
            copy(out)

        none()  # искажатель текста

    # distorter()

    def secret_num():
        user_answer = int(input('какое число вы загадали? '))
        mem = 100  # max
        mem2 = 0  # min
        answer = 0
        line = ''

        while user_answer != answer:
            answer = (mem + mem2) // 2  # 50
            if user_answer < answer:  # 49 > 50
                mem = answer  # +max
                line += '↓'
            elif user_answer > answer:
                mem2 = answer  # +min
                line += '↑'
            print(answer, end='')
            if user_answer != answer:
                print(end=' > ')
        print()
        print(line)

        none()  # вычисление загаданного числа

    # secret_num()

    def game_snake():
        import msvcrt
        import random

        def get_key():
            key = msvcrt.getch()
            return ord(key)

        def add_to_tail(tail, player_pos, score):
            tail.append(player_pos)  # добавляем новую позицию в хвост
            if len(tail) > score + 1:  # если хвост длиннее счета
                tail.pop(0)  # удаляем старую позицию из хвоста
            return tail

        size = 20
        x = y = size  # размер поля
        x += 3
        y += 1
        y *= 2
        player_x, player_y = 2, 2  # игрок
        apple_x = random.randint(2, x - 2)  # х яблока
        apple_y = random.randrange(2, y - 3, 2)  # у яблока
        score = 0
        tail = [(player_x, player_y)]  # инициализация хвоста

        print('начало игры')
        while True:
            print('очки:', score)

            for x2 in range(1, x):
                for y2 in range(1, y):
                    if x2 == 1 or x2 == x - 1 or y2 == 1 or y2 == y - 1:
                        print('#', end='')  # отрисовка стен
                    elif (player_x == y2 and player_y == x2) or ((y2, x2) in tail):
                        print('^', end='')  # отрисовка игрока
                    elif apple_x == x2 and apple_y == y2:
                        print('*', end='')  # отрисовка яблока
                    else:
                        print(' ', end='')  # отрисовка пробелов
                print()
            print()

            # Получаем следующую позицию игрока
            move = get_key()
            if move == 119:  # w
                new_player_y = player_y - 1
                new_player_x = player_x
            elif move == 97:  # a
                new_player_x = player_x - 2
                new_player_y = player_y
            elif move == 115:  # s
                new_player_y = player_y + 1
                new_player_x = player_x
            elif move == 100:  # d
                new_player_x = player_x + 2
                new_player_y = player_y
            else:
                print('игра окончена')
                break

            if score >= (size ** 2) - 1:
                print('игра окончена')
                break
            if (new_player_x, new_player_y) in tail:  # игрок наткнулся на свой хвост
                print('игра окончена')
                break

            tail = add_to_tail(tail, (new_player_x, new_player_y), score)  # обновление хвоста
            player_x, player_y = new_player_x, new_player_y  # обновление положения игрока

            if player_y == apple_x and player_x == apple_y:  # проверка на сбор яблока
                score += 1
                apple_x = random.randint(2, x - 2)
                apple_y = random.randrange(2, y - 3, 2)

        none()  # игра змейка

    # game_snake()

    def lotareya():
        import random

        count = int(input('сколько билетов покупать будете (1 билет - 100 руб)? '))
        win = 0
        stat = ''
        jak = very = ok = nah = 0

        for un in range(count):
            winer = random.randint(1, 5000)
            if winer // 100 < 10 and winer // 100 != 0 and winer % 5 == 0 and winer // 100 == 1:
                print(f'билет №-{winer} - ДЖЕКПОТ!!!!!!!!!!!')
                win += 100000
                jak += 1
            elif winer // 100 < 10 and winer // 100 != 0 and winer % 5 == 0:
                print(f'билет №-{winer} - очень выигрышный!!!')
                win += 1000
                very += 1
            elif winer // 100 < 10 and winer // 100 != 0:
                print(f'билет №-{winer} - выигрышный')
                win += 300
                ok += 1
            elif winer < 2500:
                print(f'билет №-{winer} - окупаемый')
                win += 100
                nah += 1
            else:
                print(f'билет №-{winer} - мусор')
        print(f'\nстатистика:\nокуп - {nah}\nнебольшой выйгрыш (300 рублей) - {ok}\nбольшой выйгрыш (1000 рублей)'
              f' - {very}\nджекпот (100000 рублей) - {jak}\n')
        print(f'потрачено на билеты: {count * 100}, сумма выйгрыша составила: {win}')
        print(f'теперь у вас есть {win - count * 100} денег')

        none()  # вторая азартная игра

    # lotareya()

    def cod_morse():
        morse_dict = {
            '.-': 'А', '-...': 'Б', '.--': 'В', '--.': 'Г', '-..': 'Д', '.': 'Е',
            '...-': 'Ж', '--..': 'З', '..': 'И', '.---': 'Й', '-.-': 'К', '.-..': 'Л',
            '--': 'М', '-.': 'Н', '---': 'О', '.--.': 'П', '.-.': 'Р', '...': 'С',
            '-': 'Т', '..-': 'У', '..-.': 'Ф', '....': 'Х', '-.-.': 'Ц', '---.': 'Ч',
            '----': 'Ш', '--.-': 'Щ', '--.--': 'Ъ', '-.--': 'Ы', '-..-': 'Ь',
            '..-..': 'Э', '..--': 'Ю', '.-.-': 'Я'
        }

        word = input('введите код морзе (пример -- .. .-.. ---): ').split()

        for letter in word:
            print(morse_dict.get(letter, ''), end='')

        none()  # расшифровка кода морзе

    # cod_morse()

    def pypon():
        variables = dict()
        switch = quotes = 0

        while True:
            inp = input().split()
            if not inp:
                break

            if len(inp) >= 3 and inp[1] == '=':  # присвоение переменных
                variables[inp[0]] = inp[2]

            elif inp[0].startswith('print'):  # print
                out = ''
                for i in inp[0]:
                    if i == '(':
                        switch = 1
                    elif i == ')':
                        switch = 0

                    if i == '"' and quotes == 0:
                        quotes = 1

                    if switch == 1:
                        out += i

                if quotes == 0:
                    out = variables.get(out[1:], 'Variable not found')
                    print(out)
                else:
                    print(out[2:-1])

        none()  # python

    # pypon()

    def matrix():
        import random
        import time

        def draw(x, y, object_cord_set):
            for x1 in range(x):
                for y1 in range(y):
                    if x1 == 0 or (y1, x1) in object_cord_set:
                        print(random.randint(0, 1), end='')
                    else:
                        print(' ', end='')
                print()

        a = 20
        b = a * 2
        random_x = 0
        lit = []

        for i in range(20):
            random_x = random.randint(1, a) * 2
            lit.append([random_x, 0, 0])

            lit = [item for item in lit if item[2] <= 2]

            object_cord_set = set((item[0], item[1]) for item in lit)

            for i in range(len(lit)):
                lit.append([lit[i][0], lit[i][1] + 1, 0])
                lit[i][2] += 1

            draw(a, b, object_cord_set)

            time.sleep(0.1)

        none()  # матрица

    # matrix()

    def graphic():
        def funk_visualaser(ax, ay, bx, by):
            m, b, sym = linear(ax, ay, bx, by)

            min_x = min(ax, bx)
            max_x = max(ax, bx)
            min_y = min(ay, by)
            max_y = max(ay, by)

            for y in range(max_y, min_y - 1, -1):
                for x in range(min_x, max_x + 1):
                    if round(y) == round(x * m + b):
                        print(sym, end=' ')
                    elif y == 0 or x == 0:
                        print('#', end=' ')
                    else:
                        print(end='  ')
                print()

        def linear(ax, ay, bx, by):
            # y = mx + b
            m = (by - ay) / (bx - ax)
            b = ay - m * ax
            sym = '\\'
            if m == 0:
                sym = '-'
            elif m > 0:
                sym = '/'
            return m, b, sym

        funk_visualaser(-10, -5, 10, 5)

        none()  # вычисление линейного графика функций

    # graphic()

    def twany_one():
        import random

        cards = [6, 7, 8, 9, 10, 11]
        random.shuffle(cards)
        player_score = bot_score = 0
        card = operation = bot = 0

        while True:
            if player_score > 21:
                print('ты проиграл')
                break
            elif bot_score > 21:
                print('ты выйграл')

            if operation != 2:
                operation = int(input('1-взять, 2-не брать\n: '))
                if operation == 1:
                    player_score += cards[card]
                    cards.pop(card)
                    print('ваш счёт:', player_score)

            if bot != 1:
                choice = random.randint(bot_score, 25)
                if choice < 20:
                    bot_score += cards[card]
                    cards.pop(card)
                    print('бот взял')
                else:
                    bot = 1
            else:
                print('бот пропускает')

            if operation == 2 and bot == 1:
                if player_score > bot_score:
                    print('ты выйграл')
                else:
                    print('ты проиграл')
                break
        print('очки бота:', bot_score)

        none()  # игра "21"

    # twany_one()

    def NoAdsSteam():
        import pygetwindow as gw
        import subprocess as sb

        debug = gw.getWindowsWithTitle('cmd')[0]
        debug.minimize()

        steam = r'D:\Steam\steam.exe'
        sb.Popen(steam)

        while True:
            ads = gw.getWindowsWithTitle('Специальные предложения')
            if ads:
                ads[0].close()
                debug.close()
                break

        none()  # убирает рекламу в стиме

    # NoAdsSteam()

    none()  # сохранённые прикольчики и мини проекты


saves()


def theory():
    # итерация - тело цикла
    for i in range(10):  # цикл
        print(i, end=' ')  # итерация

    # Машинный эпсилон (ε) - предельно маленькое различимое вещественное число
    #
    # Если B < ε, то A + B == A
    # Если A - B < ε, то A == B

    # 143e-4:  143 - мантиса,  -4 - Порядок
    # 143 * 10 ** -4   = 0.143 
    none()  # теория


# theory()


def biblies():
    # можно выполнять только определённые значения, что бы не подключать всю библиотеку
    from math import sqrt
    print(sqrt(9))

    # как записывать:
    # y = abc(x)

    # =========================== math ==========================

    import math

    x = 1
    abs(x)  # = |x|  модуль

    math.floor(x)  # округление числа в меньшую сторону
    math.ceil(x)  # округление числа в большую сторону
    math.sqrt(x)  # Квадратный корень
    math.exp(x)  # значение экспоненты e в степени x
    math.log(x)  # Натуральный логарифм. B виде log(x., b) возвращает логарифм по основанию Ь
    math.log2(x)  # Двоичный логарифм.	log2(1024) == 10.0
    math.log10(x)  # Десятичный логарифм.	log10(100) == 2.0
    math.factorial(x)  # Факториал целого числа
    math.sin(x)  # Синус угла, !задаваемого в радианах
    math.cos(x)  # Косинус угла, !задаваемого в радианах

    var = math.e  # Константа экспонента е «2,71828....
    var = math.pi  # Константа π «3,141592653589793

    # ========================== random =========================

    random.seed(42)  # Устанавливаем начальное значение, все следующие элементы рандома будут привязаны к сиду
    random.random()  # число от 0 до 1
    random.randint(0, 10)  # число от 0 до 10
    random.randrange(0, 20, 2)  # число от 0 до 10 с шагом 2
    random.uniform(1, 10)  # вещественное число от 1 до 10

    items = ["яблоко", "банан", "апельсин"]
    random.choice(items)  # рандомный элемент из списка
    random.shuffle(items)  # перемешивает список
    random.sample(items, 2)  # возвращает определённое количество элементов из списка

    # =========================== time ==========================

    import time

    current_time = time.time()
    localtime_time = time.localtime()
    time_string = "2023-01-01 12:30:00"

    time.sleep(1)  # программа приостановится на секунду
    time.time()  # показывает сейчасшнее время в странной форме, пример: 1700398883.115157

    time.ctime(current_time)  # преобразует тот набор цифр в читаемую дату: Sun Nov 19 16:58:17 2023
    utc_time = time.gmtime(current_time)  # показывает глобальное время

    current_time = time.localtime()  # показывает твоё время в другой странной форме:
    # time.struct_time(tm_year=2023, tm_mon=11, tm_mday=19, tm_hour=17, tm_min=13,
    #                  tm_sec=20, tm_wday=6, tm_yday=323, tm_isdst=0)

    # показывает форматированное время, вывод будет: 2023-11-19 16:58:54
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    # %Y - год | %m - месяц | %d - день месяца | %H - час | %M - минута | %S - секунда

    # определяет структуру времени, то есть определяет что например из этой строки год
    formatted_time = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    # Вывод: time.struct_time(tm_year=2023, tm_mon=1, tm_mday=1, tm_hour=12,
    #                         tm_min=30, tm_sec=0, tm_wday=6, tm_yday=1, tm_isdst=-1)

    # так можно засечь время 
    start_time = time.time()  # начало таймера
    end_time = time.time()  # конец таймера
    elapsed_time = end_time - start_time  # вычисление разницы

    # ============================ os ============================

    import os
    # позволяет работать с файловой системой.

    # >>> path <<<

    # например нам нужно получить путь к какому-нибудь файлу на компьютере
    directory, folder, file = 'source', 'repos', 'maw.txt'

    rel = os.path.join(directory, folder, file)  # так можно получить правильный вид пути до какого то файла
    print(rel)  # OneDrive\Рабочий стол\example.txt

    abs_path = os.path.abspath(file)  # abspath сам ищет путь до файла
    print(abs_path)  # C:\Users\v-v\source\repos\lav\lav\example.txt

    dirc = os.listdir(os.path.abspath(os.path.join('..', '..', '..', folder)))  # listdir выдаст список файлов в папке
    print(dirc)  # ['.idea', 'lav', 'maw.txt', 'Python_Basic', 'safev', 'Вывод-Сборка.cpp']

    os.path.exists('лемон')  # проверяет есть ли этот путь на компе
    os.path.isdir(abs_path)  # проверяет на папку
    os.path.isfile(abs_path)  # проверяет на файл
    os.path.islink(abs_path)  # проверяет на ссылку

    # >>> остальное <<<

    # ======================== subprocess ========================

    import subprocess
    # subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False,
    # check=False, если тут False, то не будет выдавать понятные ошибки
    # timeout=None, text=None, cwd=None, env=None)

    # run([(в какой программе будет запускаться файл), (название файла)]) # открывает программу
    subprocess.run(['notepad.exe', 'result.txt'], check=True)  # если программы нет, то он создаёт её

    # Создает новый процесс и возвращает объект Popen, который предоставляет методы для управления этим процессом.
    process = subprocess.Popen(['notepad.exe', 'result.txt'])

    process.wait()  # дождаться выполнения кода

    # ======================== pyautogui =========================

    import pyautogui as pag

    # >>> click <<<
    pag.click()  # кликает курсором
    # clicks=99 - указывает на кол-во кликов (по умолчанию 1)
    # interval=1 - сколько секунд ждать между нажатиями
    # button='left' - "LEFT", "MIDDLE", "RIGHT" какая кнопка нажата
    # duration=10 - сколько секунд будет двигаться курсор в x, y

    # >>> остальное <<<
    pag.moveTo("""100, 100, 0.5""")  # передвигает курсор, последний параметр это время
    pag.moveRel()  # смещает курсор, относительно курсора
    pag.mouseDown()  # зажимает курсор
    pag.mouseUp()  # отжимает курсор
    pag.scroll(1)  # прокручивает вверх (например 10) или вниз (-10)
    pag.position()  # показывает координаты курсора
    pag.mouseInfo()  # показывает состояние кнопки мыши

    pag.hotkey('ctrl', 'c')  # нажимает эти кнопки
    pag.keyDown("1")  # зажимает клавишу
    pag.keyUp("1")  # отжимает клавишу

    pag.screenshot('screen.png')  # делает скриншот и сохраняет его в указанный файл
    pag.locateOnScreen('фото.png')  # ищет картинку на экране и возвращает координаты левого верхнего угла
    # pag.locateCenterOnScreen('фото.png')  # то же самое, но возвращает в центре

    # ======================= pygetwindow ========================

    import pygetwindow as gw

    win = gw.getWindowsWithTitle('cmd')[0]
    print(win)

    gw.getAllTitles()  # выдаёт список открытых окон
    gw.getWindowsWithTitle("cmd")  # выдаёт список окон с указанным заголовком
    gw.getActiveWindow()  # возвращает активное окно

    win.activate()  # активирует окно (тут активируется win)
    win.move(300, 150)  # двигает окно
    win.resize()  # изменяет размер окна
    win.minimize()  # сворачивает окно
    win.maximize()  # разворачивает окно
    win.restore()  # возвращает открытое во весь экран или свёрнуте окно в нормальное состояние

    win.isMinimized()  # проверка: окно свёрнуто
    win.isMaximized()  # проверка: окно активно
    win.isForeground()  # проверка: окно открыто

    # ========================== pygame ==========================

    import pygame

    pygame.init()  # инициализация pygame

    # >>> display <<< # (настройки окна)
    screen = pygame.display.set_mode((800, 600))  # задаёт размеры окна
    pygame.display.set_caption('о')  # задаёт название окна
    screen.fill((255, 255, 255))  # цвет экрана

    # >>> draw <<< (рисование на экране)
    # (<где будет находится>, <цветRGB>, (<x>, <y>, <ширина>, <высота>), <толщина границы>)
    # pygame.draw.rect()  # прямоугольник
    # (<поверхность>, <цветRGB>, (<x_центра>, <у_центра>), <радиус>, <толщина границы>)
    # pygame.draw.circle()  # круг
    # (<поверхность>, <цветRGB>, (<x1>, <у1>), (<x2>, <у2>), <толщина границы>)
    # pygame.draw.line()  # линия
    # (<поверхность>, <цветRGB>, [(список, координат), (х2, у2), ...], <толщина границы>)
    # pygame.draw.polygon()  # полигон

    # >>> event <<<
    pygame.event.get()  # выводит событие
    # QUIT
    # KEYDOWN и KEYUP
    # MOUSEBUTTONDOWN и ...UP
    # MOUSEMOTION двигается ли курсор

    # >>> остальное <<<
    var = pygame.image  # позволяет загрузить изображение
    pygame.mouse.get_pos()  # выводит координаты курсора
    pygame.key.get_pressed()  # выводит нажимаемые кнопки

    pygame.mixer.init()  # иницилизирует звуковую систему
    pygame.mixer.Sound("file")  # производит звук

    # pygame.font # шрифты

    # основной цикл программы
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # код

        pygame.display.flip()  # обновление экрана

    # ========================== socket ==========================

    import socket

    host_name = socket.gethostname  # показывает название хоста
    ip_address = socket.gethostbyname(host_name)  # показывает ip хоста

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаём сокет объект

    address = (ip_address, 1389)  # (<ip>, <порт>)
    server.bind(address)  # связываем сокет адресом и потром
    server.connect(address)  # что бы подключится

    server.listen(1)  # начинаем прослушивание входящих сообщений

    client_socket, client_address = server.accept()  # ждём соединения

    data = client_socket.recv(1024)  # принимаем данные
    message = 'a'
    client_socket.sendall(message.encode())  # отправляем данные

    client_socket.close()
    server.close()

    # ========================= мелочные =========================

    # >>> pyjokes <<<
    import pyjokes
    # пишет шутки
    joke = pyjokes.get_joke()
    print(joke)

    # >>> emoji <<<
    import emoji
    # позволяет работать с эмодзи
    result = emoji.emojize('Python is :thumbs_up:')
    print(result)

    # >>> googletrans <<<
    from googletrans import Translator

    # пример переводчика
    def translate(text, lang='ru'):
        translator = Translator()
        translation = translator.translate(text, dest=lang)
        # в функцию translate текст и язык (параметр: dest)
        translation_text = translation.text
        # .text делает текст читаемым
        return translation_text

        # >>> pyperclip <<<

    import pyperclip

    pyperclip.copy('')  # Копирует текст в буфер обмена.
    pyperclip.paste()  # Возвращает последний текст из буфера обмена.

    # >>> win10toast <<<

    from win10toast import ToastNotifier

    # Создаем объект ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast("Заголовок уведомления", "Текст уведомления", duration=10)  # Отправляем уведомление
    time.sleep(2)
    toaster.update_options({"duration": 2})  # обновляем настройки
    time.sleep(2)
    toaster.hide_toast()  # скрываем уведомление

    none()  # библиотеки


# biblies()


def prin():
    # ============================ \n ===========================

    print('1111\n2222')  # \n переносит на следующую строчку

    # =========================== end ===========================

    for a in range(5):
        for b in range(5):
            print(a + b, end=' ')  # end={} на что будет меняться перенос строки
        print()  # в этом случае на пробел, так что ещё нужно будет переносить строку другим принтом

    # ============================ \t ===========================

    for a in range(5):
        for b in range(90, 105):
            print(a + b, end='\t')  # \t будет выравнивать числа
        print()

        # ========================== round ==========================

    a = 1579.384
    print(round(a))  # округляет число, по умолчанию до 0 знаков после запятой

    print(round(a, 2))  # можно задать до какого числа будет округлятся через запятую
    #                     !эту функцию можно использовать не только в принте

    # ========================== format =========================

    user, file = 'обязательное поле', 'новый файл '
    # подставит переменные в строку на место выделенных фигурными скобками слов и ещё они должны быть написаны в format
    path = 'C:/{poly}/docs/floder/{listok}.txt'.format(poly=user, listok=file)
    print(path)  # C:/обязательное поле/docs/floder/новый файл .txt

    # если заранее известно положение и порядок этих слов, то можно написать просто порядковый номер переменной:
    path_2 = 'C:/{0}/docs/{0}/floder/{1}.txt'.format(user, file)
    # например тут порядковый номер переменной user ^ это 0
    print(path_2)  # C:/обязательное поле/docs/обязательное поле/floder/новый файл .txt

    # ========================= f-строки ========================

    a = 999
    print(f'переменная в равна: {a} секунд')  # f можно писать переменные прямо в строке
    # это имба

    five_milions = 50000000
    ship = 39.1527654
    procent = 0.29434

    print('это число называется {:d} увлувльув'.format(five_milions))  # это число называется 50000000 увлувльув
    #                             ^ мы говорим коду, что переменная это целое число
    print('это число называется {:,d} увлувльув'.format(five_milions))  # это число называется 50,000,000 увлувльув
    #                             ^и здесь будет символ, который разделяет это число
    print('aaa {:f}!'.format(ship))  # aaa 39.152765!
    #            ^ вещественное число
    print('aaa {:.2f}!'.format(ship))  # aaa 39.15!
    #             ^ количество знаков после запятой
    print('гуль {:%}'.format(procent))  # гуль 29.434000%
    # это процент ^
    print('гуль {:.1%}'.format(procent))  # гуль 29.4%
    # это округлить процент ^
    print('||| {:.0e} |||'.format(five_milions))  # ||| 5e+07 |||
    #            ^ написать в экспоненциальной форме

    # ======================== isinstance =======================

    # isinstance(<элемент>, <тип данных>) True, если элемент принадлежит к этому типу данных
    op = 'stringngng'
    print(isinstance(op, int))  # False
    print(isinstance(op, str))  # True

    none()  # print


# prin()


def variables():
    variable_4 = 4  # создает переменную
    #            a ≠ A
    #            в начале переменной должна быть буква
    #            переменную нельзя писать с пробелом
    #            можно использовать только английские буквы

    #   можно присваивать значения сразу нескольким переменным, через запятую:
    a, b, c = 'rule', 3, variable_4
    # {переменная 1}, {переменная 2}, ... = {значение для 1}, {значение для 2}, ...
    print(a, b, c)  # rule 3 4

    # что бы присвоить одно и то же значение:
    x = y = 0

    str_variable = input('строка: ')  # пользователь задаёт переменную

    # int() = целые числа. Отрезает плавающие числа (не округляет)
    # float() = не целые числа  (float(5) + 0.6 = 5.6)
    # str() = строка с символами
    # bool() = False (если переменная пуста ('', 0, None))
    type(a)  # вернёт тип переменной

    int_variable = int(input('число: '))
    five = int_variable // 2

    id(five)  # с помощью id можно узнать id значения переменной

    return int_variable, five  # переменные


# variables()


def lists():
    #    переменным можно присваивать несколько значений
    uwu = 1, 2, 3, 5, 10
    print(uwu)  # (1, 2, 3, 5, 10)
    print(uwu[3], uwu[0])  # с помощью [{номер значения}] можно выводить определённые значения

    # пояснение:
    # 1 = [0]
    # 2 = [1]
    # 3 = [2]
    # 5 = [3]
    # 10 = [4]

    owo = range(10)  # этой переменной будет присваиваться значения от ноля до цифры в range

    #    range можно задать правила
    owo = range(1, 10, 2)  # ({с какого числа начинать}, {на каком числе заканчивать}, {шаг, ну... не важно})

    #    а что бы разделять их нужно воспользоваться квадратными скобками
    print(owo[0], owo[4], owo[3])  # (начиная с ноля)

    # можно делать вложные списки
    inv = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(inv[1])  # [4, 5, 6]
    print(inv[2][1])  # 8

    chips = [x ** 2 for x in range(10)]
    #        ^ здесь то что будет делаться с каждым значением из range
    say(chips)

    chips = [(x ** 2 if x % 2 != 0 else 2) for x in range(10)]
    # можно сразу писать условие ^
    say(chips)

    # если условие одно, можно написать так
    chips = [x ** 2 for x in range(10) if x % 2 != 0]
    say(chips)

    # вот как выглядит не сокращённый код:
    chips = []

    for x in range(10):
        if x % 2 != 0:
            chips.append(x ** 2)
        else:
            chips.append(2)

    print(chips)

    # ============================ in ===========================

    pole = [1, 2, 4, 5]
    if 4 in pole:
        # in проверяет есть ли какое-то значение в списке (или строке)
        print('lkdflkflkdf')

    # ========================== append =========================

    uwu = [10]  # ещё можно создавать пустой список
    #    что бы прибавить ещё одно значение к списку нужно написать так:
    #    что бы эта программа работала обязательно нужно поставить квадратные скобки в списке []

    cnNcok = [9, 7, 5]
    #    ещё можно изменять значение в списке как в переменной:
    print(cnNcok)  # [9, 7, 5]
    cnNcok[1] *= 2
    print(cnNcok)  # [9, 14, 5]

    print(cnNcok[-1])  # начинает с конца

    # =========================== list ==========================

    a = 'pypon'
    li = list(a)  # выведет каждый символ в список
    print(li)  # ['p', 'y', 'p', 'o', 'n']

    rangee = list(range(1, 10))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(rangee, end=' ')

    # =========================== len ===========================

    word = 'hey fu'
    count = len(word)  # показывает сколько символов в строке
    print(count)  # 6

    # в списке же показывает количество значений
    a = [10, 20, 30]
    print(len(a))  # 3

    # ========================== insert =========================

    # нужен, что бы добавить значение в нужную позицию
    long = ['a', 'c', 'd']

    long.insert(1, 'b')
    #    индекс ^
    say(long)  # ['a', 'b', 'c', 'd']

    # ========================== index ==========================

    # определяет индекс значения
    dgo = [';', 'aa', 'we', '^']

    indi = dgo.index('aa')
    say(indi)  # 2

    # ========================== remove =========================

    # удаляет значение в списке
    dgo = [';', 'aa', 'we', '^']

    dgo.remove(';')
    say(dgo)  # ['aa', 'we', '^']

    # ========================== extend =========================

    first = [1, 2, 4]
    second = [3, 5, 6]
    # добавляет один список к другому

    first.extend(second)
    # работает только со списками

    print(first)  # [1, 2, 4, 3, 5, 6]

    # ========================== count ==========================

    cod = [1, 0, 0, 1, 1]

    cout = cod.count(1)
    # показывает количество одного значения

    print(cout)  # 3, потому что в cod три единицы

    # ====================== срезы_списков ======================

    listik = [x for x in range(0, 21, 2)]
    # что бы создать копию списка нужны [:]
    copy = listik[:]

    print(copy[2:7])  # [4, 6, 8, 10, 12]
    # будут выведены значения с индексами от 2 до 6 
    print(copy[:6])  # [0, 2, 4, 6, 8, 10]
    # тут автоматически вывод будет от 0-индекса
    print(copy[2:8:2])  # [4, 8, 12]
    # от 2 до 7 с шагом 2
    print(copy[::])  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    # это означает весь список будет задействован
    print(copy[::-1])  # [20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0]
    # -1 это шаг, а значит список развернётся
    copy[:3] = [1]
    print(copy)  # [1, 6, 8, 10, 12, 14, 16, 18, 20]
    # заменит три первых значения на одну 1

    none()  # переменные 2 - списки


# lists()


def strings():
    frukt = 'АРБУЗ не еда-а тире'  # это строка

    # ========================== split ==========================

    les = frukt.split()  # разделяет слова пробелами и преобразует в список
    print(les)  # ['арбуз', 'не', 'еда-а', 'тире']

    les2 = frukt.split('-')  # в скобках писать каким символом обозначено разделение
    print(les)  # ['арбуз не еда', 'а тире']

    # =========================== join ==========================

    mathod = '-'.join(les)  # пишет между значениями в списке
    # символ, ^ который тут
    print(mathod)  # арбуз-не-еда-а-тире

    # =================== endswith и startswith ==================

    if frukt.endswith('тут что в конце строки'):  # проверяет конец строки
        print('всё хорошо')

    if frukt.startswith('тут что в начале'):  # проверяет начало строки
        print('всё ещё лучше, но этого не произойдёт')

    # ====================== upper и lower ======================

    low = frukt.lower()  # делает все буквы маленькие
    print(low)  # арбуз не еда-а тире
    up = frukt.upper()  # делает все буквы большие
    print(low)  # АРБУЗ НЕ ЕДА-А ТИРЕ

    # ========================== find() =========================

    eda = frukt.find('еда')  # показывает номер первого символа "еда" в строке frukt
    # если не находит выводить "-1"
    print(eda)  # 9
    # АРБУЗ не еда-а тире
    #         ^
    # 12345678912345...

    # ===================== остальная мелочь =====================

    print(frukt.title())  # Первую букву каждого слова делает большой, а все остальные маленькими
    print(frukt.isdigit())  # Состоит ли строка из цифр
    print(frukt.isalpha())  # Состоит ли строка из букв
    print(frukt.isalnum())  # Состоит ли строка из цифр или букв
    print(frukt.islower())  # Состоит ли строка из символов из маленьких букв
    print(frukt.isupper())  # Состоит ли строка из символов из больших букв

    none()  # переменные 3 - методы строк


# strings()


def dicts():
    address = None

    Users = {  # Создает словарь
        'U1': {  # Создает вложеный словарь
            address: 'mixa8240@gmail.com',  # << тут запятая ставится
            'password': 1278347  # Здесь можно использовать строки в качестве переменных
        }
    }
    # для определения переменной нужно вписать "путь"
    user = Users['U1'][address]
    password = Users['U1']['password']
    print(user, password)  # mixa8240@gmail.com 1278347

    example = dict()  # dict значит что это пустой словарь
    example['коробка'] = 10  # добавляет это в словарь
    print(example)  # {'коробка': 10}

    # ====================== keys и values ======================

    diktant = {'a': 1, 'b': 1, 'point': '.', 'гриб': 0, 'd': 9}

    for i in diktant.keys():  # i будет применяться к каждому названию в словаре
        print(i)  # a b point гриб d

    for i2 in diktant.values():  # тут вместо названий их значения
        print(i2)  # 1 1 . 0 9

    # ========================== update =========================

    cola = {'a': 1, 'b': 2}
    mentos = {'c': 3, 'd': 4}

    cola.update(mentos)  # добавляет 1 словарь к другому

    print(cola)  # взрыв

    # =========================== pop ===========================

    fish = {'lemon': 9093128, 'ogurec': 99999999, 'OKYHb': 200}

    fish.pop('ogurec')  # удаляет ключ

    table = fish.pop('lemon')  # удаляет ключ и выводит его значение в переменную
    print(table)  # 9093128

    # еще можно вот так изменить название ключа
    fish['potato'] = fish.pop('OKYHb')
    print(fish)  # {'potato': 200}

    # =========================== get ===========================

    dead = {'hau': 1, 'geforce': 1, 'game': 0, 'doors': 1}

    dead.get('hau')  # если ключ с таким названием есть в словаре, то выводит его значение

    dead.get('geometry dash')  # а если нет добавляет ключ со значением None
    # вместо None можно написать своё значение
    dead.get('pokemon', 10)

    # ======================== остальное ========================

    abe = {'g': 1, 'r': 4, 'a': 2, 'b': 0}

    sorted(abe)  # сортирует список
    abe.items()  # items() позволяет сразу обратиться и к ключам, и к значениям словаря

    none()  # переменные 4 - словари


# dicts()


def cortezhs():
    cartredzh = (3, 1, 4, 1, 5)
    # кортеж нельзя изменить
    # для функций нужно делать копию картежа, что бы с ней работать
    parentheses = 9, 8, 765  # картридж можно сделать и без скобок
    print(parentheses)  # (9 8 765)

    # можно переделать картеж в переменные
    nine, eit, svn = parentheses
    print(nine, eit, svn)  # 9 8 765

    lit = [9, 9, 9]
    cat = (10, 20, 30, lit)
    print(cat)  # (10, 20, 30, [9, 9, 9])

    # в списке, который находится в картридже можно менять значения
    cat[3][0] = 40
    print(cat)  # (10, 20, 30, [40, 9, 9])

    # ========================== tuple ==========================

    some_list = [1, 1, 1]

    wha_tuple = tuple(some_list)  # переделывает что то в картредж
    print(wha_tuple)  # (1, 1, 1)

    # ========================== методы =========================

    cartredzh.index(1)  # показывает индекс значения, если там больше одного, то показывает первый
    cartredzh.count(1)  # показывает количество 1 в картридже

    none()  # переменные 5 - кортежи


# cortezhs()


def sets():
    a = {'o', 'b', 'x', 'd'}  # множество это словарь без значений и без индексов
    b = {'o', 'f', 'x'}

    # ========================= операции ========================    

    a.intersection(b)  # Находит одинаковые значения в этих... множествах -_-
    # можно записать и так: a & b
    a.intersection_update(b)  # Оставляет в множестве a только те элементы, которые есть в множестве b
    # a &= b
    a.union(b)  # объединяет их
    # a | b
    a.difference(b)  # оставляет только те, которые не пересекаются
    # a - b
    a.difference_update(b)  # Удаляет из, a все элементы, входящие в b
    # a -= b
    a.update(b)  # Добавляет в множество, a все элементы из множества b
    # a |= b 
    print(a)  # {'f', 'o', 'x'}

    # ========================== методы =========================

    nums = {2, 3, 4, 5, 6}

    nums.add(1)  # добавляет элемент в множество.
    nums.remove(6)  # удаляет элемент из множества
    nums.discard(9)  # Удаляет элемент, если он находится в множестве. Если элемента нет, то ничего не происходит
    nums.pop()  # удаляет первый элемент из множества
    nums.clear()  # очистка множества
    print(nums)  # set()

    none()  # переменные 6 - множества


# sets()


def general_var():
    # в разных списках можно хранить разные списки
    a = [(1, 9), [4, 4, 5], {0, 1, 0, 0, 1}, {'q': 9, 'b': 6}]

    letters = ['i', 'q', 'y']
    numbers = [4, 26, 14]
    asphalt = zip(letters, numbers)  # объединяет элементы списков, тут будет [('i', 4), ('q', 26), ('y',14)]
    print(asphalt)  # <zip object at 0x000001F6EAFA3300>

    for i in asphalt:
        print(i, end=' ')  # ('i', 4) ('q', 26) ('y', 14)

    isinstance(a, str)  # Проверяет переменную на то какая она цифра или буква или список и т. д.

    none()  # переменные 7 - общее


# general_var()


def if_operator():
    int_variable = random.randint(1, 10)
    five = int_variable // 2

    if int_variable < 10:  # что будет проверять условие
        int_variable += 10  # что будет выполняться при этом условии (отделено отступом)
        print('ну это число меньше 10')

    #   >  - Больше
    #   <  - Меньше
    #   >= - Больше либо равно
    #   <= - Меньше либо равно
    #   == - Равно
    #   != - Не равно

    # для if так же есть дополнения

    if five > 5:
        print('не правильно, 1')

    elif five == 5:  # проверяет другое условие, если предыдущее не подошло
        print('не правильно, 2')

    else:  # если ничего из вышеперечисленного не подошло
        print('не правильно, 3')

    #     и ещё можно задавать сразу несколько условий
    #     их лучше записывать в скобочках, что бы не запутаться

    if (int_variable < 15) and (five > 3):
        print('! совпадение (это редкость)')

    a = 0
    if a:  # если в условие вписать переменную, то оно будет выполняться, когда переменная не равна 0
        print('a ≠ 0')
    else:
        print('a = 0')  # if


# if_operator()


def while_cycle():
    correct = 0

    while correct != 1:  # то, что после этого цикла будет повторяться, пока условие правильно

        correct = int(input('введите "1": '))  # это будет повторяться, пока пользователь не введёт "14"

    # ========================== break ==========================

    while True:  # если в условии написано True, то он будет продолжаться бесконечно
        v = input('0 = прекратить цикл ')
        if v == '0':
            break
        print(v, 'meow')

    # ========================= continue ========================

    v = int(v)

    while v < 10:  # continue пропускает оставшуюся часть цикла
        v += 1
        if v % 3 == 0:  # если число кратно трём
            print('skip', end=' ')
            continue  # то цикл начинается заново
        print(v, end=' ')
    print()

    # =========================== else ==========================

    cycle = 0
    while cycle != 5:

        cycle += 1
        print('до завершения цикла осталось:', 5 - cycle + 1)
        brik = input('закончить цикл сейчас? (y/n): ')

        if brik == 'y':
            break
    else:  # если цикл прервётся через break, то else не будет выполняться
        print('получена награда за терпение... и труд')  # в остальных случаях else бесполезен
    none()  # while


# while_cycle()


def for_cycle():
    # counter это переменная, которой будет присваиваться по очереди то, что идёт после in
    for counter in 1, 2, 3, 5, 10:
        print(counter, end=' ')
    print()

    # это можно упростить написав range
    for strike in range(5):  # теперь strike будет присваиваться числа от одного до числа в range
        print(strike, end=' ')
        if strike == 4:
            print('цикл прерван')
            break
    else:  # else будет выполняться, когда цикл завершится без break
        print('цикл завершён')
    print()

    for two in range(1, 10, 2):  # ну и ещё можно сделать как с переменными вобщем
        print(two, end=' ')
    print()

    for star in 'python':  # если написать строку, то цикл будет повторяться для каждого символа отдельно
        print(star, end=' ')
    print()

    a = [13, 43, 55, 2]
    for i in a:  # цикл будет выполняться для каждого значения переменной
        print(i, end=' ')

    # ======================== enumerate ========================

    scores = [54, 67, 48, 99, 27]

    # enumerate выводит индексы значений и сами значения
    for india in enumerate(scores):
        print(india)  # (0, 54) (1, 67) (2, 48) (3, 99) (4, 27)

    # в for можно работать сразу с несколькими переменными
    for os, el in enumerate(scores):
        # тут os - индексы, а el - значения
        print(el, end=' ')  # 54 67 48 99 27

    none()  # for


# for_cycle()


def defs():
    def funct():  # создаёт функцию

        for a in range(10):  # в которой будет выполняться этот код
            print(a, end='')  # в функции переменные не влияют на основой код
        print()

    funct()  # так нужно использовать эту функцию

    # что бы пользоваться переменными в функции их нужно добавить в скобочки

    def pirtn(meaning):
        print(meaning)

    meaning = '1-???'
    pirtn(meaning)

    pirtn('Hello word?')  # ну и не обязательно переменную конечно

    # в функции отдельные переменные
    def foo(x):
        print(x)

    x = 10  # и даже если переменная задана ранее
    foo(5)  # всё равно будет 5

    # !! не распространяется на списки
    def key(a):
        a[1] = 4

    el = [9, 1, 3]
    key(el)  # т
    print(el)  # [9, 4, 3]

    # ========================== return =========================

    def apple(inp):
        count = inp
        mass = count / 100 * 15  # %

        return mass, count, 'fl', 1 + 2  # return выводит переменные, или значения
        # и по сути создаёт список

    ohio = 20

    a1 = apple(ohio)
    b1, b2, b3, b4 = apple(ohio)
    c1 = apple(ohio)[1]

    print(b1, b2, b3, b4)  # 3.0 20 fl 3
    print(a1)  # (3.0, 20, 'fl', 3)
    print(c1)  # 20

    # =========================== знак "=" ========================

    def fed(op, not_necessary='defalt', pus=8):  # здесь мы заранее указываем значение этой переменной
        print(op, not_necessary, pus)

    # теперь её не обязательно указывать при вызове функции

    fed('гриб', 'сложно')  # гриб сложно 8
    fed('пельмени')  # пельмени defalt 8
    fed('уфа', pus=4)  # уфа defalt 4

    # ========================== *args ===========================

    # что бы передать в функцию неизвестное количество значения нужно написать "*"
    def sumator(*pop):
        print(pop)  # (9, 5, 3, 6, 6)
        return sum(pop)

    o = sumator(9, 5, 3, 6, 6)
    print(o)  # 29

    # ========================= **kwargs =========================

    # **kwargs позволяет передавать произвольное количество именованных аргументов и создаёт из них словарь
    def print_info(**kwargs):
        for key, value in kwargs.items():
            print(f"{key}: {value}")

    print_info(name="John", age=25, city="New York")  # name: John, age: 25, city: New York

    none()  # def


# defs()


def files():
    # =========================== open ===========================

    file = open('C:/Users/v-v/OneDrive/Рабочий стол/example.txt', 'r', encoding='UTF-8')
    #                                                   присваивает кодировку ^
    # r - прочитать информацию из файла

    # =========================== read ===========================

    data = file.read()  # read выводит всё из файла
    print(data)

    data = file.read(10)  # номер в функции это кол-во символов, которые будет читать программа
    # и курсор остановится там, где закончился прошлый read
    print(data)

    # вместо read можно использовать цикл
    for string in file:
        print(string)

    # ========================== close ===========================

    file.close()  # закрывает файл

    # это обязательно нужно сделать

    # ========================== write ===========================

    def exam():
        x = open('example.txt', 'r')
        out = []
        for i in x:
            out.append(f'{len(i)} - {i}')
        out = ''.join(out)
        print(out)
        x.close()
        return out

    ou = exam()

    file = open('example.txt', 'w')
    # w означает, что файл будет полностью перезаписываться
    file.write(ou)  # write - то что будет передано в файл

    file = open('example.txt', 'a')
    # А значит, что туда будет добавляться что то
    file.write('\n44444444')

    # =========================== seek ===========================

    file.seek(0)  # в скобках будет позиция, в которую будет переведён курсор

    # =========================== with ===========================

    with open('example.txt') as file:
        # открывает файл и делает его в эту переменную
        # если использовать with, то закрывать файл не нужно
        text = file.read()
        for o in text:
            print(o)
            break

    # ======================== остальное =========================

    none()  # работа с файлами


# files()


def errors():
    a, b = 'c', 4

    try:  # если после try будет какая-то ошибка, то программа не остановится, а перейдёт к except
        a + b  # здесь будет ошибка, потому что нельзя к 4 прибавить букву
    except:
        print('ошибка')

    # ========================== ошибки ==========================

    # в except лучше писать по какой именно ошибке будет выводиться код
    try:
        open('ab')

    except FileNotFoundError:  # когда не находит указаный файл
        print('1')

    except ValueError:  # когда идёт работа с двумя разными типами переменных 'c' + 3
        print('2')

    except ZeroDivisionError:  # когда делится на ноль, что то
        print('3')

    except IndexError:  # выход за границы списка
        print('4')

    # TODO дописать ошибки

    # в except можно записать несколько ошибок except (ошибка1, ошибка2...):

    # ======================= else_finally ========================

    try:
        1 + 1
    except:
        print('ошибка какая то')
    else:  # будет выполняться если не будет этой ошибки
        print('всё хорошо')
    finally:  # код, который записан в этом блоке, будет выполняться вообще всегда
        print('уоде')

    # ========================== raise ===========================

    try:
        if a:
            raise BaseException('sxs')  # намеренно вызывает ошибку в коде
    except BaseException:
        raise

    # вместо BaseException можно написать любую ошибку

    # это можно делать без ничего
    raise

    none()  # try, except


# errors()


def classes():
    class User:  # создаём объект
        # создаём атрибуты
        name = 'aba'
        password = '8520ur0'
        is_banned = False

    user_1 = User()  # присваиваем переменной объект
    user_1.is_banned = True  # изменить атрибуты

    User.name = 'noname'  # изменить атрибуты класса (не влияет на объекты, где этот атрибут был изменён)

    class phone:
        name = 'nokia rio'
        youtube = True
        sms = False
        applications = []

        def print_info(self):  # self это ссылка означает, что функция взаимодействует с объектом
            print('name: {}\nyoutube: {}\nsms: {}'.format(
                self.name, self.youtube, self.sms))

        def add_app(self, app):
            self.applications.append(app)

    mine = phone()
    mine.print_info()
    mine.add_app('burger king')

    class op:
        def __init__(self, name, salary):  # init для того, что бы задать атрибуты
            self.name = name
            self.salary = salary

        def info(self):
            print(f'name: {self.name}\nsalary: {self.salary}')

    emp1 = op('bup', 29)
    emp1.info()

    import saved
    oa = saved.ctext("black", "black")
    print(oa)

    pass  # ООП (классы)


classes()
