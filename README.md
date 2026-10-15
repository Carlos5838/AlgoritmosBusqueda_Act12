**Nombre:** Carlos Andrés Hernández Díaz  
**No. de cuenta:** 200711  
**Materia:** Lenguajes de Computación
**Actividad:** Actividad 12 — Algoritmos de búsqueda informada (heurísticos)

## Descripción

Se implementó una API REST con FastAPI que expone dos endpoints:

- `POST /search/greedy`
- `POST /search/star`

Los algoritmos fueron implementados manualmente, sin utilizar librerías especializadas de búsqueda en grafos.

La API acepta tres representaciones: lista de adyacencia con pesos, matriz de adyacencia con pesos y vector de aristas. También recibe el nodo origen, el destino, coordenadas opcionales para la heurística y un límite opcional de visitas.

Si `visit_limit` no se especifica, cada algoritmo utiliza:

`ceil(0.80 * número_de_nodos)`

Por tanto, los límites por defecto son 8, 20 y 40 para los grafos de 10, 25 y 50 nodos, respectivamente.

## Instalación y ejecución

uvicorn main:app --reload
```

Abrir:

`http://127.0.0.1:8000/docs`

## Entrada

Ejemplo con lista:

```json
{
  "representation": "lista",
  "graph": {
    "A": [["B", 15], ["C", 22]],
    "B": [],
    "C": []
  },
  "coordinates": {
    "A": [0, 0],
    "B": [1, 1],
    "C": [2, 0]
  },
  "origin": "A",
  "destination": "C"
}
```

Para `matriz`, se agrega `nodes` para indicar el orden de filas y columnas. Para `vector`, `graph` contiene elementos `[origen, destino, peso]` y también se proporciona `nodes`.

## Búsqueda voraz

Greedy Best-First Search selecciona de la frontera el nodo con menor valor heurístico:

`f(n) = h(n)`

La heurística implementada es la distancia euclidiana:

`h(n) = sqrt((x_dest-x_n)^2 + (y_dest-y_n)^2)`

Greedy no considera el costo acumulado al seleccionar el siguiente nodo, por lo que puede encontrar una solución sin garantizar la ruta de costo mínimo.

## Búsqueda A*

A* utiliza:

`f(n) = g(n) + h(n)`

donde `g(n)` es el costo acumulado conocido desde el origen y `h(n)` es la distancia euclidiana al destino.

**Nota sobre las pruebas:** el archivo proporcionado para la actividad contiene las listas de adyacencia y pesos, pero no proporciona coordenadas numéricas de los nodos. Por ello, los JSON incluidos definen coordenadas de prueba explícitas únicamente para poder evaluar la heurística euclidiana. Estas coordenadas no forman parte de los datos originales.

Si no se envían coordenadas, `h(n)=0`. En ese caso A* se comporta como búsqueda de costo uniforme; Greedy pierde información heurística y desempata por identificador.

## Salida

Los dos endpoints devuelven:

```json
{
  "total_nodos_visitados": 5,
  "solucion": true,
  "ruta": [["A", "D"], ["D", "F"]],
  "costo_total": 38.0,
  "T_n": "O(V^2 + E) (selección lineal manual de la frontera)",
  "S_n": "O(V + E)"
}
```

`ruta` se expresa como pares `(Vértice, Arista)` representados en JSON como `[origen, destino]`.

## Complejidad

En esta implementación no se utiliza una cola de prioridad especializada. La frontera se examina linealmente para encontrar el menor valor. En el peor caso esto produce una cota de tiempo de `O(V^2 + E)`. El almacenamiento del grafo, frontera, padres, costos y visitados requiere `O(V + E)`.

## Pruebas incluidas

Se incluyen tres archivos:

- `tests/test_grafo10.json`: A → J
- `tests/test_grafo25.json`: A → Y
- `tests/test_grafo50.json`: A → AX

Para probarlos, copiar el contenido del JSON correspondiente en Swagger (`/docs`) y ejecutarlo primero en `/search/greedy` y después en `/search/star`.

### Observación del grafo de 50 nodos

El grafo de 50 nodos contiene ramas que no son alcanzables desde `A`. Esto no es un error del algoritmo: la búsqueda únicamente puede recorrer nodos conectados mediante aristas dirigidas desde el origen. En una prueba donde el destino no sea alcanzable antes de agotarse la frontera o el límite de visitas, la API devuelve `"solucion": false`.

## Resultados

Los resultados exactos dependen de las coordenadas heurísticas y del límite configurado. Los JSON suministrados permiten reproducir las pruebas. Para documentar una ejecución, registrar la respuesta obtenida desde Swagger en la siguiente tabla:

| Grafo | Algoritmo | Origen | Destino | Límite default | Visitados | Solución | Ruta | Costo |
|---|---|---|---|---:|---:|---|---|---:|
| 10 | Greedy | A | J | 8 | ejecutar | ejecutar | ejecutar | ejecutar |
| 10 | A* | A | J | 8 | ejecutar | ejecutar | ejecutar | ejecutar |
| 25 | Greedy | A | Y | 20 | ejecutar | ejecutar | ejecutar | ejecutar |
| 25 | A* | A | Y | 20 | ejecutar | ejecutar | ejecutar | ejecutar |
| 50 | Greedy | A | AX | 40 | ejecutar | ejecutar | ejecutar | ejecutar |
| 50 | A* | A | AX | 40 | ejecutar | ejecutar | ejecutar | ejecutar |

## Conclusión

La actividad permite comparar dos estrategias informadas. Greedy toma decisiones únicamente con base en la estimación hacia el destino, mientras que A* combina dicha estimación con el costo acumulado. También se incorporó un límite de visitas configurable para observar el comportamiento de ambos métodos cuando no pueden explorar indefinidamente el grafo.
