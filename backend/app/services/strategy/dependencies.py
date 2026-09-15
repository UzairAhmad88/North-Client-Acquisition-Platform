"""
Strategic Dependency & Conflict Engine for Phase 51.
Tracks initiative dependencies, detects circular blockers, and identifies goal conflicts.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


class DependencyEngine:
    """Manages directed dependency graphs among initiatives and detects circular blockages or goal conflicts."""

    def __init__(self):
        self._dependencies: List[Dict[str, Any]] = []

    def add_dependency(
        self,
        source_code: str,
        target_code: str,
        dependency_type: str = "FINISH_TO_START",
        is_critical_path: bool = False,
        lag_days: int = 0,
    ) -> Dict[str, Any]:
        """Registers a directed dependency: target_code depends on source_code."""
        dep = {
            "id": str(uuid.uuid4()),
            "source_code": source_code,
            "target_code": target_code,
            "dependency_type": dependency_type,
            "is_critical_path": is_critical_path,
            "lag_days": lag_days,
        }
        self._dependencies.append(dep)
        return dep

    def detect_circular_dependencies(self) -> List[List[str]]:
        """Finds any circular dependency loops using Depth First Search (DFS)."""
        adj: Dict[str, List[str]] = {}
        for d in self._dependencies:
            src, tgt = d["source_code"], d["target_code"]
            adj.setdefault(src, []).append(tgt)

        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, list(path))
                elif neighbor in rec_stack:
                    cycle = path[path.index(neighbor):] + [neighbor]
                    cycles.append(cycle)

            rec_stack.remove(node)

        for n in list(adj.keys()):
            if n not in visited:
                dfs(n, [])

        return cycles

    def detect_goal_conflicts(
        self,
        goals_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Detects contradictory goal pairings (e.g. Reduce Costs vs Increase Headcount)."""
        conflicts = []
        # Rules for goal conflict detection
        for i, g1 in enumerate(goals_data):
            for j, g2 in enumerate(goals_data):
                if i >= j:
                    continue
                
                cat1, cat2 = g1.get("category", ""), g2.get("category", "")
                t1, t2 = g1.get("target_delta_direction", ""), g2.get("target_delta_direction", "")

                # Cost reduction vs headcount expansion conflict
                if (cat1 == "COST" and t1 == "DECREASE" and cat2 == "HEADCOUNT" and t2 == "INCREASE") or \
                   (cat2 == "COST" and t2 == "DECREASE" and cat1 == "HEADCOUNT" and t1 == "INCREASE"):
                    conflicts.append({
                        "conflict_code": f"CONF-{uuid.uuid4().hex[:6].upper()}",
                        "title": "Cost Reduction vs Headcount Expansion Conflict",
                        "severity": "HIGH",
                        "goal_a": g1.get("name", "Goal A"),
                        "goal_b": g2.get("name", "Goal B"),
                        "description": "Operating expense reduction targets conflict with aggressive hiring commitments.",
                        "potential_resolution": "Sequence hiring post-efficiency gains or re-scope non-critical roles to automated workflows.",
                    })

        return conflicts
