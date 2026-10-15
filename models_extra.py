from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel, Field

class WeightedGraphRequest(BaseModel):
    graph: Dict[str, List[Tuple[str, float]]]
    origin: str
    destination: str

class TSPRequest(BaseModel):
    graph: Dict[str, List[Tuple[str, float]]]
    origin: str

class AlgorithmResponse(BaseModel):
    tiempo_ms: float
    memoria_bytes: int
    nodos_recorridos: int
    costo_camino: Optional[float]
    ruta: List[Tuple[str, str]]

class SyntheticGraphRequest(BaseModel):
    nodes: int = Field(ge=2, le=50)
    min_weight: int = Field(default=1, ge=1)
    max_weight: int = Field(default=100, ge=1)
    seed: Optional[int] = None
