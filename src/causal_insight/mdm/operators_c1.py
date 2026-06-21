"""
C1: Hyperdimensional Riemannian Embedding (WAD-native)
Geodesic approximation on M with implicit identity metric.
"""

from typing import List
from .core import Manifold, wad_midpoint_path
from .wad_math import wad_vec_avg


class GeodesicSolver:
    def __init__(self, manifold: Manifold, steps: int = 32, refinements: int = 2):
        self.M = manifold
        self.steps = steps
        self.refinements = refinements

    def solve(self, x0: List[int], x1: List[int]) -> List[List[int]]:
        """
        Approximate geodesic between x0 and x1 in WAD space.
        """
        path = wad_midpoint_path(x0, x1, self.steps)

        for _ in range(self.refinements):
            new_path = [path[0]]
            for i in range(1, len(path) - 1):
                midpoint = wad_vec_avg(path[i - 1], path[i + 1])
                new_path.append(midpoint)
            new_path.append(path[-1])
            path = new_path

        return path
