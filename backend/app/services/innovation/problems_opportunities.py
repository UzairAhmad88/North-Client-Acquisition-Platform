"""
Problem Discovery and Opportunity Evaluation Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.innovation.base import ProblemStatus


class ProblemOpportunityManager:
    """Manages real customer problem discovery and opportunity evaluations."""

    def __init__(self):
        self._problems: Dict[str, List[Dict[str, Any]]] = {}
        self._opportunities: Dict[str, List[Dict[str, Any]]] = {}

    # Problems
    def record_problem(
        self,
        workspace_id: str,
        statement: str,
        affected_users: Optional[str] = None,
        frequency: str = "DAILY",
        severity: str = "HIGH",
        existing_solutions: Optional[List[str]] = None,
        willingness_to_pay_signal: Optional[float] = None,
        urgency_score: float = 0.8,
        confidence_score: float = 0.7,
        evidence_sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record real-world customer pain point with evidence and willingness-to-pay signal."""
        prob_id = f"prob_{uuid.uuid4().hex[:12]}"
        problem = {
            "id": prob_id,
            "workspace_id": workspace_id,
            "statement": statement,
            "affected_users": affected_users or "Target Business Operators",
            "frequency": frequency,
            "severity": severity,
            "existing_solutions": existing_solutions or [],
            "willingness_to_pay_signal": willingness_to_pay_signal,
            "urgency_score": max(0.1, min(1.0, urgency_score)),
            "confidence_score": max(0.1, min(1.0, confidence_score)),
            "status": ProblemStatus.OBSERVED.value,
            "evidence_sources": evidence_sources or [],
            "created_at": datetime.utcnow().isoformat(),
        }
        self._problems.setdefault(workspace_id, []).append(problem)
        return problem

    def validate_problem(
        self,
        workspace_id: str,
        problem_id: str,
        status: ProblemStatus = ProblemStatus.VALIDATED,
        corroborating_evidence: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Mark problem as validated or refuted based on empirical research."""
        problems = self._problems.get(workspace_id, [])
        target = next((p for p in problems if p["id"] == problem_id), None)
        if not target:
            raise ValueError(f"Problem {problem_id} not found in workspace {workspace_id}")

        target["status"] = status.value if hasattr(status, "value") else str(status)
        if corroborating_evidence:
            target["evidence_sources"].extend(corroborating_evidence)
        if status == ProblemStatus.VALIDATED:
            target["confidence_score"] = min(1.0, target["confidence_score"] + 0.2)
        return target

    def list_problems(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._problems.get(workspace_id, [])

    # Opportunities
    def create_opportunity_from_problem(
        self,
        workspace_id: str,
        title: str,
        description: Optional[str] = None,
        market_potential: str = "HIGH",
        revenue_potential_usd: Optional[float] = None,
        competitive_intensity: str = "MEDIUM",
        technical_feasibility: str = "FEASIBLE",
        strategic_alignment_score: float = 0.85,
        time_to_market_months: float = 3.0,
        risk_level: str = "MEDIUM",
    ) -> Dict[str, Any]:
        """Convert validated problem into a prioritized commercial opportunity."""
        opp_id = f"opp_{uuid.uuid4().hex[:12]}"
        opp = {
            "id": opp_id,
            "workspace_id": workspace_id,
            "title": title,
            "description": description or title,
            "market_potential": market_potential,
            "revenue_potential_usd": revenue_potential_usd or 250000.0,
            "competitive_intensity": competitive_intensity,
            "technical_feasibility": technical_feasibility,
            "strategic_alignment_score": max(0.1, min(1.0, strategic_alignment_score)),
            "time_to_market_months": time_to_market_months,
            "risk_level": risk_level,
            "status": "OPEN",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._opportunities.setdefault(workspace_id, []).append(opp)
        return opp

    def list_opportunities(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._opportunities.get(workspace_id, [])
