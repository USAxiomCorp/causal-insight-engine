"""
═══════════════════════════════════════════════════════════════════════════════
CAUSAL INFERENCE ENGINE — IDENTIFICATION & ADJUSTMENT
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Set, Tuple, Optional, List
from itertools import combinations
import logging

from .constitution import *
from .causal_graph import CausalGraph

class CausalInferenceEngine:
    """
    Determines if causal effects are identifiable and computes adjustment sets.
    """
    
    def __init__(self, graph: CausalGraph):
        self.graph = graph
        self.logger = logging.getLogger("CausalInference")

    def is_identifiable(self, treatment: str, outcome: str,
                        observed: Set[str]) -> Tuple[bool, str]:
        """
        Check if causal effect P(Y|do(X)) is identifiable.
        
        Tests back-door, front-door, and instrumental variable criteria.
        """
        # Back-door criterion
        ok, adjustment = self._check_backdoor_criterion(treatment, outcome, observed)
        if ok:
            return True, f"Identifiable via back-door adjustment: {adjustment}"
        
        # Front-door criterion
        ok, mediator = self._check_frontdoor_criterion(treatment, outcome, observed)
        if ok:
            return True, f"Identifiable via front-door adjustment: {mediator}"
        
        # Instrumental variables
        ok, instruments = self._check_instrumental_variables(treatment, outcome, observed)
        if ok:
            return True, f"Identifiable via instrumental variables: {instruments}"
        
        return False, "Causal effect not identifiable from observational data"

    def _check_backdoor_criterion(self, treatment: str, outcome: str,
                                   observed: Set[str]) -> Tuple[bool, Optional[Set[str]]]:
        """
        Check if a set Z satisfies back-door criterion:
        1. Z blocks all back-door paths from X to Y
        2. No Z is a descendant of X
        """
        backdoor_paths = self._find_backdoor_paths(treatment, outcome)
        
        if not backdoor_paths:
            return True, set()
        
        # Check all subsets of observed variables
        for size in range(len(observed) + 1):
            for candidate in combinations(observed, size):
                z_set = set(candidate)
                
                # No Z should be a descendant of treatment
                if any(n in self.graph.get_descendants(treatment) for n in z_set):
                    continue
                
                # Z should block all backdoor paths
                if self._blocks_all_paths(backdoor_paths, z_set):
                    return True, z_set
        
        return False, None

    def _check_frontdoor_criterion(self, treatment: str, outcome: str,
                                    observed: Set[str]) -> Tuple[bool, Optional[Set[str]]]:
        """
        Check if a set M satisfies front-door criterion:
        1. M intercepts all directed paths from X to Y
        2. No back-door path from X to M
        3. X blocks all back-door paths from M to Y
        """
        all_paths = self.graph.find_paths(treatment, outcome)
        
        if not all_paths:
            return False, None
        
        # Find a mediator that intercepts all paths
        for size in range(1, len(observed) + 1):
            for candidate in combinations(observed, size):
                m_set = set(candidate)
                
                # M should intercept all paths from X to Y
                if self._intercepts_all_paths(all_paths, m_set):
                    return True, m_set
        
        return False, None

    def _check_instrumental_variables(self, treatment: str, outcome: str,
                                       observed: Set[str]) -> Tuple[bool, Optional[Set[str]]]:
        """
        Check for instrumental variables.
        An instrument Z must:
        1. Affect treatment (Z is ancestor of X)
        2. Not affect outcome except through treatment
        """
        instruments = set()
        
        for candidate in observed:
            # Z should be an ancestor of treatment
            if treatment not in self.graph.get_descendants(candidate):
                continue
            
            # Z should not directly affect outcome
            if outcome in self.graph.get_children(candidate):
                continue
            
            instruments.add(candidate)
        
        return len(instruments) > 0, instruments or None

    def _find_backdoor_paths(self, treatment: str, outcome: str) -> List[List[str]]:
        """Find all back-door paths from treatment to outcome."""
        paths = []
        
        # Back-door paths go from treatment to a parent, then to outcome
        for parent in self.graph.get_parents(treatment):
            for path in self.graph.find_paths(parent, outcome):
                paths.append([treatment] + path)
        
        return paths

    def _blocks_all_paths(self, paths: List[List[str]], blocking_set: Set[str]) -> bool:
        """Check if a set blocks all paths."""
        return all(self.graph._is_path_blocked(p, blocking_set) for p in paths)

    def _intercepts_all_paths(self, paths: List[List[str]], intercept_set: Set[str]) -> bool:
        """Check if a set intercepts all paths."""
        return all(any(n in intercept_set for n in p[1:-1]) for p in paths)

    def compute_adjustment_formula(self, treatment: str, outcome: str,
                                    adjustment_set: Set[str]) -> str:
        """
        Generate the adjustment formula for a given adjustment set.
        """
        if not adjustment_set:
            return f"P({outcome}|do({treatment})) = P({outcome}|{treatment})"
        
        z = ", ".join(sorted(adjustment_set))
        return f"P({outcome}|do({treatment})) = Σ_{{{z}}} P({outcome}|{treatment},{z}) P({z})"
