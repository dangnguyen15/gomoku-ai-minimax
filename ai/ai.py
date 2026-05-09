# ==============================
# TRANSPOSITION TABLE & AI
# ==============================
transposition_table = {}

import ui.ui as ui
import ui.game as game

def board_to_key():
    return tuple(tuple(row) for row in ui.v_board)

def get_candidates():
    moves = set()
    for r in range(game.n):
        for c in range(game.n):
            if ui.v_board[r][c] != "":
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < game.n and 0 <= nc < game.n and ui.v_board[nr][nc] == "":
                            moves.add((nr, nc))
    return list(moves) if moves else [(game.n//2, game.n//2)]

def evaluate():
    score = 0
    for r in range(game.n):
        for c in range(game.n):
            if ui.v_board[r][c] == game.bot_player:
                score += evaluate_position(r, c, game.bot_player)
            elif ui.v_board[r][c] == game.human_player:
                score -= int(evaluate_position(r, c, game.human_player) * 1.2)
    return score

def evaluate_position(row, col, player):
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    total_score = 0
    opponent = game.human_player if player == game.bot_player else game.bot_player

    for dr, dc in directions:
        count = 1
        # Kiểm tra trạng thái 2 đầu
        open_ends = 0
        
        # Đi về phía trước
        r, c = row + dr, col + dc
        while 0 <= r < game.n and 0 <= c < game.n and ui.v_board[r][c] == player:
            count += 1
            r, c = r + dr, c + dc
        # Sau khi hết chuỗi quân mình, xem ô tiếp theo có trống không
        if 0 <= r < game.n and 0 <= c < game.n and ui.v_board[r][c] == "":
            open_ends += 1

        # Đi về phía sau
        r, c = row - dr, col - dc
        while 0 <= r < game.n and 0 <= c < game.n and ui.v_board[r][c] == player:
            count += 1
            r, c = r - dr, c - dc
        # Xem ô phía sau có trống không
        if 0 <= r < game.n and 0 <= c < game.n and ui.v_board[r][c] == "":
            open_ends += 1

        # --- TÍNH ĐIỂM CHIẾN THUẬT ---
        if count >= 5:
            total_score += 1000000  # Thắng ngay lập tức
        elif count == 4:
            if open_ends == 2:
                total_score += 100000 # 4 quân trống 2 đầu
            elif open_ends == 1:
                total_score += 10000  # 4 quân bị chặn 1 đầu
        elif count == 3:
            if open_ends == 2:
                total_score += 5000   # Ưu tiên cực cao cho 3 quân trống 2 đầu
            elif open_ends == 1:
                total_score += 500    # 3 quân bị chặn 1 đầu
        elif count == 2:
            if open_ends == 2:
                total_score += 100
            elif open_ends == 1:
                total_score += 10

    return total_score

def minimax(depth, alpha, beta, maximizing):
    key = (board_to_key(), depth, maximizing)

    if key in transposition_table:
        return transposition_table[key]

    if depth == 0:
        score = evaluate()
        transposition_table[key] = score
        return score

    moves = get_candidates()

    if maximizing:
        max_eval = -float("inf")

        for r, c in moves:
            ui.v_board[r][c] = game.bot_player
            eval = minimax(depth - 1, alpha, beta, False)
            ui.v_board[r][c] = ""

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        transposition_table[key] = max_eval
        return max_eval

    else:
        min_eval = float("inf")

        for r, c in moves:
            ui.v_board[r][c] = game.human_player
            eval = minimax(depth - 1, alpha, beta, True)
            ui.v_board[r][c] = ""

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break

        transposition_table[key] = min_eval
        return min_eval

def bot_move():
    if game.game_over or game.is_calculating:
        return

    game.is_calculating = True

    best_score = -float("inf")
    best_move = None

    for r, c in get_candidates():
        ui.v_board[r][c] = game.bot_player
        score = minimax(game.max_depth - 1, -float("inf"), float("inf"), False)
        ui.v_board[r][c] = ""

        if score > best_score:
            best_score = score
            best_move = (r, c)

    if best_move:
        r, c = best_move
        ui.v_board[r][c] = game.bot_player
        ui.board[r][c].config(text=game.bot_player, fg=ui.color_white)

        game.log_move("Bot", r, c)

        if game.check_winner(r, c):
            game.is_calculating = False
            return

        game.curr_player = game.human_player
        ui.label.config(text=game.curr_player + "'s turn")

    game.is_calculating = False