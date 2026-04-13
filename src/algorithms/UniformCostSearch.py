import heapq

def ucs(start, goal, get_neighbors):
    """
    Perform Uniform Cost Search (UCS).
    :param start: tuple (row, col)
    :param goal: tuple (row, col)
    :param get_neighbors: function returning list of (row, col)
    :return: (path, cost, path_length, expanded_nodes, expanded_count)
    """
    # Priority Queue stores: (cumulative_cost, current_node, path)
    # We use cumulative_cost as the priority
    frontier = [(0, start, [start])]
    
    visited = {} # node -> minimum cost found to reach it
    expanded_nodes = []

    while frontier:
        cost, node, path = heapq.heappop(frontier)

        # Optimization: If we already found a cheaper way to this node, skip
        if node in visited and visited[node] <= cost:
            continue
        
        visited[node] = cost
        expanded_nodes.append(node)

        if node == goal:
            return path, cost, len(path), expanded_nodes, len(expanded_nodes)

        row, col = node
        for neighbor in get_neighbors(row, col):
            # In your maze, every move costs 1. 
            # If you add weights to cells later, replace '1' with cell.weight
            new_cost = cost + 1 
            
            if neighbor not in visited or new_cost < visited[neighbor]:
                heapq.heappush(frontier, (new_cost, neighbor, path + [neighbor]))

    return None