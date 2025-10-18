from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

from datetime import datetime

# создаём приложение.
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))  # путь к папке, где лежит app.py
db_path = os.path.join(project_dir, 'data', 'site.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}, password={self.password}>"

# Главная страница
@app.route('/')
def index():
    # render_template возвращает HTML файл
    return render_template('index.html')

# Дополнительная страница
@app.route('/about')
@app.route('/additional_page') # можно добавить несколько адресов на одну функцию
def about():
    return render_template('about.html')


@app.route('/auth', methods=['POST', 'GET'])  # динамический URL для обработки аутентификации
def auth():
    # Обработка POST-запроса (отправка формы)
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form['username']
        password = request.form['password']

        # Проверяем, что оба поля заполнены
        if username and password:
            # Создаем нового пользователя
            user = User(username=username, password=password)
            try:
                # Пытаемся добавить пользователя в базу данных
                db.session.add(user)
                db.session.commit()
                # При успехе переводим пользователя на главную страницу
                return redirect(f'/users/{user.id}')
            except:
                # Обрабатываем ошибку при добавлении в БД
                return "При добавлении пользователя произошла ошибка"
        else:
            # Если поля не заполнены
            return "Поля не заполнены"
    
    # Обработка GET-запроса (отображение формы)
    else:
        # Рендерим страницу с формой аутентификации
        return render_template('auth.html')



# Обработка пользователей
@app.route('/users')
def users():
    # Получаем всех пользователей из базы данных
    users_list = User.query.order_by(User.date_registered.desc()).all()
    # Рендерим страницу со списком пользователей
    return render_template('users.html', users=users_list)


@app.route('/users/<int:user_id>')
def user_profile(user_id):
    # Получаем пользователя по ID
    user = User.query.get_or_404(user_id)
    # Рендерим страницу профиля пользователя
    return render_template('user_profile.html', user=user)


@app.route('/users/<int:user_id>/delete')
def user_delete(user_id):
    # Получаем пользователя по ID
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        return "При удалении пользователя произошла ошибка"

    return redirect('/users')

# Редактирование профиля пользователя
@app.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
def edit_profile(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['edit_name']
        try:
            db.session.commit()
            return redirect(f'/users/{user.id}')
        except:
            return "При добавлении пользователя произошла ошибка"
    else:
        return render_template('/edit_profile.html', user=user)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

