import requests

# =============================================================================
# ОСНОВЫ BIBLIOTEKI REQUESTS
# =============================================================================

# GET-запрос (получение данных)
response = requests.get('https://api.example.com/data')

# POST-запрос (отправка данных)
data = {'key': 'value'}
response = requests.post('https://api.example.com/data', json=data)

# PUT-запрос (обновление данных)
response = requests.put('https://api.example.com/data/1', json=data)

# DELETE-запрос (удаление данных)
response = requests.delete('https://api.example.com/data/1')

# 3. ПАРАМЕТРЫ ЗАПРОСОВ
# =============================================================================

# Параметры URL (query parameters)
params = {'page': 1, 'limit': 10}
response = requests.get('https://api.example.com/items', params=params)
# URL будет: https://api.example.com/items?page=1&limit=10

# Заголовки запроса
headers = {
    'User-Agent': 'MyApp/1.0',
    'Authorization': 'Bearer token123'
}
response = requests.get('https://api.example.com/data', headers=headers)

# Данные формы (form data)
form_data = {'username': 'user', 'password': 'pass'}
response = requests.post('https://api.example.com/login', data=form_data)

# JSON данные
json_data = {'name': 'John', 'age': 30}
response = requests.post('https://api.example.com/users', json=json_data)

# 4. ОБРАБОТКА ОТВЕТА
# =============================================================================

# Проверка статуса код
if response.status_code == 200:
    print("Успешный запрос!")
elif response.status_code == 404:
    print("Страница не найдена!")

# Удобные проверки
if response.ok:  # True если статус 200-400
    print("Запрос успешен!")

# Получение содержимого ответа
text_content = response.text  # Текст ответа
json_content = response.json()  # JSON как словарь/список
binary_content = response.content  # Бинарные данные

# Заголовки ответа
print(response.headers)
print(response.headers['Content-Type'])

# 5. РАБОТА С JSON API
# =============================================================================

# Пример работы с JSONPlaceholder API
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

if response.status_code == 200:
    post_data = response.json()
    print(f"Title: {post_data['title']}")
    print(f"Body: {post_data['body']}")

# 6. ОБРАБОТКА ОШИБОК
# =============================================================================

try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Вызывает исключение для статусов 4xx/5xx
    
except requests.exceptions.HTTPError as err:
    print(f"HTTP ошибка: {err}")
except requests.exceptions.ConnectionError as err:
    print(f"Ошибка подключения: {err}")
except requests.exceptions.Timeout as err:
    print(f"Таймаут: {err}")
except requests.exceptions.RequestException as err:
    print(f"Ошибка запроса: {err}")

# 7. СЕССИИ (для множественных запросов)
# =============================================================================

# Создание сессии
session = requests.Session()

# Настройка сессии
session.headers.update({'User-Agent': 'MyApp/1.0'})
session.auth = ('username', 'password')

# Использование сессии
response1 = session.get('https://api.example.com/data1')
response2 = session.get('https://api.example.com/data2')

# 8. ФАЙЛЫ И ЗАГРУЗКИ
# =============================================================================

# Загрузка файла
files = {'file': open('document.pdf', 'rb')}
response = requests.post('https://api.example.com/upload', files=files)

# Скачивание файла
response = requests.get('https://example.com/image.jpg')
with open('image.jpg', 'wb') as f:
    f.write(response.content)

# 9. ПРОКСИ И АУТЕНТИФИКАЦИЯ
# =============================================================================

# Аутентификация
auth = ('username', 'password')
response = requests.get('https://api.example.com/protected', auth=auth)

# Прокси
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}
response = requests.get('http://example.com', proxies=proxies)

# 10. ТАЙМАУТЫ
# =============================================================================

# Таймаут на весь запрос
response = requests.get('https://api.example.com/data', timeout=5)

# Разные таймауты на подключение и чтение
response = requests.get('https://api.example.com/data', timeout=(3.05, 27))

# 11. ПРАКТИЧЕСКИЕ ПРИМЕРЫ
# =============================================================================

# Пример 1: Получение данных о погоде
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': 'your_api_key',
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Пример 2: Отправка данных формы
def login(username, password):
    login_data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(
        'https://example.com/login',
        data=login_data,
        allow_redirects=True
    )
    
    return response

# =============================================================================
# ВАЖНЫЕ МОМЕНТЫ:
# =============================================================================
# 1. Всегда обрабатывайте исключения
# 2. Используйте таймауты для избежания зависаний
# 3. Проверяйте статус ответа response.raise_for_status()
# 4. Для множественных запросов используйте сессии
# 5. Уважайте API - соблюдайте rate limits
# 6. Не храните чувствительные данные в коде