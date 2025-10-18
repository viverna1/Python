import yt_dlp
import os
from typing import List


def get_youtube_playlist(url: str) -> List[str]:
    """
    url - ссылка на плейлист
    Возвращает список названий видео
    """

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'extractor_args': {
            'youtube': {'lang': ['ru']}
        }
    }

    result_videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        for video in info['entries']:
            result_videos.append(video['title'])
    return result_videos
        

def get_downloaded(disk: str, path: str) -> List[str]:
    """
    disk - буква диска, для которой будет путь
    path - абсолютный путь до директории с видео без буквы диска
    Возвращает список названий видео .mkv
    """
    
    disk += ":\\"
    if os.path.exists(disk):
        exist = os.listdir(os.path.join(disk, path))
        correct = [video for video in exist if video.endswith(".mkv")]
        return correct
    else:
        raise Exception(f"Диска {disk} Не существует")


def rem_square_brackets(s: str) -> str:
    """Удаляет текст после '[' и убирает лишние пробелы"""
    return s.split('[')[0].strip()


def compare(title1: str, title2: str) -> bool:
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


def main():
    # Входные данные
    url = "https://www.youtube.com/playlist?list=PLZIJHyH-zaLFPYdVUTA2GQti55MzV91S5"
    disk, path = "E", "/Медиа/youtube"

    # Получениче видео
    youtube_videos = get_youtube_playlist(url)
    downloaded = get_downloaded(disk, path)
    clean_downloaded = [rem_square_brackets(video) for video in downloaded]

    # Сравнение скачаных видео и с ютуба
    missing = []
    for yt_video in youtube_videos:
        if not any(compare(yt_video, dw_video) for dw_video in clean_downloaded):
            missing.append(yt_video)

    print("\033[31mОтсутствуют видео:\033[0m")
    print("\n".join(missing))
    print(f"\033[31mПотеряно: {len(missing)} из {len(youtube_videos)}\033[0m")

if __name__ == "__main__":
    main()
