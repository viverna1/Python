from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    username = data.get('username', 'неизвестно')
    print(f'Кнопка нажата от пользователя: {username}')
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5001, debug=True)
