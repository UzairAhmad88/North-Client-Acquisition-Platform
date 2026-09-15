"""Multi-dimensional Impact Analyzer for Change Requests."""

from typing import Any, Dict, List
from agents.change_management.models import ChangeImpactItem, ImpactAnalysisResult


class ChangeImpactAnalyzer:
    """Analyzes multi-dimensional scope, schedule, deliverable, and resource impacts."""

    def analyze_impact(
        self, change_request_id: str, title: str, description: str, baseline_data: Dict[str, Any] = None
    ) -> ImpactAnalysisResult:
        content_lower = f"{title} {description}".lower()
        impacts: List[ChangeImpactItem] = []
        requires_contract = False
        requires_commercial = False
        overall_level = "LOW"

        # Requirement Impact
        impacts.append(
            ChangeImpactItem(
                impact_type="REQUIREMENT",
                impact_action="MODIFIED" if "update" in content_lower else "ADDED",
                impact_description=f"Requirement adjustment derived from change request: '{title}'.",
                confidence="HIGH",
            )
        )

        # Deliverable Impact
        if any(w in content_lower for w in ["app", "portal", "module", "dashboard", "integration", "gateway"]):
            impacts.append(
                ChangeImpactItem(
                    impact_type="DELIVERABLE",
                    impact_action="ADDED",
                    impact_description=f"New or modified deliverable scope item: {title}.",
                    confidence="HIGH",
                )
            )
            requires_contract = True
            requires_commercial = True
            overall_level = "HIGH"

        # Schedule / Effort Impact
        impacts.append(
            ChangeImpactItem(
                impact_type="SCHEDULE",
                impact_action="AFFECTED",
                impact_description="Project delivery timeline shifted due to additional work items.",
                confidence="MEDIUM",
            )
        )

        # Risk Impact
        if "integration" in content_lower or "payment" in content_lower or "mobile" in content_lower:
            impacts.append(
                ChangeImpactItem(
                    impact_type="RISK",
                    impact_action="AFFECTED",
                    impact_description="Introduces external technical dependency & API integration risks.",
                    confidence="MEDIUM",
                )
            )

        return ImpactAnalysisResult(
            change_request_id=change_request_id,
            overall_impact_level=overall_level,
            impacts=impacts,
            requires_contract_amendment=requires_contract,
            requires_commercial_adjustment=requires_commercial,
            risk_level="HIGH" if overall_level == "HIGH" else "MEDIUM",
        )
