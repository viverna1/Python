import shutil
import sys
import tkinter as tk
import os

import PIL
from PIL import Image, ImageTk
path1 = r'E:\для восстановления винды\D\Personal\Furry2\safe2'
path2 = r'E:\для восстановления винды\D\Personal\Furry2\not safe'
path3 = r'E:\для восстановления винды\D\Personal\Furry2\temp 2' 


def check_password(password):
    try:
        if int(password) ^ 999 == 678:
            root.authenticated = True
        else:
            root.destroy()
            raise Exception("Invalid password")
    except Exception:
        root.destroy()
        raise Exception("Invalid password")


# Создаем графическое окно
root = tk.Tk()
root.authenticated = False

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=0, column=0)
password_button = tk.Button(root, text="Войти", command=lambda: check_password(password_entry.get()))
password_button.grid(row=0, column=1)

while not root.authenticated:
    root.update()

password_entry.destroy()
password_button.destroy()

# Глобальная переменная для хранения текущего индекса изображения
current_image_index = 0

label = tk.Label(root)
label_2 = tk.Label(root)
label_3 = tk.Label(root)
label_text = tk.Label(root, text="123")


def show_image(image_path, image_path_2, image_path_3):
    root.geometry("1200x1050")
    # Открываем изображение
    try:
        image = Image.open(image_path)
        image_2 = Image.open(image_path_2)
        image_3 = Image.open(image_path_3)

        # Масштабируем изображение
        max_size = (900, 900)
        image.thumbnail(max_size)

        max_size2 = (300, 300)
        image_2.thumbnail(max_size2)
        image_3.thumbnail(max_size2)

        # Преобразуем его в формат, понятный tkinter
        photo = ImageTk.PhotoImage(image)
        photo_2 = ImageTk.PhotoImage(image_2)
        photo_3 = ImageTk.PhotoImage(image_3)
        # Создаем метку и отображаем изображение на ней
        label.configure(image=photo)
        label.image = photo  # сохраняем ссылку на изображение, чтобы избежать удаления из памяти
        label.grid(row=1, columnspan=6)

        label_2.configure(image=photo_2)
        label_2.image = photo_2
        label_2.grid(row=1, column=7)

        label_3.configure(image=photo_3)
        label_3.image = photo_3
        label_3.grid(row=1, column=8)
    except PIL.UnidentifiedImageError:
        save_image(image_path, path3)
        image_name = os.path.basename(image_path)
        mess = f"Ошибка: Изображение {image_name} пропущено и добавлено в папку 3"
        label_text.configure(text=mess)
        print(mess)


def next_image():
    global current_image_index, last_image_path, open_button  # объявляем, что будем использовать глобальную переменную

    # Получаем список всех файлов в директории
    images = os.listdir(images_directory)
    print(images[0])

    # Сортируем их по возрастанию
    images.sort()

    # Если достигли конца списка изображений, обнуляем индекс
    if current_image_index >= len(images):
        current_image_index = 0

    # Получаем путь к следующему изображению
    image_path = os.path.join(images_directory, images[current_image_index])
    image_path_2 = os.path.join(images_directory, images[current_image_index + 1])
    image_path_3 = os.path.join(images_directory, images[current_image_index + 2])

    last_image_path = image_path
    # Отображаем изображение
    show_image(image_path, image_path_2, image_path_3)

    open_button.configure(text="Открыть " + image_path.split(".")[-1])

    # Увеличиваем индекс для следующего изображения
    current_image_index += 1


def previous_image():
    global current_image_index, last_image_path  # объявляем, что будем использовать глобальную переменную

    # Получаем список всех файлов в директории
    images = os.listdir(images_directory)

    # Сортируем их по возрастанию
    images.sort()

    # Если достигли начала списка изображений, устанавливаем индекс на последний элемент
    if current_image_index <= 0:
        current_image_index = 0
    else:
        current_image_index -= 1

    # Получаем путь к предыдущему изображению
    image_path = os.path.join(images_directory, images[current_image_index])
    image_path_2 = os.path.join(images_directory, images[current_image_index + 1])
    image_path_3 = os.path.join(images_directory, images[current_image_index + 2])

    last_image_path = image_path

    # Отображаем изображение
    show_image(image_path, image_path_2, image_path_3)


def save_image(image_path, directory):
    # Извлекаем имя файла из пути к изображению
    file_name = os.path.basename(image_path)

    # Сохраняем изображение в указанной директории
    try:
        shutil.copyfile(image_path, os.path.join(directory, file_name))
        delete_image(image_path, notify=False)
        mess = f"Изображение {file_name} сохранено в {directory} и удалено"
        label_text.configure(text=mess)
        print(mess)
    except Exception as e:
        mess = f"Ошибка при сохранении изображения: {e}"
        label_text.configure(text=mess)
        print(mess)


def delete_image(image_path, notify=True):
    image_name = os.path.basename(image_path)
    # Удаляем изображение
    os.remove(image_path)
    previous_image()
    if notify:
        mess = f"Изображение {image_name} удалено"
        label_text.configure(text=mess)
        print(mess)


def open_image():
    global last_image_path
    os.startfile(last_image_path)


def change_path(new_path, button, line_number, path_number):
    filename = sys.argv[0]
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

        if 0 < line_number <= len(lines):
            lines[line_number - 1] = f"path{path_number} = r'{new_path}'\n"

            with open(filename, 'w', encoding="utf-8") as file:
                file.writelines(lines)
            print("Путь успешно изменен.")
            button.config(text="Сохранено")
        else:
            print("Неверный номер строки.")


def on_entry_change(args, button):
    if len(args) == 3:
        button.config(text="Подтвердить")


def open_file(path):
    os.startfile(path)


def create_folder_widgets(row, folder_num, path_var, path):
    text = tk.Label(root, text=f"Папка {folder_num}")
    text.grid(row=row, column=0)

    confirm_button = tk.Button(root, text="Сохранено", command=lambda: change_path(path_var.get(), confirm_button, row, folder_num))
    confirm_button.grid(row=row, column=2)

    user_path_var = tk.StringVar()
    user_path = tk.Entry(root, width=30, textvariable=user_path_var)
    user_path.insert(0, path)
    user_path_var.trace_add('write', lambda arg1, arg2, arg3: on_entry_change((arg1, arg2, arg3), confirm_button))
    user_path.grid(row=row, column=1)

    open_button = tk.Button(root, text="Открыть", command=lambda: open_file(path))
    open_button.grid(row=row, column=3)


last_image_path = ""
images_directory = r'E:\для восстановления винды\D\Personal\Furry2\temp'


create_folder_widgets(7, 1, tk.StringVar(), path1)
create_folder_widgets(8, 2, tk.StringVar(), path2)
create_folder_widgets(9, 3, tk.StringVar(), path3)


# Создаем кнопку для переключения на предыдущее изображение
previous_button = tk.Button(root, text='Предыдущее изображение', command=previous_image)
previous_button.grid(row=0, column=1, padx=10, pady=0)

button = tk.Button(root, text='Следующее изображение', command=next_image)
button.grid(row=0, column=2, padx=10, pady=0)

save_button = tk.Button(root, text='Сохранить 1', command=lambda: save_image(last_image_path, path1))
save_button.grid(row=0, column=3, padx=10, pady=0)

save_button2 = tk.Button(root, text='Сохранить  2', command=lambda: save_image(last_image_path, path2))
save_button2.grid(row=0, column=4, padx=10, pady=0)

save_button3 = tk.Button(root, text='Сохранить  3', command=lambda: save_image(last_image_path, path3))
save_button3.grid(row=0, column=5, padx=10, pady=0)

delete_button = tk.Button(root, text='Удалить', command=lambda: delete_image(last_image_path))
delete_button.grid(row=0, column=0, padx=10, pady=0)

label_text.grid(row=0, column=6, padx=10, pady=0, columnspan=3)

open_button = tk.Button(root, text='Открыть ', command=open_image)
open_button.grid(row=2, column=0, padx=10, pady=0, columnspan=6)

next_image()

# Запускаем главный цикл событий
root.mainloop()
