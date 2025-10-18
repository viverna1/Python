import asyncio
import math
import random
import time
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import numpy as np


class Window:
    def __init__(self, general_root, is_true):
        self.root = general_root
        self.is_true = is_true
        self.x = 900
        self.y = 450
        self.x_size = 200
        self.y_size = 150

        # Создаем главное окно и скрываем его
        self.root = general_root
        # Создаем новое окно для гифки
        self.window = tk.Toplevel()
        # Задаем размер окна (ширина x высота + смещение по горизонтали + смещение по вертикали)
        self.window.geometry("300x200")

        self.window.title("")

        self.window.geometry(f"{self.x_size}x{self.y_size}+{self.x}+{self.y}")
        additional_quit = lambda: (self.root.quit(), print('nya') if self.is_true else print('fuck'))
        self.window.protocol("WM_DELETE_WINDOW", additional_quit)  # Обработка закрытия окна

        # Загружаем гифку
        # gif = Image.open(f'../../L/ключ1.gif')
        gif = Image.open(r'd:\Personal\Git\python\Архив 2\python\L\ключ1.gif')
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        # Создаем метку для отображения гифки
        gif_label = tk.Label(self.window)
        gif_label.pack()

        def update_frame(index):
            frame = gif_frames[index]
            gif_label.configure(image=frame)
            self.window.after(50, update_frame, (index + 1) % len(gif_frames))

        update_frame(0)

    def geometry(self, x_size, y_size):
        self.window.geometry(f"{x_size}x{y_size}")

    async def move_to(self, x, y):
        self.x = x
        self.y = y
        self.animate_move()

    def animate_move(self):
        target_x, target_y = self.x, self.y
        current_x, current_y = self.window.winfo_x(), self.window.winfo_y()

        if current_x != target_x or current_y != target_y:
            dx = (target_x - current_x) // 5 if current_x != target_x else 0
            dy = (target_y - current_y) // 5 if current_y != target_y else 0

            new_x = math.floor(current_x + dx)
            new_y = math.floor(current_y + dy)

            self.window.geometry(f"{self.x_size}x{self.y_size}+{new_x}+{new_y}")
            self.window.after(10, self.animate_move)

    def get_pos(self):
        return self.x, self.y


async def shuffle():
    tasks = []

    for window_index in range(4):
        x_pos = start_pos + window_index * step
        tasks.append(windows[window_index].move_to(x_pos, 250))

    for window_index in range(4, 8):
        x_pos = start_pos + (window_index - 4) * step
        tasks.append(windows[window_index].move_to(x_pos, 750))

    await asyncio.gather(*tasks)


async def shuffle_patten(pattern):
    global windows
    tasks = []
    positions = [wind.get_pos() for wind in windows]

    # 0 1 2 3
    # 4 5 6 7

    new_windows = []
    window_index = 0
    for pattern_index in pattern:
        x_pos, y_pos = positions[pattern_index][0], positions[pattern_index][1]
        tasks.append(windows[window_index].move_to(x_pos, y_pos))
        new_windows.append(windows[pattern_index])
        window_index += 1

    windows = new_windows[:]

    await asyncio.gather(*tasks)


def create_windows():
    root = tk.Tk()
    root.withdraw()
    global windows
    lucky_window = random.randint(0, 7)
    for num in range(8):
        window = Window(root, num == lucky_window)
        windows.append(window)
    root.mainloop()


def distribute_points(length, num_points):
    return length / (num_points - 1)


async def show_true():
    for wind in windows:
        if wind.is_true:
            pos = wind.get_pos()
            await wind.move_to(pos[0], pos[1]-100)
            time.sleep(0.5)
            await wind.move_to(pos[0], pos[1])
            break


async def loop_objects():
    global windows

    # Параметры овала
    h = 900  # x-координата центра овала
    k = 500  # y-координата центра овала
    a = 600  # длина полуоси по x
    b = 350  # длина полуоси по y

    # Функция для получения координат точек по овалу
    def oval_points(num_points, angle):
        t = np.linspace(0, 2 * np.pi, num_points)
        x = h + a * np.cos(t + angle)
        y = k + b * np.sin(t + angle)
        return x, y

    # Угол для движения по овалу
    angle = 0

    while True:
        # Получаем координаты точек по овалу
        pos = oval_points(len(windows)+1, angle)
        pos = list(zip(pos[0], pos[1]))

        # Двигаем окна к полученным координатам
        for i in range(len(windows)):
            await windows[i].move_to(pos[i][0], pos[i][1])

        # Увеличиваем угол для движения по овалу
        angle += 0.05
        await asyncio.sleep(0.1)  # Для контроля скорости движения


windows = []


line_length = 1440
start_pos = 150
step = distribute_points(line_length, 4)

threading.Thread(target=create_windows).start()
time.sleep(1)
loop = asyncio.get_event_loop()

patterns = {
    'shuffle_x': [7, 6, 5, 4, 3, 2, 1, 0],
    'shuffle_xx': [5, 4, 7, 6, 1, 0, 3, 2],
    'shuffle_reverse_horizontal': [3, 2, 1, 0, 7, 6, 5, 4],
    'shuffle_x_pair': [6, 7, 4, 5, 2, 3, 0, 1],
    'shuffle_circle': [1, 2, 3, 7, 0, 4, 5, 6],
    'shuffle_reverse_circle': [4, 0, 1, 2, 5, 6, 7, 3],
    'shuffle_pair_circle': [4, 5, 0, 1, 6, 7, 2, 3],
    'shuffle_2_circle': [1, 5, 6, 2, 0, 4, 7, 3],
    'shuffle_obtuse_angle': [7, 2, 4, 6, 1, 3, 5, 0],
    'shuffle_vertical_stripes': [1, 0, 3, 2, 5, 4, 7, 6]
}

# 0 1 2 3
# 4 5 6 7


def main():
    loop.run_until_complete(shuffle())
    time.sleep(1)
    loop.run_until_complete(show_true())
    time.sleep(1)

    for i in range(10):
        current_pattern = random.choice(list(patterns.values()))
        loop.run_until_complete(shuffle_patten(current_pattern))
        time.sleep(0.4)

    time.sleep(0.1)
    loop.run_until_complete(loop_objects())


main()
