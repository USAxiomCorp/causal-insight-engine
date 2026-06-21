"""
C17: WAD Hamiltonian Operator
Simple Hamiltonian dynamics in WAD space.
"""

from typing import List, Tuple
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, SCALE


class HamiltonianSystem:
    def __init__(self, mass: int = SCALE):
        self.mass = mass

    def step(self, q: List[int], p: List[int], dt: int = SCALE // 10) -> Tuple[List[int], List[int]]:
        q_new = [wad_add(qi, wad_mul(pi, dt)) for qi, pi in zip(q, p)]
        p_new = [wad_sub(pi, wad_mul(qi, dt)) for qi, pi in zip(q, p)]
        return q_new, p_new
