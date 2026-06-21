"""
C6: Topological Invariant Conservation (WAD-native)
Simplified persistent-homology-style invariant extractor.

This does NOT compute full barcodes (requires heavy libs).
Instead, it computes WAD-stable invariants:
- WAD L1 norm
- WAD L-infinity norm
- Sign-change count
These remain stable under admissible transforms.
"""

from typing import List
from .wad_math import wad_add, wad_sub, wad_mul, wad_div, SCALE


def wad_abs(x: int) -> int:
    return x if x >= 0 else -x


def wad_l1(vec: List[int]) -> int:
    total = 0
    for x in vec:
        total += wad_abs(x)
    return total


def wad_linf(vec: List[int]) -> int:
    m = 0
    for x in vec:
        ax = wad_abs(x)
        if ax > m:
            m = ax
    return m


def sign_changes(vec: List[int]) -> int:
    count = 0
    for i in range(1, len(vec)):
        if (vec[i] >= 0 and vec[i-1] < 0) or (vec[i] < 0 and vec[i-1] >= 0):
            count += 1
    return count


class TopologicalInvariants:
    """
    Computes stable invariants for constraint checking.
    """

    def compute(self, vec: List[int]) -> dict:
        return {
            "l1": wad_l1(vec),
            "linf": wad_linf(vec),
            "sign_changes": sign_changes(vec),
        }

    def preserved(self, before: dict, after: dict, tolerance: int = SCALE // 1000) -> bool:
        """
        Check if invariants are preserved within tolerance.
        """
        for key in before:
            if key not in after:
                return False
            if wad_abs(before[key] - after[key]) > tolerance:
                return False
        return True
