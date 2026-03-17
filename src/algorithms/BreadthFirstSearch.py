from collections import deque

def bfs(start, goal, get_neighbors):
    """
    Perform Breadth-First Search (BFS).
    :param start: tuple, The starting position
    :param goal: tuple, The starting position
    :param get_neighbors: A function that takes (row, col) and returns
            all valid neighboring cells that can be reached.
    :return tuple: (path, cost)
            path -> list of coordinates from start to goal
            cost -> total number of steps in that path
        or None if no path exists
    """
    frontier = deque()
    frontier.append((start, [start], 0))   # (node, path, cost)

    while frontier:
        node, path, cost = frontier.popleft()

        if node == goal:
            return path, cost

        row, col = node

        for neighbor in get_neighbors(row, col):
            if neighbor not in path:
                frontier.append((neighbor, path + [neighbor], cost + 1))

    return None

