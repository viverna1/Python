import os
import tempfile
import shutil
import zipfile

def main():
    temp_dir = None
    try:
        # Создаем временную папку на диске D
        temp_dir = tempfile.mkdtemp(dir='D:\\', prefix='temp_folder_')
        print(f'Создана временная папка: {temp_dir}')

        # Открываем папку
        os.startfile(temp_dir)

        # В данном месте вы можете выполнить необходимые действия, например, скопировать файлы в эту папку
        folder = input('1-бит сайбер\n2-новая папка на рабочем столе\nпуть: ')
        if folder == '1':
            folder = r'D:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels'
        elif folder == '2':
            folder_name = "archives"
            folder_path = create_folder_on_desktop(folder_name)
            folder = folder_path

        source_folder = temp_dir
        process_archives(source_folder, folder)
        
    finally:
        print('=' * 20)
        if temp_dir:
            # Закрываем и удаляем временную папку вместе с файлами
            print(f'Закрываем и удаляем временную папку: {temp_dir}')
            try:
                shutil.rmtree(temp_dir)  # Удаляем папку рекурсивно
            except Exception as e:
                print(f'Ошибка при удалении временной папки: {e}')


def process_archives(source_folder, destination_folder):
    # Получаем список файлов в папке с архивами
    archive_files = [f for f in os.listdir(source_folder) if f.endswith('.zip')]

    print('=' * 20)
    # Обработка каждого архива
    for archive_file in archive_files:
        # Получаем полный путь к архиву
        zip_file_path = os.path.join(source_folder, archive_file)

        # Получаем имя архива без расширения
        archive_name = os.path.splitext(archive_file)[0]

        # Создаем папку в указанной директории с именем архива
        extraction_path = os.path.join(destination_folder, archive_name)

        # Если папка уже существует, добавляем числовой суффикс
        count = 1
        while os.path.exists(extraction_path):
            extraction_path = os.path.join(destination_folder, f'{archive_name}_{count}')
            count += 1

        os.makedirs(extraction_path)

        # Извлекаем файлы из архива
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_path)

        # Копируем название архива в папку
        with open(os.path.join(extraction_path, 'archive_name.txt'), 'w') as name_file:
            name_file.write(archive_name)

        print(f'Файлы из архива "{archive_file}" успешно извлечены и скопированы в папку: {extraction_path}\n')


def create_folder_on_desktop(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive\Рабочий стол")
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        print('=' * 20)
        # Проверяем, существует ли папка
        if not os.path.exists(folder_path):
            # Создаем папку
            os.makedirs(folder_path)
            print(f'Папка "{folder_name}" создана на рабочем столе по пути: {folder_path}')
        
        return folder_path

    except Exception as e:
        print(f'Ошибка при создании папки: {e}')
        return None

if __name__ == "__main__":
    main()