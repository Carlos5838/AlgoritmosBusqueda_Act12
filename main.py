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
