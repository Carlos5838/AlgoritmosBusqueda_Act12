# Documentación adicional — Dijkstra y Agente Viajero

## Identificación

**Nombre:** ______________________________  
**No. de cuenta:** _______________________  
**Materia:** _____________________________  
**Actividad:** Algoritmos de rutas y generación de grafos sintéticos  

## Endpoints agregados

| Método | Endpoint | Función |
|---|---|---|
| POST | `/search/dijkstra` | Camino mínimo entre origen y destino |
| POST | `/search/tsp` | Agente viajero exacto por fuerza bruta |
| POST | `/search/tsp-greedy` | Agente viajero mediante vecino más cercano |
| POST | `/graphs/synthetic` | Generación de grafos ponderados sintéticos |

Todos los algoritmos reportan tiempo de ejecución en milisegundos, pico de memoria medido durante la ejecución, número de nodos recorridos/evaluados y costo del camino encontrado. También se incluye `ruta` para facilitar la comprobación.

## 1. Dijkstra

Dijkstra encuentra el camino de costo mínimo desde un nodo origen hasta un destino cuando los pesos son no negativos. Se mantiene para cada nodo la mejor distancia conocida. En cada iteración se selecciona manualmente el nodo pendiente con menor distancia, sin utilizar librerías especializadas.

La implementación utiliza selección lineal, por lo que su complejidad temporal es aproximadamente `O(V² + E)` y la espacial `O(V + E)`.

Ejemplo:

```json
{
  "graph": {
    "A": [["B", 4], ["C", 2]],
    "B": [["A", 4], ["C", 1]],
    "C": [["A", 2], ["B", 1]]
  },
  "origin": "A",
  "destination": "B"
}
```

## 2. Agente viajero exacto

El problema del agente viajero (TSP) busca un ciclo que comience en el origen, visite todos los nodos exactamente una vez y regrese al origen con costo mínimo.

La implementación exacta prueba todas las permutaciones posibles de los nodos restantes. Por ello su complejidad es factorial, aproximadamente `O((V-1)! · V)`. Esto hace que el método sea útil únicamente para grafos pequeños.

Por seguridad, el endpoint exacto se limita a **10 nodos**. Una prueba exacta de 15 nodos implicaría evaluar `14! = 87,178,291,200` órdenes posibles, por lo que no es una prueba práctica. Para 15 nodos se utiliza el endpoint voraz.

## 3. Agente viajero con heurística voraz

El algoritmo comienza en el origen y selecciona repetidamente, entre los nodos todavía no visitados, el vecino alcanzable con menor peso. Al terminar intenta regresar al origen.

Esta estrategia es mucho más rápida que la búsqueda exhaustiva, pero no garantiza encontrar el ciclo óptimo. Con la representación utilizada, su costo temporal es aproximadamente `O(V² + E)`.

## 4. Generador de grafos sintéticos

`POST /graphs/synthetic` genera un grafo completo, no dirigido y ponderado. Al ser completo, existe conexión entre cada par de nodos y se garantiza la existencia de ciclos Hamiltonianos para las pruebas del agente viajero.

Entrada:

```json
{
  "nodes": 5,
  "min_weight": 1,
  "max_weight": 100,
  "seed": 42
}
```

La semilla permite reproducir el mismo grafo.

## 5. Métricas

El tiempo se obtiene con `time.perf_counter()` y se convierte a milisegundos. La memoria se obtiene mediante `tracemalloc`, reportando el pico de bytes reservados durante la ejecución del algoritmo.

Las métricas pueden cambiar entre ejecuciones según el equipo, sistema operativo y carga del sistema; por ello no deben documentarse como constantes universales.

## 6. Pruebas

### Prueba 1 — 5 nodos

1. Generar el grafo:

```json
{"nodes": 5, "min_weight": 1, "max_weight": 50, "seed": 5}
```

2. Usar el `graph` retornado para probar Dijkstra (`A` a `E`), TSP exacto (`A`) y TSP voraz (`A`).

### Prueba 2 — 10 nodos

```json
{"nodes": 10, "min_weight": 1, "max_weight": 50, "seed": 10}
```

Probar Dijkstra de `A` a `J`, TSP exacto desde `A` y TSP voraz desde `A`. El TSP exacto con 10 nodos evalúa hasta `9! = 362880` permutaciones.

### Prueba 3 — 15 nodos

```json
{"nodes": 15, "min_weight": 1, "max_weight": 50, "seed": 15}
```

Probar Dijkstra de `A` a `O` y TSP voraz desde `A`.

El TSP exacto deliberadamente no se ejecuta con 15 nodos porque `14!` posibilidades hacen inviable la prueba por fuerza bruta. Esta limitación documenta precisamente el crecimiento factorial del algoritmo exacto.

## Tabla de resultados

Completar con las respuestas reales obtenidas en el equipo donde se ejecute la API:

| Nodos | Algoritmo | Tiempo (ms) | Memoria (bytes) | Nodos recorridos/evaluados | Costo |
|---:|---|---:|---:|---:|---:|
| 5 | Dijkstra | | | | |
| 5 | TSP exacto | | | | |
| 5 | TSP voraz | | | | |
| 10 | Dijkstra | | | | |
| 10 | TSP exacto | | | | |
| 10 | TSP voraz | | | | |
| 15 | Dijkstra | | | | |
| 15 | TSP exacto | No ejecutado: factorial | No ejecutado | No ejecutado | No ejecutado |
| 15 | TSP voraz | | | | |

## Ejecución

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger:

`http://127.0.0.1:8000/docs`

## Conclusión

Dijkstra resuelve eficientemente caminos mínimos con pesos no negativos. El agente viajero exacto permite encontrar el óptimo, pero su crecimiento factorial limita severamente el tamaño de los grafos que puede resolver. La heurística voraz sacrifica la garantía de optimalidad a cambio de una reducción muy importante del tiempo de ejecución. El generador sintético permite reproducir estas diferencias usando grafos de distintos tamaños.
