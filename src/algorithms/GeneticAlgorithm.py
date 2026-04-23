import random
import time

def ga(start, goal, get_neighbors, max_iter=500, pop_size=100):
    directions = [0, 1, 2, 3]
    path_limit = (abs(start[0] - goal[0]) + abs(start[1] - goal[1])) * 4
    
    # Track how many times each node has been visited across the whole GA run
    global_visit_count = {}

    def get_path_from_genes(genes):
        current = start
        path = [current]
        for move in genes:
            r, c = current
            if move == 0: next_node = (r - 1, c)
            elif move == 1: next_node = (r + 1, c)
            elif move == 2: next_node = (r, c - 1)
            else: next_node = (r, c + 1)
            
            if next_node in get_neighbors(r, c):
                current = next_node
                path.append(current)
                if current == goal: break
            else:
                break 
        return path

    def calculate_fitness(genes, path):
        last_node = path[-1]
        
        # 1. Standard Distance Metric
        min_dist = min(abs(r - goal[0]) + abs(c - goal[1]) for r, c in path)
        
        # 2. Novelty/Exploration Bonus
        # We reward paths that spend time in nodes that haven't been visited much
        exploration_reward = 0
        for node in path:
            # The fewer times a node has been seen globally, the higher the reward
            count = global_visit_count.get(node, 0)
            exploration_reward += (1.0 / (count + 1))

        # 3. Success Bonus
        if last_node == goal:
            return 10000 + (1000 / len(path))
        
        # Combine: Distance score + survival + curiosity
        # We multiply exploration to make it significant enough to counter-act 
        # the 'penalty' of moving away from the goal.
        return (1 / (min_dist + 1)) + (len(path) * 0.05) + (exploration_reward * 0.1)

    # Initialize Population
    population = [[random.choice(directions) for _ in range(path_limit)] for _ in range(pop_size)]
    expanded_nodes = set()
    best_overall_genes = None
    best_fitness = -1
    
    for _ in range(max_iter):
        # Pre-calculate paths and update global discovery
        paths = [get_path_from_genes(ind) for ind in population]
        for path in paths:
            for node in path:
                expanded_nodes.add(node)
                global_visit_count[node] = global_visit_count.get(node, 0) + 1

        # Evaluation
        scored_pop = []
        for i in range(pop_size):
            fit = calculate_fitness(population[i], paths[i])
            scored_pop.append((fit, population[i]))

        scored_pop.sort(key=lambda x: x[0], reverse=True)
        
        if scored_pop[0][0] > best_fitness:
            best_fitness = scored_pop[0][0]
            best_chromosome = scored_pop[0][1]

        if paths[0][-1] == goal: # If the best of this gen reached the goal
            # We can break or continue to optimize path length
            best_overall_genes = scored_pop[0][1]
            break

        # Selection & Two-Point Crossover
        next_gen = [ind for score, ind in scored_pop[:20]]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(next_gen[:10], 2)
            pt1, pt2 = sorted([random.randint(0, path_limit-1), random.randint(0, path_limit-1)])
            child = p1[:pt1] + p2[pt1:pt2] + p1[pt2:]
            
            if random.random() < 0.3:
                child[random.randint(0, path_limit - 1)] = random.choice(directions)
            next_gen.append(child)
        
        population = next_gen

    final_path = get_path_from_genes(best_chromosome if best_chromosome else population[0])
    success = 1 if final_path[-1] == goal else 0
    cost = len(final_path) - 1
    
    return final_path, cost, len(final_path), list(expanded_nodes), len(expanded_nodes), success