"""Central Event Registry defining cataloged domain events, schemas, and sensitivity."""

from typing import Any, Dict, List, Optional
from app.events.schemas import (
    BusinessDiscoveredPayload,
    LeadCreatedPayload,
    ResearchCompletedPayload,
    AuditCompletedPayload,
    LeadQualifiedPayload,
    ServiceRecommendedPayload,
    OutreachDraftCreatedPayload,
    OutreachApprovedPayload,
    OutreachSentPayload,
    MessageReceivedPayload,
    RequirementsConfirmedPayload,
    SolutionApprovedPayload,
    EstimateApprovedPayload,
    ProposalAcceptedPayload,
    ContractSignedPayload,
    ProjectCreatedPayload,
    ChangeApprovedPayload,
    UATAcceptedPayload,
    DeliveryAcceptedPayload,
    SupportRequestCreatedPayload,
    AIIncidentDetectedPayload,
    AgentEvaluationCompletedPayload,
)


class EventDefinition:
    """Metadata specification for a cataloged domain event."""

    def __init__(
        self,
        event_name: str,
        current_version: str,
        description: str,
        aggregate_type: str,
        producer: str,
        consumers: List[str],
        payload_cls: Any,
        sensitivity: str = "INTERNAL",
        retention_policy: str = "90_DAYS",
    ):
        self.event_name = event_name
        self.current_version = current_version
        self.description = description
        self.aggregate_type = aggregate_type
        self.producer = producer
        self.consumers = consumers
        self.payload_cls = payload_cls
        self.sensitivity = sensitivity
        self.retention_policy = retention_policy


class EventRegistry:
    """Central registry maintaining versioned domain event specifications."""

    def __init__(self):
        self._events: Dict[str, EventDefinition] = {}
        self._register_default_events()

    def register(self, definition: EventDefinition) -> None:
        """Register a new or updated event definition."""
        self._events[definition.event_name] = definition

    def get(self, event_name: str) -> Optional[EventDefinition]:
        """Retrieve event definition by name."""
        return self._events.get(event_name)

    def list_all(self) -> List[EventDefinition]:
        """List all cataloged domain events."""
        return list(self._events.values())

    def validate_payload(self, event_name: str, payload: Dict[str, Any]) -> bool:
        """Validate an event payload against registered schema."""
        defn = self.get(event_name)
        if not defn or not defn.payload_cls:
            return True
        try:
            defn.payload_cls(**payload)
            return True
        except Exception:
            return False

    def _register_default_events(self) -> None:
        """Populate the central event registry with core system domain events."""
        events = [
            EventDefinition(
                event_name="business.discovered",
                current_version="v1",
                description="A new target business was identified via discovery engine.",
                aggregate_type="business",
                producer="discovery_service",
                consumers=["research_service", "analytics_service"],
                payload_cls=BusinessDiscoveredPayload,
            ),
            EventDefinition(
                event_name="lead.created",
                current_version="v1",
                description="A new lead opportunity was created in CRM.",
                aggregate_type="lead",
                producer="lead_service",
                consumers=["scoring_service", "research_service"],
                payload_cls=LeadCreatedPayload,
            ),
            EventDefinition(
                event_name="research.completed",
                current_version="v1",
                description="Digital footprint research job was completed for a business.",
                aggregate_type="business",
                producer="research_service",
                consumers=["audit_service", "qualification_service"],
                payload_cls=ResearchCompletedPayload,
            ),
            EventDefinition(
                event_name="audit.completed",
                current_version="v1",
                description="Automated digital presence audit was executed.",
                aggregate_type="business",
                producer="audit_service",
                consumers=["qualification_service", "scoring_service"],
                payload_cls=AuditCompletedPayload,
            ),
            EventDefinition(
                event_name="lead.qualified",
                current_version="v1",
                description="Lead qualification evaluated BANT and fit criteria.",
                aggregate_type="lead",
                producer="qualification_service",
                consumers=["personalization_service", "recommendation_service"],
                payload_cls=LeadQualifiedPayload,
            ),
            EventDefinition(
                event_name="service.recommended",
                current_version="v1",
                description="Deterministic service recommendation calculated for a lead.",
                aggregate_type="lead",
                producer="recommendation_service",
                consumers=["personalization_service"],
                payload_cls=ServiceRecommendedPayload,
            ),
            EventDefinition(
                event_name="outreach.draft.created",
                current_version="v1",
                description="Personalized outreach draft was synthesized by AI agent.",
                aggregate_type="lead",
                producer="personalization_service",
                consumers=["risk_engine", "human_task_queue"],
                payload_cls=OutreachDraftCreatedPayload,
            ),
            EventDefinition(
                event_name="outreach.approved",
                current_version="v1",
                description="Human operator approved an outreach draft with content hash.",
                aggregate_type="lead",
                producer="outreach_service",
                consumers=["communication_guard"],
                payload_cls=OutreachApprovedPayload,
            ),
            EventDefinition(
                event_name="outreach.sent",
                current_version="v1",
                description="Outreach message was safely dispatched by CommunicationGuard.",
                aggregate_type="lead",
                producer="communication_guard",
                consumers=["analytics_service", "conversation_service"],
                payload_cls=OutreachSentPayload,
            ),
            EventDefinition(
                event_name="conversation.message_received",
                current_version="v1",
                description="Inbound client communication message received via webhook.",
                aggregate_type="conversation",
                producer="response_intelligence",
                consumers=["requirements_service", "notification_service"],
                payload_cls=MessageReceivedPayload,
            ),
            EventDefinition(
                event_name="requirements.confirmed",
                current_version="v1",
                description="Client discovery requirements confirmed by human operator.",
                aggregate_type="lead",
                producer="requirements_service",
                consumers=["solution_service", "estimation_service"],
                payload_cls=RequirementsConfirmedPayload,
            ),
            EventDefinition(
                event_name="solution.approved",
                current_version="v1",
                description="Architecture blueprint and feature breakdown approved.",
                aggregate_type="lead",
                producer="solution_service",
                consumers=["proposal_service"],
                payload_cls=SolutionApprovedPayload,
            ),
            EventDefinition(
                event_name="estimate.approved",
                current_version="v1",
                description="Internal effort WBS and cost estimation approved.",
                aggregate_type="lead",
                producer="estimation_service",
                consumers=["proposal_service"],
                payload_cls=EstimateApprovedPayload,
            ),
            EventDefinition(
                event_name="proposal.accepted",
                current_version="v1",
                description="Client formally accepted commercial proposal.",
                aggregate_type="lead",
                producer="proposal_service",
                consumers=["contract_service", "billing_service"],
                payload_cls=ProposalAcceptedPayload,
            ),
            EventDefinition(
                event_name="contract.signed",
                current_version="v1",
                description="Contract signed and immutable baseline locked.",
                aggregate_type="contract",
                producer="contract_service",
                consumers=["project_service"],
                payload_cls=ContractSignedPayload,
            ),
            EventDefinition(
                event_name="project.created",
                current_version="v1",
                description="Delivery project initialized from signed contract baseline.",
                aggregate_type="project",
                producer="project_service",
                consumers=["client_portal", "qa_service"],
                payload_cls=ProjectCreatedPayload,
            ),
            EventDefinition(
                event_name="change.approved",
                current_version="v1",
                description="Scope or schedule change request formally approved.",
                aggregate_type="change_request",
                producer="change_service",
                consumers=["project_service", "contract_service"],
                payload_cls=ChangeApprovedPayload,
            ),
            EventDefinition(
                event_name="uat.accepted",
                current_version="v1",
                description="Client signed off on UAT test cases and release milestone.",
                aggregate_type="project",
                producer="qa_service",
                consumers=["delivery_service"],
                payload_cls=UATAcceptedPayload,
            ),
            EventDefinition(
                event_name="delivery.accepted",
                current_version="v1",
                description="Formal client acceptance of final delivery package and handover.",
                aggregate_type="project",
                producer="delivery_service",
                consumers=["support_service", "billing_service"],
                payload_cls=DeliveryAcceptedPayload,
            ),
            EventDefinition(
                event_name="support.request.created",
                current_version="v1",
                description="New client support ticket or maintenance work order submitted.",
                aggregate_type="support_request",
                producer="support_service",
                consumers=["human_task_queue"],
                payload_cls=SupportRequestCreatedPayload,
            ),
            EventDefinition(
                event_name="ai.incident.detected",
                current_version="v1",
                description="High severity AI agent failure or security anomaly flagged.",
                aggregate_type="ai_incident",
                producer="ai_governance",
                consumers=["kill_switch_engine", "human_task_queue"],
                payload_cls=AIIncidentDetectedPayload,
            ),
            EventDefinition(
                event_name="agent.evaluation.completed",
                current_version="v1",
                description="Offline benchmark or regression test completed for an agent.",
                aggregate_type="agent_evaluation",
                producer="ai_governance",
                consumers=["continuous_improvement"],
                payload_cls=AgentEvaluationCompletedPayload,
            ),
        ]
        for evt in events:
            self.register(evt)


# Global singleton instance
global_event_registry = EventRegistry()
