import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import urlparse, parse_qs
import requests
import os
import subprocess
from io import BytesIO
from PIL import Image  # Добавляем Pillow для работы с изображениями

from config import TELEGRAM_BOT_TOKEN, E621API

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def resize_image(image_data, max_size=(1000, 1000)):
    """Обрезает изображение до максимальных размеров 1000x1000"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Получаем текущие размеры
            width, height = img.size
            
            # Если изображение уже меньше или равно максимальным размерам, возвращаем как есть
            if width <= max_size[0] and height <= max_size[1]:
                return image_data
            
            # Вычисляем новые размеры с сохранением пропорций
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Сохраняем в BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output.getvalue()
            
    except Exception as e:
        print(f"Ошибка при изменении размера изображения: {e}")
        return image_data  # Возвращаем оригинал в случае ошибки


def parse_e621_link(link):
    try:
        parsed = urlparse(link)
        try:
            post_id = int(parsed.path.strip("/").split("/")[-1])
        except (ValueError, IndexError):
            return "Ошибка: не удалось извлечь ID"

        query = parse_qs(parsed.query)
        tag = query.get("q", [""])[0].split("+")[-1].split()[-1]
        if not tag:
            return "Ошибка: тег q=... не найден"

        search_link = f"https://e621.net/posts?tags={tag}"
        return search_link, tag, post_id
    except IndexError as e:
        return f"Ошибка: {e}"


def process_user_data(func):
    """chat_id, username, first_name, message/call, user_data, data

    - chat_id (int): id чата.
    - username (str): username пользователя.
    - first_name (str): ник пользователя.
    - message/call (cls): объект сообщения.
    """
    # Получаем объект кода функции
    code_obj = func.__code__

    arguments = code_obj.co_varnames[:code_obj.co_argcount]

    def wrapper(message):
        try:

            username = message.from_user.username
            first_name = message.from_user.first_name if 'first_name' in arguments else None
            try:
                chat_id = message.chat.id if 'chat_id' in arguments else None
            except AttributeError:
                chat_id = message.from_user.id if 'chat_id' in arguments else None

            allowed_args = [arg for arg in [
                chat_id,
                username if 'username' in arguments else None,
                first_name,
                message if 'message' in arguments or 'call' in arguments else None,
            ] if arg is not None]

            func(*allowed_args)

        except TypeError as e:
            print(e)
            bot.send_message(message.chat.id, "Ошибка, введите /start\nЕсли проблема повторится, опишите её в /report")

    return wrapper


def get_file_url_and_type(post_id):
    url = f"https://e621.net/posts/{post_id}.json"
    response = requests.get(url, auth=("v-v4", E621API), headers={
        "User-Agent": "TelegramBot/1.0 (by v-v4)"
    })

    if response.status_code == 200:
        data = response.json()
        file_url = data["post"]["file"]["url"]
        file_ext = data["post"]["file"]["ext"]
        return file_url, file_ext
    else:
        print("Ошибка:", response.status_code)
        return None, None


def convert_webm_to_mp4(webm_url, output_path="converted.mp4"):
    webm_file = "temp_video.webm"
    try:
        FFMPEG_PATH = r"D:\Programs\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

        with requests.get(webm_url, stream=True) as r:
            with open(webm_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Конвертация через ffmpeg
        subprocess.run([
            FFMPEG_PATH, "-i", webm_file,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            output_path
        ], check=True)

        return output_path
    except Exception as e:
        print("Ошибка конвертации:", e)
        return None
    finally:
        if os.path.exists(webm_file):
            os.remove(webm_file)


@bot.message_handler(func=lambda message: True)
@process_user_data
def handle_message(chat_id, message):
    try:
        post_url = message.text
        url, name, post_id = parse_e621_link(post_url)

        file_url, file_ext = get_file_url_and_type(post_id)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Открыть ссылку", url=url))

        if not file_url:
            bot.send_message(chat_id, f"`{name}`", reply_markup=markup, parse_mode="MarkdownV2")
            return

        if file_ext in ["webm"] or file_ext in ["gif"]:
            mp4_path = convert_webm_to_mp4(file_url)
            if mp4_path:
                with open(mp4_path, "rb") as video_file:
                    bot.send_video(chat_id, video_file, caption=f"`{name}`", reply_markup=markup, parse_mode="MarkdownV2")
                os.remove(mp4_path)
            else:
                bot.send_message(chat_id, "Не удалось конвертировать видео.")

        elif file_ext in ["mp4"]:
            bot.send_video(chat_id, file_url, caption=f"`{name}`", reply_markup=markup, parse_mode="MarkdownV2")

        else:
            try:
                # Сначала пробуем отправить как есть
                bot.send_photo(chat_id, file_url, caption=f"`{name}`", reply_markup=markup, parse_mode="MarkdownV2")
            except telebot.apihelper.ApiTelegramException:
                # Если не получается, скачиваем и обрабатываем изображение
                response = requests.get(file_url)
                if response.status_code == 200:
                    # Обрезаем изображение до 1000x1000
                    resized_image_data = resize_image(response.content)
                    
                    img = BytesIO(resized_image_data)
                    img.name = "image.jpg"  # обязательно имя с расширением
                    bot.send_photo(chat_id, img, caption=f"`{name}`", reply_markup=markup, parse_mode="MarkdownV2")
                else:
                    bot.send_message(chat_id, "Не удалось загрузить изображение")

    except ValueError:
        bot.send_message(chat_id, "Ошибка, введите ссылку на арт")


if __name__ == '__main__':
    print("Бот активирован")
    bot.infinity_polling()