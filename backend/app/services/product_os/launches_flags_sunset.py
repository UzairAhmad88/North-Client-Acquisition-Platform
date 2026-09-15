"""Launches, Feature Flags, Rollback and Governed Sunset Service.

Enforces launch readiness checklists, audited feature flags, controlled rollback workflows,
technical debt tracking, and strict human-governed product sunset lifecycles.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        ReleaseStrategy,
    )
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        ReleaseStrategy,
    )


logger = logging.getLogger(__name__)


class LaunchesFlagsSunsetService:
    """Manages launch readiness checklists, feature flag audits, rollbacks, tech debt, and sunsets."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._launches: Dict[str, Dict[str, Any]] = {}
        self._flags: Dict[str, Dict[str, Any]] = {}
        self._tech_debt: Dict[str, Dict[str, Any]] = {}
        self._sunset_plans: Dict[str, Dict[str, Any]] = {}

    def create_launch_plan(
        self,
        tenant_id: str,
        product_id: str,
        release_name: str,
        target_release_date: str,
        strategy: str = ReleaseStrategy.PHASED_ROLLOUT.value,
        audience_segment: str = "Beta & Enterprise Early Adopters",
        checklists: Optional[Dict[str, bool]] = None,
        rollback_plan: str = "Automated canary revert upon error rate > 1.5%",
    ) -> AttrDict:
        """Create a release launch plan with pre-flight checklist."""
        launch_id = generate_product_id("lnch")
        now = datetime.now(timezone.utc).isoformat()

        default_checklists = {
            "engineering_ready": True,
            "qa_passed": True,
            "security_cleared": True,
            "privacy_reviewed": True,
            "docs_published": False,
            "support_trained": False,
            "marketing_aligned": True,
            "rollback_verified": True,
        }
        if checklists:
            default_checklists.update(checklists)

        total_checks = len(default_checklists)
        passed_checks = sum(1 for v in default_checklists.values() if v is True)
        readiness_pct = (passed_checks / max(1, total_checks)) * 100.0

        record = {
            "launch_id": launch_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "release_name": release_name,
            "target_release_date": target_release_date,
            "strategy": strategy,
            "audience_segment": audience_segment,
            "checklists": default_checklists,
            "readiness_pct": round(readiness_pct, 2),
            "status": "APPROVED_FOR_RELEASE" if readiness_pct == 100.0 else "PENDING_CHECKLIST",
            "rollback_plan": rollback_plan,
            "governance_approval_required": True,
            "created_at": now,
            "updated_at": now,
        }
        self._launches[launch_id] = record
        return AttrDict(record)

    def register_feature_flag(
        self,
        tenant_id: str,
        flag_key: str,
        name: str,
        environment: str = "production",
        is_enabled: bool = False,
        rollout_percentage: int = 10,
        targeting_rules: Optional[Dict[str, Any]] = None,
        owner_email: str = "product-ops@uzaii.com",
    ) -> AttrDict:
        """Register or update an auditable feature flag."""
        flag_id = generate_product_id("flag")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "flag_id": flag_id,
            "tenant_id": tenant_id,
            "flag_key": flag_key,
            "name": name,
            "environment": environment,
            "is_enabled": is_enabled,
            "rollout_percentage": max(0, min(100, rollout_percentage)),
            "targeting_rules": targeting_rules or {"allowed_tiers": ["ENTERPRISE", "PRO"]},
            "owner_email": owner_email,
            "audit_trail": [
                {"action": "INITIAL_CREATION", "timestamp": now, "actor": owner_email}
            ],
            "created_at": now,
            "updated_at": now,
        }
        self._flags[flag_id] = record
        return AttrDict(record)

    def record_technical_debt(
        self,
        tenant_id: str,
        product_id: str,
        title: str,
        area: str,
        severity: str = "MEDIUM",
        estimated_remediation_days: float = 5.0,
        impact_description: str = "",
        remediation_strategy: str = "",
    ) -> AttrDict:
        """Track technical debt item linked to product health and roadmaps."""
        debt_id = generate_product_id("debt")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "debt_id": debt_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "title": title,
            "area": area,
            "severity": severity,
            "estimated_remediation_days": estimated_remediation_days,
            "impact_description": impact_description,
            "remediation_strategy": remediation_strategy,
            "status": "LOGGED",
            "created_at": now,
            "updated_at": now,
        }
        self._tech_debt[debt_id] = record
        return AttrDict(record)

    def initiate_sunset_workflow(
        self,
        tenant_id: str,
        product_id: str,
        product_name: str,
        reason: str,
        active_customer_count: int,
        revenue_impact_usd: float,
        alternative_product_id: str,
        target_sunset_date: str,
        governance_approver: str,
    ) -> AttrDict:
        """Initiate governed sunset and migration workflow. AI cannot execute autonomously."""
        sunset_id = generate_product_id("sunset")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "sunset_id": sunset_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "product_name": product_name,
            "reason": reason,
            "active_customer_count": active_customer_count,
            "revenue_impact_usd": revenue_impact_usd,
            "alternative_product_id": alternative_product_id,
            "target_sunset_date": target_sunset_date,
            "governance_approver": governance_approver,
            "governance_status": "PENDING_EXECUTIVE_APPROVAL",
            "lifecycle_stage": "SUNSET_PLANNED",
            "migration_milestones": [
                {"step": "Customer Communication 90D", "status": "PENDING"},
                {"step": "Data Export Toolkit Ready", "status": "IN_PROGRESS"},
                {"step": "API Deprecation Notice Sent", "status": "PENDING"},
                {"step": "Final Sunset & Archive", "status": "SCHEDULED"},
            ],
            "created_at": now,
            "updated_at": now,
        }
        self._sunset_plans[sunset_id] = record
        return AttrDict(record)
