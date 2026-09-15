"""
Unit test suite for Phase 68: Autonomous Infrastructure, Cloud Operating System,
Kubernetes Intelligence, FinOps, Capacity Planning & Self-Optimizing Platform.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.autonomous_infrastructure_cloud_os import Base as InfraBase
from app.services.infrastructure.service import AutonomousInfrastructureCloudOsService

# 18 Autonomous Infrastructure AI Agents
from agents.core.context import AgentContext
from agents.infrastructure import (
    InfrastructureOrchestratorAgent,
    InventoryAgent,
    CloudHealthAgent,
    KubernetesAgent,
    ScalingAgent,
    CapacityAgent,
    FinOpsAgent,
    CostAnomalyAgent,
    NetworkAgent,
    StorageAgent,
    DatabaseInfrastructureAgent,
    GpuAgent,
    DriftAgent,
    ReliabilityAgent,
    DisasterRecoveryAgent,
    OptimizationAgent,
    IncidentAgent,
    RemediationAgent,
)


@pytest.fixture(scope="module")
def db_session():
    """In-memory SQLite test database for Phase 68 isolated to infra_ tables."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    infra_tables = [t for name, t in InfraBase.metadata.tables.items() if name.startswith("infra_")]
    InfraBase.metadata.create_all(bind=engine, tables=infra_tables)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def infra_service(db_session):
    return AutonomousInfrastructureCloudOsService(db_session)


def test_cloud_account_lifecycle(infra_service):
    """Test registering cloud accounts with credential vault references."""
    account = infra_service.accounts.register_account(
        provider="AWS",
        account_identifier="123456789012",
        organization="Uzaii Enterprise Cloud Org",
        environment="PRODUCTION",
        default_region="us-east-1",
        tenant_id="t_infra_01"
    )
    assert account["account_identifier"] == "123456789012"
    assert account["provider"] == "AWS"
    assert account["security_state"] == "COMPLIANT"
    assert account["status"] == "ACTIVE"

    accounts = infra_service.accounts.list_accounts("t_infra_01")
    assert len(accounts) >= 1


def test_multi_region_catalog(infra_service):
    """Test querying cloud regions and validating latency and health."""
    regions = infra_service.regions.list_regions(provider="AWS", tenant_id="t_infra_01")
    assert len(regions) >= 3
    assert regions[0]["health_status"] == "HEALTHY"
    assert regions[0]["region_name"] == "us-east-1"


def test_resource_inventory_and_tagging(infra_service):
    """Test cataloging cloud resources with mandatory governance metadata."""
    res = infra_service.resources.catalog_resource(
        account_id="acc_aws_01",
        resource_type="LOAD_BALANCER",
        native_id="arn:aws:elasticloadbalancing:us-east-1:123456:loadbalancer/app/k8s-alb",
        name="k8s-ingress-alb",
        region="us-east-1",
        environment="PRODUCTION",
        tenant_id="t_infra_01"
    )
    assert res["name"] == "k8s-ingress-alb"
    assert res["criticality"] == "TIER_1"
    assert res["status"] == "ACTIVE"

    all_res = infra_service.resources.list_resources("t_infra_01")
    assert len(all_res) >= 1


def test_resource_graph_and_blast_radius(infra_service):
    """Test infrastructure dependency relationships and blast radius traversal."""
    edge = infra_service.resource_graph.link_resources(
        source_id="res_api_gateway",
        target_id="res_aurora_db",
        relation="DEPENDS_ON",
        tenant_id="t_infra_01"
    )
    assert edge["source_id"] == "res_api_gateway"
    assert edge["relation"] == "DEPENDS_ON"

    impact = infra_service.resource_graph.query_impact(
        resource_id="res_api_gateway"
    )
    assert impact["resource_id"] == "res_api_gateway"
    assert impact["blast_radius_count"] >= 1
    assert "res_aurora_db" in impact["affected_downstream"]


def test_compute_instance_management(infra_service):
    """Test tracking virtual machines and compute telemetry."""
    metrics = infra_service.compute.get_compute_metrics(
        instance_id="i-0123456789abcdef0"
    )
    assert metrics["status"] == "HEALTHY"
    assert metrics["cpu_utilization_pct"] > 0
    assert metrics["memory_utilization_pct"] > 0


def test_kubernetes_platform_and_workloads(infra_service):
    """Test managing Kubernetes clusters, nodes, workloads, and cluster health."""
    cluster = infra_service.clusters.register_cluster(
        cluster_name="eks-prod-us-east-1",
        provider="EKS",
        region="us-east-1",
        tenant_id="t_infra_01"
    )
    assert cluster["cluster_name"] == "eks-prod-us-east-1"
    assert cluster["health_status"] == "HEALTHY"

    nodes = infra_service.nodes.list_nodes(cluster["id"])
    assert len(nodes) >= 2
    assert nodes[0]["ready"] is True

    workloads = infra_service.workloads.list_workloads(cluster["id"], namespace="production")
    assert len(workloads) >= 2
    assert workloads[0]["health_status"] == "HEALTHY"

    k8s_health = infra_service.kubernetes.get_platform_health("t_infra_01")
    assert k8s_health["status"] == "OPTIMAL"
    assert k8s_health["failing_pods"] == 0


def test_gpu_infrastructure_and_scheduling(infra_service):
    """Test tracking GPU accelerator pools and inference workload statistics."""
    gpu = infra_service.gpu.get_gpu_cluster_stats("t_infra_01")
    assert gpu["total_gpus"] >= 16
    assert gpu["status"] == "OPTIMAL"
    assert "NVIDIA_H100_SXM5" in gpu["gpu_types"]


def test_drift_detection_and_reconciliation(infra_service):
    """Test continuous reconciliation between declared IaC and real infrastructure."""
    drift = infra_service.drift.scan_for_drift(
        cluster_id="res_alb_01"
    )
    assert drift["drift_detected"] is False
    assert drift["status"] == "IN_SYNC"


def test_autoscaling_policies_and_safety_checks(infra_service):
    """Test autoscaling evaluation considering utilization and safety guardrails."""
    decision = infra_service.scaling.evaluate_scaling(
        "deploy-order-processor",
        88.5,
        tenant_id="t_infra_01"
    )
    assert decision["target_replicas"] >= 4
    assert decision["requires_human_approval"] is False


def test_predictive_capacity_forecasting(infra_service):
    """Test 90-day demand and capacity exhaustion horizons."""
    cap = infra_service.capacity.forecast_capacity(
        resource_type="CPU_CORES",
        horizon_days=90
    )
    assert cap["horizon_days"] == 90
    assert cap["headroom_percentage"] > 0
    assert cap["risk_level"] == "LOW"

    growth = infra_service.forecasting.predict_load_growth("core-api")
    assert growth["service_name"] == "core-api"
    assert growth["projected_q4_qps_growth_pct"] > 0


def test_finops_budgets_and_anomalies(infra_service):
    """Test cloud cost attribution, budget thresholds, and FinOps analytics."""
    budget = infra_service.budgets.get_budget_status("t_infra_01")
    assert budget["monthly_limit_usd"] == 20000.0
    assert budget["alert_state"] == "HEALTHY"

    cost = infra_service.cost.get_monthly_spend("t_infra_01")
    assert cost["total_spend_usd"] > 0
    assert "kubernetes_nodes" in cost["by_service"]

    finops = infra_service.finops.analyze_finops("t_infra_01")
    assert finops["finops_maturity_score"] > 90.0


def test_resource_self_optimization_and_savings(infra_service):
    """Test identifying waste, rightsizing opportunities, and verified savings."""
    opts = infra_service.optimization.identify_optimizations("t_infra_01")
    assert len(opts) >= 2
    assert any(o["type"] == "RIGHTSIZING" for o in opts)

    savings = infra_service.savings.get_savings_report()
    assert savings["realized_savings_ytd_usd"] > 0
    assert savings["active_initiatives"] >= 1


def test_disaster_recovery_and_backup_validation(infra_service):
    """Test DR plans, sandbox restore tests, and RPO/RTO validation."""
    dr = infra_service.disaster_recovery.validate_dr_plan("Core DR")
    assert dr["failover_readiness"] == "READY"
    assert dr["last_drill_status"] == "PASSED"

    backup = infra_service.backups.verify_backup("bk_01")
    assert backup["checksum_verified"] is True
    assert backup["restore_test_status"] == "PASSED"


def test_change_simulation_and_blast_radius(infra_service):
    """Test deterministic blast radius and dry run safety simulation."""
    sim = infra_service.change_management.simulate_change(
        "res_01",
        "RIGHTSIZE_NODE_GROUP"
    )
    assert sim["dry_run_passed"] is True
    assert sim["rollback_plan_verified"] is True
    assert "core-api" in sim["affected_services"]


@pytest.mark.asyncio
async def test_all_18_infrastructure_agents():
    """Verify all 18 Autonomous Infrastructure Agents execute cleanly under AgentContext."""
    agents = [
        InfrastructureOrchestratorAgent(),
        InventoryAgent(),
        CloudHealthAgent(),
        KubernetesAgent(),
        ScalingAgent(),
        CapacityAgent(),
        FinOpsAgent(),
        CostAnomalyAgent(),
        NetworkAgent(),
        StorageAgent(),
        DatabaseInfrastructureAgent(),
        GpuAgent(),
        DriftAgent(),
        ReliabilityAgent(),
        DisasterRecoveryAgent(),
        OptimizationAgent(),
        IncidentAgent(),
        RemediationAgent(),
    ]
    assert len(agents) == 18

    ctx = AgentContext(
        workflow_id="wf_infra_test",
        task_id="task_cloud_health",
        agent_run_id="run_infra_001",
        metadata={"tenant_id": "t_infra_01"}
    )

    for agent in agents:
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["tenant_id"] == "t_infra_01"
        assert len(agent.get_required_permissions()) > 0


def test_closed_loop_10_stage_operating_cycle(infra_service):
    """Test the complete closed-loop autonomous operating cycle."""
    cycle = infra_service.run_infrastructure_optimization_cycle(
        tenant_id="t_infra_01",
        cluster_name="prod-cluster-01",
        dry_run=True
    )
    assert cycle["status"] == "COMPLETED"
    assert len(cycle["phases_executed"]) == 6
    assert len(cycle["actions_taken"]) >= 6
    assert cycle["dry_run"] is True


def test_command_center_summary(infra_service):
    """Test executive command center KPI aggregation."""
    summary = infra_service.get_command_center_summary(tenant_id="t_infra_01")
    assert summary["cloud_health_score"] >= 90.0
    assert summary["active_infrastructure_agents"] == 18
    assert summary["kubernetes_clusters_count"] > 0
    assert summary["monthly_cloud_spend_usd"] > 0
