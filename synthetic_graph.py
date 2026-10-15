import random

def generate_synthetic_graph(nodes, min_weight=1, max_weight=100, seed=None):
    if nodes < 2:
        raise ValueError("El grafo debe tener al menos 2 nodos.")
    if min_weight <= 0 or max_weight < min_weight:
        raise ValueError("Rango de pesos inválido.")

    rng = random.Random(seed)
    names = [chr(65 + i) if i < 26 else f"N{i + 1}" for i in range(nodes)]
    graph = {n: [] for n in names}

    # Grafo completo, no dirigido y ponderado.
    # Garantiza que siempre exista un ciclo Hamiltoniano para las pruebas de TSP.
    for i in range(nodes):
        for j in range(i + 1, nodes):
            weight = rng.randint(min_weight, max_weight)
            graph[names[i]].append([names[j], weight])
            graph[names[j]].append([names[i], weight])

    return graph
