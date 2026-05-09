from ui.ui import window, show_mode_selection

# ==============================
# START APP
# ==============================
window.title("Caro (Gomoku)")
window.resizable(False, False)

show_mode_selection()

window.geometry("800x700")
window.mainloop()