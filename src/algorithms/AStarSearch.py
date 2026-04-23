import heapq


def manhattan(node, goal):
    """
    Compute Manhattan distance between current node and goal.
    """
    row, col = node
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)

def astar(start, goal, get_neighbors, heuristic=manhattan) -> tuple | None:
    """
    Perform A* Search.

    :param start: tuple, starting position
    :param goal: tuple, goal position
    :param get_neighbors: function that takes (row, col) and returns valid neighbors
    :param heuristic: heuristic function h(n), default is Manhattan distance

    :return: (path, cost, path_length, expanded_nodes, expanded_count)
             path -> final path from start to goal
             cost -> total number of moves in the final path
             path_length -> total number of nodes in the final path
             expanded_nodes -> list of nodes expanded by A*
             expanded_count -> number of expanded nodes
             or None if no path exists
    """
    insertion_id = 0

    # heap item = (f, insertion_id, node, path, g)
    frontier = []
    start_h = heuristic(start, goal)
    heapq.heappush(frontier, (start_h, insertion_id, start, [start], 0))

    # best known g-cost to each node
    best_g = {start: 0}
    expanded_nodes = []

    while frontier:
        f_value, _, node, path, g_cost = heapq.heappop(frontier)

        # Skip stale entries
        if g_cost > best_g.get(node, float("inf")):
            continue

        expanded_nodes.append(node)

        if node == goal:
            path_length = len(path)
            expanded_count = len(expanded_nodes)
            return path, g_cost, path_length, expanded_nodes, expanded_count

        row, col = node
        for neighbor in get_neighbors(row, col):
            new_g = g_cost + 1

            # Graph-search version: only keep better path to a node
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                insertion_id += 1
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (new_f, insertion_id, neighbor, path + [neighbor], new_g)
                )

    return None