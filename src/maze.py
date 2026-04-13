import time
import tkinter as tk
from typing import Any
from cell import Cell, Cord
from algorithms.BreadthFirstSearch import bfs
from algorithms.DepthFirstSearch import dfs
from algorithms.UniformCostSearch import ucs


class Maze:

    def toggle_button(self, button: tk.Button, cord1: Cord, cord2: Cord) -> None:
        """
        Toggle the barrier between two neighboring cells and update the wall button text.

        This function is used when the user clicks one of the small wall buttons
        in the maze UI. It tries to add or remove a barrier between the two given
        cell positions. After that, it changes the button text to show the new state:
        "." for open path and "x" for blocked path.

        :param button: The wall button that was clicked in the UI.
        :param cord1: The coordinate of the first cell.
        :param cord2: The coordinate of the second neighboring cell.
        :return: None
        """
        result = self.toggle_barrier(cord1, cord2)
        if result == -1:
            print("cant toggle")
        button.config(text="." if result == 0 else "x")

    def point(self, row, col)->list|None|Any:
        """
        Return the cell object at the given row and column.

        This function safely checks whether the given position is inside the maze.
        If the position is valid, it returns the cell stored there.
        If the position is outside the maze, it returns None.

        :param row: Row index of the cell.
        :param col: Column index of the cell.
        :return: The Cell object at that position, or None if the position is invalid.
        """
        return self.grid[row][col] if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]) else None

    def __init__(self, root, rows, cols)->None:
        """
        Create a new maze and initialize all important variables.

        This constructor builds the maze grid, links each cell with its valid
        neighboring cells, stores the Tkinter root window, and sets the start
        and goal positions. It also prepares variables that will later store
        BFS and DFS results such as time, path, cost, and expanded nodes.

        :param root: The main Tkinter window.
        :param rows: Number of rows in the maze.
        :param cols: Number of columns in the maze.
        :return: None
        """
        self.root = root
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.view = {}
        self.bfs_time = None
        self.dfs_time = None
        self.ucs_time = None
        self.bfs_path = None
        self.dfs_path = None
        self.ucs_path = None
        self.bfs_cost = None
        self.dfs_cost = None
        self.ucs_cost = None
        
        self.bfs_path_length = None
        self.dfs_path_length = None
        self.ucs_path_length = None
        self.bfs_expanded_nodes = None
        self.dfs_expanded_nodes = None
        self.ucs_expanded_nodes = None
        self.bfs_expanded_count = None
        self.dfs_expanded_count = None
        self.ucs_expanded_count = None

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

    def __str__(self)-> str|None :
        """
        Return a text version of the maze.

        This function creates a simple string representation of the maze so that
        it can be printed in the terminal. It shows walls, open paths, and the
        values stored inside each cell such as S, G, E, or *.

        :return: A string version of the maze layout.
        """
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
    
    def display(self)->None:
        """
        Draw the maze and control buttons on the screen.

        This function creates the full maze UI using Tkinter buttons. It shows
        each cell, each wall, and colors important cells such as the start,
        goal, and path cells. It also creates the BFS and DFS buttons and
        the result label that displays algorithm outputs.

        :return: None
        """
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=20)

        center_frame = tk.Frame(main_frame)
        center_frame.pack(side=tk.LEFT, padx=20)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, padx=20)

        # LEFT SIDE -> BFS output
        self.bfs_label = tk.Label(
            left_frame,
            text="",
            justify="left",
            anchor="n",
            wraplength=250
        )
        self.bfs_label.pack()

        self.ucs_label = tk.Label(
            left_frame, 
            text="",
            justify="left",
            anchor="n",
            wraplength=250
        )
        self.ucs_label.pack()

        # CENTER -> buttons + maze
        controls = tk.Frame(center_frame)
        controls.pack(pady=10)

        bfs_btn = tk.Button(controls, text="Run BFS", command=self.run_bfs)
        bfs_btn.pack(side=tk.LEFT, padx=5)

        dfs_btn = tk.Button(controls, text="Run DFS", command=self.run_dfs)
        dfs_btn.pack(side=tk.LEFT, padx=5)

        ucs_btn = tk.Button(controls, text="Run UCS", command=self.run_ucs)
        ucs_btn.pack(side=tk.LEFT, padx=5)

        outer = tk.Frame(center_frame, bd=2, relief="solid")
        outer.pack(padx=10, pady=10)

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

                hori.config(
                    command=lambda b=hori, cord1=Cord(r, c), cord2=Cord(r, c - 1): self.toggle_button(b, cord1, cord2))
                vert.config(
                    command=lambda b=vert, cord1=Cord(r, c), cord2=Cord(r - 1, c): self.toggle_button(b, cord1, cord2))

                hori = tk.Button(maze, text="x" if self.grid[r][self.cols - 1].get_right() is None else ".")
                hori.grid(row=r * 2 + 1, column=self.cols * 2)

        for c in range(self.cols):
            (vert := tk.Button(maze, text="x" if self.grid[self.rows - 1][c].get_down() is None else ".")).grid(
                row=self.rows * 2, column=c * 2 + 1)

        # RIGHT SIDE -> DFS output
        self.dfs_label = tk.Label(
            right_frame,
            text="",
            justify="left",
            anchor="n",
            wraplength=250
        )
        self.dfs_label.pack()

        self.refresh_cells()
        self.update_result_label()

    def move_start(self, row, col)->None:
        """
        Move the start position to a new cell.

        This function changes the current start cell to the given position.
        The old start cell is reset back to a normal empty cell, and the new
        cell is marked as the start using the value "S".

        :param row: New row for the start position.
        :param col: New column for the start position.
        :return: None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[self.start.row][self.start.col].val = "E"
            self.start.row = row
            self.start.col = col
            self.grid[row][col].val = "S"

    def move_goal(self, row, col)->None:
        """
        Move the start position to a new cell.

        This function changes the current start cell to the given position.
        The old start cell is reset back to a normal empty cell, and the new
        cell is marked as the start using the value "S".

        :param row: New row for the start position.
        :param col: New column for the start position.
        :return: None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[self.goal.row][self.goal.col].val = "E"
            self.goal.row = row
            self.goal.col = col
            self.grid[row][col].val = "G"

    def toggle_barrier(self, cord1: Cord, cord2: Cord)-> int:
        """
        Add or remove a barrier between two neighboring cells.

        This function checks whether the two given coordinates are valid neighbors.
        If they are connected, it removes the connection and creates a barrier.
        If they are blocked, it reconnects them and removes the barrier.

        It works for both horizontal and vertical neighboring cells.

        :param cord1: Coordinate of the first cell.
        :param cord2: Coordinate of the second neighboring cell.
        :return:
            -1 if the cells are invalid or not neighbors
             0 if a barrier was removed and path was opened
             1 if a barrier was added and path was blocked
        """
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
    
    def reset(self)->None:
        """
        Reset all search-related results in the maze.

        This function clears any highlighted search path from the maze and
        removes all stored BFS and DFS outputs such as time, path, cost,
        path length, expanded nodes, and expanded count. It then refreshes
        the result label on the screen.

        :return: None
        """
        self.clear_search_marks()
        self.bfs_time = None
        self.dfs_time = None
        self.ucs_time = None
        self.bfs_path = None
        self.dfs_path = None
        self.ucs_path = None
        self.bfs_cost = None
        self.dfs_cost = None
        self.ucs_cost = None
        self.bfs_path_length = None
        self.dfs_path_length = None
        self.ucs_path_length = None
        self.bfs_expanded_nodes = None
        self.dfs_expanded_nodes = None
        self.ucs_expanded_nodes = None
        self.bfs_expanded_count = None
        self.dfs_expanded_count = None
        self.ucs_expanded_count = None
        self.update_result_label()

    def refresh_cells(self)->None:
        """
        Update the maze cell buttons on the screen.

        This function refreshes the text and background color of every cell
        button based on the current cell value. For example, it shows start
        as green, goal as red, path as yellow, and normal cells as white.

        :return: None
        """
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

    def clear_search_marks(self) -> None:
        """
        Remove old BFS or DFS path markings from the maze.

        This function resets all cells back to their normal values before
        running a new search. It keeps the start cell marked as "S" and the
        goal cell marked as "G", while all other cells are reset to "E".

        :return: None
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if r == self.start.row and c == self.start.col:
                    self.grid[r][c].val = "S"
                elif r == self.goal.row and c == self.goal.col:
                    self.grid[r][c].val = "G"
                else:
                    self.grid[r][c].val = "E"
        self.refresh_cells()

    def get_neighbors(self, row, col)->list:
        """
        Return all valid neighboring cells that can be reached from a given cell.

        This function is used by BFS and DFS. It checks the current cell and
        looks in all four directions: up, down, left, and right. If movement
        is possible in a direction, that neighboring cell is added to the list.

        :param row: Row of the current cell.
        :param col: Column of the current cell.
        :return: A list of reachable neighboring coordinates as (row, col) tuples.
        """
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

    def update_result_label(self) -> None:
        """
        Run Breadth-First Search on the current maze.

        This function clears old search markings, starts the BFS algorithm,
        measures the execution time, stores all BFS results, highlights the
        final BFS path on the maze, prints the results in the terminal, and
        updates the result label in the UI.

        BFS is expected to find the shortest path in terms of number of steps
        when all moves have equal cost.

        :return: None
        """

        bfs_text = ""
        dfs_text = ""
        ucs_text = ""

        if self.bfs_time is None:
            bfs_text += "BFS Time: Not run yet\n"
        else:
            bfs_text += f"BFS Time: {self.bfs_time:.6f} s\n"

        if self.bfs_path is None:
            bfs_text += "BFS Path: Not run yet\n"
        else:
            bfs_text += f"BFS Path: {self.bfs_path}\n"

        if self.bfs_cost is None:
            bfs_text += "BFS Cost: Not run yet\n"
        else:
            bfs_text += f"BFS Cost: {self.bfs_cost}\n"

        if self.bfs_path_length is None:
            bfs_text += "BFS Path Length: Not run yet\n"
        else:
            bfs_text += f"BFS Path Length: {self.bfs_path_length}\n"

        if self.bfs_expanded_nodes is None:
            bfs_text += "BFS Expanded Nodes: Not run yet\n"
        else:
            bfs_text += f"BFS Expanded Nodes: {self.bfs_expanded_nodes}\n"

        if self.bfs_expanded_count is None:
            bfs_text += "BFS Expanded Count: Not run yet\n"
        else:
            bfs_text += f"BFS Expanded Count: {self.bfs_expanded_count}\n"

        if self.dfs_time is None:
            dfs_text += "DFS Time: Not run yet\n"
        else:
            dfs_text += f"DFS Time: {self.dfs_time:.6f} s\n"

        if self.dfs_path is None:
            dfs_text += "DFS Path: Not run yet\n"
        else:
            dfs_text += f"DFS Path: {self.dfs_path}\n"

        if self.dfs_cost is None:
            dfs_text += "DFS Cost: Not run yet\n"
        else:
            dfs_text += f"DFS Cost: {self.dfs_cost}\n"

        if self.dfs_path_length is None:
            dfs_text += "DFS Path Length: Not run yet\n"
        else:
            dfs_text += f"DFS Path Length: {self.dfs_path_length}\n"

        if self.dfs_expanded_nodes is None:
            dfs_text += "DFS Expanded Nodes: Not run yet\n"
        else:
            dfs_text += f"DFS Expanded Nodes: {self.dfs_expanded_nodes}\n"

        if self.dfs_expanded_count is None:
            dfs_text += "DFS Expanded Count: Not run yet\n"
        else:
            dfs_text += f"DFS Expanded Count: {self.dfs_expanded_count}\n"
        
        if self.ucs_time is None:   
            ucs_text += "UCS Time: Not run yet\n"
        else:
            ucs_text += f"UCS Time: {self.ucs_time:.6f} s\n"

        if self.ucs_path is None:
            ucs_text += "UCS Path: Not run yet\n"
        else:
            ucs_text += f"UCS Path: {self.ucs_path}\n"

        if self.ucs_cost is None:
            ucs_text += "UCS Cost: Not run yet\n"
        else:
            ucs_text += f"UCS Cost: {self.ucs_cost}\n"

        if self.ucs_path_length is None:
            ucs_text += "UCS Path Length: Not run yet\n"
        else:
            ucs_text += f"UCS Path Length: {self.ucs_path_length}\n"

        if self.ucs_expanded_nodes is None:
            ucs_text += "UCS Expanded Nodes: Not run yet\n"
        else:
            ucs_text += f"UCS Expanded Nodes: {self.ucs_expanded_nodes}\n"

        if self.ucs_expanded_count is None:
            ucs_text += "UCS Expanded Count: Not run yet\n"
        else:
            ucs_text += f"UCS Expanded Count: {self.ucs_expanded_count}\n"

        self.bfs_label.config(text=bfs_text)
        self.dfs_label.config(text=dfs_text)
        self.ucs_label.config(text=ucs_text)


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

    def run_dfs(self)-> None:
        """
        Run Depth-First Search on the current maze.

        This function clears old search markings, starts the DFS algorithm,
        measures the execution time, stores all DFS results, highlights the
        final DFS path on the maze, prints the results in the terminal, and
        updates the result label in the UI.

        DFS explores deeply along one path before backtracking, so the final
        path is not always the shortest one.

        :return: None
        """
        print("DFS button clicked")
        self.clear_search_marks()

        start_time = time.perf_counter()

        start = (self.start.row, self.start.col)
        goal = (self.goal.row, self.goal.col)
        dfs_result = dfs(start, goal, self.get_neighbors)

        end_time = time.perf_counter()
        elapsed = end_time - start_time
        self.dfs_time = elapsed

        if dfs_result:
            path, cost, path_length, expanded_nodes, expanded_count = dfs_result

            self.dfs_path = path
            self.dfs_cost = cost
            self.dfs_path_length = path_length
            self.dfs_expanded_nodes = expanded_nodes
            self.dfs_expanded_count = expanded_count

            start = (self.start.row, self.start.col)
            goal = (self.goal.row, self.goal.col)

            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    self.grid[r][c].val = "*"

            self.grid[self.start.row][self.start.col].val = "S"
            self.grid[self.goal.row][self.goal.col].val = "G"
            self.refresh_cells()

            print("DFS Path:", path)
            print("DFS Cost:", cost)
            print("DFS Path Length:", path_length)
            print("DFS Expanded Nodes:", expanded_nodes)
            print("DFS Expanded Count:", expanded_count)
        else:
            self.dfs_path = None
            self.dfs_cost = None
            self.dfs_path_length = None
            self.dfs_expanded_nodes = None
            self.dfs_expanded_count = None
            print("No DFS path found")

        print(f"DFS Time: {elapsed:.6f} seconds")
        print("------------------------")

        self.update_result_label()

    def run_ucs(self):
        """
        Run Uniform Cost Search on the current maze.

        This function clears old search markings, starts the UCS algorithm,
        measures the execution time, stores all UCS results, highlights the
        final UCS path on the maze, prints the results in the terminal, and
        updates the result label in the UI.

        :return: None
        """
        print("UCS button clicked")
        self.clear_search_marks()

        start_time = time.perf_counter()
        start = (self.start.row, self.start.col)
        goal = (self.goal.row, self.goal.col)
        
        result = ucs(start, goal, self.get_neighbors)
        
        self.ucs_time = time.perf_counter() - start_time

        if result:
            path, cost, path_length, expanded_nodes, expanded_count = result
            self.ucs_path = path
            self.ucs_cost = cost
            self.ucs_path_length = path_length
            self.ucs_expanded_nodes = expanded_nodes
            self.ucs_expanded_count = expanded_count

            # Highlight path
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    self.grid[r][c].val = "*"
            
            self.refresh_cells()
        
        self.update_result_label()