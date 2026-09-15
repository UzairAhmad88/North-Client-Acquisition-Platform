"""
Phase 76 Test Suite: Autonomous Enterprise AI Operating System (AEAI-OS),
Multi-Agent Intelligence, Agent Mesh, Memory, Tool Orchestration & Governed Autonomous Execution.
Validating Command Center KPIs, Natural Language Control, Agent Mesh Topology, 7-Layer Memory Fabric,
Tool Sandboxing, Human Approvals, Emergency Autonomy Lockdown, 16 Agents/Supervisors, and REST Endpoints.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.services.ai_os.service import AutonomousEnterpriseAIOperatingService
from app.api.v1.ai_os import router as ai_os_router
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS
)
from app.agents import (
    EnterpriseSupervisor,
    BusinessSupervisor,
    FinanceSupervisor,
    OperationsSupervisor,
    StrategySupervisor,
    CustomerSupervisor,
    EngineeringSupervisor,
    SecuritySupervisor,
    ComplianceSupervisor,
    ResearchAgent,
    AnalystAgent,
    PlannerAgent,
    CriticAgent,
    VerifierAgent,
    ApprovalAgent,
    OrchestratorAgent
)
from agents.core.base import AgentContext


@pytest.fixture
def ai_service():
    return AutonomousEnterpriseAIOperatingService()


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(ai_os_router)
    return TestClient(app)


# ----------------------------------------------------------------------
# 1. AI Command Center & Summary Telemetry
# ----------------------------------------------------------------------
def test_command_center_summary(ai_service):
    """Verify synthesis of enterprise AI health, active agents, and ROI metrics."""
    summary = ai_service.get_command_center_summary("tenant-corp-1")
    assert summary["system_health_score"] >= 95.0
    assert summary["active_agents_count"] == 16
    assert summary["running_tasks_count"] >= 0
    assert summary["completed_tasks_count"] > 0
    assert summary["autonomous_actions_executed"] > 0
    assert summary["autonomy_lockdown_active"] is False
    assert summary["total_cost_usd"] > 0
    assert summary["roi_percentage"] > 100.0


# ----------------------------------------------------------------------
# 2. Natural-Language Business Control & Supervisor Routing
# ----------------------------------------------------------------------
def test_natural_language_control_routing(ai_service):
    """Verify natural-language requests route to appropriate domain supervisors."""
    # Finance query
    fin_res = ai_service.execute_natural_language_command(
        "Analyze enterprise revenue variances and overdue invoices",
        tenant_id="tenant-corp-1",
        requested_autonomy="L3"
    )
    assert fin_res["assigned_supervisor"] == "FinanceSupervisor"
    assert len(fin_res["decomposed_tasks"]) >= 3

    # Operations query
    ops_res = ai_service.execute_natural_language_command(
        "Identify supply chain procurement bottlenecks in European distribution",
        tenant_id="tenant-corp-1",
        requested_autonomy="L3"
    )
    assert ops_res["assigned_supervisor"] == "OperationsSupervisor"

    # Strategy query
    strat_res = ai_service.execute_natural_language_command(
        "Simulate demand shocks and customer churn under high inflation",
        tenant_id="tenant-corp-1",
        requested_autonomy="L3"
    )
    assert strat_res["assigned_supervisor"] == "StrategySupervisor"


# ----------------------------------------------------------------------
# 3. Governed Task Execution & Emergency Lockdown Kill-Switch
# ----------------------------------------------------------------------
def test_governed_task_execution_and_lockdown():
    """Verify task execution within policy and immediate blocking under emergency lockdown."""
    svc = AutonomousEnterpriseAIOperatingService()
    
    # 1. Normal execution
    task_res = svc.execute_governed_task(
        task_code="TASK-TEST-01",
        goal="Synthesize risk brief",
        agent_id="aeai_analyst_agent",
        inputs={"scope": "GLOBAL"}
    )
    assert task_res["status"] == "COMPLETED"
    assert task_res["autonomy_level"] == "L4"
    assert "audit_hash" in task_res

    # 2. Engage Emergency Lockdown
    lockdown = svc.trigger_emergency_autonomy_lockdown(
        reason="Suspected automated credential anomaly detected",
        triggered_by="chief-security-officer"
    )
    assert lockdown["status"] == "LOCKDOWN_ENGAGED"
    assert lockdown["lockdown_active"] is True

    # 3. Post-lockdown task must be blocked
    blocked_task = svc.execute_governed_task(
        task_code="TASK-TEST-02",
        goal="Execute automated supplier order",
        agent_id="aeai_orchestrator_agent",
        inputs={"scope": "PROCUREMENT"}
    )
    assert blocked_task["status"] == "BLOCKED_BY_LOCKDOWN"


# ----------------------------------------------------------------------
# 4. Agent Mesh Topology & Observable Channels
# ----------------------------------------------------------------------
def test_agent_mesh_topology(ai_service):
    """Verify agent mesh topology exposes all supervisors and observable channels."""
    mesh = ai_service.get_agent_mesh_topology("tenant-corp-1")
    assert mesh["enterprise_orchestrator"] == "OrchestratorAgent"
    assert len(mesh["supervisors"]) == 9
    assert len(mesh["execution_agents"]) == 6
    assert mesh["active_channels_count"] > 0
    assert mesh["channel_status"] == "POLICY_INSPECTED_AND_OBSERVABLE"


# ----------------------------------------------------------------------
# 5. 7-Layer Memory Fabric & Tool Gateway
# ----------------------------------------------------------------------
def test_memory_fabric_and_tool_gateway(ai_service):
    """Verify 7-layer memory storage/retrieval and sandboxed tool execution."""
    # Memory store
    mem_store = ai_service.store_memory(
        memory_type="EPISODIC",
        key="supplier_shock_response_2026",
        content={"action": "rebalance_buffer", "outcome": "zero_downtime"},
        tenant_id="tenant-corp-1"
    )
    assert mem_store["memory_type"] == "EPISODIC"
    assert mem_store["confidence_score"] == 1.0

    # Memory retrieve
    retrieved = ai_service.retrieve_memory("supplier_shock", memory_type="EPISODIC")
    assert len(retrieved) >= 1
    assert retrieved[0]["confidence_score"] > 0.9

    # Tool execution in sandbox
    tool_res = ai_service.execute_tool(
        tool_code="TOOL-OPS-MRP-EXPLOSION",
        agent_id="aeai_planner_agent",
        inputs={"sku": "CHIP-ADV-01"},
        sandbox_override="RESTRICTED"
    )
    assert tool_res["status"] == "COMPLETED"
    assert tool_res["sandbox_mode"] == "RESTRICTED"
    assert "audit_hash" in tool_res


# ----------------------------------------------------------------------
# 6. Human Approval Engine
# ----------------------------------------------------------------------
def test_human_approval_workflow(ai_service):
    """Verify routing of high-risk actions to human approval gates and decision recording."""
    # Route approval
    appr = ai_service.route_approval(
        task_id="task-capex-99",
        action_name="AUTHORIZE_HIGH_VALUE_DISBURSEMENT",
        risk_level="HIGH",
        impact_summary="Authorize $450,000 procurement commitment",
        evidence={"roi": "24.5%", "supplier_verified": True}
    )
    assert appr["status"] == "PENDING"
    assert "APPR-" in appr["approval_code"]

    # Resolve approval
    resolved = ai_service.resolve_approval(
        approval_code=appr["approval_code"],
        action="APPROVE",
        approver_id="cfo-user-1",
        reason="Verified quarterly budget runway"
    )
    assert resolved["status"] == "APPROVED"
    assert resolved["approver_id"] == "cfo-user-1"


# ----------------------------------------------------------------------
# 7. Security Permissions & Non-Negotiable Safety Prohibitions
# ----------------------------------------------------------------------
def test_aeai_permissions_and_prohibitions():
    """Verify Phase 76 AgentPermissions and strict non-negotiable prohibitions exist."""
    # Permissions verification
    assert AgentPermission.READ_AEAI_OS.value == "READ_AEAI_OS"
    assert AgentPermission.ORCHESTRATE_ENTERPRISE_AGENT_MESH.value == "ORCHESTRATE_ENTERPRISE_AGENT_MESH"
    assert AgentPermission.EXECUTE_GOVERNED_AUTONOMOUS_WORKFLOW.value == "EXECUTE_GOVERNED_AUTONOMOUS_WORKFLOW"
    assert AgentPermission.MANAGE_AEAI_TOOL_REGISTRY.value == "MANAGE_AEAI_TOOL_REGISTRY"
    assert AgentPermission.ACCESS_ENTERPRISE_MEMORY_FABRIC.value == "ACCESS_ENTERPRISE_MEMORY_FABRIC"
    assert AgentPermission.GOVERN_AGENT_LIFECYCLE_DEPLOYMENT.value == "GOVERN_AGENT_LIFECYCLE_DEPLOYMENT"
    assert AgentPermission.TRIGGER_EMERGENCY_AUTONOMY_LOCKDOWN.value == "TRIGGER_EMERGENCY_AUTONOMY_LOCKDOWN"

    # Non-negotiable strategic prohibitions verification
    expected_prohibitions = [
        "AUTONOMOUS_MODIFY_OWN_PERMISSIONS",
        "AUTONOMOUS_DISABLE_GOVERNANCE_GUARDRAILS",
        "AUTONOMOUS_EXCEED_ACTION_LIMITS",
        "AUTONOMOUS_BYPASS_HUMAN_APPROVAL_GATES",
        "UNRESTRICTED_AUTONOMOUS_SELF_MODIFICATION",
        "AUTONOMOUS_EXPOSE_CREDENTIALS_TO_CONTEXT"
    ]
    for p in expected_prohibitions:
        assert p in PROHIBITED_PERMISSIONS


# ----------------------------------------------------------------------
# 8. All 16 Autonomous Enterprise AI Agents & Supervisors Execution
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_all_16_autonomous_ai_agents():
    """Verify all 16 autonomous agents and supervisors instantiate and execute safely."""
    agents = [
        EnterpriseSupervisor(),
        BusinessSupervisor(),
        FinanceSupervisor(),
        OperationsSupervisor(),
        StrategySupervisor(),
        CustomerSupervisor(),
        EngineeringSupervisor(),
        SecuritySupervisor(),
        ComplianceSupervisor(),
        ResearchAgent(),
        AnalystAgent(),
        PlannerAgent(),
        CriticAgent(),
        VerifierAgent(),
        ApprovalAgent(),
        OrchestratorAgent()
    ]
    assert len(agents) == 16

    context = AgentContext(
        workflow_id="wf-aeai-test",
        task_id="t-aeai-test-1",
        agent_run_id="run-aeai-test-1",
        metadata={"tenant_id": "tenant-corp-1", "autonomy_level": "L4"}
    )
    for agent in agents:
        res = await agent.run(context)
        assert res.status == "COMPLETED"
        assert res.confidence == "HIGH"
        assert "summary" in res.result
        assert res.result["autonomy_level"] == "L4"
        assert len(res.result["recommendations"]) >= 1


# ----------------------------------------------------------------------
# 9. FastAPI REST Endpoints Integration
# ----------------------------------------------------------------------
def test_api_command_center_and_control(test_client):
    """Test GET /ai-os/command-center/summary and POST /ai-os/control/natural-language."""
    summary_resp = test_client.get("/ai-os/command-center/summary?tenant_id=tenant-corp-1")
    assert summary_resp.status_code == 200
    summary_data = summary_resp.json()
    assert summary_data["system_health_score"] >= 95.0
    assert summary_data["active_agents_count"] == 16

    control_resp = test_client.post(
        "/ai-os/control/natural-language",
        json={
            "query": "Review Q3 financial runway and flag burn rate anomalies",
            "tenant_id": "tenant-corp-1",
            "requested_autonomy": "L3"
        }
    )
    assert control_resp.status_code == 200
    control_data = control_resp.json()
    assert control_data["assigned_supervisor"] == "FinanceSupervisor"


def test_api_tasks_and_agents(test_client):
    """Test POST /ai-os/tasks/execute, GET /ai-os/agents, and GET /ai-os/mesh/topology."""
    task_resp = test_client.post("/ai-os/tasks/execute?task_code=T-90&goal=Analyze+Lead+Quality")
    assert task_resp.status_code == 200
    assert task_resp.json()["status"] == "COMPLETED"

    agents_resp = test_client.get("/ai-os/agents?tenant_id=tenant-corp-1")
    assert agents_resp.status_code == 200
    agents = agents_resp.json()
    assert len(agents) >= 2

    mesh_resp = test_client.get("/ai-os/mesh/topology?tenant_id=tenant-corp-1")
    assert mesh_resp.status_code == 200
    assert len(mesh_resp.json()["supervisors"]) == 9


def test_api_tools_and_memory(test_client):
    """Test tools and memory endpoints."""
    # List tools
    tools_resp = test_client.get("/ai-os/tools")
    assert tools_resp.status_code == 200
    assert len(tools_resp.json()) >= 2

    # Execute tool
    tool_exec_resp = test_client.post(
        "/ai-os/tools/execute",
        json={
            "tool_code": "TOOL-FIN-GENERAL-LEDGER",
            "agent_id": "aeai_analyst_agent",
            "inputs": {"fiscal_period": "2026-Q2"}
        }
    )
    assert tool_exec_resp.status_code == 200
    assert tool_exec_resp.json()["status"] == "COMPLETED"

    # Store memory
    store_resp = test_client.post(
        "/ai-os/memory/store",
        json={
            "memory_type": "SEMANTIC",
            "key": "corp_discount_policy",
            "content": {"max_unreviewed_discount_pct": 10.0}
        }
    )
    assert store_resp.status_code == 200
    assert store_resp.json()["memory_type"] == "SEMANTIC"

    # Retrieve memory
    retrieve_resp = test_client.post(
        "/ai-os/memory/retrieve",
        json={"query": "discount_policy", "memory_type": "SEMANTIC"}
    )
    assert retrieve_resp.status_code == 200
    assert len(retrieve_resp.json()) >= 1


def test_api_approvals_lockdown_roi(test_client):
    """Test approvals, emergency lockdown, and ROI metrics endpoints."""
    # List approvals
    appr_resp = test_client.get("/ai-os/approvals")
    assert appr_resp.status_code == 200
    assert len(appr_resp.json()) >= 1

    # Action approval
    appr_action_resp = test_client.post(
        "/ai-os/approvals/APPR-2026-CAPEX-EU/action",
        json={"action": "APPROVE", "approver_id": "exec-ceo", "reason": "Strategic priority"}
    )
    assert appr_action_resp.status_code == 200
    assert appr_action_resp.json()["status"] == "APPROVED"

    # Emergency lockdown
    lockdown_resp = test_client.post(
        "/ai-os/emergency/lockdown",
        json={
            "event_type": "EMERGENCY_LOCKDOWN",
            "target_scope": "GLOBAL",
            "reason": "Security Drill Simulation",
            "triggered_by": "sec-ops-team"
        }
    )
    assert lockdown_resp.status_code == 200
    assert lockdown_resp.json()["lockdown_active"] is True

    # ROI metrics
    roi_resp = test_client.get("/ai-os/roi/metrics?period=2026-Q3")
    assert roi_resp.status_code == 200
    assert roi_resp.json()["net_roi_percentage"] > 200.0
