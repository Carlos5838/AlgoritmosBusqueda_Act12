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

def star_search(graph, origin, destination, coordinates=None, visit_limit=None):
    if origin not in graph or destination not in graph:
        raise ValueError("Origen o destino inexistente.")

    limit = visit_limit if visit_limit is not None else ceil(0.8 * len(graph))
    g = {node: float("inf") for node in graph}
    g[origin] = 0.0
    parent = {}
    frontier = [(heuristic(origin, destination, coordinates), origin)]
    closed = set()
    visited = []
    solution = False

    while frontier and len(visited) < limit:
        best_i = min(range(len(frontier)), key=lambda i: (frontier[i][0], frontier[i][1]))
        _, current = frontier.pop(best_i)

        if current in closed:
            continue
        closed.add(current)
        visited.append(current)

        if current == destination:
            solution = True
            break

        for neighbor, weight in graph[current]:
            tentative = g[current] + weight
            if tentative < g[neighbor]:
                g[neighbor] = tentative
                parent[neighbor] = current
                f = tentative + heuristic(neighbor, destination, coordinates)
                frontier.append((f, neighbor))

    route = []
    if solution:
        nodes = [destination]
        while nodes[-1] != origin:
            nodes.append(parent[nodes[-1]])
        nodes.reverse()
        route = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]

    return {
        "total_nodos_visitados": len(visited),
        "solucion": solution,
        "ruta": route,
        "costo_total": g[destination] if solution else None,
        "T_n": "O(V^2 + E) (selección lineal manual de la frontera)",
        "S_n": "O(V + E)"
    }
