from random import randint
from time import sleep

class Matrix:
    def __init__(self, size):
        self.size = size
        # Более понятные названия для состояний клеток
        self.cell_states = {
            0: "  ",  # Мёртвая клетка - пробелы
            1: "██"   # Живая клетка
        }
        self.matrix = self.create_matrix()

    def print_matrix(self):
        # Очистка экрана для анимации
        print("\033[H\033[J", end="")
        print("Игра 'Жизнь' (Ctrl+C для выхода)")
        print("═" * (self.size * 2))
        
        for row in self.matrix:
            for cell in row:
                print(self.cell_states[cell], end="")
            print()

    def create_matrix(self):
        # Создаём пустое поле
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def get_neighbors_count(self, x, y):
        total = -self.matrix[y][x]  # берём значение текущей клетки
        rows = cols = self.size
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny = (y + dy) % rows
                nx = (x + dx) % cols
                total += self.matrix[ny][nx]
        
        return total

    @staticmethod
    def rules(status: int, neighbors: int) -> int:
        if status == 1 and neighbors in (2, 3):  # если клетка жива и вокруг неё 2 или 3 соседа то выживает
            return 1
        elif status == 0 and neighbors == 3:  # если клетка мертва и вокруг неё 3 соседа, то рождается
            return 1
        return 0

    def next_step(self):
        """Рассчитываем следующее поколение"""
        new_matrix = self.create_matrix()  # Используем существующий метод
        
        for y in range(self.size):
            for x in range(self.size):
                neighbors = self.get_neighbors_count(x, y)
                new_matrix[y][x] = self.rules(self.matrix[y][x], neighbors)
        
        self.matrix = new_matrix

    def templates(self, name: str) -> list[tuple[int, int]]:
        templates_dict = {
            "random": [(randint(0, self.size-1), randint(0, self.size-1)) 
                      for _ in range(self.size * 4)],
            "glider": [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)],  # Глайдер
            "blinker": [(2, 1), (2, 2), (2, 3)],  # Мигалка
            "glider_gun": [  # Пушка Госпера
                (5, 1), (5, 2), (6, 1), (6, 2),
                (5, 11), (6, 11), (7, 11),
                (4, 12), (8, 12),
                (3, 13), (9, 13),
                (3, 14), (9, 14),
                (6, 15),
                (4, 16), (8, 16),
                (5, 17), (6, 17), (7, 17),
                (6, 18)
            ],
            "nuke": [(0, 1), (1, 0), (1, 1), (2, 1), (1, 2)],
            "two_gliders": [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3),
                            (11, 6), (12, 5), (13, 7), (13, 6), (13, 5)]
        }
        return templates_dict.get(name, [])  # Возвращаем пустой список если шаблон не найден

    def create_template(self, name: str, centered=True):
        # создаёт шаблон в центре
        coords = self.templates(name)
        if centered and coords:
            offset_y = (self.size // 2) - max(y for y, _ in coords) // 2
            offset_x = (self.size // 2) - max(x for _, x in coords) // 2
            coords = [(y + offset_y, x + offset_x) for y, x in coords]

        for y, x in coords:
            if 0 <= y < self.size and 0 <= x < self.size:
                self.matrix[y][x] = 1

    def clear_matrix(self):
        """Очистка поля"""
        self.matrix = self.create_matrix()


def main():
    matr = Matrix(20)
    
    matr.create_template("two_gliders")
    
    try:
        generation = 0
        while True:
            matr.print_matrix()
            print(f"Поколение: {generation}")
            matr.next_step()
            generation += 1
            sleep(0.2)
    except KeyboardInterrupt:
        print("\nИгра завершена!")


if __name__ == "__main__":
    # print(*[(i[0]+10, i[1]+5) for i in [(1, 1), (2, 0), (3, 2), (3, 1), (3, 0)]], sep=", ")
    main()