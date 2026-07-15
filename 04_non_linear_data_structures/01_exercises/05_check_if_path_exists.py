from collections import deque, defaultdict

def validPath(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    # --- Step 1: Build the adjacency list ---
    # Represent the graph using a dictionary where keys are nodes and values are lists of neighbors.
    # We use a bi-directional (undirected) connection, so we append both ways.
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # --- Step 2: Initialize Breadth-First Search (BFS) structures ---
    # We use a double-ended queue (deque) for efficient $O(1)$ pop operations from the left.
    queue = deque([source])
    # A set is used to track visited nodes to prevent infinite loops (cycles)
    visited = {source}

    # --- Step 3: Traverse the graph ---
    while queue:
        current_node = queue.popleft()

        # Check if we have successfully navigated to our destination
        if current_node == destination:
            return True

        # Check all unvisited neighbors of the current node
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # --- Step 4: Default return ---
    # If the queue empties and we never reached the destination, no path exists
    return False
