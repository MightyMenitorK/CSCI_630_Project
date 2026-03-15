# CSCI_630_Project
Optimizing Maze Exit Strategies using Search Algorithms

Build a maze game where an agent must navigate from a start cell to
a goal cell while avoiding walls/obstacles. The objective is to 
compute and visualize a path, and compare multiple algorithms by 
path quality, runtime, and nodes expanded.

We represent the maze as a graph: Node/state, edges, cost/weight

#### Algorithms: 
1. DFS (Depth-First Search)
2. BFS (Breadth-First Search)
3. Uniform Cost Search (Dijkstra’s Algorithm)
4. Greedy Algorithm
5. A* Search
6. Genetic Algorithm 

#### Validation & Evaluation:

We will compare algorithms on the same mazes using:
1. Path length (#steps)
2. Path cost (if weighted tiles)
3. Nodes expanded (work done)
4. Runtime
5. Success rate (especially for GA)