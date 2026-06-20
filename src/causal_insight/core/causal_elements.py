"""
═══════════════════════════════════════════════════════════════════════════════
CAUSAL ELEMENTS — WAD-GROUNDED NODES AND EDGES
═══════════════════════════════════════════════════════════════════════════════
"""

from enum import Enum
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from .constitution import *

class EdgeType(Enum):
    """Types of causal edges in the graph."""
    DIRECTED   = "directed"      # A → B (causal arrow)
    BIDIRECTED = "bidirected"    # A ↔ B (unobserved confounder)
    UNDIRECTED = "undirected"    # A - B (unknown direction)

@dataclass
class CausalEdge:
    """
    A causal edge between two nodes.
    
    All numeric values are WAD integers — no floating point.
    """
    source: str
    target: str
    edge_type: EdgeType
    strength_wad: int = WAD_ONE          # Effect size, [0, WAD] or signed
    mechanism: str = ""                   # Description of causal mechanism
    confidence_wad: int = WAD_90PCT       # Epistemic confidence, [0, WAD]
    evidence: List[str] = field(default_factory=list)  # Supporting evidence

    def __post_init__(self):
        """Validate WAD values are in range."""
        if not (WAD_ZERO <= self.confidence_wad <= WAD_ONE):
            raise ValueError(f"confidence_wad must be in [0, WAD]. Got {self.confidence_wad}")
        # Strength can be negative for inhibitory effects
        if abs(self.strength_wad) > 7 * WAD:
            raise ValueError(f"strength_wad magnitude exceeds 7*WAD. Got {self.strength_wad}")

    def reverse(self) -> 'CausalEdge':
        """Return a reversed copy of this edge."""
        return CausalEdge(
            source=self.target,
            target=self.source,
            edge_type=self.edge_type,
            strength_wad=self.strength_wad,
            mechanism=f"Reverse: {self.mechanism}",
            confidence_wad=self.confidence_wad,
            evidence=self.evidence
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "source": self.source,
            "target": self.target,
            "type": self.edge_type.value,
            "strength_wad": self.strength_wad,
            "strength": wformat(self.strength_wad),
            "confidence_wad": self.confidence_wad,
            "confidence": wpct(self.confidence_wad),
            "mechanism": self.mechanism,
            "evidence": self.evidence
        }

@dataclass
class CausalNode:
    """
    A node in the causal graph.
    
    Represents a variable in the causal system.
    """
    name: str
    node_type: str = "observed"          # observed, intervention, outcome, latent
    domain: str = "continuous"           # continuous, binary, discrete, ordinal
    description: str = ""
    possible_values: Optional[List[Any]] = None
    observed_distribution: Optional[Dict] = None

    def __hash__(self):
        return hash(self.name)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "type": self.node_type,
            "domain": self.domain,
            "description": self.description
        }
