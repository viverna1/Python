import yt_dlp
import os

url = "https://www.youtube.com/playlist?list=PLZIJHyH-zaLFPYdVUTA2GQti55MzV91S5"


youtube_videos = ["So.. I changed the water's code", 'Жертвы Прогрессивных Активистов, и Левой Повестки - Чарли Кирк и Ирина Заруцкая', 'МОЖНО ЛИ ПРОЙТИ PLAGUE INC БЕЗ СИМПТОМОВ', 'КОРОЧЕ ГОВОРЯ, Я ОПОЗДАЛ НА САМОЛЕТ', 'Террария, но каждый день МИР ИЗ СЛУЧАЙНОГО БЛОКА! [Полное прохождение террарии] • terraria', 'Уровень сложности: НЕВОЗМОЖНО ( A Difficult Game About Climbing 2 )', 'Я Прошел Самый Сложный Мод На Subnautica', 'МАЖОРНЫЕ ДЕВУШКИ | ТИК ТОК', 'Twitch нарезка №27 | 1000 и 1 причина игнорировать Миссионерская позу', 'Худший Диктатор в Tropico 6', 'Can you beat Deathworld with NO WEAPONS?', 'Зачем я прошёл Plants vs. Zombies: Hard Mode без подсолнухов?', 'What is the FASTEST way to TUNNEL in Minecraft', "Про невозможные сиды, и как я их пройти пытался в Baldi's Basics Plus", 'Проект Апокалипсис в Cities Skylines', 'Тик ток качки флексят мускулами .', 'TORCH ENDS STOCKFISH!!!!!', '100 Дней Хардкора в Sons of the Forest', '100 Дней Хардкора в Raft', '50 Дней в Voices of The Void', 'Путь к Божеству в Civilization 6 | Этап 1\\2', 'Путь к Божеству в Civilization 6 | Этап 2\\2', '25 Забегов в Noita', '60 Забегов в Noita', 'Милиционер гигант ( Militsioner )', 'Страдания и боль ( Only up в доспехах )', 'Мы vs гора ( PEAK )', 'Гора приколов ( PEAK )', 'Под градусом ( CS 2/ Just another night shift )', 'Ты не продержишься 30 раундов ( Bodycam zombie )', 'Найди 50 отличий на DUST 2 ( Teardown )', 'VR комната ( VR эксперимент/ MADiSON VR )', 'Шипы, огонь и зайцы ( Super bunny man )', 'Горе грабитель ( The Professional / Pools )', 'Опять 25 ( Minecraft )', 'Помогите мне ( A Difficult Game About Climbing )', 'Клиника Джохана и Мармока  ( Surgeon Simulator )', 'Террария БЕЗ Мобов', 'ТЕРРАРИЯ В ПУСТОМ МИРЕ 1/2', 'Террария в ПУСТОМ мире 2/2', 'КОРОЧЕ ГОВОРЯ, Я ПРОДАЮ КАНАЛ...', 'КОРОЧЕ ГОВОРЯ, Я ОТКАЗАЛСЯ ОТ МЯСА', 'ВОТ ПОЧЕМУ НЕ СТОИТ СТРОИТЬ ТЫСЯЧИ АЭРОПОРТОВ | PLAGUE INC', 'КОРОЧЕ ГОВОРЯ, КУПИЛ IPHONE 17', 'Леваков МАССОВО Увольняют с Работы - за посты о Чарли Кирке', 'ОНИ ДЕЛАЮТ ЛЕКАРСТВО ЗА 60 СЕКУНД В PLAGUE INC', 'Как меня затопили , Развалили тачку и Унизили в кофейне (Смешные истории из жизни в Саратове)', 'ИВАНГАЙ стал новым Маркаряном - грибной просветитель', '[Видео удалено]', 'КОРОЧЕ ГОВОРЯ, Я ОБОГНАЛ МИСТЕРА БИСТА', 'Сложность - невозможно (Без гейзеров, High Temp) ► Oxygen not included ► Bionic pack', 'Каждые 100 циклов падает ядерная бомба ► Oxygen not included ► Spaced Out', 'Что, если.. узкий мир 9 блоков 600% ► 25 часов полное прохождение ► Factorio', 'Что, если.. Mini base ► Oxygen not included ► Spaced Out', 'Что, если.. Warptorio 2 ► 35 часов хардкора ► Factorio', 'Водный мир ► 30 часов хардкора ► События каждые 10 минут! ► Oxygen not included ► Spaced Out', 'Что, если.. Скайблок без гейзеров? Empty World ► Oxygen Not Included ► Spaced Out', 'Сильвер Катка Возвращается в CS2 / PUBG', 'Прохождение стартовой локации на 100% (A Difficult Game About Climbing)', 'Я Попробовал Все Страхи Человечества', 'ЭПОХА ПЕРЕПОТРЕБЛЕНИЯ — самое бедное поколение', 'КОРОЧЕ ГОВОРЯ, ШКОЛУ ОТМЕНИЛИ!', 'КОРОЧЕ ГОВОРЯ, УНИЧТОЖАЮ АЙФОН 17', 'В Майнкрафте Кончился ВОЗДУХ...', 'ТЫСЯЧА МЕЛКИХ ЖНЕЦОВ В НАЧАЛЕ ИГРЫ SUBNAUTICA', 'АНАРХИЯ - МОЩНЕЙШАЯ КИРКА на проекте', 'Читаю ПЕРВОНАЧАЛЬНЫЙ сценарий Последней Кнопки 2', 'Новый GENESIS Кейс - ПРОСТО ИМБА в CS2!', 'ОЧЕНЬ ХАРДКОРНОЕ ИСПЫТАНИЕ В PLAGUE INC', "Докажи, что ты НЕ РОБОТ, чтобы пройти эту игру | I'm Not a Robot", 'Что лишнее 2 ( Teardown )', 'Отключили ВСЕ магазины игроков (это было непросто)', '[Видео с ограниченным доступом]', 'Он говорил c БОГОМ через компьютер. Программист шизофреник и TempleOS', 'Оно не тонет ( Paddle Paddle Paddle )', 'Мне выпало ЭТО с GENESIS Кейса в CS2 / Самый Редкий Скин Коллекции GENESIS']

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'extractor_args': {
        'youtube': {'lang': ['ru']}
    }
}

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
    
#     for video in info['entries']:
#         youtube_videos.append(video['title'])
        

exist = os.listdir(path=os.path.abspath("/media/v-v/External HD/Медиа/youtube"))
correct = [video for video in exist if video.endswith(".mkv")]
print(len(exist))
print(len(correct))

x = "ОЧЕНЬ ХАРДКОРНОЕ ИСПЫТАНИЕ В PLAGUE INC [cpk_2-V8hBc].mkv"

def rem_square_brackets(s):
    temp = ""
    for i in s:
        if i == "[":
            break
        temp += i
    return temp[:-1]

very_correct = [rem_square_brackets(video) for video in correct]

print("Мы vs гора ( PEAK )" in very_correct)

sw = False


youtube_videos2 = [
    "Victims of Progressive Activists and the Left Agenda - Charlie Kirk and Irina Zarutskaya",
    "IS IT POSSIBLE TO GO THROUGH PLAGUE INC WITHOUT SYMPTOMS",
    "IN SHORT, I MISSED THE PLANE",
    "gfgfgdtetretrt55555"
]


def maybe_correct(check, what):
    try:
        temp = {}
        for i in range(len(check)):
            if check[i] not in temp:
                temp[check[i]] = 0
            temp[check[i]] += 1
        temp2 = {}
        for i in range(len(what)):
            if check[i] not in temp2:
                temp2[check[i]] = 0
            temp2[check[i]] += 1
        
        what_should_be = sum([p for p in temp.values()])
        coincidences = 0
        for i in temp:
            if i in temp2:
                coincidences += min(temp.get(i, 0), temp2.get(i, 0))

        return coincidences >= what_should_be - 2
        

        # if len(temp) > len(temp2):
        #     res = abs(temp - temp2)
        # else:
        #     res = abs(temp2 - temp)
        # return sum(res.values()) <= 5
    except Exception as e:
        return False


def maybe_correct(title1, title2):
    """Сравнивает два названия, допуская небольшие различия"""
    # Приводим к нижнему регистру для более мягкого сравнения
    t1 = title1.lower().strip()
    t2 = title2.lower().strip()
    
    # Если названия практически идентичны - считаем совпадением
    if t1 == t2:
        return True
    
    # Если одно название содержится в другом - тоже совпадение
    if t1 in t2 or t2 in t1:
        return True
    
    # Можно добавить сравнение по первым N символам
    if len(t1) > 10 and len(t2) > 10:
        if t1[:10] == t2[:10]:  # Первые 15 символов совпадают
            return True
    
    return False



u = maybe_correct("Мы vs гора ( PEAK )((()))", "Мы vs г ( P )(()")
print(u)


# print(youtube_videos)
# print(very_correct)


for video in youtube_videos:
    sw = True
    for video2 in very_correct:
        if maybe_correct(video, video2):
            # print(video)
            sw = False
            break
    if sw:
        print(video)
            

   