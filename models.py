from typing import Dict, List, Optional, Tuple, Literal
from pydantic import BaseModel, Field, model_validator

AdjacencyList = Dict[str, List[Tuple[str, float]]]
Coordinates = Dict[str, Tuple[float, float]]

class SearchRequest(BaseModel):
    representation: Literal["lista", "matriz", "vector"] = "lista"
    graph: object
    nodes: Optional[List[str]] = None
    coordinates: Optional[Coordinates] = None
    origin: str
    destination: str
    visit_limit: Optional[int] = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_input(self):
        if self.representation in ("matriz", "vector") and not self.nodes:
            raise ValueError("Para matriz o vector debes enviar 'nodes' con el orden de los nodos.")
        return self

class SearchResponse(BaseModel):
    total_nodos_visitados: int
    solucion: bool
    ruta: List[Tuple[str, str]]
    costo_total: Optional[float] = None
    T_n: str
    S_n: str
