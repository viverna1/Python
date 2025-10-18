import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

plt.plot(x, y, label='Линейный график')  # добавить первый график

plt.plot(y, x,  # добавить второй график
         label='Линейный график 2',  # (str) - название графика
         color="black",  # (str, кортеж(r, g, b, a)) - цвет линии
         linewidth=10,  # (int) - толщина линии
         # linestyle=1,  # (str) - тип линии
         marker="o",  # (int (0-11), str) - тип маркера
         markerfacecolor=(0.5, 0, 1),  # (str, кортеж(r, g, b, a)) - цвет маркера
         markersize=15,  # (int) - размер маркера
         alpha=0.7,  # (float) - прозрачность
         fillstyle="left"  # ('full', 'left', 'right', 'bottom', 'top', 'none') - стиль заливки
         )

plt.xlabel('Ось X')  # название оси X
plt.ylabel('Ось Y')  # название оси Y
plt.title('Пример графика линии')  # название графика
plt.legend()  # добавление названий графиков в углу диаграммы (в panel)
plt.grid(True)  # отображение сетки
plt.show()  # Кусочки куриного филе обжарь, смешай с салатом, помидорами и сыром, полей соусом Цезарь.
