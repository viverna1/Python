from functions import clear_console, ctext, remove_ansi_codes
from time import sleep

class Board:
    def __init__(self) -> None:
        self.board = [[ctext(str(j*3 + i + 1), "dark_grey") for i in range(3)] for j in range(3)]
        self.turn = "X"
        self.move_log = []
        self.max_sym = 7

    def draw_board(self):
        clear_console()
        print(f" {self.board[0][0]} │ {self.board[0][1]} │ {self.board[0][2]} ")
        print("───┼───┼───")
        print(f" {self.board[1][0]} │ {self.board[1][1]} │ {self.board[1][2]} ")
        print("───┼───┼───")
        print(f" {self.board[2][0]} │ {self.board[2][1]} │ {self.board[2][2]} ")

    def is_busy(self, x, y):
        return remove_ansi_codes(self.board[y][x]) in ("X", "O")

    def move(self, x, y):
        if not self.is_busy(x, y):
            self.board[y][x] = self.turn

            self.move_log.append((x, y))
            if len(self.move_log) > self.max_sym:
                del_x, del_y = self.move_log.pop(0)
                self.board[del_y][del_x] = ctext(str(del_y*3 + del_x + 1), "dark_grey")

            if len(self.move_log) > self.max_sym - 1:
                last_x, last_y = self.move_log[0]
                self.board[last_y][last_x] = ctext(remove_ansi_codes(self.board[last_y][last_x]), "red")

            self.turn = "XO"[self.turn == "X"]  # смена очереди

        else:
            raise Exception(f"Клетка {x}; {y} занята.")

    def check_winner(self):
        # Проверка строк
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] in ("X", "O"):
                return self.board[row][0]
        
        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] in ("X", "O"):
                return self.board[0][col]
        
        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] in ("X", "O"):
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] in ("X", "O"):
            return self.board[0][2]
        
        return None

    def is_full(self):
        for row in range(3):
            for col in range(3):
                if not self.is_busy(col, row):
                    return False
        return True

    def get_empty_cells(self):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if not self.is_busy(col, row):
                    empty_cells.append((col, row))
        return empty_cells

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        
        # Оценка конечных состояний
        if winner == "O":  # ИИ выиграл
            return 10 - depth
        elif winner == "X":  # Игрок выиграл
            return depth - 10
        elif self.is_full():  # Ничья
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for x, y in self.get_empty_cells():
                # Сохраняем текущее состояние
                original_value = self.board[y][x]
                original_turn = self.turn
                
                # Делаем ход за ИИ (O)
                self.board[y][x] = "O"
                self.turn = "X"
                
                # Рекурсивно оцениваем ход
                score = self.minimax(depth + 1, False)
                
                # Отменяем ход
                self.board[y][x] = original_value
                self.turn = original_turn
                
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for x, y in self.get_empty_cells():
                # Сохраняем текущее состояние
                original_value = self.board[y][x]
                original_turn = self.turn
                
                # Делаем ход за игрока (X)
                self.board[y][x] = "X"
                self.turn = "O"
                
                # Рекурсивно оцениваем ход
                score = self.minimax(depth + 1, True)
                
                # Отменяем ход
                self.board[y][x] = original_value
                self.turn = original_turn
                
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        
        for x, y in self.get_empty_cells():
            # Сохраняем текущее состояние
            original_value = self.board[y][x]
            original_turn = self.turn
            
            # Делаем ход за ИИ (O)
            self.board[y][x] = "O"
            self.turn = "X"
            
            # Оцениваем ход
            score = self.minimax(0, False)
            
            # Отменяем ход
            self.board[y][x] = original_value
            self.turn = original_turn
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move


board = Board()
play_with_ai = 1# input("Играть с ИИ? (y/n): ").lower() == 'y'

while True:
    try:
        board.draw_board()
        winner = board.check_winner()
        if winner:
            input(winner + " победили")
            break
        if board.is_full():
            input("Ничья!")
            break
            
        if board.turn == "X" or not play_with_ai:
            # Ход игрока
            pos = int(input(board.turn + ": ")) - 1
            board.move(pos % 3, pos // 3)
        else:
            # Ход ИИ
            print("ИИ думает...")
            sleep(1)
            x, y = board.get_best_move()
            board.move(x, y)
            
    except ValueError:
        break
    except Exception as e:
        print(f"Ошибка: {e}")
        continue