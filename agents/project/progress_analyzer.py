"""Project progress and deterministic effort variance analyzer."""

from typing import Any, Dict, List


class ProjectProgressAnalyzer:
    """Computes deterministic task progress and effort variance metrics."""

    def calculate_progress(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not tasks:
            return {
                "overall_progress_percent": 0.0,
                "completed_count": 0,
                "total_count": 0,
                "estimated_hours": 0.0,
                "actual_hours": 0.0,
                "effort_variance_hours": 0.0,
            }

        total_count = len(tasks)
        completed_count = sum(1 for t in tasks if t.get("status") == "COMPLETED")
        
        # Weighted progress by estimated hours if available
        total_estimated = sum(float(t.get("estimated_hours") or 0.0) for t in tasks)
        total_actual = sum(float(t.get("actual_hours") or 0.0) for t in tasks)

        if total_estimated > 0:
            weighted_progress = sum(
                (float(t.get("progress_percent") or 0.0) / 100.0) * float(t.get("estimated_hours") or 0.0)
                for t in tasks
            )
            overall_progress = (weighted_progress / total_estimated) * 100.0
        else:
            overall_progress = (completed_count / total_count) * 100.0

        variance = total_actual - total_estimated

        return {
            "overall_progress_percent": round(overall_progress, 2),
            "completed_count": completed_count,
            "total_count": total_count,
            "estimated_hours": total_estimated,
            "actual_hours": total_actual,
            "effort_variance_hours": round(variance, 2),
        }
