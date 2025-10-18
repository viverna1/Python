import random


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
            - 'cyan': голубой
            - 'white': белый
            - 'reset': сбросить цвет на стандартный (по умолчанию)
        style (str): Стиль текста. Может принимать следующие значения:
            - 'bold': жирный
            - 'italic': курсивный
            - 'underline': подчеркнутый
            - 'strikethrough': перечеркнутый
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
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'grey': '\033[37m',
        'darkgrey': '\033[90m',
        'reset': '\033[0m'
    }
    if color not in colors or style not in styles:
        return text  # Вывести текст без изменений, если цвет не определён
    else:
        return styles[style] + colors[color] + text + colors['reset'] + styles['reset']


class Cell:
    def __init__(self, value):
        self.value = value

    def isBusy(self):
        return self.value in ("0", "X")

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value


class Board:
    def __init__(self):
        self.board = []
        for i in range(9):
            self.board.append(Cell(ctext(str(i+1), "darkgrey")))

    def __str__(self):
        return (f" {self.board[0]} | {self.board[1]} | {self.board[2]} \n"
                f"---+---+---\n"
                f" {self.board[3]} | {self.board[4]} | {self.board[5]} \n"
                f"---+---+---\n"
                f" {self.board[6]} | {self.board[7]} | {self.board[8]} \n")

    def __getitem__(self, index):
        return self.board[index]


def move(master: Board, position, symbol: str) -> None:
    master.board[position].value = symbol


def check_win(curr_board):
    # Возможные выигрышные комбинации
    win_combinations = [
        (0, 1, 2),  # Первая строка
        (3, 4, 5),  # Вторая строка
        (6, 7, 8),  # Третья строка
        (0, 3, 6),  # Первый столбец
        (1, 4, 7),  # Второй столбец
        (2, 5, 8),  # Третий столбец
        (0, 4, 8),  # Первая диагональ
        (2, 4, 6)  # Вторая диагональ
    ]

    # Проверка всех возможных выигрышных комбинаций
    for combo in win_combinations:
        if (curr_board[combo[0]] == curr_board[combo[1]] == curr_board[combo[2]]
                and curr_board[combo[0]] is not None):
            return curr_board[combo[0]]

    return None


def check_draw(curr_board):
    return all(cell.isBusy() for cell in curr_board)


def bot_move(curr_board, symbol):
    free_cells = [cell_index for cell_index in range(9) if not board[cell_index].isBusy()]
    position = random.choice(free_cells)
    print(position)
    move(curr_board, position, symbol)


board = Board()
players = ("X", "0")
current_turn = 0

print(board)
while True:
    # Ход игрока
    while True:
        try:
            player_position = int(input(f"Ход {players[current_turn]}: "))
            if not 0 < player_position < 10:
                raise IndexError
        except (ValueError, IndexError):
            continue
        move(board, player_position-1, players[current_turn])
        break
    current_turn = (current_turn + 1) % 2  # Смена игрока
    bot_move(board, players[current_turn])  # Ход бота
    current_turn = (current_turn + 1) % 2

    print(board)
    if check_win(board) is not None:
        print(f"Победил {check_win(board)}")
        break
    elif check_draw(board):
        print(f"Ничья")
        break
