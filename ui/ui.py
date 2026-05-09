import tkinter as tk

# ==============================
# SETTINGS (UI Colors)
# ==============================
color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"
color_white = "#ffffff"
color_red = "#ff4d4d"

window = tk.Tk()

board = []
v_board = []
label = None
log_text = None

import ui.game as game

# ==============================
# UI FUNCTIONS
# ==============================
def show_mode_selection():

    game.reset_state()

    for widget in window.winfo_children():
        widget.destroy()

    frame = tk.Frame(window, bg=color_gray)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="CARO GOMOKU",
             font=("Consolas", 28, "bold"),
             bg=color_gray, fg=color_yellow).pack(pady=30)

    tk.Label(frame, text="Choose Game Mode",
             font=("Consolas", 24),
             bg=color_gray, fg="white").pack(pady=40)

    tk.Button(frame, text="Player vs Player",
              font=("Consolas", 16),
              bg=color_blue, fg="white",
              width=20,
              command=start_pvp).pack(pady=20)

    tk.Button(frame, text="Player vs Bot",
              font=("Consolas", 16),
              bg=color_blue, fg="white",
              width=20,
              command=start_pve).pack(pady=20)

def start_pvp():
    game.game_mode = "PVP"
    init_game_ui()

def start_pve():
    game.game_mode = "PVE"
    init_game_ui()

def init_game_ui():
    global board, v_board, label, log_text

    for widget in window.winfo_children():
        widget.destroy()

    frame = tk.Frame(window, bg=color_gray)
    frame.pack(side="left", expand=True, fill="both")

    label = tk.Label(frame, text=game.curr_player + "'s turn",
                     font=("Consolas", 18),
                     bg=color_gray, fg="white")
    label.grid(row=0, column=0, columnspan=game.n)

    board = [[None]*game.n for _ in range(game.n)]
    v_board = [[""]*game.n for _ in range(game.n)]

    for r in range(game.n):
        for c in range(game.n):
            btn = tk.Button(frame, text="",
                            font=("Consolas", 12, "bold"),
                            bg=color_gray, fg=color_blue,
                            width=3, height=1,
                            command=lambda r=r, c=c: game.set_title(r, c))
            btn.grid(row=r+1, column=c, sticky="nsew")
            board[r][c] = btn

    log_frame = tk.Frame(window, bg=color_gray)
    log_frame.pack(side="right", fill="y", padx=10)

    tk.Label(log_frame, text="Move Log",
             font=("Consolas", 14),
             bg=color_gray, fg="white").pack()

    log_text = tk.Text(log_frame, width=25, height=30,
                       font=("Consolas", 10),
                       bg="#222", fg="white",
                       state="disabled")
    log_text.pack()

    # Nút Quay lại Menu 
    tk.Button(frame, text="Back to Menu",
              font=("Consolas", 14),
              bg=color_light_gray, fg="white", 
              command=show_mode_selection).grid(row=game.n+1, column=0, columnspan=game.n//2, sticky="nsew")

    # Nút Restart 
    tk.Button(frame, text="Restart",
              font=("Consolas", 14),
              bg=color_light_gray, fg="white",
              command=game.new_game).grid(row=game.n+1, column=game.n//2, columnspan=game.n - (game.n//2), sticky="nsew")


    for i in range(game.n):
        frame.grid_rowconfigure(i+1, weight=1)
        frame.grid_columnconfigure(i, weight=1)