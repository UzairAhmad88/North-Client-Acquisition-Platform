"""
Unit test suite for Phase 78: Enterprise Process Intelligence, Process Mining,
Workflow Discovery, Operational Conformance, Bottleneck Intelligence & Autonomous Process Optimization.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.services.process_intelligence.service import enterprise_process_intelligence_service
from backend.app.agents.process import (
    ProcessOrchestrator,
    DiscoveryAgent,
    ConformanceAgent,
    BottleneckAgent,
    RootCauseAgent,
    ProcessAnalystAgent,
    SimulationAgent,
    OptimizationAgent,
    AutomationAgent,
    ProcessRiskAgent,
    ProcessComplianceAgent,
    CaseRoutingAgent,
    ProcessChangeAgent,
    ProcessCopilot,
)
from backend.app.api.v1.enterprise_process_intelligence import enterprise_process_intelligence_router


@pytest.fixture
def client():
    app = FastAPI(title="Test Enterprise Process Intelligence")
    app.include_router(enterprise_process_intelligence_router)
    return TestClient(app)


def test_command_center_telemetry():
    telemetry = enterprise_process_intelligence_service.get_command_center_telemetry()
    assert telemetry is not None
    assert "catalog_summary" in telemetry
    assert "bottlenecks_detected" in telemetry
    assert "conformance_overall_rate" in telemetry
    assert "war_room" in telemetry
    assert telemetry["conformance_overall_rate"] >= 0.85
    assert telemetry["automation_pipeline_value_usd"] > 0


def test_process_catalog_and_discovery():
    catalog = enterprise_process_intelligence_service.get_process_catalog()
    assert len(catalog) >= 7
    proc_ids = [p["process_id"] for p in catalog]
    assert "PROC-O2C-001" in proc_ids
    assert "PROC-P2P-001" in proc_ids

    discovery = enterprise_process_intelligence_service.discover_process_model("PROC-O2C-001")
    assert discovery["process_id"] == "PROC-O2C-001"
    assert "directly_follows_graph" in discovery
    assert "bpmn_xml" in discovery
    assert "discovered_variants" in discovery
    assert len(discovery["nodes"]) > 0
    assert len(discovery["edges"]) > 0


def test_conformance_checking():
    conformance = enterprise_process_intelligence_service.run_conformance_check("PROC-O2C-001")
    assert conformance["process_id"] == "PROC-O2C-001"
    assert conformance["fitness"] >= 0.8
    assert conformance["conformance_rate"] >= 0.8
    assert "deviations" in conformance
    assert "skipped_approvals" in conformance
    assert "rework_loops" in conformance


def test_bottlenecks_and_heatmaps():
    bottlenecks = enterprise_process_intelligence_service.detect_bottlenecks("PRC-O2C")
    assert bottlenecks.process_code == "PRC-O2C"
    assert bottlenecks.total_bottlenecks > 0
    assert bottlenecks.critical_activity is not None
    assert bottlenecks.avg_wait_hours > 0
    assert bottlenecks.lean_waste_category == "WAITING"


def test_waste_and_lean_analysis():
    waste = enterprise_process_intelligence_service.analyze_process_waste("PRC-O2C")
    assert waste.process_code == "PRC-O2C"
    assert waste.total_hours_wasted_per_month > 0
    assert "WAITING" in waste.waste_by_category
    assert "REWORK" in waste.waste_by_category
    assert len(waste.top_wasteful_activities) > 0


def test_discrete_event_simulation():
    scenario = {
        "demand_multiplier": 1.25,
        "additional_fte": 2,
        "automated_activities": ["Credit Check Automation"],
    }
    sim = enterprise_process_intelligence_service.run_discrete_event_simulation("PROC-O2C-001", scenario)
    assert sim["process_id"] == "PROC-O2C-001"
    assert "baseline_metrics" in sim
    assert "simulated_metrics" in sim
    assert "cycle_time_reduction_pct" in sim
    assert sim["simulated_metrics"]["avg_cycle_time_hours"] <= sim["baseline_metrics"]["avg_cycle_time_hours"]


def test_multi_objective_optimization():
    opt = enterprise_process_intelligence_service.run_multi_objective_optimization(
        "PROC-O2C-001", ["speed", "cost", "compliance"]
    )
    assert opt["process_id"] == "PROC-O2C-001"
    assert "pareto_front" in opt
    assert len(opt["pareto_front"]) >= 3
    assert "recommended_configuration" in opt


def test_automation_opportunities_and_roi():
    opps = enterprise_process_intelligence_service.evaluate_automation_opportunities("PROC-O2C-001")
    assert opps["process_id"] == "PROC-O2C-001"
    assert len(opps["opportunities"]) > 0
    assert opps["total_annual_savings_usd"] > 0

    first_opp = opps["opportunities"][0]
    assert "technology_fit" in first_opp
    assert "payback_period_months" in first_opp
    assert "roi_pct" in first_opp


def test_governed_process_change_control():
    # Submit change
    submission = enterprise_process_intelligence_service.submit_change_request(
        process_code="PRC-O2C",
        proposed_version="2.1.0",
        description="Deploy validated AI agent to pre-screen invoices under $500",
        rollback_plan="Restore manual routing rule if error rate exceeds 0.5%",
        submitter="Finance Automation Architect"
    )
    assert submission.change_code.startswith("CR-PRC-O2C")
    assert submission.status == "PENDING_APPROVAL"
    change_id = submission.change_code

    # Review & approve change
    review = enterprise_process_intelligence_service.review_change_request(
        change_id, "APPROVE", reviewer="VP Operations & Compliance", comments="Approved with rollback guardrails active"
    )
    assert review["status"] == "APPROVED"
    assert review["reviewer"] == "VP Operations & Compliance"

    # Deploy change
    deploy = enterprise_process_intelligence_service.deploy_change_request(change_id)
    assert deploy["status"] == "DEPLOYED"
    assert deploy["deployed_at"] is not None


def test_intelligent_case_routing():
    routing = enterprise_process_intelligence_service.route_case(
        case_code="CASE-2026-9912",
        process_code="PRC-O2C",
        urgency="HIGH",
        risk_tier="LOW"
    )
    assert routing.case_code == "CASE-2026-9912"
    assert routing.routed_actor_type == "AI_AGENT"
    assert routing.assigned_target == "OrderProcessingAgent"
    assert routing.priority_rank == 1


def test_ai_process_copilot():
    question = "Why is the Procure-to-Pay process experiencing high wait times in approval?"
    response = enterprise_process_intelligence_service.ask_copilot(question, "PROC-P2P-001")
    assert response["question"] == question
    assert response["process_id"] == "PROC-P2P-001"
    assert "answer" in response
    assert len(response["evidence_sources"]) > 0
    assert "recommended_actions" in response


from agents.core.context import AgentContext


@pytest.mark.asyncio
async def test_14_process_intelligence_agents():
    agents = [
        ProcessOrchestrator(),
        DiscoveryAgent(),
        ConformanceAgent(),
        BottleneckAgent(),
        RootCauseAgent(),
        ProcessAnalystAgent(),
        SimulationAgent(),
        OptimizationAgent(),
        AutomationAgent(),
        ProcessRiskAgent(),
        ProcessComplianceAgent(),
        CaseRoutingAgent(),
        ProcessChangeAgent(),
        ProcessCopilot(),
    ]

    assert len(agents) == 14

    ctx = AgentContext(
        workflow_id="wf-test-epi-001",
        task_id="task-test-epi-001",
        agent_run_id="run-test-epi-001",
        metadata={"tenant_id": "test_tenant", "process_id": "PROC-O2C-001"}
    )

    for agent in agents:
        res = await agent.run(ctx)
        assert res is not None
        assert res.status == "COMPLETED"
        assert res.metadata["name"] == agent.name
        assert "confidence_score" in res.result




def test_fastapi_rest_endpoints(client):
    # 1. Command Center Summary
    resp = client.get("/enterprise-process-intelligence/command-center/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_processes_cataloged"] > 0
    assert data["active_bottlenecks_count"] >= 0

    # 2. Catalog
    resp = client.get("/enterprise-process-intelligence/catalog")
    assert resp.status_code == 200
    catalog = resp.json()
    assert catalog["total_processes"] >= 5

    # 3. Discovery
    resp = client.post(
        "/enterprise-process-intelligence/discovery/run",
        json={"process_code": "PRC-O2C", "model_type": "BPMN", "time_window_days": 30},
    )
    assert resp.status_code == 200
    assert resp.json()["process_code"] == "PRC-O2C"

    # 4. Conformance
    resp = client.post(
        "/enterprise-process-intelligence/conformance/check",
        json={"process_code": "PRC-O2C", "reference_model_code": "REF-O2C-01"},
    )
    assert resp.status_code == 200
    assert resp.json()["conformance_rate_percentage"] >= 90.0

    # 5. Bottlenecks
    resp = client.get("/enterprise-process-intelligence/bottlenecks/PRC-O2C")
    assert resp.status_code == 200
    assert resp.json()["total_bottlenecks"] > 0

    # 6. Waste
    resp = client.get("/enterprise-process-intelligence/waste/PRC-O2C")
    assert resp.status_code == 200
    assert "waste_by_category" in resp.json()

    # 7. Simulation
    resp = client.post(
        "/enterprise-process-intelligence/simulations/run",
        json={"process_code": "PRC-O2C", "scenario_name": "Automation Pre-Check", "modified_variables": {"fte_delta": 2}},
    )
    assert resp.status_code == 200
    assert resp.json()["predicted_cycle_time_delta_percent"] < 0

    # 8. Optimization
    resp = client.post(
        "/enterprise-process-intelligence/optimizations/solve",
        json={"process_code": "PRC-O2C", "weights": {"speed": 0.5, "cost": 0.5}},
    )
    assert resp.status_code == 200
    assert "pareto_solutions_count" in resp.json()

    # 9. Automation
    resp = client.get("/enterprise-process-intelligence/automation/opportunities/PRC-O2C")
    assert resp.status_code == 200
    assert len(resp.json()["opportunities"]) > 0

    # 10. Change Request Submission
    change_req = {
        "process_code": "PRC-O2C",
        "proposed_version": "2.1.0",
        "description": "Auto-approve low risk invoices",
        "rollback_plan": "Revert to rule v2.0",
        "submitter": "EnterpriseArchitect"
    }
    resp = client.post("/enterprise-process-intelligence/changes/submit", json=change_req)
    assert resp.status_code == 200
    assert resp.json()["status"] == "PENDING_APPROVAL"

    # 11. Case Routing
    resp = client.post(
        "/enterprise-process-intelligence/cases/route",
        json={"case_code": "CASE-TEST-1", "process_code": "PRC-O2C", "urgency": "HIGH", "risk_tier": "LOW"},
    )
    assert resp.status_code == 200
    assert resp.json()["routed_actor_type"] == "AI_AGENT"

    # 12. Copilot Query
    resp = client.post(
        "/enterprise-process-intelligence/copilot/query",
        json={"query": "Identify top bottlenecks in O2C", "process_code": "PRC-O2C"},
    )
    assert resp.status_code == 200
    assert "answer" in resp.json()

    # 13. Agents List
    resp = client.get("/enterprise-process-intelligence/agents")
    assert resp.status_code == 200
    assert resp.json()["total_agents"] == 14

    # 14. SLAs
    resp = client.get("/enterprise-process-intelligence/slas")
    assert resp.status_code == 200
    assert resp.json()["overall_sla_compliance"] > 90.0

    # 15. Drift
    resp = client.get("/enterprise-process-intelligence/drift/PRC-O2C")
    assert resp.status_code == 200
    assert resp.json()["drift_detected"] is True

