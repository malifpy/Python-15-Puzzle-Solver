import tkinter as tk
import time
import PuzzleSolver as PS

class PuzzleGUI:
    def __init__(self, master, layout=[str(i) for i in range(1,17)]):

        self.canvas = tk.Canvas(
                master,
                width=400,
                height=400
            )

        self.rect_size = 100
        
        self.load_layout(layout)

        self.canvas.pack(side="left")

        self.is_moving = False

    def load_layout(self, layout):
        # Ngebikin tiap bagian puzzle
        self.canvas.delete("all")
        self.tiles = layout
        for idx, tile in enumerate(layout):
            if(tile != "16"):
                tp = (idx //  4) * self.rect_size
                lt = (idx %  4) * self.rect_size
                self.canvas.create_rectangle(
                        lt, 
                        tp, 
                        lt + self.rect_size, 
                        tp + self.rect_size, 
                        fill="white",
                        tags="tile" + tile
                    )

                self.canvas.create_text(
                        lt + self.rect_size // 2,
                        tp + self.rect_size // 2,
                        text= tile,
                        font = ("Arial", 22),
                        tags="tile" + tile
                    )

                self.canvas.create_text(
                        lt + self.rect_size // 8,
                        tp + self.rect_size // 8,
                        text= 0,
                        font = ("Arial", 11),
                        tags=("tile" + tile, "kurangTile" + tile)
                    )
            else:
                self.xIdx = idx

        self.refreshKurang()

    def refreshKurang(self):
        # Hitung ulang nilai KURANG di display
        for tile in self.tiles:
            if tile != '16':
                self.canvas.itemconfigure(
                    self.canvas.find_withtag("kurangTile" + tile)[0],
                    text = self.KURANG(tile)
                )

    def solve(self):
        ps = PS.PuzzleSolver()
        sSteps, t, found, nAwakened = ps.solve(self.tiles)
        if not found:
            raise Exception("Time Limit Reached")
        self.arr_move(sSteps)

        return t, nAwakened

    def str_move(self, move):
        if (move == "Up"):
            self.up()
        elif (move ==  "Down"):
            self.down()
        elif (move == "Right"):
            self.right()
        elif (move == "Left"):
            self.left()

    def arr_move(self, arr):
        for el in arr:
            self.str_move(el)

    def moveRec(self, tag, x, y):
        # Bergerak sedikit-sedikit supaya terlihat seperti animasi
        newX = x
        if (x > 0):
            self.canvas.move(tag, 5, 0)
            newX -= 5
        elif (x < 0):
            self.canvas.move(tag, -5, 0)
            newX += 5

        newY = y
        if (y > 0):
            self.canvas.move(tag, 0, 5)
            newY -= 5
        elif (y < 0):
            self.canvas.move(tag, 0, -5)
            newY += 5

        if(x != 0 or y != 0):
            self.canvas.update()
            self.canvas.after(10)
            self.moveRec(tag, newX, newY)

    def move(self, tag, x, y):
        self.moveRec(tag, x, y)
        self.refreshKurang()

    def swap(self, idx):
        # Tukar Tile
        tmp = self.tiles[idx]
        self.tiles[idx] = "16"
        self.tiles[self.xIdx] = tmp
        self.xIdx = idx

        return tmp

    def down(self):
        # Yang kosong ke Bawah
        if(not self.is_moving and self.xIdx // 4 != 3):
            print("Down")
            self.is_moving = True
            nLoc = self.xIdx + 4
            nTag = self.swap(nLoc)
            self.move("tile" + nTag, 0, -self.rect_size)
            print(self.tiles)
            self.is_moving = False

    def up(self):
        if(not self.is_moving and self.xIdx // 4 != 0):
            print("Up")
            self.is_moving = True
            nLoc = self.xIdx - 4
            nTag = self.swap(nLoc)
            self.move("tile" + nTag, 0, self.rect_size)
            print(self.tiles)
            self.is_moving = False

    def right(self):
        if(not self.is_moving and self.xIdx % 4 != 3):
            print("Right")
            self.is_moving = True
            nLoc = self.xIdx + 1
            nTag = self.swap(nLoc)
            self.move("tile" + nTag, -self.rect_size, 0)
            print(self.tiles)
            self.is_moving = False

    def left(self):
        if(not self.is_moving and self.xIdx % 4 != 0):
            print("Left")
            self.is_moving = True
            nLoc = self.xIdx - 1
            nTag = self.swap(nLoc)
            self.move("tile" + nTag, self.rect_size, 0)
            print(self.tiles)
            self.is_moving = False
    
    def KURANG(self, tile):
        res = int(tile) - 1
        idx = 0
        while(self.tiles[idx] != tile):
            if(int(tile) > int(self.tiles[idx])):
                res -= 1
            idx += 1
        return res

    def ALL_KURANG(self):
        res = 0
        for i in range(1, 17):
            res += self.KURANG(str(i))
        return res

    def X_val(self):
        row = (self.xIdx % 4) % 2 == 0
        col = (self.xIdx // 4) % 2 == 0

        return row ^ col

    def reachable(self):
        return (self.ALL_KURANG() + self.X_val()) % 2 == 0
