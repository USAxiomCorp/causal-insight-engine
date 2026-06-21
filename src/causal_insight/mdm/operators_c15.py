"""
C15: WAD Adversarial Robustness
Projects vectors away from adversarial directions.
"""

from typing import List
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, SCALE


class AdversarialRobustness:
    def __init__(self, epsilon: int = SCALE // 50):
        self.epsilon = epsilon

    def defend(self, vec: List[int], adv: List[int]) -> List[int]:
        out = []
        for x, a in zip(vec, adv):
            adjust = wad_mul(a, self.epsilon)
            out.append(x - adjust)
        return out
