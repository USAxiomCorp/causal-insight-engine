"""
MDM Core Model (WAD-native)
M: manifold
g(x): metric (implicit identity)
A: axioms
S: constraint manifold
anchors, safety gates, deterministic replay
"""

from dataclasses import dataclass
from typing import Callable, List, Any
from .wad_math import wad_vec_avg, wad_add, wad_mul, wad_div, SCALE


@dataclass
class Axiom:
    axiom_id: str
    confidence_wad: int
    proof_ref: str | None = None


@dataclass
class Anchor:
    axiom: Axiom


class Manifold:
    """
    Conceptual manifold M in WAD coordinates.
    """
    def __init__(self, dim: int):
        self.dim = dim


class ConstraintManifold:
    """
    Ethical/safety constraint manifold S.
    """
    def __init__(self, project_fn: Callable[[list[int]], list[int]] | None = None):
        self.project_fn = project_fn or (lambda x: x)

    def project(self, x: list[int]) -> list[int]:
        return self.project_fn(x)


class SafetyGate:
    """
    G_i: M -> {0,1} in WAD space.
    """
    def __init__(self, fn: Callable[[list[int]], bool]):
        self.fn = fn

    def check(self, x: list[int]) -> bool:
        return bool(self.fn(x))


class DeterministicReplay:
    """
    Deterministic event log for replay.
    """
    def __init__(self):
        self._events: List[Any] = []

    def record(self, event: Any) -> None:
        self._events.append(event)

    def events(self) -> List[Any]:
        return list(self._events)


def wad_midpoint_path(p0: list[int], p1: list[int], steps: int) -> list[list[int]]:
    """
    WAD-linear interpolation between two WAD vectors.
    """
    if steps < 2:
        return [p0, p1]

    path = []
    for i in range(steps):
        t_num = i
        t_den = steps - 1

        # t in WAD
        t = wad_div(t_num * SCALE, t_den * SCALE)
        one_minus_t = SCALE - t

        point = [
            wad_div(wad_add(wad_mul(one_minus_t, x0), wad_mul(t, x1)), SCALE)
            for x0, x1 in zip(p0, p1)
        ]
        path.append(point)

    return path
