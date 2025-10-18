import os
import subprocess

# Введи URL страницы e621 с комиксом
comic_url = 'https://e621.net/pools/47395'

# Создаём папку для сохранения комикса
save_directory = r"D:\Personal\Git\python\MiniProjects\furry"
if not os.path.exists(save_directory):  
    os.makedirs(save_directory)

# Команда для gallery-dl
command = f'gallery-dl -d "{save_directory}" {comic_url}'

# Выполняем команду
try:
    print("Скачивание началось...")
    subprocess.run(command, shell=True, check=True)
    print(f"Комикс успешно сохранён в папке: {save_directory}")
except subprocess.CalledProcessError as e:
    print("Что-то пошло не так. Проверь ссылку или установку gallery-dl.")
