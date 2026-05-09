# Setup player & Settings
bot_player = "O"
human_player = "X"
max_depth = 3
game_mode = None 
n = 14
win_length = 5
curr_player = human_player
game_over = False
is_calculating = False

import ui.ui as ui
import ai.ai as ai

# ==============================
# GAME LOGIC
# ==============================

def reset_state():
    global game_over, curr_player, is_calculating, game_mode
    game_over = False
    is_calculating = False
    curr_player = human_player
    game_mode = None
    ai.transposition_table.clear()

def set_title(row, col):
    global curr_player, game_over, is_calculating

    if game_over or is_calculating or ui.v_board[row][col] != "":
        return

    ui.v_board[row][col] = curr_player

    if curr_player == human_player:
        # Nếu là X: Lấy biến color_red từ file ui.py
        ui.board[row][col].config(text=curr_player, fg=ui.color_red) 
    else:
        # Nếu là O: Lấy biến color_white từ file ui.py
        ui.board[row][col].config(text=curr_player, fg=ui.color_white)
    
    log_move(curr_player, row, col)


    if check_winner(row, col):
        return

    switch_player()

    if game_mode == "PVE" and curr_player == bot_player:
        ui.window.after(50, ai.bot_move)

def switch_player():
    global curr_player
    curr_player = human_player if curr_player == bot_player else bot_player
    ui.label.config(text=curr_player + "'s turn")

def check_winner(row, col):
    global game_over

    player = ui.board[row][col]["text"]
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        count = 1
        cells = [(row, col)]

        r, c = row + dr, col + dc
        while 0 <= r < n and 0 <= c < n and ui.board[r][c]["text"] == player:
            cells.append((r, c))
            count += 1
            r += dr
            c += dc

        r, c = row - dr, col - dc
        while 0 <= r < n and 0 <= c < n and ui.board[r][c]["text"] == player:
            cells.append((r, c))
            count += 1
            r -= dr
            c -= dc

        if count >= win_length:
            highlight_win(cells)
            ui.label.config(text=player + " wins!", fg=ui.color_yellow)
            game_over = True
            return True

    return False

def highlight_win(cells):
    for r, c in cells:
        ui.board[r][c].config(bg=ui.color_light_gray, fg=ui.color_yellow)

def log_move(player, row, col):
    ui.log_text.config(state="normal")
    ui.log_text.insert("end", f"{player}: ({row}, {col})\n")
    ui.log_text.see("end")
    ui.log_text.config(state="disabled")

def new_game():
    global game_over, curr_player
    game_over = False
    curr_player = human_player
    ui.label.config(text=curr_player + "'s turn", fg="white")

    for r in range(n):
        for c in range(n):
            ui.v_board[r][c] = ""
            ui.board[r][c].config(text="", bg=ui.color_gray, fg=ui.color_red)

    ui.log_text.config(state="normal")
    ui.log_text.delete(1.0, "end")
    ui.log_text.config(state="disabled")

    ai.transposition_table.clear()