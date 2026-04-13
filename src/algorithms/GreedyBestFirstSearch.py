def greedy_bfs(start, goal, get_neighbors, heuristic) -> tuple | None:
    """
    Perform Greedy Best-First Search.

    :param start: tuple, starting position
    :param goal: tuple, goal position
    :param get_neighbors: function that takes (row, col) and returns valid neighbors
    :param heuristic: function that takes (row, col) and returns heuristic value
    :return: (path, cost, path_length, expanded_nodes, expanded_count)
             or None if no path exists
    """
    frontier = []
    frontier.append((start, [start], 0))   # (node, path, cost)

    visited = set()
    expanded_nodes = []

    while len(frontier) > 0:
        best_index = 0
        best_node = frontier[0][0]
        best_value = heuristic(best_node[0], best_node[1])

        i = 1
        while i < len(frontier):
            current_node = frontier[i][0]
            current_value = heuristic(current_node[0], current_node[1])

            if current_value < best_value:
                best_value = current_value
                best_index = i

            i = i + 1

        node, path, cost = frontier.pop(best_index)

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

        i = 0
        while i < len(neighbors):
            neighbor = neighbors[i]

            if neighbor not in visited:
                frontier.append((neighbor, path + [neighbor], cost + 1))

            i = i + 1

    return None