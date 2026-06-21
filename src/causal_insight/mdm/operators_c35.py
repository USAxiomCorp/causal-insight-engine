"""
C35: Ethical Constraint Manifold (WAD-native)
Implements proximal projection onto ethical constraints.

Given a proposed step x', solve:
    x* = argmin_x ||x - x'||^2 + λ Σ [h_i(x)]_+

Where h_i(x) are constraint functions returning WAD integers.
"""

from typing import List, Callable
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, wad_vec_avg, SCALE


def relu_wad(x: int) -> int:
    return x if x > 0 else 0


class EthicalProjection:
    def __init__(self, constraints: List[Callable[[List[int]], int]], lam: int = SCALE // 10):
        """
        constraints: list of functions h_i(x) -> WAD int
        lam: WAD penalty weight
        """
        self.constraints = constraints
        self.lam = lam

    def project(self, x: List[int]) -> List[int]:
        """
        Simple proximal step:
        x_new = x - λ * grad(h_i(x)) approx via sign of violation.
        """
        x_new = x[:]

        for h in self.constraints:
            violation = h(x_new)
            if violation > 0:
                # Push back proportionally to violation
                adjust = violation // len(x_new)
                x_new = [xi - adjust for xi in x_new]

        return x_new
