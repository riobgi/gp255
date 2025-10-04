import tkinter as tk
from tkinter import messagebox
import random


class Minesweeper:
    def __init__(self, root, rows=8, cols=8, mines=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.buttons = {}
        self.mine_positions = set()
        self.numbers = {}
        self.game_over = False
        self.first_click = True

        self.setup_ui()
        # self.default_placer()
        self.calculate_numbers()
        

    def setup_ui(self):
        self.root.title("Minesweeper")
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1)
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn
                
                btn.bind("<Button-1>", lambda event, r=r, c=c: self.left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.right_click(r, c))
    
    # this function will be used to ensure that the first click is always safe
    def safe_first_click(self, safe_r, safe_c):
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        
        # creates 3 x 3 safe area
        safe_zone = [(r, c)
                     #range(inclusive, exclusive)
            for r in range(safe_r - 1, safe_r + 2)
            for c in range(safe_c - 1, safe_c + 2)
            # check to make sure it stays within the board
            if 0 <= r < self.rows and 0 <= c < self.cols]
        # available positions includes all positions that are not in the safe zone
        available_positions = [pos for pos in all_positions if pos not in safe_zone]
        
        # set the mine positions
        self.mine_positions = set(random.sample(available_positions, self.mines))
        # recalculate the numbers
        self.calculate_numbers()
        
        
    # 🚩 use this emoji to place a flag later on
    def default_placer(self):
        # make a list of possible locations
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        # take a random sample of the locations to be mines
        self.mine_positions = set(random.sample(all_positions, self.mines))

    def calculate_numbers(self):
        # Calculate adjacent mine counts for each cell
        self.numbers = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mine_positions:
                    self.numbers[(r, c)] = -1
                else:
                    count = 0
                    for nr in range(r - 1, r + 2):
                        for nc in range(c - 1, c + 2):
                            if (nr, nc) in self.mine_positions:
                                count += 1
                    self.numbers[(r, c)] = count

    def left_click(self, r, c):
        if self.game_over or self.buttons[(r, c)]['state'] == tk.DISABLED:
            return
        
        # the following code bit is to ensure that the first spot you click is safe
        if self.first_click:
            self.safe_first_click(r, c)
            self.first_click = False

        btn = self.buttons[(r, c)]
        if (r, c) in self.mine_positions:
            btn.config(text="💥", bg="red")
            self.end_game(False)
        else:
            self.reveal_cell(r, c)
            # TODO: Haven't implemented win check
    
    def right_click(self, r, c):
        btn = self.buttons[(r,c)]
        # do nothing if the button is disabled (has been revealed)
        if btn['state'] == tk.DISABLED:
            return
        
        current_text = btn.cget("text")
        if current_text == "🚩":
            btn.config(text="")
        else:
            btn.config(text="🚩")

    def reveal_cell(self, r, c):
        btn = self.buttons[(r, c)]
        if btn['state'] == tk.DISABLED:
            return
        btn.config(state=tk.DISABLED)
        number = self.numbers[(r, c)]
        if number == 0:
            btn.config(text="", bg="green")
            self.reveal_neighbors(r, c)
        else:
            btn.config(text=str(number), bg="orange")

    def reveal_neighbors(self, r, c):
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self.reveal_cell(nr, nc)

    def end_game(self, won):
        self.game_over = True
        if won:
            messagebox.showinfo("Game Over", "You win!")
        else:
            messagebox.showerror("Game Over", "You clicked on a mine!")
        # Disable all buttons so game is ended
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()

    # TODO: We may show players the remaining mines count as game info to make the game easier

    # TODO: We may want to give the option to restart the game

    # TODO: Write Project Summary
