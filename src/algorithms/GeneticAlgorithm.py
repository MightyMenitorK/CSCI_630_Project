import random
import time

def ga(start, goal, get_neighbors, max_iter=500, pop_size=100):
    # Directions: 0: Up, 1: Down, 2: Left, 3: Right
    directions = [0, 1, 2, 3]
    
    # Estimate a reasonable path length (Manhattan distance * constant)
    path_limit = (abs(start[0] - goal[0]) + abs(start[1] - goal[1])) * 2
    
    def get_path_from_genes(genes):
        current = start
        path = [current]
        for move in genes:
            r, c = current
            if move == 0: next_node = (r - 1, c)
            elif move == 1: next_node = (r + 1, c)
            elif move == 2: next_node = (r, c - 1)
            else: next_node = (r, c + 1)
            
            # Check if move is valid via get_neighbors
            if next_node in get_neighbors(r, c):
                current = next_node
                path.append(current)
                if current == goal:
                    break
            else:
                break # Hit a wall/boundary
        return path

    def calculate_fitness(genes):
        path = get_path_from_genes(genes)
        last_node = path[-1]
        # Distance to goal (lower is better, so we use inverse)
        dist = abs(last_node[0] - goal[0]) + abs(last_node[1] - goal[1])
        if last_node == goal:
            return 1000 + (100 / len(path)) # Huge bonus for reaching goal
        return 1 / (dist + 1)

    # Initialize Population
    population = [[random.choice(directions) for _ in range(path_limit)] for _ in range(pop_size)]
    
    expanded_nodes = set()
    best_overall_path = []
    
    for _ in range(max_iter):
        # Evaluation
        scored_pop = [(calculate_fitness(ind), ind) for ind in population]
        scored_pop.sort(key=lambda x: x[0], reverse=True)
        
        current_best_path = get_path_from_genes(scored_pop[0][1])
        for node in current_best_path: expanded_nodes.add(node)
        
        if not best_overall_path or scored_pop[0][0] > calculate_fitness(best_overall_path):
            best_overall_path = scored_pop[0][1]

        if current_best_path[-1] == goal:
            break # Converged early

        # Selection (Top 20%)
        next_gen = [ind for score, ind in scored_pop[:20]]

        # Crossover & Mutation
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(next_gen[:10], 2)
            cut = random.randint(1, path_limit - 1)
            child = p1[:cut] + p2[cut:]
            # Mutation
            if random.random() < 0.1:
                child[random.randint(0, path_limit - 1)] = random.choice(directions)
            next_gen.append(child)
        
        population = next_gen

    final_path = get_path_from_genes(best_overall_path)
    success = 1 if final_path[-1] == goal else 0
    cost = len(final_path) - 1
    
    return final_path, cost, len(final_path), list(expanded_nodes), len(expanded_nodes), success