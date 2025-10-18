import random
import tkinter as tk


def generate_board(size):
    board2 = []
    for i2 in range(size):
        board2.append([])
        for j2 in range(size):
            board2[i2].append(random.randint(0, 1))
    return board2


def show_board(curr_board):
    for row in curr_board:
        for cell in row:
            print(cell, end=" ")
        print()
    print()
    print()


def around_count(board, x, y):
    count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
            count += board[ny][nx]
    return count


def next_gen():
    global board
    new_board = [[0] * board_size for _ in range(board_size)]

    for i in range(board_size):
        for j in range(board_size):
            curr_around_count = around_count(board, j, i)
            if board[i][j] == 1:
                if curr_around_count < 2 or curr_around_count > 3:
                    new_board[i][j] = 0
                else:
                    new_board[i][j] = 1
            else:
                if curr_around_count == 3:
                    new_board[i][j] = 1

    board = new_board
    draw_grid()


def draw_grid():
    # Функция для рисования сетки квадратов
    for i in range(board_size):
        for j in range(board_size):
            x1 = j * square_size
            y1 = i * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = board[i][j] == 1
            fill_color = "black" if color else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")


board_size = 9
board = generate_board(board_size)
root = tk.Tk()

# Размер окна и квадратов
canvas_width = 450
canvas_height = 450
square_size = 50

# Создаем холст для рисования
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=0)

show_board(board)
draw_grid()

next_gen_button = tk.Button(root, text="next_gen", command=next_gen)
next_gen_button.grid(row=1, column=0)

# Запускаем главный цикл
root.mainloop()
