from math import ceil, hypot

def heuristic(node, goal, coordinates):
    if not coordinates or node not in coordinates or goal not in coordinates:
        return 0.0
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]
    return hypot(x2 - x1, y2 - y1)

def reconstruct(parent, origin, destination):
    if destination == origin:
        return []
    if destination not in parent:
        return []
    nodes = [destination]
    while nodes[-1] != origin:
        nodes.append(parent[nodes[-1]])
    nodes.reverse()
    return [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]

def path_cost(route, graph):
    total = 0.0
    for u, v in route:
        for neighbor, weight in graph[u]:
            if neighbor == v:
                total += weight
                break
    return total

def greedy_search(graph, origin, destination, coordinates=None, visit_limit=None):
    if origin not in graph or destination not in graph:
        raise ValueError("Origen o destino inexistente.")

    limit = visit_limit if visit_limit is not None else ceil(0.8 * len(graph))
    frontier = [(heuristic(origin, destination, coordinates), origin)]
    discovered = {origin}
    parent = {}
    visited = []
    solution = False

    while frontier and len(visited) < limit:
        best_i = min(range(len(frontier)), key=lambda i: (frontier[i][0], frontier[i][1]))
        _, current = frontier.pop(best_i)
        visited.append(current)

        if current == destination:
            solution = True
            break

        for neighbor, _ in graph[current]:
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                frontier.append((heuristic(neighbor, destination, coordinates), neighbor))

    route = reconstruct(parent, origin, destination) if solution else []
    return {
        "total_nodos_visitados": len(visited),
        "solucion": solution,
        "ruta": route,
        "costo_total": path_cost(route, graph) if solution else None,
        "T_n": "O(V^2 + E) (selección lineal manual de la frontera)",
        "S_n": "O(V + E)"
    }
