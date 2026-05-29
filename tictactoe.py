import tkinter as tk
from tkinter import font
import random

WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.board = [None] * 9
        self.current = "X"
        self.game_over = False
        self.mode = tk.StringVar(value="pvp")
        self.scores = {"X": 0, "O": 0, "draw": 0}

        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        pad = dict(bg="#1a1a2e")

        title_font = font.Font(family="Segoe UI", size=22, weight="bold")
        label_font = font.Font(family="Segoe UI", size=11)
        status_font = font.Font(family="Segoe UI", size=13)
        cell_font  = font.Font(family="Segoe UI", size=36, weight="bold")
        btn_font   = font.Font(family="Segoe UI", size=10, weight="bold")
        score_font = font.Font(family="Segoe UI", size=22, weight="bold")

        tk.Label(self.root, text="Tic Tac Toe", font=title_font,
                 fg="#e94560", **pad).pack(pady=(20, 8))

        # Mode toggle
        mode_frame = tk.Frame(self.root, **pad)
        mode_frame.pack(pady=(0, 10))
        for text, val in [("2 Players", "pvp"), ("vs CPU", "cpu")]:
            tk.Radiobutton(
                mode_frame, text=text, variable=self.mode, value=val,
                command=self.reset_game, font=btn_font,
                bg="#16213e", fg="#aaaaaa", activebackground="#1e1e3f",
                activeforeground="#e94560", selectcolor="#1e1e3f",
                indicatoron=False, padx=12, pady=5,
                relief="flat", bd=2, cursor="hand2"
            ).pack(side="left", padx=4)

        # Scores
        score_frame = tk.Frame(self.root, **pad)
        score_frame.pack(pady=(0, 10))
        self.score_labels = {}
        for col, (label, key, color) in enumerate([
            ("X", "X", "#e94560"),
            ("Draw", "draw", "#f4a261"),
            ("O", "O", "#a8dadc"),
        ]):
            box = tk.Frame(score_frame, bg="#16213e", padx=18, pady=6)
            box.grid(row=0, column=col, padx=8)
            tk.Label(box, text=label, font=label_font,
                     fg="#aaaaaa", bg="#16213e").pack()
            lbl = tk.Label(box, text="0", font=score_font,
                           fg=color, bg="#16213e")
            lbl.pack()
            self.score_labels[key] = lbl

        # Status
        self.status_var = tk.StringVar(value="Player X's turn")
        tk.Label(self.root, textvariable=self.status_var, font=status_font,
                 fg="#a8dadc", **pad).pack(pady=(0, 10))

        # Board
        board_frame = tk.Frame(self.root, bg="#1a1a2e")
        board_frame.pack(padx=20)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame, text="", font=cell_font,
                width=3, height=1,
                bg="#16213e", fg="#ffffff", activebackground="#0f3460",
                relief="flat", bd=0, cursor="hand2",
                command=lambda i=i: self.handle_click(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5,
                     ipadx=10, ipady=10)
            self.buttons.append(btn)

        # Reset button
        tk.Button(
            self.root, text="New Game", font=btn_font,
            bg="#e94560", fg="white", activebackground="#c73652",
            activeforeground="white", relief="flat", padx=20, pady=8,
            cursor="hand2", command=self.reset_game
        ).pack(pady=16)

    def handle_click(self, i):
        if self.game_over or self.board[i]:
            return
        if self.mode.get() == "cpu" and self.current == "O":
            return
        self.place(i, self.current)
        if not self.game_over and self.mode.get() == "cpu" and self.current == "O":
            self.root.after(350, self.cpu_move)

    def place(self, i, player):
        self.board[i] = player
        color = "#e94560" if player == "X" else "#a8dadc"
        self.buttons[i].config(text=player, fg=color, state="disabled",
                               disabledforeground=color)

        win_combo = self.check_win(player)
        if win_combo:
            for idx in win_combo:
                self.buttons[idx].config(bg="#0f3460")
            self.status_var.set(f"Player {player} wins!")
            self.scores[player] += 1
            self.update_scores()
            self.game_over = True
        elif all(self.board):
            self.status_var.set("It's a draw!")
            self.scores["draw"] += 1
            self.update_scores()
            self.game_over = True
        else:
            self.current = "O" if self.current == "X" else "X"
            label = "CPU's turn" if self.mode.get() == "cpu" and self.current == "O" \
                    else f"Player {self.current}'s turn"
            self.status_var.set(label)

    def check_win(self, player):
        return next((c for c in WINS if all(self.board[i] == player for i in c)), None)

    def cpu_move(self):
        if self.game_over:
            return
        self.place(self.best_move(), "O")

    def best_move(self):
        # Win if possible
        for i in range(9):
            if not self.board[i]:
                self.board[i] = "O"
                if self.check_win("O"):
                    self.board[i] = None
                    return i
                self.board[i] = None
        # Block X
        for i in range(9):
            if not self.board[i]:
                self.board[i] = "X"
                if self.check_win("X"):
                    self.board[i] = None
                    return i
                self.board[i] = None
        # Center
        if not self.board[4]:
            return 4
        # Corners
        corners = [i for i in [0, 2, 6, 8] if not self.board[i]]
        if corners:
            return random.choice(corners)
        # Any open
        return random.choice([i for i in range(9) if not self.board[i]])

    def update_scores(self):
        for key, lbl in self.score_labels.items():
            lbl.config(text=str(self.scores[key]))

    def reset_game(self):
        self.board = [None] * 9
        self.current = "X"
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#16213e")
        self.status_var.set("Player X's turn")

if __name__ == "__main__":
    TicTacToe()
