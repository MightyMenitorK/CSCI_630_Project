from collections import deque

def bfs(start, goal, get_neighbors):
    """
    Perform Breadth-First Search (BFS).
    :param start: tuple, The starting position
    :param goal: tuple, The goal position
    :param get_neighbors: A function that takes (row, col) and returns
            all valid neighboring cells that can be reached.

    :return tuple: (path, cost, path_length, expanded_nodes, expanded_count)
            path -> list of coordinates from start to goal
            cost -> total number of steps in that path
            path_length -> total number of nodes in the final path
            expanded_nodes -> list of nodes expanded by BFS
            expanded_count -> number of expanded nodes
        or None if no path exists
    """

    frontier = deque()
    frontier.append((start, [start], 0))   # (node, path, cost)

    visited = set()
    expanded_nodes = []

    while frontier:
        node, path, cost = frontier.popleft()

        if node in visited:
            continue

        visited.add(node)
        expanded_nodes.append(node)

        if node == goal:
            path_length = len(path)
            expanded_count = len(expanded_nodes)
            return path, cost, path_length, expanded_nodes, expanded_count

        row, col = node

        for neighbor in get_neighbors(row, col):
            if neighbor not in visited:
                frontier.append((neighbor, path + [neighbor], cost + 1))

    return None