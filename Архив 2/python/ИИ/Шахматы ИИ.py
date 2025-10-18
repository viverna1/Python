import copy

def ctext_param(r1, g1, b1, r2, g2, b2, text):
    return f"\033[38;2;{r1};{g1};{b1};48;2;{r2};{g2};{b2}m{text}\033[0m"


class Board(object):
    def __init__(self):
        self.board = [[Empty() for _ in range(8)] for _ in range(8)]
        self.fill_board()

    def __str__(self):
        res = ""
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                piece_color = (0, 0, 0) if self.get_color(row, col) == 1 else (255, 255, 255)
                if (row + col) % 2 == 0:
                    res += ctext_param(*piece_color, 235, 236, 208, " " + str(self.board[col][row]) + " ")
                else:
                    res += ctext_param(*piece_color, 115, 149, 82, " " + str(self.board[col][row]) + " ")
            res += "\n"
        return res
        # return "\n".join(" ".join(map(str, row)) for row in self.board)

    def get_color(self, x, y):
        return self.board[y][x].color

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def fill_board(self):
        for i in range(8):
            self.board[6][i] = Pawn(Color.WHITE)
            self.board[1][i] = Pawn(Color.BLACK)

        self.board[0][4] = King(Color.BLACK)
        self.board[7][4] = King(Color.WHITE)

        self.board[0][3] = Queen(Color.BLACK)
        self.board[7][3] = Queen(Color.WHITE)

        self.board[0][2] = self.board[0][5] = Bishop(Color.BLACK)
        self.board[7][2] = self.board[7][5] = Bishop(Color.WHITE)

        self.board[0][1] = self.board[0][6] = Knight(Color.BLACK)
        self.board[7][1] = self.board[7][6] = Knight(Color.WHITE)

        self.board[0][0] = self.board[0][7] = Rook(Color.BLACK)
        self.board[7][0] = self.board[7][7] = Rook(Color.WHITE)

    def move(self, xy_from, xy_to):
        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Empty()


class Color(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Piece(object):
    IMG = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.IMG


class Empty(object):
    color = Color.EMPTY

    def __str__(self):
        return " "

    def get_moves(self, board, x, y):
        raise NotImplementedError("Ошибка. Ходит пустая клетка.")

# Фигуры


class Pawn(Piece):
    IMG = "♟"

    def get_moves(self, board, x, y):
        moves = []
        # ход белых
        if self.color == Color.WHITE:
            # ход вперёд
            if y > 0 and board.get_color(x, y - 1) == Color.EMPTY:
                moves.append([x, y - 1])
            # ход на 2 клетки
            if y == 6 and board.get_color(x, y - 1) == Color.EMPTY and board.get_color(x, y - 2) == Color.EMPTY:
                moves.append([x, y - 2])
            # взятие фигуры
            if x - 1 > 0 and x > 0 and board.get_color(x - 1, y - 1) == Color.BLACK:
                moves.append([x - 1, y - 1])
            if x + 1 < 8 and x > 0 and board.get_color(x + 1, y - 1) == Color.BLACK:
                moves.append([x + 1, y - 1])

        # ход чёрных
        else:
            # ход вперёд
            if y < 7 and board.get_color(x, y + 1) == Color.EMPTY:
                moves.append([x, y + 1])
            # ход на 2 клетки
            if y == 1 and board.get_color(x, y + 1) == Color.EMPTY and board.get_color(x, y + 2) == Color.EMPTY:
                moves.append([x, y + 2])
            # взятие фигуры
            if x - 1 > 0 and y < 7 and board.get_color(x - 1, y + 1) == Color.WHITE:
                moves.append([x - 1, y + 1])
            if x + 1 < 8 and y < 7 and board.get_color(x + 1, y + 1) == Color.WHITE:
                moves.append([x + 1, y + 1])
        return moves


class King(Piece):
    IMG = "♚"

    def get_moves(self, board, x, y):
        moves = []
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and board.get_color(nx, ny) != self.color:
                moves.append([nx, ny])
        return moves


class Queen(Piece):
    IMG = "♛"

    def get_moves(self, board, x, y):
        moves = []

        # Ходы как у ладьи (горизонтальные и вертикальные)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board.get_color(nx, ny) == Color.EMPTY:
                        moves.append([nx, ny])
                    elif board.get_color(nx, ny) != self.color:
                        moves.append([nx, ny])
                        break
                    else:
                        break
                else:
                    break

        # Ходы как у слона (диагонали)
        for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board.get_color(nx, ny) == Color.EMPTY:
                        moves.append([nx, ny])
                    elif board.get_color(nx, ny) != self.color:
                        moves.append([nx, ny])
                        break
                    else:
                        break
                else:
                    break

        return moves


class Bishop(Piece):
    IMG = "♝"

    def get_moves(self, board, x, y):
        moves = []

        # Диагонали
        for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board.get_color(nx, ny) == Color.EMPTY:
                        moves.append([nx, ny])
                    elif board.get_color(nx, ny) != self.color:
                        moves.append([nx, ny])
                        break
                    else:
                        break
                else:
                    break

        return moves


class Rook(Piece):
    IMG = "♜"

    def get_moves(self, board, x, y):
        moves = []

        # Горизонтали и вертикали
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board.get_color(nx, ny) == Color.EMPTY:
                        moves.append([nx, ny])
                    elif board.get_color(nx, ny) != self.color:
                        moves.append([nx, ny])
                        break
                    else:
                        break
                else:
                    break

        return moves


class Knight(Piece):
    IMG = "♞"

    def get_moves(self, board, x, y):
        moves = []

        # Ходы коня (буква "Г")
        for dx, dy in ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and board.get_color(nx, ny) != self.color:
                moves.append([nx, ny])

        return moves


def minimax(board, turn, max_depth, depth=0):
    """
    Алгоритм минимакс для шахмат.
    :param board: Текущая доска.
    :param turn: Текущий ход (чёрные или белые).
    :param max_depth: Максимальная глубина рекурсии.
    :param depth: Текущая глубина.
    """
    if depth >= max_depth or is_game_over(board):
        return evaluate_board(board)

    is_max = turn == bot_color
    best_score = float('-inf') if is_max else float('inf')

    for xy_from in get_all_pieces(board):
        for xy_to in board.get_move_names(*xy_from):
            new_board = copy.deepcopy(board)
            new_board.move(xy_from, xy_to)

            score = minimax(new_board, "white" if turn == "black" else "black", max_depth, depth + 1)

            if is_max:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)

    return best_score


def is_game_over(board):
    """
    Проверяет конец игры (шах и мат или пат).
    """
    white_king = False
    black_king = False

    for row in board.board:
        for piece in row:
            if isinstance(piece, King):
                if piece.color == Color.WHITE:
                    white_king = True
                elif piece.color == Color.BLACK:
                    black_king = True

    return not (white_king and black_king)


PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 3,
    "Rook": 5,
    "Queen": 9,
    "King": 1000
}


def evaluate_board(board):
    """
    Оценивает текущую позицию на доске.
    Положительные значения выгодны для белых, отрицательные для чёрных.
    """
    score = 0
    for row in board.board:
        for piece in row:
            if isinstance(piece, Piece):
                value = PIECE_VALUES.get(type(piece).__name__, 0)
                if piece.color == Color.WHITE:
                    score += value
                elif piece.color == Color.BLACK:
                    score -= value
    return score


def get_all_pieces(curr_board):
    pieces = []
    for y in range(len(curr_board.board)):
        for x in range(len(curr_board.board[y])):
            piece = curr_board.board[y][x]
            # Проверяем только фигуры текущего игрока
            if isinstance(piece, Piece) and piece.color in (Color.WHITE, Color.BLACK):
                pieces.append((x, y))
    return pieces


def get_best_move(board, turn, max_depth):
    """
    Возвращает лучший ход для текущего игрока.
    :param board: Текущая доска.
    :param turn: Чей ход ('white' или 'black').
    :param max_depth: Максимальная глубина поиска.
    :return: Пара координат: (xy_from, xy_to).
    """
    best_score = float('-inf') if turn == bot_color else float('inf')
    best_move = None

    # Перебираем все возможные ходы
    for xy_from in get_all_pieces(board):
        for xy_to in board.get_move_names(*xy_from):
            new_board = copy.deepcopy(board)  # Копируем доску
            new_board.move(xy_from, xy_to)

            # Вызываем minimax для оценки этого хода
            score = minimax(new_board, "white" if turn == "black" else "black", max_depth)

            # Обновляем лучший ход
            if turn == bot_color:
                if score > best_score:
                    best_score = score
                    best_move = (xy_from, xy_to)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (xy_from, xy_to)

    return best_move


# Пример теста:
b = Board()
b.board[2][2] = Queen(Color.WHITE)
bot_color = "white"

# Добавим несколько фигур для теста
b.board[1][1] = Pawn(Color.BLACK)
b.board[6][6] = Pawn(Color.WHITE)
b.board[0][0] = Rook(Color.BLACK)
b.board[7][7] = Queen(Color.WHITE)

print("Текущая доска:")
print(b)

# Находим лучший ход
best_move = get_best_move(b, "black", max_depth=2)

# Применяем лучший ход
if best_move:
    b.move(*best_move)
    print("Доска после хода:")
    print(b)

