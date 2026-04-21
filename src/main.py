import sys
import random
import tkinter as tk
from maze import Maze
from cell import Cord
    
def extract(filename: str):
    """Parses a .cnfg file for maze dimensions, points, and barriers."""
    try:
        with open(filename, 'r') as f:
            # Filter out comments and empty lines
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Parse dimensions
        rows, cols = map(int, lines[0].split(','))
        # Parse Start/Goal
        sr, sc = map(int, lines[1].split(','))
        gr, gc = map(int, lines[2].split(','))
        
        # Parse Barriers (the remaining lines)
        barriers = []
        for line in lines[3:]:
            coords = list(map(int, line.split(',')))
            if len(coords) == 4:
                # Store as (Cord1, Cord2)
                barriers.append((Cord(coords[0], coords[1]), Cord(coords[2], coords[3])))
                
        return rows, cols, sr, sc, gr, gc, barriers
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing config: {e}")
        sys.exit(1)

def prompt():
    """Handles terminal-based input for all maze parameters, including barriers."""
    def get_val(msg, default_range, limit=None):
        val = input(msg).strip()
        if val == "":
            return random.randint(default_range[0], default_range[1])
        try:
            res = int(val)
            if limit is not None and (res >= limit or res < 0):
                return limit - 1
            return res
        except ValueError:
            return default_range[0]

    r = get_val("Enter rows (Enter for random, max 20): ", (3, 15), 20)
    c = get_val("Enter cols (Enter for random, max 20): ", (3, 15), 20)
    
    sr = get_val(f"Start row (0-{r-1}, Enter for random): ", (0, r-1), r)
    sc = get_val(f"Start col (0-{c-1}, Enter for random): ", (0, c-1), c)
    
    gr = get_val(f"Goal row (0-{r-1}, Enter for random): ", (0, r-1), r)
    gc = get_val(f"Goal col (0-{c-1}, Enter for random): ", (0, c-1), c)
    
    while sr == gr and sc == gc:
        gr, gc = random.randint(0, r-1), random.randint(0, c-1)

    # Manual Barrier Entry
    barriers = []
    print("\n--- Barrier Entry ---")
    print("Enter barriers as 'r1,c1,r2,c2' (e.g., 0,0,0,1). Press Enter when done.")
    while True:
        b_input = input("Add barrier: ").strip()
        if b_input == "":
            break
        try:
            coords = [int(x.strip()) for x in b_input.split(',')]
            if len(coords) == 4:
                barriers.append((Cord(coords[0], coords[1]), Cord(coords[2], coords[3])))
            else:
                print("Invalid format. Use r1,c1,r2,c2")
        except ValueError:
            print("Invalid numbers. Please try again.")
        
    return r, c, sr, sc, gr, gc, barriers

if __name__ == "__main__":
    barriers = []
    if len(sys.argv) > 1:
        file = sys.argv[1].strip()
        if not file.endswith(".cnfg"):
            print("Error: Please provide a .cnfg file.")
            sys.exit(1)
        rows, cols, s_row, s_col, g_row, g_col, barriers = extract(file)
    else:
        rows, cols, s_row, s_col, g_row, g_col, barriers = prompt()

    root = tk.Tk()
    root.title("Maze Simulator")

    maze = Maze(root, rows, cols)
    
    # Move start and goal
    maze.move_start(s_row, s_col)
    maze.move_goal(g_row, g_col)

    # Apply the barriers from the file
    for c1, c2 in barriers:
        maze.toggle_barrier(c1, c2)

    maze.display()
    print(maze)
    root.mainloop()
