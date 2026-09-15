"""Customer Success Platform Service coordinating health scoring, Client 360, risks, renewals, and opportunities."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.customer_success.base import (
    ClientLifecycleStage,
    HealthBand,
    HealthCalculationResult,
    RelationshipStrength,
    RiskCategory,
    OpportunityType,
    RenewalStatus,
)
from app.customer_success.health_engine import HealthScoringEngine
from app.customer_success.timeline import ClientTimelineAggregator
from app.customer_success.client_360 import Client360Synthesizer
from app.customer_success.authorization import CustomerSuccessAuthorizationManager


class CustomerSuccessPlatformService:
    """Unified service orchestrating customer success and client relationship operations."""

    def __init__(self):
        self.health_engine = HealthScoringEngine()
        self.timeline_aggregator = ClientTimelineAggregator()
        self.synthesizer = Client360Synthesizer()
        self.auth = CustomerSuccessAuthorizationManager()

    # --- Health Scoring & Trends ---

    def calculate_health(
        self,
        client_id: str,
        factors: Dict[str, Optional[Decimal]],
        custom_weights: Optional[Dict[str, Decimal]] = None,
        historical_scores: Optional[List[Decimal]] = None,
        evidence_notes: Optional[Dict[str, str]] = None,
    ) -> HealthCalculationResult:
        """Calculates multi-factor health score with explainability and missing data protection."""
        return self.health_engine.calculate_health_score(
            client_id=client_id,
            factors_input=factors,
            custom_weights=custom_weights,
            historical_scores=historical_scores,
            evidence_notes=evidence_notes,
        )

    # --- Client 360 View ---

    def get_client_360(
        self,
        profile: Dict[str, Any],
        contacts: List[Dict[str, Any]],
        health_score: Optional[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        success_plans: List[Dict[str, Any]],
        projects: List[Dict[str, Any]],
        financial_summary: Dict[str, Any],
        support_summary: Dict[str, Any],
        risks: List[Dict[str, Any]],
        opportunities: List[Dict[str, Any]],
        renewals: List[Dict[str, Any]],
        surveys: List[Dict[str, Any]],
        is_client: bool = False,
    ) -> Dict[str, Any]:
        """Synthesizes Client 360 view and applies client privacy boundaries."""
        raw_view = self.synthesizer.build_360_view(
            profile=profile,
            contacts=contacts,
            health_score=health_score,
            goals=goals,
            success_plans=success_plans,
            projects=projects,
            financial_summary=financial_summary,
            support_summary=support_summary,
            risks=risks,
            opportunities=opportunities,
            renewals=renewals,
            surveys=surveys,
        )
        return self.auth.mask_client_360_payload(raw_view, is_client=is_client)

    # --- Timeline Events ---

    def log_timeline_event(
        self,
        client_id: str,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        actor_type: str = "SYSTEM",
        actor_id: Optional[str] = None,
        source_entity_type: Optional[str] = None,
        source_entity_id: Optional[str] = None,
        occurred_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Creates a standardized timeline event."""
        return self.timeline_aggregator.create_timeline_event(
            client_id=client_id,
            event_type=event_type,
            title=title,
            description=description,
            actor_type=actor_type,
            actor_id=actor_id,
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            occurred_at=occurred_at,
            metadata=metadata,
        )

    # --- Customer Success Playbooks ---

    def get_recommended_playbook(self, health_band: HealthBand, is_renewal_due: bool) -> Dict[str, Any]:
        """Recommends standard customer success playbook based on health and commercial lifecycle."""
        if health_band in (HealthBand.CRITICAL, HealthBand.AT_RISK):
            return {
                "playbook_name": "AT_RISK_CLIENT_RECOVERY",
                "priority": "HIGH",
                "steps": [
                    "Review recent health factor drops and open support tickets",
                    "Conduct internal account review with project and delivery owners",
                    "Schedule check-in meeting with client decision maker",
                    "Update Customer Success Plan with risk remediation items",
                ],
            }
        elif is_renewal_due:
            return {
                "playbook_name": "UPCOMING_RENEWAL_ALIGNMENT",
                "priority": "MEDIUM",
                "steps": [
                    "Review completed goals and delivered business value",
                    "Audit open tickets and ensure resolution",
                    "Prepare renewal proposal draft for internal review",
                    "Schedule commercial review meeting with client",
                ],
            }
        else:
            return {
                "playbook_name": "STANDARD_HEALTH_MONITORING",
                "priority": "LOW",
                "steps": [
                    "Monitor ongoing project milestone velocity",
                    "Track goal achievement progress",
                    "Gather periodic satisfaction feedback",
                ],
            }
