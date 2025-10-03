import tkinter as tk
from tkinter import messagebox


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

        self.setup_ui()
        self.default_placer()
        self.calculate_numbers()

    def setup_ui(self):
        self.root.title("Minesweeper")
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1,
                                command=lambda r=r, c=c: self.click_cell(r, c)
                                )
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # TODO: We need a random or strategic placer, currently placed mines top-left, row by row
    def default_placer(self):
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if count < self.mines:
                    self.mine_positions.add((r, c))  # change here to randomly place mine
                    count += 1
                else:
                    return

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

    def click_cell(self, r, c):
        if self.game_over or self.buttons[(r, c)]['state'] == tk.DISABLED:
            return

        btn = self.buttons[(r, c)]
        if (r, c) in self.mine_positions:
            btn.config(text="💥", bg="red")
            self.end_game(False)
        else:
            self.reveal_cell(r, c)
            # TODO: Haven't implemented win check

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
