"""
═══════════════════════════════════════════════════════════════════════════════
PHARMACEUTICAL DOMAIN — WAD-GROUNDED CAUSAL GRAPHS
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Optional
from ..core.constitution import *
from ..core.causal_graph import CausalGraph
from ..core.causal_elements import CausalNode, CausalEdge, EdgeType


class PharmaCausalGraph(CausalGraph):
    """
    Pharmaceutical-specific causal graph with WAD arithmetic.
    
    Pre-built nodes and edges for clinical trial and drug development applications.
    """
    
    def __init__(self, name: str = "PharmaCausalGraph"):
        super().__init__(name)
        self._build_clinical_trial_structure()
    
    def _build_clinical_trial_structure(self):
        """Build the standard clinical trial causal structure."""
        # Add all nodes
        nodes = [
            # Demographic factors
            CausalNode("patient_age", "observed", "continuous", 
                      description="Patient age in years"),
            CausalNode("patient_sex", "observed", "binary", 
                      description="Patient biological sex"),
            CausalNode("patient_bmi", "observed", "continuous", 
                      description="Body mass index"),
            
            # Disease characteristics
            CausalNode("disease_severity", "observed", "continuous", 
                      description="Baseline disease severity score"),
            CausalNode("comorbidities", "observed", "continuous", 
                      description="Charlson comorbidity index"),
            
            # Intervention
            CausalNode("dosing_regimen", "intervention", "continuous", 
                      description="Drug dose and schedule"),
            CausalNode("treatment_arm", "intervention", "binary", 
                      description="Treatment vs control group assignment"),
            
            # Pharmacokinetics (latent)
            CausalNode("drug_absorption", "latent", "continuous", 
                      description="Rate of drug absorption"),
            CausalNode("drug_clearance", "latent", "continuous", 
                      description="Drug metabolism and elimination rate"),
            CausalNode("drug_exposure", "latent", "continuous", 
                      description="Area under the curve (AUC)"),
            
            # Pharmacodynamics
            CausalNode("target_engagement", "latent", "continuous", 
                      description="Target protein binding level"),
            CausalNode("biomarker_response", "observed", "continuous", 
                      description="Biomarker level after treatment"),
            
            # Outcomes
            CausalNode("efficacy_endpoint", "outcome", "continuous", 
                      description="Primary efficacy measure"),
            CausalNode("adverse_events", "outcome", "binary", 
                      description="Presence of adverse events"),
            CausalNode("patient_survival", "outcome", "binary", 
                      description="Patient survival status"),
            CausalNode("quality_of_life", "outcome", "continuous", 
                      description="Quality of life score"),
        ]
        
        for node in nodes:
            self.add_node(node)
        
        # Add causal edges with WAD strengths
        edges = [
            # Demographics → Disease
            CausalEdge("patient_age", "disease_severity", EdgeType.DIRECTED,
                      to_wad(0.3), "Age increases disease severity", WAD_80PCT),
            CausalEdge("patient_age", "comorbidities", EdgeType.DIRECTED,
                      to_wad(0.5), "Age increases comorbidity risk", WAD_85PCT),
            CausalEdge("patient_sex", "disease_severity", EdgeType.DIRECTED,
                      to_wad(0.15), "Sex influences disease severity", WAD_75PCT),
            CausalEdge("patient_bmi", "comorbidities", EdgeType.DIRECTED,
                      to_wad(0.4), "BMI affects comorbidity risk", WAD_80PCT),
            
            # Disease → Outcomes
            CausalEdge("disease_severity", "efficacy_endpoint", EdgeType.DIRECTED,
                      to_wad(-0.6), "Higher severity reduces efficacy", WAD_85PCT),
            CausalEdge("disease_severity", "adverse_events", EdgeType.DIRECTED,
                      to_wad(0.4), "Higher severity increases AE risk", WAD_80PCT),
            CausalEdge("disease_severity", "patient_survival", EdgeType.DIRECTED,
                      to_wad(-0.7), "Higher severity reduces survival", WAD_90PCT),
            CausalEdge("comorbidities", "adverse_events", EdgeType.DIRECTED,
                      to_wad(0.6), "Comorbidities increase AE risk", WAD_85PCT),
            
            # Treatment → Drug Exposure
            CausalEdge("dosing_regimen", "drug_absorption", EdgeType.DIRECTED,
                      to_wad(0.8), "Higher dose increases absorption", WAD_90PCT),
            CausalEdge("treatment_arm", "dosing_regimen", EdgeType.DIRECTED,
                      to_wad(1.0), "Treatment arm determines dosing", WAD_95PCT),
            
            # Patient factors → Pharmacokinetics
            CausalEdge("patient_age", "drug_clearance", EdgeType.DIRECTED,
                      to_wad(-0.5), "Age reduces drug clearance", WAD_85PCT),
            CausalEdge("patient_bmi", "drug_clearance", EdgeType.DIRECTED,
                      to_wad(0.3), "Higher BMI affects clearance", WAD_78PCT),
            
            # Pharmacokinetics → Pharmacodynamics
            CausalEdge("drug_absorption", "drug_exposure", EdgeType.DIRECTED,
                      to_wad(0.9), "Absorption determines exposure", WAD_92PCT),
            CausalEdge("drug_clearance", "drug_exposure", EdgeType.DIRECTED,
                      to_wad(-0.8), "Clearance reduces exposure", WAD_90PCT),
            CausalEdge("drug_exposure", "target_engagement", EdgeType.DIRECTED,
                      to_wad(0.85), "Exposure drives target engagement", WAD_88PCT),
            
            # Pharmacodynamics → Biomarker
            CausalEdge("target_engagement", "biomarker_response", EdgeType.DIRECTED,
                      to_wad(0.7), "Target engagement changes biomarker", WAD_85PCT),
            
            # Biomarker → Outcomes
            CausalEdge("biomarker_response", "efficacy_endpoint", EdgeType.DIRECTED,
                      to_wad(0.85), "Biomarker predicts efficacy", WAD_90PCT),
            CausalEdge("biomarker_response", "patient_survival", EdgeType.DIRECTED,
                      to_wad(0.65), "Biomarker predicts survival", WAD_85PCT),
            
            # Direct treatment effects
            CausalEdge("target_engagement", "adverse_events", EdgeType.DIRECTED,
                      to_wad(0.5), "Target engagement causes AEs", WAD_78PCT),
            CausalEdge("target_engagement", "patient_survival", EdgeType.DIRECTED,
                      to_wad(0.8), "Target engagement improves survival", WAD_88PCT),
            
            # Outcomes interconnections
            CausalEdge("efficacy_endpoint", "patient_survival", EdgeType.DIRECTED,
                      to_wad(0.75), "Better efficacy improves survival", WAD_85PCT),
            CausalEdge("adverse_events", "quality_of_life", EdgeType.DIRECTED,
                      to_wad(-0.6), "AEs reduce quality of life", WAD_82PCT),
            CausalEdge("efficacy_endpoint", "quality_of_life", EdgeType.DIRECTED,
                      to_wad(0.5), "Better efficacy improves QoL", WAD_80PCT),
        ]
        
        for edge in edges:
            self.add_edge(edge)
    
    def get_clinical_trial_subgraph(self) -> CausalGraph:
        """Return a focused subgraph for clinical trial analysis."""
        subgraph = CausalGraph(f"{self.name}_ClinicalTrial")
        
        # Key nodes for clinical trials
        trial_nodes = [
            "dosing_regimen",
            "treatment_arm",
            "biomarker_response",
            "efficacy_endpoint",
            "adverse_events",
            "patient_survival",
            "patient_age",
            "disease_severity",
            "comorbidities"
        ]
        
        # Copy nodes
        for node_name in trial_nodes:
            if node_name in self.nodes:
                subgraph.add_node(self.nodes[node_name])
        
        # Copy edges between trial nodes
        for edge in self.edges:
            if edge.source in trial_nodes and edge.target in trial_nodes:
                subgraph.add_edge(edge)
        
        return subgraph
    
    def get_drug_discovery_subgraph(self) -> CausalGraph:
        """Return a focused subgraph for drug discovery applications."""
        subgraph = CausalGraph(f"{self.name}_DrugDiscovery")
        
        # Key nodes for drug discovery
        discovery_nodes = [
            "dosing_regimen",
            "drug_absorption",
            "drug_clearance",
            "drug_exposure",
            "target_engagement",
            "biomarker_response",
            "efficacy_endpoint",
            "adverse_events"
        ]
        
        # Copy nodes
        for node_name in discovery_nodes:
            if node_name in self.nodes:
                subgraph.add_node(self.nodes[node_name])
        
        # Copy edges between discovery nodes
        for edge in self.edges:
            if edge.source in discovery_nodes and edge.target in discovery_nodes:
                subgraph.add_edge(edge)
        
        return subgraph
