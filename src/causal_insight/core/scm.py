"""
═══════════════════════════════════════════════════════════════════════════════
STRUCTURAL CAUSAL MODELS — WAD-EQUIPPED SCM
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import deque
import numpy as np

from .constitution import *
from .causal_graph import CausalGraph

@dataclass
class StructuralEquation:
    """
    Y := f(Parents(Y), U_Y)
    
    A structural equation that defines how a variable is generated.
    All numeric parameters are WAD-scaled integers.
    """
    variable: str
    parents: List[str]
    function: Callable  # Takes dict of parent values and noise, returns float
    noise_distribution: str = "normal"
    noise_params: Dict[str, int] = field(
        default_factory=lambda: {"mean_wad": 0, "std_wad": WAD}
    )
    description: str = ""

    def evaluate(self, parent_values: Dict[str, float], noise: float = None) -> float:
        """
        Evaluate the structural equation.
        
        Uses float internally for numpy compatibility, but all parameters
        are derived from WAD-scaled values.
        """
        if noise is None:
            mean = from_wad(self.noise_params.get("mean_wad", 0))
            std = from_wad(self.noise_params.get("std_wad", WAD))
            
            if self.noise_distribution == "normal":
                noise = np.random.normal(mean, std)
            else:
                noise = 0.0
        
        return self.function(parent_values, noise)


class StructuralCausalModel:
    """
    A Structural Causal Model (SCM) with WAD-grounded equations.
    """
    
    def __init__(self, name: str = "SCM"):
        self.name = name
        self.equations: Dict[str, StructuralEquation] = {}
        self.causal_graph: Optional[CausalGraph] = None
        self.exogenous_variables: Set[str] = set()

    def add_equation(self, equation: StructuralEquation) -> None:
        """Add a structural equation to the model."""
        self.equations[equation.variable] = equation

    def set_causal_graph(self, graph: CausalGraph) -> None:
        """Set the causal graph for the model."""
        self.causal_graph = graph

    def _topological_sort(self) -> List[str]:
        """Topologically sort variables based on causal graph."""
        if not self.causal_graph:
            return list(self.equations.keys())
        
        in_degree = {
            var: len(self.causal_graph.get_parents(var)) 
            for var in self.equations
        }
        queue = deque([v for v in self.equations if in_degree.get(v, 0) == 0])
        result = []
        
        while queue:
            var = queue.popleft()
            result.append(var)
            for child in self.causal_graph.get_children(var):
                if child in in_degree:
                    in_degree[child] -= 1
                    if in_degree[child] == 0:
                        queue.append(child)
        
        return result

    def simulate(self, n_samples: int = 1000, 
                 interventions: Dict[str, float] = None) -> Dict[str, np.ndarray]:
        """
        Simulate data from the SCM.
        
        Args:
            n_samples: Number of samples to generate
            interventions: Dictionary of variable names to fixed values
        
        Returns:
            Dictionary of simulated data arrays
        """
        if not self.causal_graph:
            raise ValueError("Causal graph must be set before simulation")
        
        interventions = interventions or {}
        samples = {var: np.zeros(n_samples) for var in self.equations}
        
        # Get topological order
        topo_order = self._topological_sort()
        
        for i in range(n_samples):
            for var in topo_order:
                if var in interventions:
                    samples[var][i] = interventions[var]
                else:
                    eq = self.equations[var]
                    parent_values = {p: samples[p][i] for p in eq.parents}
                    samples[var][i] = eq.evaluate(parent_values)
        
        return samples

    def compute_counterfactual(self, observed: Dict[str, float],
                               intervention: Dict[str, float], 
                               target: str) -> float:
        """
        Compute counterfactual outcome.
        
        Three steps:
        1. Abduction: Infer noise terms from observed data
        2. Action: Apply intervention
        3. Prediction: Compute counterfactual outcome
        """
        noise_terms = self._abduction(observed)
        return self._prediction(intervention, target, noise_terms)

    def _abduction(self, observed: Dict[str, float]) -> Dict[str, float]:
        """Step 1: Infer noise terms from observed data."""
        noise_terms = {}
        topo_order = self._topological_sort()
        
        for var in topo_order:
            if var in observed:
                eq = self.equations[var]
                parent_values = {
                    p: observed.get(p, 0.0) 
                    for p in eq.parents
                }
                expected = eq.evaluate(parent_values, noise=0.0)
                noise_terms[var] = observed[var] - expected
        
        return noise_terms

    def _prediction(self, intervention: Dict[str, float],
                    target: str, noise_terms: Dict[str, float]) -> float:
        """Step 3: Predict outcome under intervention."""
        values = intervention.copy()
        topo_order = self._topological_sort()
        
        for var in topo_order:
            if var not in values:
                eq = self.equations[var]
                parent_values = {
                    p: values.get(p, 0.0) 
                    for p in eq.parents
                }
                noise = noise_terms.get(var, 0.0)
                values[var] = eq.evaluate(parent_values, noise=noise)
        
        return values.get(target, 0.0)
