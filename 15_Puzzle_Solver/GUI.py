import tkinter as tk
from tkinter import filedialog as fd
import random as rd
import PuzzleGUI as PGUI
import Parser

class GUI:
    def __init__(self, interactive=True):
        self.window = tk.Tk()
        self.window.title("15 Puzzle")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        self.puzzle = PGUI.PuzzleGUI(self.window)

        openButton = tk.Button(
                self.window,
                text = "Open File",
                command = (self.from_file)
            )

        openButton.place(x = 450, y = 25, width = 100)

        solveButton = tk.Button(
                self.window,
                text = "Solve",
                command = (self.solve)
            )

        solveButton.place(x = 450, y = 60, width = 100)

        resetButton = tk.Button(
                self.window,
                text = "Reset",
                command = (self.reset)
            )

        resetButton.place(x = 450, y = 95, width = 100)

        if(interactive):
            self.bind_key()

    def solve(self):
        if self.puzzle.reachable():
            try:
                self.puzzle.solve()
            except Exception as err:
                tk.messagebox.showinfo("Information", err)

        else:
            tk.messagebox.showinfo("Information", "Puzzle cannot be Solved!")

    def from_file(self):
        filename = fd.askopenfilename()
        try:
            l = Parser.Parser.parse(filename)
            self.load_layout(l)
        except Exception as err:
            tk.messagebox.showinfo("Information", err)

    def reset(self):
        self.load_layout([str(i) for i in range(1, 17)])

    def show(self):
        self.window.mainloop()

    def random_layout(self):
        normal = [str(i) for i in range(1, 17)]
        rd.shuffle(normal)
        self.load_layout(normal)
    
    def load_layout(self, layout):
        self.puzzle.load_layout(layout)

    def bind_key(self):
        # Key Gerak
        self.window.bind("<KeyPress-Left>", lambda _: self.puzzle.left())
        self.window.bind("<KeyPress-Right>", lambda _: self.puzzle.right())
        self.window.bind("<KeyPress-Up>", lambda _: self.puzzle.up())
        self.window.bind("<KeyPress-Down>", lambda _: self.puzzle.down())

        # Key Random Reset
        self.window.bind("<space>", lambda _: self.random_layout())

if __name__ == "__main__":
    G = GUI()
    G.show()

