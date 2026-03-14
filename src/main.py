import tkinter as tk
from maze import Maze
from cell import Cord
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Simulator")
    maze = Maze(root, 5, 5)
    maze.toggle_barrier(Cord(0, 0), Cord(0, 1))
    maze.toggle_barrier(Cord(1, 0), Cord(1, 1))
    maze.toggle_barrier(Cord(1, 1), Cord(2, 1))
    maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    maze.toggle_barrier(Cord(3, 1), Cord(2, 1))
    maze.display()
    print(maze)
    root.mainloop()

