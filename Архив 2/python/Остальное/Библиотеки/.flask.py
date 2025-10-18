from flask import Flask

# создаём приложение.
app = Flask(__name__)

# говорит Flask, что функция home() отвечает на запрос к главной странице /
@app.route('/')
def index():
    # что возвращается пользователю
    return "Привет, мир!"

if __name__ == "__main__":
    # запускает сервер, debug=True позволяет видеть ошибки и изменения сразу
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)

