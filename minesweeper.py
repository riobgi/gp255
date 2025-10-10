import tkinter as tk
from tkinter import messagebox
import random


class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=15):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.mine_positions = set()
        self.numbers = {}
        self.flags = set()
        self.revealed = set()
        self.game_over = False
        self.first_click = True
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Minesweeper")
        
        self.info_label = tk.Label(self.root, text=f"Mines: {self.mines}; Revealed: {len(self.revealed)}", font=("Arial", 12, "bold"))
        self.info_label.grid(row=0, column=0, columnspan=self.cols, pady=5)
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1, font=("Arial", 10, "bold"))
                btn.grid(row=r+1, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn
                
                btn.bind("<Button-1>", lambda event, r=r, c=c: self.left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.right_click(r, c))
                
        restart_btn = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Arial", 10))
        restart_btn.grid(row=self.rows+1, column=0, columnspan=self.cols, sticky="we", pady=5)
    
    def update_info_label(self):
        remaining = self.mines - len(self.flags)
        self.info_label.config(text=f"Mines: {remaining}; Revealed: {len(self.revealed)}")

    def safe_first_click(self, safe_r, safe_c):
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        
        safe_zone = [
            (r, c)
            for r in range(safe_r - 1, safe_r + 2)
            for c in range(safe_c - 1, safe_c + 2)
            if 0 <= r < self.rows and 0 <= c < self.cols
        ]
        
        available_positions = [pos for pos in all_positions if pos not in safe_zone]
        
        self.mine_positions = set(random.sample(available_positions, self.mines))
        self.calculate_numbers()

    def calculate_numbers(self):
        self.numbers = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mine_positions:
                    self.numbers[(r, c)] = -1
                else:
                    count = sum(
                        1 for nr in range(r - 1, r + 2)
                        for nc in range(c - 1, c + 2)
                        if (nr, nc) in self.mine_positions
                    )
                    self.numbers[(r, c)] = count

    def left_click(self, r, c):
        if self.game_over or self.buttons[(r, c)]['state'] == tk.DISABLED:
            return
        
        if (r, c) in self.flags:
            return
        
        if self.first_click:
            self.safe_first_click(r, c)
            self.first_click = False

        btn = self.buttons[(r, c)]
        if (r, c) in self.mine_positions:
            btn.config(text="💥", bg="red")
            self.end_game(False)
        else:
            self.reveal_cell(r, c)
            self.check_win()

        self.update_info_label()
    
    def right_click(self, r, c):
        if self.game_over:
            return
            
        btn = self.buttons[(r, c)]
        
        if btn['state'] == tk.DISABLED:
            return
        
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            self.flags.add((r, c))
            btn.config(text="🚩")
        
        self.update_info_label()

    def reveal_cell(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
            
        btn = self.buttons[(r, c)]
        
        if btn['state'] == tk.DISABLED or (r, c) in self.flags:
            return
        
        btn.config(state=tk.DISABLED)
        self.revealed.add((r, c))
        
        number = self.numbers[(r, c)]
        if number == 0:
            btn.config(text="", bg="lightgray")
            self.reveal_neighbors(r, c)
        else:
            colors = {
                1: "blue", 2: "green", 3: "red", 4: "darkblue",
                5: "darkred", 6: "cyan", 7: "black", 8: "gray"
            }
            btn.config(text=str(number), fg=colors.get(number, "black"), bg="lightgray")

    def reveal_neighbors(self, r, c):
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if (nr, nc) != (r, c):
                    self.reveal_cell(nr, nc)

    def check_win(self):
        total_cells = self.rows * self.cols
        if len(self.revealed) == total_cells - self.mines:
            self.end_game(True)

    def end_game(self, won):
        self.game_over = True
        
        if not won:
            for pos in self.mine_positions:
                btn = self.buttons[pos]
                if pos not in self.flags:
                    btn.config(text="💣", bg="red")
        
        if won:
            messagebox.showinfo("Congratulations!", "You win! 🎉")
        else:
            messagebox.showerror("Game Over", "You hit a mine! 💥")
        
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)

    def restart_game(self):
        self.game_over = False
        self.first_click = True
        self.mine_positions = set()
        self.flags = set()
        self.revealed = set()
        self.numbers = {}
        
        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL, text="", bg="SystemButtonFace", fg="black")
        
        self.update_info_label()


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
