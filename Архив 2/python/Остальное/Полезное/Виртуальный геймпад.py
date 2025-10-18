import json
import time
import vgamepad as vg
from pynput import keyboard

# Загрузка конфигурации кнопок из JSON-файла
with open('key_mapping.json', 'r') as file:
    key_mapping = json.load(file)

# Создание объекта геймпада
gamepad = vg.VX360Gamepad()

# Функция для обработки нажатий клавиш
def on_press(key):
    try:
        # Преобразуем нажатую клавишу в строку
        key_str = key.char if hasattr(key, 'char') else key.name
        # Ищем соответствие в key_mapping
        for gamepad_button, keyboard_key in key_mapping.items():
            if key_str == keyboard_key:
                print(gamepad_button)
                # Нажимаем соответствующую кнопку геймпада
                gamepad.press_button(getattr(vg.XUSB_BUTTON, gamepad_button))
                gamepad.update()
                break
    except Exception as e:
        print(f"Error processing key press: {e}")

# Функция для обработки отпускания клавиш
def on_release(key):
    try:
        # Преобразуем нажатую клавишу в строку
        key_str = key.char if hasattr(key, 'char') else key.name
        # Ищем соответствие в key_mapping
        for gamepad_button, keyboard_key in key_mapping.items():
            if key_str == keyboard_key:
                # Отпускаем соответствующую кнопку геймпада
                gamepad.release_button(getattr(vg.XUSB_BUTTON, gamepad_button))
                gamepad.update()
                break
    except Exception as e:
        print(f"Error processing key release: {e}")

# Запуск прослушивания клавиатуры
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("геймпад подключен..")
    listener.join()
