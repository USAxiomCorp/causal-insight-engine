"""
C12: WAD Causal Graph Operator
Lightweight causal graph with WAD-weighted edges.
"""

from typing import Dict, List, Tuple
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, SCALE


class CausalGraph:
    def __init__(self):
        self.edges: Dict[Tuple[str, str], int] = {}

    def add_edge(self, a: str, b: str, weight_wad: int):
        self.edges[(a, b)] = weight_wad

    def parents(self, node: str) -> List[str]:
        return [a for (a, b) in self.edges if b == node]

    def children(self, node: str) -> List[str]:
        return [b for (a, b) in self.edges if a == node]

    def influence(self, a: str, b: str) -> int:
        return self.edges.get((a, b), 0)

    def propagate(self, values: Dict[str, int]) -> Dict[str, int]:
        out = values.copy()
        for (a, b), w in self.edges.items():
            out[b] = wad_add(out.get(b, 0), wad_mul(values.get(a, 0), w))
        return out
