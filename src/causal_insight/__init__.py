"""
═══════════════════════════════════════════════════════════════════════════════
CAUSAL INSIGHT ENGINE — WAD-GROUNDED CAUSAL REASONING
═══════════════════════════════════════════════════════════════════════════════

A production-ready causal reasoning engine for pharmaceutical applications.
All arithmetic uses WAD (1e18) fixed-point precision.
═══════════════════════════════════════════════════════════════════════════════
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "WAD-grounded causal reasoning for pharmaceutical applications"

# Core components
from .core.constitution import *
from .core.causal_elements import *
from .core.causal_graph import CausalGraph
from .core.scm import StructuralCausalModel, StructuralEquation
from .core.inference import CausalInferenceEngine
from .core.counterfactual import CounterfactualEngine, CounterfactualQuery

# Domain components
from .domains.pharma import PharmaCausalGraph
from .domains.clinical_trials import ClinicalTrialSimulator

# API
from .api.server import app

__all__ = [
    # Core
    'WAD', 'to_wad', 'from_wad', 'wmul', 'wdiv', 'wadd', 'wsub',
    'wclamp', 'wabs', 'wformat', 'wpct',
    'WAD_ZERO', 'WAD_ONE', 'WAD_HALF',
    'WAD_95PCT', 'WAD_90PCT', 'WAD_85PCT', 'WAD_80PCT',
    'WAD_75PCT', 'WAD_70PCT', 'WAD_60PCT', 'WAD_50PCT',
    'CausalNode', 'CausalEdge', 'EdgeType',
    'CausalGraph',
    'StructuralCausalModel', 'StructuralEquation',
    'CausalInferenceEngine',
    'CounterfactualEngine', 'CounterfactualQuery',
    
    # Domains
    'PharmaCausalGraph',
    'ClinicalTrialSimulator',
    
    # API
    'app'
]

# Optional: verify WAD constitution at import
def verify():
    """Verify WAD constitutional mathematics."""
    try:
        from .core.constitution import verify_constitution
        verify_constitution()
        print("✅ WAD Constitutional Mathematics: VERIFIED")
        print(f"✅ Causal Insight Engine v{__version__} ready")
        return True
    except Exception as e:
        print(f"❌ WAD Constitution verification failed: {e}")
        return False

# Auto-verify on import
verify()
