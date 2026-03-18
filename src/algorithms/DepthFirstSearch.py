def dfs(start, goal, get_neighbors)-> tuple|None:
    """
    Perform Depth-First Search (DFS).
    :param start: tuple, starting position
    :param goal: tuple, goal position
    :param get_neighbors: function that takes (row, col) and returns
                          all valid neighboring cells
    :return: (path, cost, path_length, expanded_nodes, expanded_count)
             path -> final path from start to goal
             cost -> total number of moves in the final path
             path_length -> total number of nodes in the final path
             expanded_nodes -> list of nodes explored by DFS
             expanded_count -> number of explored nodes
             or None if no path exists
    """
    frontier = []
    frontier.append((start, [start], 0))   # (node, path, cost)

    visited = set()
    expanded_nodes = []

    while frontier:
        node, path, cost = frontier.pop()

        if node in visited:
            continue

        visited.add(node)
        expanded_nodes.append(node)

        if node == goal:
            path_length = len(path)
            expanded_count = len(expanded_nodes)
            return path, cost, path_length, expanded_nodes, expanded_count

        row, col = node
        neighbors = get_neighbors(row, col)

        i = len(neighbors) - 1
        while i >= 0:
            neighbor = neighbors[i]

            if neighbor not in visited:
                frontier.append((neighbor, path + [neighbor], cost + 1))

            i = i - 1

    return None