"""
═══════════════════════════════════════════════════════════════════════════════
CLINICAL TRIAL SIMULATOR — WAD-GROUNDED TRIAL SIMULATION
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import logging

from ..core.constitution import *
from ..core.causal_graph import CausalGraph
from ..core.scm import StructuralCausalModel, StructuralEquation
from ..core.inference import CausalInferenceEngine
from ..core.counterfactual import CounterfactualEngine, CounterfactualQuery

from .pharma import PharmaCausalGraph


class ClinicalTrialSimulator:
    """
    Clinical trial simulator using WAD-grounded causal reasoning.
    
    Simulates trials, optimizes dosing, and predicts outcomes.
    All numeric values use WAD arithmetic for precision and auditability.
    """
    
    def __init__(self, graph: Optional[PharmaCausalGraph] = None):
        """
        Initialize the simulator.
        
        Args:
            graph: Pre-built PharmaCausalGraph, or create default
        """
        self.graph = graph if graph else PharmaCausalGraph()
        self.scm = self._build_scm()
        self.inference_engine = CausalInferenceEngine(self.graph)
        self.counterfactual_engine = CounterfactualEngine(self.scm, self.graph)
        self.logger = logging.getLogger("ClinicalTrialSimulator")
    
    def _build_scm(self) -> StructuralCausalModel:
        """Build the Structural Causal Model from the graph."""
        scm = StructuralCausalModel(f"SCM_{self.graph.name}")
        scm.set_causal_graph(self.graph)
        
        for node_name, node in self.graph.nodes.items():
            parents = list(self.graph.get_parents(node_name))
            parent_edges = [
                e for e in self.graph.edges
                if e.target == node_name and e.edge_type == EdgeType.DIRECTED
            ]
            
            def make_fn(edges: List[CausalEdge]) -> callable:
                """Create the structural equation function."""
                def fn(pvals: Dict[str, float], noise: float) -> float:
                    total = noise
                    for e in edges:
                        strength = from_wad(e.strength_wad)
                        total += strength * pvals.get(e.source, 0.0)
                    return total
                return fn
            
            scm.add_equation(StructuralEquation(
                variable=node_name,
                parents=parents,
                function=make_fn(parent_edges),
                noise_distribution="normal",
                noise_params={"mean_wad": 0, "std_wad": to_wad(0.1)},
                description=f"Linear structural equation for {node_name}"
            ))
        
        return scm
    
    def simulate_trial(self, 
                       dosing: float, 
                       n_patients: int = 1000,
                       patient_profile: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Simulate a clinical trial with given dosing regimen.
        
        Args:
            dosing: The dosing regimen to test
            n_patients: Number of patients to simulate
            patient_profile: Optional distribution parameters for patients
        
        Returns:
            Dictionary with trial results
        """
        # Set up interventions
        interventions = {"dosing_regimen": dosing}
        
        # Simulate
        samples = self.scm.simulate(n_patients, interventions)
        
        # Compute WAD-scaled outcomes
        efficacy_wad = to_wad(np.mean(samples['efficacy_endpoint']))
        safety_wad = to_wad(1.0 - np.mean(samples['adverse_events']))
        survival_wad = to_wad(np.mean(samples['patient_survival']))
        
        # Confidence based on effect sizes
        confidence_wad = self._compute_trial_confidence(samples)
        
        return {
            'efficacy_wad': efficacy_wad,
            'safety_wad': safety_wad,
            'survival_wad': survival_wad,
            'efficacy': from_wad(efficacy_wad),
            'safety': from_wad(safety_wad),
            'survival': from_wad(survival_wad),
            'n_patients': n_patients,
            'dosing': dosing,
            'samples': samples,
            'confidence_wad': confidence_wad,
            'confidence': from_wad(confidence_wad)
        }
    
    def _compute_trial_confidence(self, samples: Dict[str, np.ndarray]) -> int:
        """Compute confidence in trial results."""
        # Get outcome variance
        efficacy_var = np.var(samples['efficacy_endpoint'])
        safety_var = np.var(samples['adverse_events'])
        
        # Higher variance = lower confidence
        max_var = 0.25  # Maximum expected variance
        efficacy_confidence = 1.0 - (efficacy_var / max_var)
        safety_confidence = 1.0 - (safety_var / max_var)
        
        # Clamp and convert to WAD
        avg_confidence = max(0.5, (efficacy_confidence + safety_confidence) / 2)
        return to_wad(min(0.95, avg_confidence))
    
    def optimize_dosing(self, 
                        efficacy_weight: float = 0.5,
                        safety_weight: float = 0.5,
                        n_patients: int = 1000) -> Dict[str, Any]:
        """
        Find optimal dosing regimen.
        
        Args:
            efficacy_weight: Weight for efficacy in objective (0-1)
            safety_weight: Weight for safety in objective (0-1)
            n_patients: Number of patients per simulation
        
        Returns:
            Dictionary with optimal dosing results
        """
        best_dose = 0.0
        best_score = 0.0
        results = []
        
        # Search across dosing range
        for dose in np.linspace(0.1, 2.0, 20):
            result = self.simulate_trial(dose, n_patients)
            
            # WAD-weighted objective
            efficacy_wad = result['efficacy_wad']
            safety_wad = result['safety_wad']
            
            # Weighted composite score
            eff_w = to_wad(efficacy_weight)
            safe_w = to_wad(safety_weight)
            
            score_wad = wadd(
                wmul(eff_w, efficacy_wad),
                wmul(safe_w, safety_wad)
            )
            
            results.append({
                'dose': dose,
                'efficacy_wad': efficacy_wad,
                'safety_wad': safety_wad,
                'score_wad': score_wad,
                'score': from_wad(score_wad)
            })
            
            if score_wad > best_score:
                best_score = score_wad
                best_dose = dose
        
        return {
            'optimal_dose': best_dose,
            'optimal_score_wad': best_score,
            'optimal_score': from_wad(best_score),
            'results': results,
            'recommendation': f"Recommended dose: {best_dose:.2f}",
            'confidence_wad': WAD_85PCT
        }
    
    def predict_outcome(self, 
                        intervention: Dict[str, float],
                        target_variable: str = "efficacy_endpoint") -> Dict[str, Any]:
        """
        Predict outcome under intervention.
        
        Args:
            intervention: Dictionary of variables to intervene on
            target_variable: Variable to predict
        
        Returns:
            Dictionary with prediction results
        """
        # Check identifiability
        treatment = list(intervention.keys())[0] if intervention else None
        identifiable, adjustment = self.inference_engine.is_identifiable(
            treatment=treatment,
            outcome=target_variable,
            observed=set(self.graph.nodes.keys())
        ) if treatment else (False, None)
        
        # Simulate intervention
        samples = self.scm.simulate(
            n_samples=1000,
            interventions=intervention
        )
        
        predicted_wad = to_wad(np.mean(samples[target_variable]))
        
        return {
            'target_variable': target_variable,
            'predicted_wad': predicted_wad,
            'predicted': from_wad(predicted_wad),
            'identifiable': identifiable,
            'adjustment_set': adjustment,
            'confidence_wad': WAD_85PCT if identifiable else WAD_60PCT,
            'intervention': intervention
        }
    
    def answer_why(self, 
                   actual_world: Dict[str, float],
                   intervention: Dict[str, float],
                   target_variable: str) -> Dict[str, Any]:
        """
        Answer "why" questions using counterfactual reasoning.
        
        Args:
            actual_world: Observed values
            intervention: Counterfactual intervention
            target_variable: Target variable to explain
        
        Returns:
            Dictionary with counterfactual analysis
        """
        query = CounterfactualQuery(
            actual_world=actual_world,
            intervention=intervention,
            target_variable=target_variable
        )
        
        result = self.counterfactual_engine.answer_why_question(query)
        
        return {
            'actual_outcome_wad': result.actual_outcome_wad,
            'counterfactual_outcome_wad': result.counterfactual_outcome_wad,
            'effect_size_wad': result.effect_size_wad,
            'confidence_wad': result.confidence_wad,
            'explanation': result.explanation,
            'causal_pathway': result.causal_pathway,
            'alternatives': result.alternative_explanations
        }
    
    def get_graph_visualization(self) -> str:
        """Get ASCII visualization of the causal graph."""
        return self.graph.visualize_ascii()
    
    def get_graph_dict(self) -> Dict:
        """Get the causal graph as a dictionary."""
        return self.graph.to_dict()
