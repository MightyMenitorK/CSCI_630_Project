import tkinter as tk

class Cord:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Cell:
    def __init__(self, left:'Cell', right:'Cell', up:'Cell', down:'Cell'):
        self.val = "E"
        self._left = left
        self._right = right
        self._up = up
        self._down = down

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_up(self):
        return self._up

    def get_down(self):
        return self._down   
    
    def set_left(self, cell:'Cell'):
        self._left = cell

    def set_right(self, cell:'Cell'):
        self._right = cell

    def set_up(self, cell:'Cell'):
        self._up = cell

    def set_down(self, cell:'Cell'):
        self._down = cell

    def __str__(self):
        return self.val

class Maze:

    def point(self, row, col):
        return self.grid[row][col] if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]) else None

    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.grid = []

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
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()
        top = tk.Button(frame, text="T", command=lambda: self.toggle_barrier()).grid()
        bottom = tk.Button(frame, text="B", command=lambda: self.toggle_barrier()).grid()
        left = tk.Button(frame, text="L", command=lambda: self.toggle_barrier()).grid()
        right = tk.Button(frame, text="R", command=lambda: self.toggle_barrier()).grid()
        cell = tk.Label(frame, text=str(self.grid[0][0]))

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

    def toggle_barrier(self, cord: Cord, direction: str):
        cell = self.point(cord.row, cord.col)
        if cell is not None:
            if direction == "up":
                cell.set_up(None)
                up_cell = self.point(cord.row - 1, cord.col)
                if up_cell is not None:
                    up_cell.set_down(None)
            elif direction == "down":
                cell.set_down(None)
                down_cell = self.point(cord.row + 1, cord.col)
                if down_cell is not None:
                    down_cell.set_up(None)
            elif direction == "left":
                cell.set_left(None)
                left_cell = self.point(cord.row, cord.col - 1)
                if left_cell is not None:
                    left_cell.set_right(None)
            elif direction == "right":
                cell.set_right(None)
                right_cell = self.point(cord.row, cord.col + 1)
                if right_cell is not None:
                    right_cell.set_left(None)
        elif cell is None:
            if direction == "up":
                cell.set_up(self.point(cord.row - 1, cord.col))
                up_cell = self.point(cord.row - 1, cord.col)
                if up_cell is not None:
                    up_cell.set_down(cell)
            elif direction == "down":
                cell.set_down(self.point(cord.row + 1, cord.col))
                down_cell = self.point(cord.row + 1, cord.col)
                if down_cell is not None:
                    down_cell.set_up(cell)
            elif direction == "left":
                cell.set_left(self.point(cord.row, cord.col - 1))
                left_cell = self.point(cord.row, cord.col - 1)
                if left_cell is not None:
                    left_cell.set_right(cell)
            elif direction == "right":
                cell.set_right(self.point(cord.row, cord.col + 1))
                right_cell = self.point(cord.row, cord.col + 1)
                if right_cell is not None:
                    right_cell.set_left(cell)

    def toggle_barrier(self, cord1: Cord, cord2: Cord):
        cell1 = self.point(cord1.row, cord1.col)
        cell2 = self.point(cord2.row, cord2.col)
        if cell1 is not None and cell2 is not None:
            if cord1.row == cord2.row and abs(cord1.col - cord2.col) == 1:
                if cord1.col < cord2.col:
                    cell1.set_right(None)
                    cell2.set_left(None)
                else:
                    cell1.set_left(None)
                    cell2.set_right(None)
            elif cord1.col == cord2.col and abs(cord1.row - cord2.row) == 1:
                if cord1.row < cord2.row:
                    cell1.set_down(None)
                    cell2.set_up(None)
                else:
                    cell1.set_up(None)
                    cell2.set_down(None)
    
    def reset(self):
        return
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Simulator")
    maze = Maze(root, 5, 5)
    maze.block_cell(Cord(0, 0), Cord(0, 1))
    maze.block_cell(Cord(1, 0), Cord(1, 1))
    maze.block_cell(Cord(1, 1), Cord(2, 1))
    maze.display()
    print(maze)
    root.mainloop()

