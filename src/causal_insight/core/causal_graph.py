"""
═══════════════════════════════════════════════════════════════════════════════
CAUSAL GRAPH — WAD-GROUNDED DAG WITH PEARL'S CAUSAL CALCULUS
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from collections import defaultdict, deque
from datetime import datetime
import copy

from .constitution import *
from .causal_elements import *

class CausalGraph:
    """
    Directed Acyclic Graph (DAG) with WAD-fixed edge weights.
    Implements Pearl's causal calculus foundations.
    """

    def __init__(self, name: str = "CausalGraph"):
        self.name = name
        self.nodes: Dict[str, CausalNode] = {}
        self.edges: List[CausalEdge] = []
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)      # source → targets
        self.reverse_adjacency: Dict[str, Set[str]] = defaultdict(set)  # target → sources
        self.creation_time = datetime.now().isoformat()

    def add_node(self, node: CausalNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.name] = node
        self.adjacency.setdefault(node.name, set())
        self.reverse_adjacency.setdefault(node.name, set())

    def add_node_if_missing(self, name: str, node_type: str = "observed") -> None:
        """Add a node if it doesn't already exist."""
        if name not in self.nodes:
            self.add_node(CausalNode(name=name, node_type=node_type))

    def add_edge(self, edge: CausalEdge) -> None:
        """Add a causal edge to the graph."""
        # Ensure both nodes exist
        self.add_node_if_missing(edge.source)
        self.add_node_if_missing(edge.target)
        
        self.edges.append(edge)
        self.adjacency[edge.source].add(edge.target)
        self.reverse_adjacency[edge.target].add(edge.source)

    def get_parents(self, node: str) -> Set[str]:
        """Get all parents (direct causes) of a node."""
        return self.reverse_adjacency.get(node, set())

    def get_children(self, node: str) -> Set[str]:
        """Get all children (direct effects) of a node."""
        return self.adjacency.get(node, set())

    def get_ancestors(self, node: str) -> Set[str]:
        """Get all ancestors (indirect causes) of a node."""
        ancestors: Set[str] = set()
        queue = deque([node])
        visited = {node}
        
        while queue:
            current = queue.popleft()
            for parent in self.get_parents(current):
                if parent not in visited:
                    ancestors.add(parent)
                    visited.add(parent)
                    queue.append(parent)
        
        return ancestors

    def get_descendants(self, node: str) -> Set[str]:
        """Get all descendants (indirect effects) of a node."""
        descendants: Set[str] = set()
        queue = deque([node])
        visited = {node}
        
        while queue:
            current = queue.popleft()
            for child in self.get_children(current):
                if child not in visited:
                    descendants.add(child)
                    visited.add(child)
                    queue.append(child)
        
        return descendants

    def get_edge_between(self, source: str, target: str) -> Optional[CausalEdge]:
        """Get the edge between two nodes if it exists."""
        for edge in self.edges:
            if edge.source == source and edge.target == target:
                return edge
        return None

    def find_paths(self, source: str, target: str, max_length: int = 10) -> List[List[str]]:
        """Find all directed paths from source to target."""
        paths: List[List[str]] = []

        def dfs(current: str, path: List[str], visited: Set[str]):
            if len(path) > max_length:
                return
            if current == target:
                paths.append(path.copy())
                return
            for child in self.get_children(current):
                if child not in visited:
                    visited.add(child)
                    path.append(child)
                    dfs(child, path, visited)
                    path.pop()
                    visited.remove(child)

        if source in self.nodes and target in self.nodes:
            dfs(source, [source], {source})
        
        return paths

    def is_d_separated(self, X: Set[str], Y: Set[str], Z: Set[str]) -> bool:
        """Check if X and Y are d-separated given Z."""
        for x in X:
            for y in Y:
                for path in self.find_paths(x, y):
                    if not self._is_path_blocked(path, Z):
                        return False
        return True

    def _is_path_blocked(self, path: List[str], conditioning_set: Set[str]) -> bool:
        """Check if a path is blocked by a conditioning set."""
        for i in range(1, len(path) - 1):
            if path[i] in conditioning_set:
                return True
        return False

    def do_operation(self, intervention_node: str) -> 'CausalGraph':
        """Apply Pearl's do-operator — removes all edges pointing into intervention_node."""
        mutilated = CausalGraph(name=f"{self.name}_do_{intervention_node}")
        
        # Copy all nodes
        for node in self.nodes.values():
            mutilated.add_node(copy.deepcopy(node))
        
        # Copy edges except those pointing to intervention_node
        for edge in self.edges:
            if edge.target != intervention_node:
                mutilated.add_edge(copy.deepcopy(edge))
        
        return mutilated

    def has_cycle(self) -> bool:
        """Check if the graph contains a directed cycle."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for child in self.get_children(node):
                if child not in visited:
                    if dfs(child):
                        return True
                elif child in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def to_dict(self) -> Dict:
        """Serialize graph to dictionary."""
        return {
            "name": self.name,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "creation_time": self.creation_time,
            "has_cycle": self.has_cycle()
        }

    def visualize_ascii(self) -> str:
        """Create a simple ASCII visualization of the graph."""
        lines = [f"Causal Graph: {self.name}", "=" * 60, "\nNodes:"]
        
        for node in self.nodes.values():
            lines.append(f"  • {node.name} ({node.node_type})")
        
        lines.append("\nCausal Edges:")
        for edge in self.edges:
            arrow = "→" if edge.edge_type == EdgeType.DIRECTED else "↔"
            lines.append(f"  {edge.source} {arrow} {edge.target}")
            if edge.mechanism:
                lines.append(f"    Mechanism: {edge.mechanism}")
            lines.append(
                f"    Strength: {wformat(edge.strength_wad)} "
                f"| Confidence: {wpct(edge.confidence_wad)}"
            )
        
        return "\n".join(lines)
