"""
Critical Path Engine for Phase 51.
Calculates longest dependency path and bottleneck timelines across strategic initiatives.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.base import StrategicInitiative
except ImportError:
    from app.services.strategy.base import StrategicInitiative

logger = logging.getLogger(__name__)


class CriticalPathEngine:
    """Calculates project timeline critical path, total duration weeks, and slack/float time."""

    def calculate_critical_path(
        self,
        initiatives: List[StrategicInitiative],
        dependencies: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Performs forward and backward pass CPM analysis to find the zero-float critical path."""
        duration_map = {init.initiative_code: init.estimated_duration_weeks for init in initiatives}
        title_map = {init.initiative_code: init.title for init in initiatives}

        # Build incoming and outgoing adjacency
        succs: Dict[str, List[str]] = {init.initiative_code: [] for init in initiatives}
        preds: Dict[str, List[str]] = {init.initiative_code: [] for init in initiatives}

        for dep in dependencies:
            src, tgt = dep["source_code"], dep["target_code"]
            if src in succs and tgt in preds:
                succs[src].append(tgt)
                preds[tgt].append(src)

        # Forward pass (Early Start, Early Finish)
        es: Dict[str, float] = {}
        ef: Dict[str, float] = {}

        # Topological sorting
        in_degree = {k: len(v) for k, v in preds.items()}
        queue = [k for k, v in in_degree.items() if v == 0]
        topo_order = []

        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            
            # ES = max(EF of preds)
            curr_es = max([ef.get(p, 0.0) for p in preds[curr]], default=0.0)
            curr_ef = curr_es + duration_map.get(curr, 4.0)
            es[curr] = curr_es
            ef[curr] = curr_ef

            for nxt in succs[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        total_duration = max(ef.values(), default=0.0)

        # Backward pass (Late Start, Late Finish)
        lf: Dict[str, float] = {}
        ls: Dict[str, float] = {}

        for curr in reversed(topo_order):
            if not succs[curr]:
                curr_lf = total_duration
            else:
                curr_lf = min([ls.get(s, total_duration) for s in succs[curr]], default=total_duration)
            
            curr_ls = curr_lf - duration_map.get(curr, 4.0)
            lf[curr] = curr_lf
            ls[curr] = curr_ls

        # Zero float indicates critical path
        critical_path_items = []
        for code in topo_order:
            float_val = round(ls.get(code, 0.0) - es.get(code, 0.0), 2)
            if float_val <= 0.01:
                critical_path_items.append({
                    "initiative_code": code,
                    "title": title_map.get(code, code),
                    "duration_weeks": duration_map.get(code, 4.0),
                    "early_start_weeks": es.get(code, 0.0),
                    "early_finish_weeks": ef.get(code, 0.0),
                })

        return {
            "total_timeline_weeks": round(total_duration, 1),
            "critical_path_length": len(critical_path_items),
            "critical_path_initiatives": critical_path_items,
            "summary": f"Strategic critical path spans {total_duration:.1f} weeks across {len(critical_path_items)} non-slack initiatives.",
        }
