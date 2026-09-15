"""
Sprint Iteration Execution, Release Planning, and Deterministic Readiness Gates Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.product_management.base import (
    SprintStatus,
    ReleaseReadinessStatus,
)


class SprintReleaseManager:
    """Manages sprint iterations, release scoping, and deterministic release readiness gates."""

    def __init__(self):
        self._sprints: Dict[str, List[Dict[str, Any]]] = {}
        self._releases: Dict[str, List[Dict[str, Any]]] = {}

    # Sprints
    def create_sprint(
        self,
        product_id: str,
        name: str,
        sprint_goal: Optional[str] = None,
        capacity_points: int = 40,
        committed_points: int = 36,
        **kwargs,
    ) -> Dict[str, Any]:
        """Initialize sprint iteration."""
        s_id = f"sprint_{uuid.uuid4().hex[:12]}"
        sprint = {
            "id": s_id,
            "product_id": product_id,
            "name": name,
            "sprint_goal": sprint_goal or kwargs.get("goal", f"Deliver sprint goals for {name}"),
            "capacity_points": capacity_points,
            "committed_points": committed_points,
            "completed_points": 0,
            "start_date": kwargs.get("start_date"),
            "end_date": kwargs.get("end_date"),
            "status": "planning",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._sprints.setdefault(product_id, []).append(sprint)
        return sprint

    def start_sprint(self, sprint_id: str) -> Dict[str, Any]:
        for sprint_list in self._sprints.values():
            for s in sprint_list:
                if s["id"] == sprint_id:
                    s["status"] = "active"
                    return s
        return {"id": sprint_id, "status": "active"}

    def list_sprints(self, product_id: str) -> List[Dict[str, Any]]:
        return self._sprints.get(product_id, [])

    # Releases
    def create_release(
        self,
        product_id: str,
        version_tag: Optional[str] = None,
        release_name: Optional[str] = None,
        scope_summary: Optional[str] = None,
        rollback_plan: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create planned release container."""
        rel_id = f"rel_{uuid.uuid4().hex[:12]}"
        vtag = version_tag or kwargs.get("version", "v1.0.0")
        rname = release_name or f"Release {vtag}"
        ssummary = scope_summary or kwargs.get("scope_description", "General feature release")
        release = {
            "id": rel_id,
            "product_id": product_id,
            "version": vtag,
            "version_tag": vtag,
            "release_name": rname,
            "scope_summary": ssummary,
            "features": kwargs.get("features", []),
            "readiness_status": "in_progress",
            "readiness_score": 0.65,
            "launch_readiness_score": 0.65,
            "critical_defects": 0,
            "critical_defects_count": 0,
            "qa_passed": False,
            "qa_sign_off": False,
            "security_reviewed": False,
            "security_sign_off": False,
            "performance_benchmarked": False,
            "rollback_tested": False,
            "blocking_reasons": [],
            "rollback_plan": rollback_plan or "Revert deployment image tag with zero-downtime traffic draining.",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._releases.setdefault(product_id, []).append(release)
        return release

    def list_releases(self, product_id: str) -> List[Dict[str, Any]]:
        return self._releases.get(product_id, [])

    def evaluate_release_readiness(
        self,
        release_id: str,
        qa_passed: bool = True,
        critical_defects: int = 0,
        security_reviewed: bool = True,
        performance_benchmarked: bool = True,
        rollback_tested: bool = True,
        product_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Evaluate deterministic gate checklist before production deployment sign-off."""
        checklist = {
            "qa_passed": qa_passed,
            "zero_critical_defects": (critical_defects == 0),
            "security_reviewed": security_reviewed,
            "performance_benchmarked": performance_benchmarked,
            "rollback_tested": rollback_tested,
        }
        blocking_reasons = []
        if not qa_passed:
            blocking_reasons.append("QA test suites must pass 100%")
        if critical_defects > 0:
            blocking_reasons.append(f"Hard block: {critical_defects} critical defects must be resolved (must be 0)")
        if not security_reviewed:
            blocking_reasons.append("Security architecture and dependency review required")
        if not performance_benchmarked:
            blocking_reasons.append("p99 latency performance benchmark required")
        if not rollback_tested:
            blocking_reasons.append("Rollback procedure must be tested and verified")

        passed_count = sum(1 for v in checklist.values() if v)
        score = passed_count / float(len(checklist))

        is_ready = bool(score >= 1.0 and critical_defects == 0)
        status = "ready" if is_ready else "blocked"

        res = {
            "release_id": release_id,
            "readiness_status": status,
            "readiness_score": round(score, 2),
            "launch_readiness_score": round(score, 2),
            "critical_defects": critical_defects,
            "critical_defects_count": critical_defects,
            "checklist": checklist,
            "is_ready_for_production": is_ready,
            "is_ready_for_approval": is_ready,
            "blocking_reasons": blocking_reasons,
            "evaluated_at": datetime.utcnow().isoformat(),
        }

        # Update cached release if present
        for rel_list in self._releases.values():
            for r in rel_list:
                if r["id"] == release_id:
                    r["readiness_status"] = status
                    r["readiness_score"] = res["readiness_score"]
                    r["launch_readiness_score"] = res["launch_readiness_score"]
                    r["critical_defects"] = critical_defects
                    r["qa_passed"] = qa_passed
                    r["security_reviewed"] = security_reviewed
                    r["performance_benchmarked"] = performance_benchmarked
                    r["rollback_tested"] = rollback_tested
                    r["blocking_reasons"] = blocking_reasons
        return res
