from copy import deepcopy


def ctext(text: any, color: str = 'reset', style: str = 'reset') -> str:
    """Описание:
        Функция позволяет выводить текст определенным цветом и стилем в терминале.

    Аргументы:
        text (any): Текст, который нужно вывести с определенным цветом и стилем
        color (str): Цвет текста. Может принимать следующие значения:
            - 'black': черный
            - 'red': красный
            - 'green': зеленый
            - 'yellow': желтый
            - 'blue': синий
            - 'purple': фиолетовый
            - 'grey': серый
            - 'dark_grey': тёмно-серый
            - 'cyan': голубой
            - 'white': белый
            - 'reset': сбросить цвет на стандартный (по умолчанию)
        style (str): Стиль текста. Может принимать следующие значения:
            - 'bold': жирный
            - 'italic': курсивный
            - 'underline': подчеркнутый
            - 'strikethrough': зачёркнутый
            - 'frame': текст в рамке
            - 'reset': сбросить стиль на стандартный (по умолчанию)

    Возвращает:
        str: Строка с примененным к ней цветом и стилем.
    """
    styles = {
        'bold': '\033[1m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'strikethrough': '\033[9m',
        'frame': '\033[51m',
        'reset': '\033[0m'
    }
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'grey': '\033[37m',
        'dark_grey': '\033[90m',
        'darkgrey': '\033[90m',
        'reset': '\033[0m'
    }

    if color not in colors or style not in styles:
        return str(text)  # Вывести текст без изменений, если цвет не определён
    else:
        return f"{styles[style]}{colors[color] if color != 'reset' else ''}{str(text)}\033[0m"


def draw_board():
    for i in range(3):  # каждый столбец
        for j in range(3):  # каждая строка
            cell = board[i * 3 + j]
            print(ctext(" " + str(i*3+j+1), "grey") if cell == 0 else " X" if cell == 1 else " O", end='')
            if j < 2:
                print(' |', end='')
        print()
        if i < 2:
            print('---+---+---')


def evaluate(curr_board):
    for a, b, c in ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
                    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
                    (0, 4, 8), (2, 4, 6)):            # по диагонали
        if curr_board[a] == curr_board[b] == curr_board[c] != 0:
            return curr_board[a]
    return 0


def game_status(curr_board):
    if evaluate(curr_board) != 0:
        return f"{'O' if evaluate(curr_board) == -1 else 'X'} победил"
    elif len([i for i in range(len(curr_board)) if curr_board[i] == 0]) == 0:
        return "Ничья"
    return "Продолжается"


def get_possible_moves(curr_board):
    return [i for i in range(len(curr_board)) if curr_board[i] == 0]


def minimax(curr_board, curr_move):
    if game_status(curr_board) != "Продолжается":
        return evaluate(curr_board)

    is_max = curr_move == bot_sym

    if is_max:
        best_score = float('-inf')
        for move in get_possible_moves(curr_board):
            new_board = deepcopy(curr_board)
            new_board[move] = bot_sym_code  # Бот делает ход
            score = minimax(new_board, player_sym)  # Следующий ход игрока
            best_score = max(best_score, score)
    else:
        best_score = float('inf')
        for move in get_possible_moves(curr_board):
            new_board = deepcopy(curr_board)
            new_board[move] = player_sym_code  # Игрок делает ход
            score = minimax(new_board, bot_sym)  # Следующий ход бота
            best_score = min(best_score, score)
    return best_score


def get_best_move(curr_board):
    best_score = float('-inf')
    best_move = -1

    for move in get_possible_moves(curr_board):
        new_board = deepcopy(curr_board)
        new_board[move] = bot_sym_code
        score = minimax(new_board, player_sym)

        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def is_forced_draw(curr_board):
    if len(get_possible_moves(curr_board)) > 3:
        return False
    for move in get_possible_moves(curr_board):
        new_board = deepcopy(curr_board)
        new_board[move] = bot_sym_code
        score = minimax(new_board, player_sym)

        if score != 0:
            return False
    return True


def game():
    while True:
        draw_board()

        move = int(input("Ваш ход (1-9): ")) - 1
        if move < 0 or move > 9 or board[move] != 0:
            print("Не правильный ввод, попробуйте ещё.")
            continue
        board[move] = player_sym_code

        if game_status(board) != "Продолжается" or is_forced_draw(board):
            draw_board()
            if is_forced_draw(board):
                print("Ничья")
                break
            print(game_status(board))
            break

        bot_move = get_best_move(board)
        board[bot_move] = bot_sym_code

        if game_status(board) != "Продолжается" or is_forced_draw(board):
            draw_board()
            if is_forced_draw(board):
                print("Ничья")
                break
            print(game_status(board))
            break


bot_sym = "X"
bot_sym_code = 1
player_sym = "O"
player_sym_code = -1

board = [0 for i in range(9)]
game()
