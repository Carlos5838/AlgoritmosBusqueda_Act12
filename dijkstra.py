import time
import tracemalloc

def dijkstra(graph, origin, destination):
    start = time.perf_counter()
    tracemalloc.start()

    distances = {node: float("inf") for node in graph}
    distances[origin] = 0.0
    parent = {}
    pending = set(graph)
    visited_count = 0

    while pending:
        current = min(pending, key=lambda n: distances[n])
        if distances[current] == float("inf"):
            break

        pending.remove(current)
        visited_count += 1

        if current == destination:
            break

        for neighbor, weight in graph[current]:
            new_cost = distances[current] + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                parent[neighbor] = current

    route = []
    if distances[destination] != float("inf"):
        node = destination
        nodes = [node]
        while node != origin:
            node = parent[node]
            nodes.append(node)
        nodes.reverse()
        route = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start) * 1000

    return {
        "tiempo_ms": round(elapsed, 6),
        "memoria_bytes": peak,
        "nodos_recorridos": visited_count,
        "costo_camino": None if distances[destination] == float("inf") else distances[destination],
        "ruta": route
    }
