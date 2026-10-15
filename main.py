from fastapi import FastAPI, HTTPException
from models import SearchRequest, SearchResponse
from greedy_search import greedy_search
from star_search import star_search

app = FastAPI(
    title="Actividad 12 - Búsqueda Voraz y A*",
    description="API para búsqueda Greedy Best-First y A* sin librerías especializadas.",
    version="1.0.0"
)

def normalize_graph(data: SearchRequest):
    if data.representation == "lista":
        graph = {}
        for node, edges in data.graph.items():
            graph[node] = [(str(v), float(w)) for v, w in edges]
        return graph

    nodes = data.nodes

    if data.representation == "matriz":
        matrix = data.graph
        if len(matrix) != len(nodes) or any(len(row) != len(nodes) for row in matrix):
            raise ValueError("La matriz debe ser cuadrada y coincidir con 'nodes'.")
        graph = {n: [] for n in nodes}
        for i, u in enumerate(nodes):
            for j, value in enumerate(matrix[i]):
                if value is not None and float(value) != 0:
                    graph[u].append((nodes[j], float(value)))
        return graph

    # Vector de aristas: [["A","B",15], ["A","C",22], ...]
    graph = {n: [] for n in nodes}
    for edge in data.graph:
        if len(edge) != 3:
            raise ValueError("Cada elemento del vector debe ser [origen, destino, peso].")
        u, v, w = edge
        if u not in graph or v not in graph:
            raise ValueError("El vector contiene un nodo que no aparece en 'nodes'.")
        graph[u].append((v, float(w)))
    return graph

def validate_limit(limit, n):
    if limit is not None and limit > n:
        raise ValueError("El límite de visitas no puede superar el total de nodos.")

@app.post("/search/greedy", response_model=SearchResponse)
def search_greedy(data: SearchRequest):
    try:
        graph = normalize_graph(data)
        validate_limit(data.visit_limit, len(graph))
        return greedy_search(
            graph, data.origin, data.destination,
            data.coordinates, data.visit_limit
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/search/star", response_model=SearchResponse)
def search_star(data: SearchRequest):
    try:
        graph = normalize_graph(data)
        validate_limit(data.visit_limit, len(graph))
        return star_search(
            graph, data.origin, data.destination,
            data.coordinates, data.visit_limit
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== Endpoints adicionales =====
from models_extra import (
    WeightedGraphRequest, TSPRequest, AlgorithmResponse, SyntheticGraphRequest
)
from dijkstra import dijkstra
from tsp import traveling_salesman
from tsp_greedy import traveling_salesman_greedy
from synthetic_graph import generate_synthetic_graph

def validate_graph_nodes(graph, *nodes):
    for node in nodes:
        if node not in graph:
            raise HTTPException(status_code=400, detail=f"El nodo '{node}' no existe en el grafo.")
    for u, edges in graph.items():
        for v, weight in edges:
            if v not in graph:
                raise HTTPException(status_code=400, detail=f"El nodo destino '{v}' no existe.")
            if weight < 0:
                raise HTTPException(status_code=400, detail="No se permiten pesos negativos.")

@app.post("/search/dijkstra", response_model=AlgorithmResponse)
def search_dijkstra(data: WeightedGraphRequest):
    validate_graph_nodes(data.graph, data.origin, data.destination)
    return dijkstra(data.graph, data.origin, data.destination)

@app.post("/search/tsp", response_model=AlgorithmResponse)
def search_tsp(data: TSPRequest):
    validate_graph_nodes(data.graph, data.origin)
    if len(data.graph) > 10:
        raise HTTPException(
            status_code=400,
            detail="El TSP exacto por fuerza bruta se limita a 10 nodos por su complejidad factorial. Usa /search/tsp-greedy para grafos mayores."
        )
    return traveling_salesman(data.graph, data.origin)

@app.post("/search/tsp-greedy", response_model=AlgorithmResponse)
def search_tsp_greedy(data: TSPRequest):
    validate_graph_nodes(data.graph, data.origin)
    return traveling_salesman_greedy(data.graph, data.origin)

@app.post("/graphs/synthetic")
def synthetic_graph(data: SyntheticGraphRequest):
    if data.max_weight < data.min_weight:
        raise HTTPException(status_code=400, detail="max_weight debe ser >= min_weight.")
    graph = generate_synthetic_graph(
        data.nodes, data.min_weight, data.max_weight, data.seed
    )
    return {"total_nodos": data.nodes, "graph": graph}
