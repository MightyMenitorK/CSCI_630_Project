import random
import tkinter as tk
from maze import Maze
from cell import Cord
    
if __name__ == "__main__":

    row_input = input("Enter number of rows (press Enter for random): ")
    col_input = input("Enter number of cols (press Enter for random): ")

    if row_input.strip() == "":
        rows = random.randint(3, 8)
    else:
        rows = int(row_input)

    if col_input.strip() == "":
        cols = random.randint(3, 8)
    else:
        cols = int(col_input)


    root = tk.Tk()
    root.title("Maze Simulator")

    maze = Maze(root, rows, cols)


    # maze = Maze(root, 5, 5)
    # maze.toggle_barrier(Cord(0, 0), Cord(0, 1))
    # maze.toggle_barrier(Cord(1, 0), Cord(1, 1))
    # maze.toggle_barrier(Cord(1, 1), Cord(2, 1))
    # maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    # maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    maze.display()
    print(maze)
    root.mainloop()

