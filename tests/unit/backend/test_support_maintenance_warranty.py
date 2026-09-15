"""Unit tests for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

import hashlib
import uuid
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from app.models.support import (
    ClientHealthSnapshot,
    Incident,
    IncidentTimeline,
    KnowledgeArticle,
    MaintenancePlan,
    MaintenanceWorkOrder,
    MonitoringEvent,
    SLAPolicy,
    SupportOpportunity,
    SupportRequest,
    SupportRequestEvent,
    SupportRequestEvidence,
    SupportRequestVersion,
    Warranty,
)
from agents.support.agent import SupportAgent
from agents.support.classifier import SupportClassifierEngine
from agents.support.opportunity_detector import OpportunityDetectorEngine
from agents.support.troubleshooter import TroubleshooterEngine
from agents.support.warranty_evaluator import WarrantyEvaluatorEngine
from agents.core.context import AgentContext
from agents.core.permissions import PROHIBITED_PERMISSIONS
from integrations.monitoring.providers.mock import MockMonitoringProvider
from app.services.support import SupportService


def test_support_agent_permission_guardrails():
    """Verify SupportAgent has ZERO autonomous permissions to approve warranty, modify contracts, approve changes, or send unguarded messages."""
    agent = SupportAgent()
    perms = {p.value for p in agent.get_required_permissions()}

    # Assert allowed READ & DRAFT permissions
    assert "READ_SUPPORT_REQUESTS" in perms
    assert "READ_INCIDENTS" in perms
    assert "READ_WARRANTY" in perms
    assert "READ_MAINTENANCE" in perms
    assert "READ_KNOWLEDGE_BASE" in perms
    assert "CREATE_CLASSIFICATION" in perms
    assert "CREATE_TROUBLESHOOTING_DRAFT" in perms
    assert "CREATE_OPPORTUNITY_DRAFT" in perms


    # Assert strictly prohibited permissions
    prohibited_actions = [
        "APPROVE_WARRANTY",
        "CHANGE_CONTRACT",
        "APPROVE_CHANGE",
        "APPROVE_PAYMENT",
        "ISSUE_REFUND",
        "CLOSE_CRITICAL_INCIDENT",
        "CHANGE_SLA",
        "DELETE_SUPPORT_HISTORY",
        "SEND_EXTERNAL_MESSAGE",
        "MODIFY_CLIENT_BASELINE",
    ]
    for prohibited in prohibited_actions:
        assert prohibited not in perms
        assert prohibited in PROHIBITED_PERMISSIONS



def test_classifier_engine_ticket_differentiation():
    """Verify SupportClassifierEngine accurately categorizes defects vs support vs change requests vs incidents."""
    classifier = SupportClassifierEngine()

    # Defect test
    defect_res = classifier.classify_request(
        request_id="req-1",
        title="Checkout button broken with 500 error",
        description="When clicking place order, API returns 500 internal server error.",
    )
    assert defect_res.classification == "DEFECT"
    assert defect_res.confidence >= 0.8

    # Change Request test
    change_res = classifier.classify_request(
        request_id="req-2",
        title="Please add feature and payment gateway integration",
        description="We would like to add a new feature to our portal.",
    )
    assert change_res.classification == "CHANGE_REQUEST"

    # Incident test
    incident_res = classifier.classify_request(
        request_id="req-3",
        title="CRITICAL: Production server down and site is down fatal crash",
        description="All customers are getting 502 bad gateway errors.",
    )
    assert incident_res.classification == "INCIDENT"
    assert incident_res.priority == "CRITICAL"

    # Maintenance test
    maint_res = classifier.classify_request(
        request_id="req-4",
        title="Renew certificate for HTTPS next week",
        description="Please renew certificate on production server.",
    )
    assert maint_res.classification == "MAINTENANCE"


def test_warranty_evaluator_engine():
    """Verify WarrantyEvaluatorEngine correctly flags in-scope defects vs excluded third-party outages."""
    evaluator = WarrantyEvaluatorEngine()

    # In-warranty baseline defect
    res_in = evaluator.evaluate_warranty_coverage(
        project_id="proj-1",
        defect_title="Authentication Login Bug",
        defect_description="Regression in login authentication flow from delivery package",
        warranty_data={"status": "ACTIVE", "covered_categories": ["FUNCTIONAL_DEFECT", "REGRESSION"]},
        is_in_baseline=True,
    )
    assert res_in.is_covered == "COVERED"
    assert res_in.requires_human_approval is True

    # Out of warranty (expired)
    res_expired = evaluator.evaluate_warranty_coverage(
        project_id="proj-1",
        defect_title="API timeout",
        defect_description="API endpoint timeout",
        warranty_data={"status": "EXPIRED"},
    )
    assert res_expired.is_covered == "NOT_COVERED"
    assert "EXPIRED" in res_expired.reasoning.upper()

    # Excluded cause: 3rd party outage
    res_excluded = evaluator.evaluate_warranty_coverage(
        project_id="proj-1",
        defect_title="AWS S3 Outage",
        defect_description="Third-party API downtime causing image load failure",
        warranty_data={"status": "ACTIVE", "exclusions": "third-party API, hosting failure"},
    )
    assert res_excluded.is_covered == "NOT_COVERED"
    assert "EXCLUSIONS" in res_excluded.reasoning.upper() or "THIRD-PARTY" in res_excluded.reasoning.upper()


def test_troubleshooter_engine():
    """Verify TroubleshooterEngine produces actionable diagnostics and root causes."""
    troubleshooter = TroubleshooterEngine()
    diag = troubleshooter.analyze_troubleshooting(
        request_id="req-1",
        title="Database connection timeout under load",
        description="API login latency spiking and session auth errors.",
        category="DEFECT",
    )

    assert len(diag.observed_symptoms) > 0
    assert len(diag.inferred_causes) > 0
    assert len(diag.recommended_next_steps) > 0


def test_opportunity_detector_engine():
    """Verify OpportunityDetectorEngine identifies account expansion signals."""
    detector = OpportunityDetectorEngine()
    opp = detector.detect_opportunity(
        project_id="proj-1",
        title="Mobile app inquiry",
        description="Can you help us build a mobile app version for iOS and Android?",
    )

    assert opp.opportunity_detected is True
    assert opp.opportunity_type == "NEW_PROJECT"
    assert opp.requires_sales_review is True


@pytest.mark.asyncio
async def test_monitoring_mock_provider():
    """Verify MockMonitoringProvider emits synthetic alerts and heartbeats."""
    provider = MockMonitoringProvider()
    health = await provider.check_health("proj-001")
    assert health.overall_status == "HEALTHY"
    assert health.uptime_percentage >= 99.0

    ingested = await provider.ingest_event("proj-001", {"type": "HEARTBEAT"})
    assert ingested is True



@pytest.mark.asyncio
async def test_support_service_lifecycle():
    """Test full SupportService ticket creation, SLA pause state, human warranty approval, and change routing."""
    mock_session = AsyncMock()
    service = SupportService(mock_session)

    # Mock repository
    mock_ticket = SupportRequest(
        id=str(uuid.uuid4()),
        request_number="SUP-001",
        project_id="proj-100",
        requester="Alice Client",
        title="Crash on report export",
        description="Exporting large CSV reports causes 500 error",
        classification="DEFECT",
        priority="HIGH",
        severity="HIGH",
        status="NEW",
        sla_status="ACTIVE",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    service.repo.get_support_request = AsyncMock(return_value=mock_ticket)
    service.repo.update_support_request = AsyncMock(side_effect=lambda x: x)
    service.repo.add_support_request_version = AsyncMock()
    service.repo.add_support_request_event = AsyncMock()
    service.repo.get_warranty_by_project = AsyncMock(return_value=Warranty(
        id="war-1",
        project_id="proj-100",
        title="Standard Warranty",
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc),
        status="ACTIVE",
    ))

    # 1. Update status to WAITING_FOR_CLIENT (verifying SLA status pause)
    updated = await service.update_support_request_status(
        req_id=mock_ticket.id,
        new_status="WAITING_FOR_CLIENT",
        actor_id="SUPPORT_ENG_1",
    )
    assert updated.status == "WAITING_FOR_CLIENT"
    assert updated.sla_status == "PAUSED"

    # 2. Evaluate warranty with human supervisor approval
    w_eval = await service.evaluate_warranty_for_request(
        req_id=mock_ticket.id,
        human_evaluator_id="SUPERVISOR_ALICE",
        approve_warranty=True,
    )
    assert w_eval["warranty_status"] == "COVERED"
    assert w_eval["evaluated_by"] == "SUPERVISOR_ALICE"

    # 3. Route out-of-scope ticket to Change Request
    routed = await service.route_to_change_request(
        req_id=mock_ticket.id,
        actor_id="SUPPORT_ENG_1",
        change_request_id="cr-500",
    )
    assert routed.status == "RESOLVED"
    assert "cr-500" in routed.resolution_summary


@pytest.mark.asyncio
async def test_support_service_incident_management():
    """Test incident declaration, timeline event logging, and status transitions."""
    mock_session = AsyncMock()
    service = SupportService(mock_session)

    mock_incident = Incident(
        id="inc-100",
        incident_number="INC-001",
        project_id="proj-100",
        title="Database High Memory Usage",
        description="Memory consumption at 95% on primary database node",
        severity="SEV-2",
        status="DETECTED",
        affected_service="DATABASE",
        impact_summary="Memory consumption at 95% on primary database node",
        detected_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )
    service.repo.get_incident = AsyncMock(return_value=mock_incident)
    service.repo.update_incident = AsyncMock(side_effect=lambda x: x)
    service.repo.add_incident_timeline = AsyncMock()

    # Advance status to CONTAINMENT
    updated = await service.update_incident_status(
        incident_id="inc-100",
        status="MITIGATING",
        actor_id="COMMANDER_BOB",
        message="Scaled up node instance memory to 64GB",
    )
    assert updated.status == "MITIGATING"
    assert updated.mitigated_at is not None

    # Complete Postmortem
    postmortem = await service.update_incident_status(
        incident_id="inc-100",
        status="CLOSED",
        actor_id="COMMANDER_BOB",
        message="Postmortem review meeting concluded.",
        root_cause="Unbounded cache retention in report generation service.",
    )
    assert postmortem.status == "CLOSED"
    assert postmortem.root_cause == "Unbounded cache retention in report generation service."


@pytest.mark.asyncio
async def test_support_service_maintenance_and_health():
    """Test maintenance work order completion and client health scoring."""
    mock_session = AsyncMock()
    service = SupportService(mock_session)

    mock_order = MaintenanceWorkOrder(
        id="wo-100",
        maintenance_plan_id="plan-1",
        project_id="proj-100",
        task_name="Monthly Security Patching",
        category="SECURITY_AUDIT",
        priority="MEDIUM",
        status="PLANNED",
        scheduled_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )
    service.repo.get_work_order = AsyncMock(return_value=mock_order)
    service.repo.update_work_order = AsyncMock(side_effect=lambda x: x)
    service.repo.create_health_snapshot = AsyncMock(side_effect=lambda x: x)

    # Complete work order
    completed = await service.complete_work_order(
        order_id="wo-100",
        actor_id="MAINT_ENG_1",
        result_summary="All CVE patches applied and reboot verified.",
    )
    assert completed.status == "COMPLETED"
    assert completed.executed_by == "MAINT_ENG_1"

    # Calculate client health score
    health = await service.calculate_client_health(
        project_id="proj-100",
        open_tickets_count=1,
        incident_count=0,
        satisfaction_score=4.8,
    )
    assert health.health_status == "HEALTHY"
    assert health.health_score > 90.0
