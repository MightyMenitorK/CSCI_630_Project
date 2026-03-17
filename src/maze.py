import time
import tkinter as tk
from cell import Cell, Cord
from algorithms.BreadthFirstSearch import bfs

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
        self.bfs_time = None
        self.dfs_time = None
        self.bfs_path = None
        self.dfs_path = None

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
        self.grid[self.start.row][self.start.col].val = "S"
        self.grid[self.goal.row][self.goal.col].val = "G"

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
        outer = tk.Frame(self.root, bd=2, relief="solid")
        outer.pack(padx=50, pady=50)

        maze = tk.Frame(outer)
        maze.pack()
        self.view["cell"] = []
        for r in range(self.rows):
            self.view["cell"].append([])
            for c in range(self.cols):
                (vert := tk.Button(maze, text=("x" if self.grid[r][c].get_up() is None else "."))).grid(row=r*2, column=c*2+1)
                (hori := tk.Button(maze, text=("x" if self.grid[r][c].get_left() is None else "."))).grid(row=r*2+1, column=c*2)
                (cell := tk.Button(maze, text=self.grid[r][c].val)).grid(row=r*2+1, column=c*2+1)
                self.view["cell"][r].append(cell)

                if self.grid[r][c].val == "S":
                    cell.config(bg="lightgreen")
                elif self.grid[r][c].val == "G":
                    cell.config(bg="lightcoral")
                else:
                    cell.config(bg="white")

                hori.config(command=lambda b=hori, cord1=Cord(r, c), cord2=Cord(r, c-1): self.toggle_button(b, cord1, cord2))
                vert.config(command=lambda b=vert, cord1=Cord(r, c), cord2=Cord(r-1, c): self.toggle_button(b, cord1, cord2))
            hori = tk.Button(maze, text="x" if self.grid[r][self.cols-1].get_right() is None else ".")
            hori.grid(row=r*2+1, column=self.cols*2)
        for c in range(self.cols):
            (vert := tk.Button(maze, text="x" if self.grid[self.rows-1][c].get_down() is None else ".")).grid(row=self.rows*2, column=c*2+1)

        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        bfs_btn = tk.Button(controls, text="Run BFS", command=self.run_bfs)
        bfs_btn.pack(side=tk.LEFT, padx=5)

        dfs_btn = tk.Button(controls, text="Run DFS")
        dfs_btn.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.root, text="", justify="left", anchor="w")
        self.result_label.pack(pady=10)
        self.update_result_label()

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
        self.clear_search_marks()
        self.bfs_time = None
        self.dfs_time = None
        self.bfs_path = None
        self.dfs_path = None
        self.update_result_label()

    def refresh_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c].val
                btn = self.view["cell"][r][c]

                btn.config(text=value)

                if value == "S":
                    btn.config(bg="lightgreen")
                elif value == "G":
                    btn.config(bg="lightcoral")
                elif value == "*":
                    btn.config(bg="yellow")
                else:
                    btn.config(bg="white")

    def clear_search_marks(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if r == self.start.row and c == self.start.col:
                    self.grid[r][c].val = "S"
                elif r == self.goal.row and c == self.goal.col:
                    self.grid[r][c].val = "G"
                else:
                    self.grid[r][c].val = "E"
        self.refresh_cells()

    def get_neighbors(self, row, col):
        neighbors = []
        cell = self.grid[row][col]

        if cell.get_up() is not None:
            neighbors.append((row - 1, col))

        if cell.get_down() is not None:
            neighbors.append((row + 1, col))

        if cell.get_left() is not None:
            neighbors.append((row, col - 1))

        if cell.get_right() is not None:
            neighbors.append((row, col + 1))

        return neighbors

    def update_result_label(self):
        bfs_time_text = "Not run yet" if self.bfs_time is None else f"{self.bfs_time:.6f} s"
        dfs_time_text = "Not run yet" if self.dfs_time is None else f"{self.dfs_time:.6f} s"

        bfs_path_text = "Not run yet" if self.bfs_path is None else str(self.bfs_path)
        dfs_path_text = "Not run yet" if self.dfs_path is None else str(self.dfs_path)

        text = (
            f"BFS Time: {bfs_time_text}\n"
            f"BFS Path: {bfs_path_text}\n\n"
            f"DFS Time: {dfs_time_text}\n"
            f"DFS Path: {dfs_path_text}"
        )

        self.result_label.config(text=text, justify="left")


    def run_bfs(self):
        print("BFS button clicked")
        self.clear_search_marks()

        start_time = time.perf_counter()

        start = (self.start.row, self.start.col)
        goal = (self.goal.row, self.goal.col)
        bfs_result = bfs(start, goal, self.get_neighbors)

        end_time = time.perf_counter()
        elapsed = end_time - start_time
        self.bfs_time = elapsed

        if bfs_result:
            path, cost = bfs_result
            self.bfs_path = path

            start = (self.start.row, self.start.col)
            goal = (self.goal.row, self.goal.col)

            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    self.grid[r][c].val = "*"

            self.grid[self.start.row][self.start.col].val = "S"
            self.grid[self.goal.row][self.goal.col].val = "G"
            self.refresh_cells()

            print("BFS Path:", path)
            print("BFS Total Cost:", cost)
        else:
            self.bfs_path = None
            print("No BFS path found")

        print(f"BFS Time: {elapsed:.6f} seconds")
        print("------------------------")

        self.update_result_label()

    def run_bfs(self):
        print("BFS button clicked")
        self.clear_search_marks()

        start_time = time.perf_counter()

        start = (self.start.row, self.start.col)
        goal = (self.goal.row, self.goal.col)
        bfs_result = bfs(start, goal, self.get_neighbors)

        end_time = time.perf_counter()
        elapsed = end_time - start_time
        self.bfs_time = elapsed

        if bfs_result:
            path, cost = bfs_result
            self.bfs_path = path

            start = (self.start.row, self.start.col)
            goal = (self.goal.row, self.goal.col)

            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    self.grid[r][c].val = "*"

            self.grid[self.start.row][self.start.col].val = "S"
            self.grid[self.goal.row][self.goal.col].val = "G"
            self.refresh_cells()

            print("BFS Path:", path)
            print("BFS Total Cost:", cost)
        else:
            self.bfs_path = None
            print("No BFS path found")

        print(f"BFS Time: {elapsed:.6f} seconds")
        print("------------------------")

        self.update_result_label()