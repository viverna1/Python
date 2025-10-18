import os
from pathlib import Path

# Словарь с эмодзи для разных типов файлов
FILE_EMOJIS = {
    "image": "🖼",
    "video": "🎞",
    "audio": "🎵",
    "default": "📄"
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".flac", ".ogg"}

def get_file_emoji(filename):
    ext = Path(filename).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return FILE_EMOJIS["image"]
    elif ext in VIDEO_EXTENSIONS:
        return FILE_EMOJIS["video"]
    elif ext in AUDIO_EXTENSIONS:
        return FILE_EMOJIS["audio"]
    else:
        return FILE_EMOJIS["default"]

def print_directory_tree(startpath, padding='', max_depth=None, current_depth=0, blacklist=None):
    """
    Рекурсивно выводит дерево директорий с файлами
    :param startpath: начальная директория
    :param padding: отступ для визуализации вложенности
    :param max_depth: максимальная глубина рекурсии (None - без ограничений)
    :param current_depth: текущая глубина рекурсии (для внутреннего использования)
    """
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        print(f"{padding}└── [Доступ запрещен]")
        return

    for i, entry in enumerate(entries):
        if blacklist and entry in blacklist:
            continue

        path = os.path.join(startpath, entry)
        is_last = i == len(entries) - 1

        if os.path.isdir(path):
            # Вывод директории с иконкой 📁
            print(f"{padding}{'└── ' if is_last else '├── '}📁 {entry}/")
            new_padding = padding + ('    ' if is_last else '│   ')
            print_directory_tree(path, new_padding, max_depth, current_depth + 1)
        else:
            # Вывод файла с подходящей иконкой
            emoji = get_file_emoji(entry)
            print(f"{padding}{'└── ' if is_last else '├── '}{emoji} {entry}")

def main():
    import argparse
    blacklist = ["tree.py", ".git"]
    
    parser = argparse.ArgumentParser(description='Вывод дерева директорий')
    parser.add_argument('path', nargs='?', default='.', help='Путь к директории (по умолчанию: текущая)')
    parser.add_argument('--depth', type=int, default=None, help='Максимальная глубина рекурсии')
    args = parser.parse_args()

    startpath = Path(args.path).resolve()
    print(f"\nДерево директорий: {startpath}\n{'═' * 50}")
    print_directory_tree(startpath, max_depth=args.depth, blacklist=blacklist)
    print(f"{'═' * 50}\nВсего файлов и папок: {sum(1 for _ in Path(startpath).rglob('*'))}")

if __name__ == "__main__":
    main()
