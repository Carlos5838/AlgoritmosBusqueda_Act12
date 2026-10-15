import time
import tracemalloc

def edge_cost(graph, u, v):
    for neighbor, weight in graph[u]:
        if neighbor == v:
            return weight
    return None

def traveling_salesman_greedy(graph, origin):
    start = time.perf_counter()
    tracemalloc.start()

    unvisited = set(graph)
    unvisited.remove(origin)
    current = origin
    route = []
    total_cost = 0.0
    visited_count = 1
    solution = True

    while unvisited:
        candidates = [(w, v) for v, w in graph[current] if v in unvisited]
        if not candidates:
            solution = False
            break

        weight, nxt = min(candidates, key=lambda x: (x[0], x[1]))
        route.append((current, nxt))
        total_cost += weight
        current = nxt
        unvisited.remove(current)
        visited_count += 1

    if solution:
        back = edge_cost(graph, current, origin)
        if back is None:
            solution = False
        else:
            route.append((current, origin))
            total_cost += back

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start) * 1000

    return {
        "tiempo_ms": round(elapsed, 6),
        "memoria_bytes": peak,
        "nodos_recorridos": visited_count,
        "costo_camino": total_cost if solution else None,
        "ruta": route if solution else []
    }
