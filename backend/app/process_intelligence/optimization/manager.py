"""
Process Optimization Manager for Phase 49: Multi-objective proposal creation and tradeoff analysis.
"""

from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import OptimizationProposal, OptimizationStatus
except ImportError:
    from app.process_intelligence.base import OptimizationProposal, OptimizationStatus


class ProcessOptimizationManager:
    """Evaluates multi-objective process optimization tradeoffs and generates versioned proposals."""

    def __init__(self):
        self._proposals: Dict[str, OptimizationProposal] = {}

    def create_proposal(
        self,
        process_id: str,
        title: str,
        problem_statement: str,
        evidence_summary: str,
        proposed_changes: Dict[str, Any],
        cycle_time_improvement_pct: float,
        cost_savings_pct: float,
        quality_score: float,  # 0.0 to 1.0
        risk_level: str = "LOW",  # LOW, MODERATE, HIGH
        compliance_score: float = 1.0,  # 0.0 to 1.0 (must be >= 0.95 for auto-compliance)
        expected_cost: float = 500.0,
        rollback_plan: str = "Revert workflow engine pointer to version N-1 with state preservation.",
        owner_id: str = "system",
        tenant_id: str = "default_tenant",
    ) -> OptimizationProposal:
        """Drafts a structured optimization proposal with multi-objective trade-offs."""
        proposal_code = f"PROP-{uuid.uuid4().hex[:6].upper()}"

        # Multi-objective Tradeoff Scorecard: (Cycle Time, Cost, Quality, Risk, Compliance)
        tradeoff_scorecard = {
            "cycle_time_score": round(min(1.0, cycle_time_improvement_pct / 50.0), 2),
            "cost_efficiency_score": round(min(1.0, cost_savings_pct / 50.0), 2),
            "quality_score": round(quality_score, 2),
            "risk_score": 0.2 if risk_level == "LOW" else (0.5 if risk_level == "MODERATE" else 0.8),
            "compliance_score": round(compliance_score, 2),
            "governance_aligned": compliance_score >= 0.95,
        }

        expected_benefits = {
            "cycle_time_reduction_percentage": cycle_time_improvement_pct,
            "cost_reduction_percentage": cost_savings_pct,
            "quality_index": quality_score,
            "annual_projected_savings_usd": round(cost_savings_pct * 1200.0, 2),
        }

        proposal = OptimizationProposal(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            proposal_code=proposal_code,
            process_id=process_id,
            title=title,
            current_version=1,
            proposed_version=2,
            problem_statement=problem_statement,
            evidence_summary=evidence_summary,
            proposed_changes=proposed_changes,
            tradeoff_scorecard=tradeoff_scorecard,
            expected_benefits=expected_benefits,
            expected_cost=expected_cost,
            risk_level=risk_level,
            rollback_plan=rollback_plan,
            owner_id=owner_id,
            status=OptimizationStatus.DRAFT,
        )

        self._proposals[proposal_code] = proposal
        return proposal

    def get_proposals_for_process(self, process_id: str, tenant_id: str = "default_tenant") -> List[OptimizationProposal]:
        """Returns all optimization proposals for a process definition."""
        return [p for p in self._proposals.values() if p.process_id == process_id and p.tenant_id == tenant_id]

    def advance_proposal_status(
        self,
        proposal_code: str,
        new_status: OptimizationStatus,
        reviewer_id: str,
        tenant_id: str = "default_tenant",
    ) -> Optional[OptimizationProposal]:
        """Transitions proposal through the governance lifecycle (DRAFT -> SIMULATION -> HUMAN_APPROVAL -> APPROVED)."""
        proposal = self._proposals.get(proposal_code)
        if not proposal or proposal.tenant_id != tenant_id:
            return None

        # Human review gating check: cannot leap from DRAFT to APPROVED directly
        proposal.status = new_status
        return proposal
