"""
═══════════════════════════════════════════════════════════════════════════════
COUNTERFACTUAL ENGINE — ABDUCTION, ACTION, PREDICTION
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

from .constitution import *
from .causal_graph import CausalGraph
from .scm import StructuralCausalModel


@dataclass
class CounterfactualQuery:
    """
    A counterfactual query.
    
    Structure:
    - actual_world: Observed values in the real world
    - intervention: What we imagine changing
    - target_variable: What we want to know would change
    """
    actual_world: Dict[str, float]
    intervention: Dict[str, float]
    target_variable: str
    context: Dict = field(default_factory=dict)


@dataclass
class CounterfactualResult:
    """
    Results of a counterfactual query.
    
    All numeric results are WAD integers for deterministic reasoning.
    """
    query: CounterfactualQuery
    actual_outcome_wad: int
    counterfactual_outcome_wad: int
    effect_size_wad: int          # Signed — can be negative
    confidence_wad: int           # [0, WAD]
    causal_pathway: List[Dict]    # Steps in the causal chain
    explanation: str              # Human-readable explanation
    alternative_explanations: List[str]

    @property
    def actual_outcome(self) -> float:
        return from_wad(self.actual_outcome_wad)

    @property
    def counterfactual_outcome(self) -> float:
        return from_wad(self.counterfactual_outcome_wad)

    @property
    def effect_size(self) -> float:
        return from_wad(self.effect_size_wad)

    @property
    def confidence(self) -> float:
        return from_wad(self.confidence_wad)


class CounterfactualEngine:
    """
    Implements Pearl's three-step counterfactual reasoning:
    1. Abduction — Infer noise terms from observations
    2. Action — Apply intervention
    3. Prediction — Compute counterfactual outcome
    """
    
    def __init__(self, scm: StructuralCausalModel, graph: CausalGraph):
        self.scm = scm
        self.graph = graph
        self.logger = logging.getLogger("Counterfactual")

    def answer_why_question(self, query: CounterfactualQuery) -> CounterfactualResult:
        """
        Answer a "why" question by computing counterfactuals.
        
        Example: "Why did this patient survive?"
        """
        # Step 1 — Abduction: Infer noise terms
        noise_terms = self.scm._abduction(query.actual_world)

        # Step 2 — Actual world outcome
        actual_float = query.actual_world.get(query.target_variable, 0.0)

        # Step 3 — Counterfactual world outcome
        cf_world = self._compute_counterfactual_world(
            query.intervention, 
            noise_terms, 
            query.actual_world
        )
        cf_float = cf_world.get(query.target_variable, 0.0)

        # Convert to WAD
        actual_wad = to_wad(actual_float)
        cf_wad = to_wad(cf_float)
        effect_wad = wsub(cf_wad, actual_wad)  # Signed delta

        # Trace causal pathway
        pathway = self._trace_causal_pathway(
            query.intervention, 
            query.target_variable, 
            cf_world
        )
        
        # Assess confidence
        confidence_wad = self._assess_confidence_wad(pathway, effect_wad)
        
        # Generate explanation
        explanation = self._generate_explanation(
            query, actual_wad, cf_wad, effect_wad, pathway
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(query, pathway)

        return CounterfactualResult(
            query=query,
            actual_outcome_wad=actual_wad,
            counterfactual_outcome_wad=cf_wad,
            effect_size_wad=effect_wad,
            confidence_wad=confidence_wad,
            causal_pathway=pathway,
            explanation=explanation,
            alternative_explanations=alternatives
        )

    def _compute_counterfactual_world(self, intervention: Dict[str, float],
                                       noise_terms: Dict[str, float],
                                       actual_world: Dict[str, float]) -> Dict[str, float]:
        """
        Compute the counterfactual world under intervention.
        """
        # Start with intervention
        world = {**intervention}
        
        # Add noise terms
        world.update({f"U_{k}": v for k, v in noise_terms.items()})
        
        # Run through topological order
        topo = self.scm._topological_sort()
        
        for var in topo:
            if var in intervention:
                continue
            if var in self.scm.equations:
                eq = self.scm.equations[var]
                parent_values = {p: world.get(p, 0.0) for p in eq.parents}
                noise = noise_terms.get(f"U_{var}", 0.0)
                world[var] = eq.evaluate(parent_values, noise=noise)
        
        return world

    def _trace_causal_pathway(self, intervention: Dict[str, float], 
                               target: str, 
                               world: Dict[str, float]) -> List[Dict]:
        """
        Trace the causal pathway from intervention to target.
        """
        pathway = []
        
        for int_var in intervention:
            paths = self.graph.find_paths(int_var, target)
            if not paths:
                continue
            
            # Use the shortest path
            path = min(paths, key=len)
            
            for i in range(len(path) - 1):
                src, dst = path[i], path[i + 1]
                edge = next(
                    (e for e in self.graph.edges 
                     if e.source == src and e.target == dst), 
                    None
                )
                
                pathway.append({
                    "from": src,
                    "to": dst,
                    "value_from_wad": to_wad(world.get(src, 0.0)),
                    "value_to_wad": to_wad(world.get(dst, 0.0)),
                    "mechanism": edge.mechanism if edge else "Unknown mechanism",
                    "strength_wad": edge.strength_wad if edge else WAD_50PCT
                })
        
        return pathway

    def _assess_confidence_wad(self, pathway: List[Dict], effect_wad: int) -> int:
        """
        Assess confidence in the counterfactual result.
        """
        if not pathway:
            return WAD_50PCT
        
        # Average pathway strength
        avg_strength_wad = sum(s["strength_wad"] for s in pathway) // len(pathway)
        
        # Effect magnitude penalty for tiny effects
        effect_threshold = to_wad(0.1)
        if wabs(effect_wad) < effect_threshold:
            effect_confidence_wad = WAD_50PCT
        else:
            effect_confidence_wad = wclamp(wdiv(wabs(effect_wad), to_wad(2.0)))
        
        # Weighted combination: 70% pathway strength, 30% effect magnitude
        w70 = to_wad(0.7)
        w30 = to_wad(0.3)
        confidence = wadd(wmul(w70, avg_strength_wad), wmul(w30, effect_confidence_wad))
        
        return wclamp(confidence, WAD_ZERO, WAD_95PCT)

    def _generate_explanation(self, query: CounterfactualQuery,
                               actual_wad: int, cf_wad: int, 
                               effect_wad: int, pathway: List[Dict]) -> str:
        """
        Generate a human-readable explanation of the counterfactual.
        """
        parts = ["**WHY THIS OUTCOME OCCURRED:**\n"]
        parts.append(f"Actual outcome: {wformat(actual_wad)} [{actual_wad} WAD]\n")
        parts.append("\n**COUNTERFACTUAL ANALYSIS:**\n")
        
        direction = "increased" if effect_wad > 0 else "decreased" if effect_wad < 0 else "unchanged"
        parts.append(
            f"Under counterfactual intervention, outcome would have {direction} to: "
            f"{wformat(cf_wad)} [{cf_wad} WAD]\n"
        )
        parts.append(f"Effect size: {wformat(wabs(effect_wad))} [{effect_wad} WAD]\n")
        
        if pathway:
            parts.append("\n**CAUSAL PATHWAY:**\n")
            for i, step in enumerate(pathway, 1):
                parts.append(
                    f"{i}. {step['from']} [{wformat(step['value_from_wad'])}] "
                    f"→ {step['to']} [{wformat(step['value_to_wad'])}]\n"
                )
                parts.append(f"   Mechanism: {step['mechanism']}\n")
                parts.append(f"   Strength:  {wpct(step['strength_wad'])}\n")
        
        return "".join(parts)

    def _generate_alternatives(self, query: CounterfactualQuery,
                                pathway: List[Dict]) -> List[str]:
        """
        Generate alternative explanations.
        """
        alternatives = []
        
        if pathway:
            src = pathway[0]['from']
            tgt = pathway[-1]['to']
            all_paths = self.graph.find_paths(src, tgt)
            pathway_nodes = [pathway[0]['from']] + [s['to'] for s in pathway]
            
            for alt in all_paths:
                if alt != pathway_nodes:
                    alternatives.append(f"Alternative pathway: {' → '.join(alt)}")
        
        alternatives.append("Alternative: Unobserved confounding may affect results")
        alternatives.append("Alternative: Non-linear effects not captured in model")
        
        return alternatives[:3]
