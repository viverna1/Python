def minimax(state, depth, is_maximizing):
    if len(state) == 0:
        return 1 if is_maximizing else -1


    if is_maximizing:
        best_score = -float('inf')
        for move in [1, 2]:
            if len(state) >= move:
                score = minimax(state[move:], depth + 1, False)
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in [1, 2]:
            if len(state) >= move:
                score = minimax(state[move:], depth + 1, True)
                best_score = min(best_score, score)
        return best_score


def best_move(state):
    best_score = -float('inf')
    move_choice = 1
    for move in [1, 2]:
        if len(state) >= move:
            score = minimax(state[move:], 0, False)
            if score > best_score:
                best_score = score
                move_choice = move
    return move_choice


board = "0987654321"
print(board)

while len(board) > 0:
    move = int(input("you (1-2): "))
    if move not in [1, 2]:
        print("Invalid move. Please enter 1 or 2.")
        continue
    board = board[move:]
    print(board)

    if len(board) == 0:
        print("You win!")
        break

    move = best_move(board)
    print(f"AI: {move}")
    board = board[move:]
    print(board)

    if len(board) == 0:
        print("AI wins!")
        break
