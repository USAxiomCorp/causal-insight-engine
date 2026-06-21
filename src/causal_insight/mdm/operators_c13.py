"""
C13: WAD Entropy Minimization
Simple WAD-stable entropy-like measure and gradient step.
"""

from typing import List
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, SCALE


def wad_entropy(vec: List[int]) -> int:
    total = 0
    for x in vec:
        ax = x if x >= 0 else -x
        total += wad_mul(ax, ax)
    return total


class EntropyMinimizer:
    def step(self, vec: List[int], lr: int = SCALE // 100) -> List[int]:
        new_vec = []
        for x in vec:
            grad = wad_mul(x, 2 * SCALE)
            new_vec.append(x - wad_mul(lr, grad))
        return new_vec
