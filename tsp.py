import time
import tracemalloc
from itertools import permutations

def edge_cost(graph, u, v):
    for neighbor, weight in graph[u]:
        if neighbor == v:
            return weight
    return None

def traveling_salesman(graph, origin):
    start = time.perf_counter()
    tracemalloc.start()

    others = [n for n in graph if n != origin]
    best_cost = float("inf")
    best_route = []
    evaluated_nodes = 0

    for order in permutations(others):
        cycle = (origin,) + order + (origin,)
        cost = 0.0
        valid = True

        for i in range(len(cycle) - 1):
            evaluated_nodes += 1
            w = edge_cost(graph, cycle[i], cycle[i + 1])
            if w is None:
                valid = False
                break
            cost += w

        if valid and cost < best_cost:
            best_cost = cost
            best_route = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start) * 1000

    return {
        "tiempo_ms": round(elapsed, 6),
        "memoria_bytes": peak,
        "nodos_recorridos": evaluated_nodes,
        "costo_camino": None if best_cost == float("inf") else best_cost,
        "ruta": best_route
    }
