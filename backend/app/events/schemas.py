"""Typed Domain Event Payload Schemas for Phase 34 Event-Driven Architecture."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# 1. Lead Discovery & CRM Events
class BusinessDiscoveredPayload(BaseModel):
    business_id: str
    company_name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None


class LeadCreatedPayload(BaseModel):
    lead_id: str
    business_id: str
    contact_name: str
    contact_email: Optional[str] = None
    source: str = "DISCOVERY"


# 2. Research & Audit Events
class ResearchCompletedPayload(BaseModel):
    job_id: str
    business_id: str
    facts_count: int
    confidence: str
    sources_count: int


class AuditCompletedPayload(BaseModel):
    audit_id: str
    business_id: str
    performance_score: int
    findings_count: int
    high_severity_count: int


# 3. Qualification & Recommendation Events
class LeadQualifiedPayload(BaseModel):
    qualification_id: str
    lead_id: str
    fit_status: str  # QUALIFIED, NOT_QUALIFIED, NEEDS_REVIEW
    score: float
    recommended_services: List[str] = Field(default_factory=list)


class ServiceRecommendedPayload(BaseModel):
    recommendation_id: str
    lead_id: str
    service_id: str
    relevance_band: str  # STRONG, GOOD, POSSIBLE, WEAK
    score: float


# 4. Outreach & Communication Events
class OutreachDraftCreatedPayload(BaseModel):
    draft_id: str
    lead_id: str
    channel: str  # EMAIL, LINKEDIN, WHATSAPP, SMS
    subject: Optional[str] = None
    requires_approval: bool = True


class OutreachApprovedPayload(BaseModel):
    draft_id: str
    lead_id: str
    approved_by: str
    content_hash: str


class OutreachSentPayload(BaseModel):
    message_id: str
    lead_id: str
    recipient: str
    channel: str
    provider_id: str


# 5. Conversation & Requirements Events
class MessageReceivedPayload(BaseModel):
    message_id: str
    conversation_id: str
    sender: str
    channel: str
    intent: Optional[str] = None


class RequirementsConfirmedPayload(BaseModel):
    discovery_session_id: str
    requirements_count: int
    readiness_score: float
    human_confirmed: bool = True


# 6. Solution, Estimation & Proposal Events
class SolutionApprovedPayload(BaseModel):
    solution_id: str
    lead_id: str
    features_count: int
    deliverables_count: int
    approved_by: str


class EstimateApprovedPayload(BaseModel):
    estimate_id: str
    lead_id: str
    total_hours: float
    recommended_commercial_min: float
    recommended_commercial_max: float
    approved_by: str


class ProposalAcceptedPayload(BaseModel):
    proposal_id: str
    lead_id: str
    contract_amount: float
    client_accepted_at: str


# 7. Contract, Project & Change Events
class ContractSignedPayload(BaseModel):
    contract_id: str
    lead_id: str
    baseline_id: str
    total_value: float
    client_signature_hash: str


class ProjectCreatedPayload(BaseModel):
    project_id: str
    contract_id: str
    name: str
    milestones_count: int


class ChangeApprovedPayload(BaseModel):
    change_request_id: str
    project_id: str
    scope_impact: str
    cost_delta: float
    schedule_delta_days: int
    internal_approved_by: str
    client_approved_by: Optional[str] = None


# 8. QA, UAT & Delivery Handover Events
class UATAcceptedPayload(BaseModel):
    uat_session_id: str
    project_id: str
    test_cases_passed: int
    signed_off_by: str


class DeliveryAcceptedPayload(BaseModel):
    package_id: str
    project_id: str
    client_acceptance_hash: str
    accepted_by: str


# 9. Support, Incidents & AI Governance Events
class SupportRequestCreatedPayload(BaseModel):
    request_id: str
    project_id: str
    severity: str
    category: str


class AIIncidentDetectedPayload(BaseModel):
    incident_number: str
    agent_key: str
    severity: str
    failure_category: str
    affected_trace_id: Optional[str] = None


class AgentEvaluationCompletedPayload(BaseModel):
    evaluation_run_id: str
    agent_key: str
    version: str
    overall_score: float
    regression_detected: bool
