import asyncio
from googletrans import Translator
import pyautogui as pag
from pynput import keyboard
import pyperclip


async def translate(text, lang='ru'):
    translator = Translator()
    translation = await translator.translate(text, dest=lang)
    return translation.text


def latin_characters():
    result = []
    for char_code in range(ord('A'), ord('Z') + 1):
        result.append(chr(char_code))
    for char_code in range(ord('a'), ord('z') + 1):
        result.append(chr(char_code))
    return result

def is_latin(line):
    all_latin_chars = latin_characters()
    for sym in all_latin_chars:
        if sym in line:
            return True
    return False


async def main_():
    word = pyperclip.paste()  # Берем текст из буфера обмена
    print(f"Скопированный текст: {word}")

    if word:  # Проверяем, что в буфере обмена не пусто
        if is_latin(word):
            word = await translate(word)
        else:
            word = await translate(word, lang='en')
    pyperclip.copy(word)

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_r:  # Используем правый Ctrl
            pag.hotkey('ctrl', 'c')
            asyncio.run(main_())  # Используем asyncio.run для вызова асинхронной функции
            pag.hotkey('ctrl', 'v')  # Вставляем переведённый текст
    except AttributeError as e:
        print(e)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def main():
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
