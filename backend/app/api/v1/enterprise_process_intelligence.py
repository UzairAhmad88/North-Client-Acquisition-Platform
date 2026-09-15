"""
Phase 78: Enterprise Process Intelligence & Autonomous Optimization FastAPI Router.
Prefix: /enterprise-process-intelligence
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.services.process_intelligence.service import EnterpriseProcessIntelligenceService
from app.schemas.enterprise_process_intelligence import (
    ProcessCommandCenterSummaryResponse,
    ProcessDiscoveryRequest,
    ProcessDiscoveryResponse,
    ConformanceCheckRequest,
    ConformanceCheckResponse,
    BottleneckDetectionResponse,
    ProcessWasteAnalysisResponse,
    ProcessSimulationRequest,
    ProcessSimulationResponse,
    ProcessOptimizationRequest,
    ProcessOptimizationResponse,
    AutomationOpportunitiesResponse,
    ProcessChangeSubmitRequest,
    ProcessChangeResponse,
    CaseRoutingRequest,
    CaseRoutingResponse,
    ProcessCopilotQueryRequest,
    ProcessCopilotQueryResponse,
)

router = APIRouter(prefix="/enterprise-process-intelligence", tags=["Enterprise Process Intelligence"])
enterprise_process_intelligence_router = router



def get_process_service() -> EnterpriseProcessIntelligenceService:
    return EnterpriseProcessIntelligenceService()


@router.get("/command-center/summary", response_model=ProcessCommandCenterSummaryResponse)
def get_command_center_summary(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Returns real-time executive operational telemetry of enterprise business workflows."""
    return service.get_command_center_summary(tenant_id=tenant_id)


@router.post("/discovery/run", response_model=ProcessDiscoveryResponse)
def discover_process(
    req: ProcessDiscoveryRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Executes process mining algorithms to discover models, variants, and happy paths."""
    return service.discover_process(
        process_code=req.process_code,
        source_system=req.source_system,
        model_type=req.model_type,
        time_window_days=req.time_window_days,
        tenant_id=req.tenant_id
    )


@router.post("/conformance/check", response_model=ConformanceCheckResponse)
def check_conformance(
    req: ConformanceCheckRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Checks conformance of empirical execution against reference process models."""
    return service.check_conformance(
        process_code=req.process_code,
        reference_model_code=req.reference_model_code,
        tenant_id=req.tenant_id
    )


@router.get("/bottlenecks/{process_code}", response_model=BottleneckDetectionResponse)
def detect_bottlenecks(
    process_code: str,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Identifies critical throughput constraints, wait times, and queue depths."""
    return service.detect_bottlenecks(process_code=process_code, tenant_id=tenant_id)


@router.get("/waste/{process_code}", response_model=ProcessWasteAnalysisResponse)
def analyze_process_waste(
    process_code: str,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Quantifies lean operational waste across waiting, rework, and over-approval."""
    return service.analyze_process_waste(process_code=process_code, tenant_id=tenant_id)


@router.post("/simulations/run", response_model=ProcessSimulationResponse)
def run_simulation(
    req: ProcessSimulationRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Executes discrete-event simulation predicting cycle time, cost, and throughput deltas."""
    return service.simulate_process(
        process_code=req.process_code,
        scenario_name=req.scenario_name,
        modified_variables=req.modified_variables,
        tenant_id=req.tenant_id
    )


@router.post("/optimizations/solve", response_model=ProcessOptimizationResponse)
def solve_optimization(
    req: ProcessOptimizationRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Solves multi-objective Pareto optimization balancing speed, cost, quality, and risk."""
    return service.optimize_process(
        process_code=req.process_code,
        weights=req.weights,
        tenant_id=req.tenant_id
    )


@router.get("/automation/opportunities/{process_code}", response_model=AutomationOpportunitiesResponse)
def get_automation_opportunities(
    process_code: str,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Returns ranked task automation opportunities with ROI and payback calculations."""
    return service.get_automation_opportunities(process_code=process_code, tenant_id=tenant_id)


@router.post("/changes/submit", response_model=ProcessChangeResponse)
def submit_change_request(
    req: ProcessChangeSubmitRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Submits versioned, governed process change request with simulation evidence."""
    return service.submit_change_request(
        process_code=req.process_code,
        proposed_version=req.proposed_version,
        description=req.description,
        simulation_code=req.simulation_code,
        rollback_plan=req.rollback_plan,
        submitter=req.submitter,
        tenant_id=req.tenant_id
    )


@router.post("/cases/route", response_model=CaseRoutingResponse)
def route_case(
    req: CaseRoutingRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Intelligently routes active workflow cases to human experts or AI agents."""
    return service.route_case(
        case_code=req.case_code,
        process_code=req.process_code,
        urgency=req.urgency,
        risk_tier=req.risk_tier,
        tenant_id=req.tenant_id
    )


@router.post("/copilot/query", response_model=ProcessCopilotQueryResponse)
def query_copilot(
    req: ProcessCopilotQueryRequest,
    service: EnterpriseProcessIntelligenceService = Depends(get_process_service)
):
    """Answers natural-language queries about process bottlenecks and performance."""
    return service.query_copilot(
        query=req.query,
        process_code=req.process_code,
        tenant_id=req.tenant_id
    )


@router.get("/agents")
def list_process_agents():
    """Lists all 14 Process Intelligence Agents and their operational status."""
    agents = [
        {"name": "ProcessOrchestrator", "id": "epi_process_orchestrator", "status": "ACTIVE", "autonomy": "L5"},
        {"name": "DiscoveryAgent", "id": "epi_discovery_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ConformanceAgent", "id": "epi_conformance_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "BottleneckAgent", "id": "epi_bottleneck_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "RootCauseAgent", "id": "epi_root_cause_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ProcessAnalystAgent", "id": "epi_process_analyst_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "SimulationAgent", "id": "epi_simulation_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "OptimizationAgent", "id": "epi_optimization_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "AutomationAgent", "id": "epi_automation_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ProcessRiskAgent", "id": "epi_process_risk_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ProcessComplianceAgent", "id": "epi_process_compliance_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "CaseRoutingAgent", "id": "epi_case_routing_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ProcessChangeAgent", "id": "epi_process_change_agent", "status": "ACTIVE", "autonomy": "L4"},
        {"name": "ProcessCopilot", "id": "epi_process_copilot", "status": "ACTIVE", "autonomy": "L4"},
    ]
    return {"total_agents": len(agents), "agents": agents}


@router.get("/catalog")
def list_process_catalog(tenant_id: str = Query("tenant-default")):
    """Returns cataloged business processes."""
    return {
        "total_processes": 5,
        "processes": [
            {"code": "PRC-O2C", "name": "Order-to-Cash", "domain": "FINANCE", "criticality": "CRITICAL"},
            {"code": "PRC-P2P", "name": "Procure-to-Pay", "domain": "OPERATIONS", "criticality": "HIGH"},
            {"code": "PRC-R2R", "name": "Record-to-Report", "domain": "FINANCE", "criticality": "HIGH"},
            {"code": "PRC-H2R", "name": "Hire-to-Retire", "domain": "HR", "criticality": "MEDIUM"},
            {"code": "PRC-I2R", "name": "Incident-to-Resolution", "domain": "IT_SECURITY", "criticality": "CRITICAL"}
        ]
    }


@router.get("/slas")
def list_process_slas(tenant_id: str = Query("tenant-default")):
    """Returns SLA compliance and predicted breach alerts."""
    return {
        "overall_sla_compliance": 94.5,
        "active_breaches": 2,
        "predicted_breaches": 4,
        "slas": [
            {"process": "PRC-O2C", "target_hours": 24.0, "actual_hours": 22.4, "status": "COMPLIANT"},
            {"process": "PRC-P2P", "target_hours": 48.0, "actual_hours": 54.2, "status": "BREACHED"}
        ]
    }


@router.get("/drift/{process_code}")
def get_process_drift(process_code: str, tenant_id: str = Query("tenant-default")):
    """Returns detected process drift metrics against approved baseline."""
    return {
        "process_code": process_code,
        "drift_detected": True,
        "drift_metric": "CYCLE_TIME_SPIKE",
        "observed_delta_percentage": 28.5,
        "threshold_percentage": 15.0,
        "severity": "HIGH",
        "alert_status": "ACTIVE_ESCALATION"
    }
