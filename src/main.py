import random
import tkinter as tk
from maze import Maze
from cell import Cord
    
if __name__ == "__main__":

    row_input = input("Enter number of rows (press Enter for random, max 10): ")
    col_input = input("Enter number of cols (press Enter for random, max 10): ")

    if row_input.strip() == "":
        rows = random.randint(3, 10)
    else:
        rows = int(row_input)
        if rows > 10 or rows <= 0 :
            rows = 10

    if col_input.strip() == "":
        cols = random.randint(3,10)
    else:
        cols = int(col_input)
        if cols > 10 or cols <= 0 :
            cols = 10

    start_row_input = input(f"Enter start row (1 to {rows}, press Enter for random): ")
    start_col_input = input(f"Enter start col (1 to {cols}, press Enter for random): ")

    if start_row_input.strip() == "":
        start_row = random.randint(0, rows - 1)
    else:
        start_row = int(start_row_input)
        if start_row >= rows - 1 or start_row <= 1:
            start_row= 0

    if start_col_input.strip() == "":
        start_col = random.randint(0, cols - 1)
    else:
        start_col = int(start_col_input)
        if start_col >= cols - 1 or start_col <= 1:
            start_col = 0

    goal_row_input = input(f"Enter goal row (1 to {rows}, press Enter for random): ")
    goal_col_input = input(f"Enter goal col (1 to {cols}, press Enter for random): ")

    if goal_row_input.strip() == "":
        goal_row = random.randint(0, rows - 1)
    else:
        goal_row = int(goal_row_input)
        if goal_row >= rows - 1 or goal_row <= 1:
            goal_row = rows - 1

    if goal_col_input.strip() == "":
        goal_col = random.randint(0, cols - 1)
    else:
        goal_col = int(goal_col_input)
        if goal_col >= cols - 1 or goal_col <= 1:
            goal_col = cols - 1

    while start_row == goal_row and start_col == goal_col:
        goal_row = random.randint(0, rows - 1)
        goal_col = random.randint(0, cols - 1)

    root = tk.Tk()
    root.title("Maze Simulator")

    maze = Maze(root, rows, cols)

    maze.move_start(start_row, start_col)
    maze.move_goal(goal_row, goal_col)

    # maze = Maze(root, 5, 5)
    # maze.toggle_barrier(Cord(0, 0), Cord(0, 1))
    # maze.toggle_barrier(Cord(1, 0), Cord(1, 1))
    # maze.toggle_barrier(Cord(1, 1), Cord(2, 1))
    # maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    # maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    maze.display()
    maze.refresh_cells()
    print(maze)
    root.mainloop()

