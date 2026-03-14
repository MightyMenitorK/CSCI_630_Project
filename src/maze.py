import tkinter as tk
from cell import Cell, Cord

class Maze:

    def toggle_button(self, button: tk.Button, cord1: Cord, cord2: Cord):
        result = self.toggle_barrier(cord1, cord2)
        if result == -1:
            print("cant toggle")
        button.config(text="." if result == 0 else "x")

    def point(self, row, col):
        return self.grid[row][col] if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]) else None

    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.view = {}

        for r in range(rows):
            self.grid.append([])
            for c in range(cols):
                left = self.point(r, c-1)
                up = self.point(r-1, c)
                #print(f"creating cell at ({r}, {c}) with left={left} and up={up}")
                self.grid[r].append(Cell(left, None, up, None))
                if left is not None:
                    #print(f"linking ({r}, {c-1}) right to ({r}, {c})")
                    left.set_right(self.grid[r][c])
                if up is not None:
                    #print(f"linking ({r-1}, {c}) down to ({r}, {c})")
                    up.set_down(self.grid[r][c])

        self.start = Cord(0, 0)
        self.goal = Cord(rows-1, cols-1)

    def __str__(self):
        result = ""
        for r in range(len(self.grid)):
            result += "  "  
            for c in range(len(self.grid[r])):
                result +=  ("-" if self.grid[r][c].get_up() is None else ".") + "    "
            result += "\n"
            for c in range(len(self.grid[r])):
                result +=  ("| " if self.grid[r][c].get_left() is None else ". ") + self.grid[r][c].val + (" |" if self.grid[r][c].get_right() is None else " .")
            result += "\n  "
            for c in range(len(self.grid[r])):
                result += ("-" if self.grid[r][c].get_down() is None else ".") + "    "
            result += "\n"
        return result
    
    def display(self):
        maze = tk.Frame(self.root)
        maze.pack()
        self.view["cell"] = []
        for r in range(self.rows):
            self.view["cell"].append([])
            for c in range(self.cols):
                (vert := tk.Button(maze, text=("x" if self.grid[r][c].get_up() is None else "."))).grid(row=r*2, column=c*2+1)
                (hori := tk.Button(maze, text=("x" if self.grid[r][c].get_left() is None else "."))).grid(row=r*2+1, column=c*2)
                (cell := tk.Button(maze, text=self.grid[r][c].val)).grid(row=r*2+1, column=c*2+1)
                hori.config(command=lambda b=hori, cord1=Cord(r, c), cord2=Cord(r, c-1): self.toggle_button(b, cord1, cord2))
                vert.config(command=lambda b=vert, cord1=Cord(r, c), cord2=Cord(r-1, c): self.toggle_button(b, cord1, cord2))
            hori = tk.Button(maze, text="x" if self.grid[r][self.cols-1].get_right() is None else ".")
            hori.grid(row=r*2+1, column=self.cols*2)
        for c in range(self.cols):
            (vert := tk.Button(maze, text="x" if self.grid[self.rows-1][c].get_down() is None else ".")).grid(row=self.rows*2, column=c*2+1)

    def move_start(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[self.start.row][self.start.col].val = "E"
            self.start.row = row
            self.start.col = col
            self.grid[row][col].val = "S"

    def move_goal(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[self.goal.row][self.goal.col].val = "E"
            self.goal.row = row
            self.goal.col = col
            self.grid[row][col].val = "G"

    def toggle_barrier(self, cord1: Cord, cord2: Cord):
        cell1 = self.point(cord1.row, cord1.col)
        cell2 = self.point(cord2.row, cord2.col)
        
        if cell1 is None or cell2 is None:
            return -1

        # Horizontal Toggle
        if cord1.row == cord2.row and abs(cord1.col - cord2.col) == 1:
            left_c, right_c = (cell1, cell2) if cord1.col < cord2.col else (cell2, cell1)
            if left_c.get_right() is None:
                left_c.set_right(right_c)
                right_c.set_left(left_c)
                return 0
            else:
                left_c.set_right(None)
                right_c.set_left(None)
                return 1

        # Vertical Toggle
        elif cord1.col == cord2.col and abs(cord1.row - cord2.row) == 1:
            up_c, down_c = (cell1, cell2) if cord1.row < cord2.row else (cell2, cell1)
            if up_c.get_down() is None:
                up_c.set_down(down_c)
                down_c.set_up(up_c)
                return 0
            else:
                up_c.set_down(None)
                down_c.set_up(None)
                return 1

        return -1
    
    def reset(self):
        return