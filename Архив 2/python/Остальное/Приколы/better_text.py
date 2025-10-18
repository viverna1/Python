import random
from pynput import keyboard
import pyperclip
import pyautogui as pag


class GetSelectedText:
    """
    Класс для получения выделенного текста из буфера обмена.
    """

    @staticmethod
    def __enter__() -> str:
        """Получает текст из буфера обмена при входе в контекст."""
        pag.hotkey('ctrl', 'c')
        return pyperclip.paste()

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        """Вставляет текст обратно в буфер обмена при выходе из контекста."""
        pag.hotkey('ctrl', 'v')


def on_press(key):
    """
    Обработчик нажатий клавиш.

    При нажатии комбинации клавиш Ctrl + R вызывается функция main_().
    """
    try:
        if key == keyboard.Key.ctrl_r:
            main_()
    except AttributeError:
        pass
    except IndexError:
        pag.hotkey('ctrl', 'c')
        print('ОШИБКА: В буфере обмена ничего нет.')


def on_release(key):
    """Обработчик отпускания клавиши. Выходит из программы при нажатии клавиши Esc."""
    if key == keyboard.Key.esc and False:
        return False


import re

def change_text_improved(text: str, intensity: float = 1.0) -> str:
    """
    Улучшенный uwu-фикатор с настраиваемой интенсивностью.
    Args:
        text: Исходный текст.
        intensity: Интенсивность (0.0 - 1.0)
    """

    # Замены слов
    word_replacements = {
        'можно': 'моня',
        'угу': 'уву',
        'что': 'фтё',
        'ничего': 'нитяво',
        'привет': 'привеет',
        'пока': 'поки',
        'спасибо': 'спасибки',
        'ладно': 'вядно',
        'да': 'дя',
        'нет': 'неть'
    }

    # Замены букв
    char_replacements = {
        'r': 'w', 'l': 'w',
        'р': 'в', 'л': 'в',
        'ш': 'ф', 'ч': 'щ',
        'ж': 'зь', 'Р': 'В', 'Л': 'В',
        'R': 'W', 'L': 'W'
    }

    # Разделяем текст на слова с сохранением пунктуации
    parts = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    new_parts = []

    for part in parts:
        # Пропускаем знаки препинания и эмодзи
        if not re.search(r'\w', part):
            new_parts.append(part)
            continue

        lower = part.lower()

        # Замена целых слов
        if lower in word_replacements and random.random() < intensity:
            new_word = word_replacements[lower]
            if part[0].isupper():
                new_word = new_word.capitalize()
            new_parts.append(new_word)
            continue

        # Побуквенные замены
        new_word = ''
        for i, ch in enumerate(part):
            prev_ch = part[i - 1] if i > 0 else ''
            next_ch = part[i + 1] if i < len(part) - 1 else ''

            if ch in char_replacements and random.random() < intensity:
                new_word += char_replacements[ch]
            elif (ch == 'а' and prev_ch not in 'аяыуеёиоюэ' 
                  and random.random() < intensity * 0.4):
                new_word += 'я'
            elif (prev_ch in ['с', 'н', 'б', 'м', 'p', 'n']
                  and ch.lower() in ['а', 'е', 'и', 'о', 'у']
                  and random.random() < intensity * 0.3):
                new_word += ch * 2
            else:
                new_word += ch

        # Добавляем “няшные” вставки
        if random.random() < intensity * 0.15:
            tail = random.choice(['~', '♥', '☆'])
            new_word += tail

        new_parts.append(new_word)

    new_text = ''.join(
        part + (' ' if i < len(parts) - 1 and re.match(r'\w', part) and re.match(r'\w', parts[i + 1]) else '')
        for i, part in enumerate(new_parts)
    )

    # Эмоции в конце
    if random.random() < intensity * 0.8:
        emotion = random.choice(['UwU', '>w<', 'OwO', ':3', '^^', '>3<', ';3'])
        if not new_text.endswith(tuple(emotion)):
            new_text += ' ' + emotion

    return new_text


def main():
    """Основная функция программы."""
    print("Программа better text | версия 1.2.1")
    print('Использование:')
    print('1. Включить программу')
    print('2. Свернуть программу на фон')
    print('3. Выделить текст, который ты хочешь улучшить')
    print('4. Нажать правый ctrl')
    print('Текст:')

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main_():
    """
    Функция для улучшения выделенного текста.

    Заменяет некоторые символы и комбинации символов в словах.
    """
    with GetSelectedText() as text:
        new_text = change_text(text)
        if text != new_text:
            print(text, '->', new_text)
        pyperclip.copy(new_text)


if __name__ == '__main__':
    # Примеры использования функции change_text
    #print(change_text('hello, cute aRl meow ninya no'))
    #print(change_text('привет, мЛар милый снег если :>'))
    main()
