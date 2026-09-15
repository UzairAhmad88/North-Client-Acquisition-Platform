"""Unit tests for Phase 43 — Unified Reliability, SRE, Disaster Recovery & Platform Resilience."""

import os
import sys
import time
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import pytest

from app.reliability.base import (
    CircuitState,
    IncidentSeverity,
    IncidentStatus,
    ServiceHealthStatus,
    SLOType,
    ErrorBudgetStatus,
    BackupStatus,
    RestoreTestStatus,
    DeploymentHealthStatus,
    DrillStatus,
    DRPlanStatus,
)
from app.reliability.dependencies import CircuitBreaker, DependencyManager, CircuitBreakerOpenException
from app.reliability.resilience import (
    RetryPolicy,
    IdempotencyGuard,
    GracefulDegradationManager,
    MaxRetriesExceededException,
    IdempotencyConflictException,
)
from app.reliability.health import DeepHealthEngine
from app.reliability.slo import SLOEngine, SLOSnapshot
from app.reliability.incidents import IncidentManager
from app.reliability.integrity import DataIntegrityChecker
from app.reliability.service import ReliabilityPlatformService

from app.disaster_recovery.backup import BackupManager
from app.disaster_recovery.restore import RestoreVerifier
from app.disaster_recovery.plans import DisasterRecoveryPlanRegistry, DEFAULT_RECOVERY_PRIORITY
from app.disaster_recovery.drills import DisasterRecoveryDrillManager
from app.disaster_recovery.service import DisasterRecoveryService

from app.operations.deployments import DeploymentManager
from app.operations.rollbacks import RollbackManager
from app.operations.feature_flags import FeatureFlagManager
from app.operations.service import OperationsService

from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
    check_tool_permission,
)
from agents.core.errors import AgentPermissionDeniedError


class TestHealthEngine:
    """Test multi-tier health diagnostics."""

    def test_deep_health_probes_healthy(self):
        engine = DeepHealthEngine()
        result = engine.evaluate_deep_health()
        assert result.total_components == 8
        assert "Redis Cache & PubSub" in result.components
        assert "Background Task Workers & Queue" in result.components
        assert "Object & Document Storage" in result.components
        assert "AI Provider Subsystem" in result.components
        assert "Payment Gateway Integration" in result.components
        assert "Workflow Orchestration Engine" in result.components
        assert "Unified Search Index" in result.components

    def test_individual_subsystem_checks(self):
        engine = DeepHealthEngine()
        redis_chk = engine.check_redis_cache()
        assert redis_chk.status == ServiceHealthStatus.HEALTHY
        assert redis_chk.latency_ms >= 0.0

        queues_chk = engine.check_queues_and_workers()
        assert queues_chk.status == ServiceHealthStatus.HEALTHY

        storage_chk = engine.check_object_storage()
        assert storage_chk.status == ServiceHealthStatus.HEALTHY

        ai_chk = engine.check_ai_providers()
        assert ai_chk.status == ServiceHealthStatus.HEALTHY

        pay_chk = engine.check_payment_gateway()
        assert pay_chk.status == ServiceHealthStatus.HEALTHY


class TestCircuitBreakersAndResilience:
    """Test circuit breaker state machine, retries, idempotency, and graceful degradation."""

    def test_circuit_breaker_transitions(self):
        cb = CircuitBreaker("payment_gateway", failure_threshold=2, recovery_timeout_seconds=0.2, half_open_success_threshold=1)
        assert cb.state == CircuitState.CLOSED
        assert cb.can_execute() is True

        # First failure
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 1

        # Second failure -> Trips to OPEN
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert cb.can_execute() is False

        # Attempt to execute on open circuit raises exception
        with pytest.raises(CircuitBreakerOpenException):
            cb.execute(lambda: "Call external")

        # Wait for recovery timeout
        time.sleep(0.25)
        assert cb.can_execute() is True
        assert cb.state == CircuitState.HALF_OPEN

        # Success in HALF_OPEN recovers to CLOSED
        cb.record_success()
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    def test_retry_policy_exponential_backoff_and_jitter(self):
        policy = RetryPolicy(max_attempts=3, initial_delay_seconds=0.01, backoff_multiplier=2.0, enable_jitter=True)
        attempts = 0

        def flaky_operation():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ValueError("Transient network glitch")
            return "SUCCESS"

        res = policy.execute(flaky_operation)
        assert res == "SUCCESS"
        assert attempts == 3

    def test_retry_policy_exhaustion(self):
        policy = RetryPolicy(max_attempts=2, initial_delay_seconds=0.01)

        def failing_operation():
            raise ConnectionRefusedError("Database node down")

        with pytest.raises(ConnectionRefusedError):
            policy.execute(failing_operation)

    def test_idempotency_guard_lifecycle(self):
        guard = IdempotencyGuard()
        key = "idem-pay-inv-12345"

        # Step 1: First check -> None (allowed to execute)
        res = guard.check_and_set(key)
        assert res is None

        # Step 2: Concurrent second check while in-flight -> Raises IdempotencyConflictException
        with pytest.raises(IdempotencyConflictException):
            guard.check_and_set(key)

        # Step 3: Complete operation
        guard.complete(key, {"transaction_id": "tx_999", "status": "COMPLETED"})

        # Step 4: Subsequent check returns completed cached response
        cached = guard.check_and_set(key)
        assert cached is not None
        assert cached["transaction_id"] == "tx_999"

        # Step 5: Clear cache
        guard.clear(key)
        assert guard.check_and_set(key) is None

    def test_graceful_degradation_manager(self):
        deg = GracefulDegradationManager()
        feature = "predictive_ai_suggestions"
        assert deg.is_feature_degraded(feature) is False

        # Execute primary
        res = deg.execute_with_fallback(
            feature,
            primary_func=lambda: "Primary AI Output",
            fallback_func=lambda: "Cached Rule Output",
        )
        assert res == "Primary AI Output"

        # Mark degraded
        deg.mark_feature_degraded(feature)
        assert deg.is_feature_degraded(feature) is True

        # Now routes to fallback immediately
        res_fallback = deg.execute_with_fallback(
            feature,
            primary_func=lambda: "Primary AI Output",
            fallback_func=lambda: "Cached Rule Output",
        )
        assert res_fallback == "Cached Rule Output"

        # Restore
        deg.mark_feature_restored(feature)
        assert deg.is_feature_degraded(feature) is False


class TestSLOAndIncidentManagement:
    """Test SLO measurement, burn rates, incident state machine, and postmortems."""

    def test_slo_evaluation_and_budget_depletion(self):
        snapshot = SLOEngine.evaluate_slo(
            name="API Availability",
            target_percentage=Decimal("99.90"),
            total_events=10000,
            good_events=9995,  # 99.95% SLI
            slo_type=SLOType.AVAILABILITY,
        )
        assert snapshot.current_sli_percentage == Decimal("99.95")
        assert snapshot.is_compliant is True
        assert snapshot.budget_status == ErrorBudgetStatus.HEALTHY
        assert snapshot.error_budget_remaining_percentage == Decimal("50.00")

    def test_slo_exhaustion(self):
        snapshot = SLOEngine.evaluate_slo(
            name="Critical Workflow Completion",
            target_percentage=Decimal("99.95"),
            total_events=1000,
            good_events=990,  # 99.0% SLI < 99.95% target
            slo_type=SLOType.COMPLETION_RATE,
        )
        assert snapshot.current_sli_percentage == Decimal("99.00")
        assert snapshot.is_compliant is False
        assert snapshot.budget_status == ErrorBudgetStatus.BREACHED
        assert snapshot.error_budget_remaining_percentage == Decimal("0.00")

    def test_incident_state_machine_transitions(self):
        assert IncidentManager.can_transition(IncidentStatus.DETECTED, IncidentStatus.ACKNOWLEDGED) is True
        assert IncidentManager.can_transition(IncidentStatus.ACKNOWLEDGED, IncidentStatus.INVESTIGATING) is True
        assert IncidentManager.can_transition(IncidentStatus.INVESTIGATING, IncidentStatus.MITIGATING) is True
        assert IncidentManager.can_transition(IncidentStatus.MITIGATING, IncidentStatus.RESOLVED) is True
        assert IncidentManager.can_transition(IncidentStatus.RESOLVED, IncidentStatus.CLOSED) is True
        # Invalid backwards transition
        assert IncidentManager.can_transition(IncidentStatus.CLOSED, IncidentStatus.DETECTED) is False

    def test_build_postmortem_draft(self):
        pm = IncidentManager.build_postmortem_draft(
            incident_id="inc-12345",
            title="Database Read Replica Failover",
            severity=IncidentSeverity.SEV2_HIGH,
            duration_minutes=15,
            affected_services=["Database", "CRM"],
            root_cause="Network partition between AZ-1 and AZ-2.",
            prevention_actions=["Increase cross-AZ link capacity", "Tune replica keepalive timeout"],
        )
        assert pm["incident_id"] == "inc-12345"
        assert pm["severity"] == IncidentSeverity.SEV2_HIGH.value
        assert len(pm["five_whys"]) == 5
        assert len(pm["action_items"]) == 2


class TestDisasterRecoveryAndDataIntegrity:
    """Test backups, sandbox restore verification, and 14-step DR plans."""

    def test_data_integrity_check(self):
        checker = DataIntegrityChecker()
        report = checker.scan_all_domains()
        assert report["overall_integrity"] == "VALID"
        assert report["findings_count"] == 0
        assert len(report["domains_checked"]) == 6

    def test_backup_registration_and_checksum(self):
        backup = BackupManager.create_backup_record(
            tenant_id="tenant-prod-main",
            backup_type="FULL",
            scope="DATABASE",
            storage_location="s3://backups-prod/uzaii_db_2026.sql.enc",
            size_bytes=52428800,
        )
        assert backup["status"] == BackupStatus.VERIFIED.value
        assert backup["scope"] == "DATABASE"
        assert len(backup["checksum_sha256"]) == 64

    def test_isolated_sandbox_restore_verification(self):
        test_run = RestoreVerifier.execute_restore_test(
            backup_id="bk-12345",
            target_environment="ISOLATED_SANDBOX",
        )
        assert test_run["status"] == RestoreTestStatus.PASSED.value
        assert test_run["checksum_verified"] is True
        assert test_run["migrations_verified"] is True
        assert test_run["data_consistency_passed"] is True
        assert test_run["rto_achieved_minutes"] > 0

    def test_14_step_recovery_plan(self):
        plan = DisasterRecoveryPlanRegistry.get_standard_dr_plan()
        assert plan["status"] == DRPlanStatus.ACTIVE.value
        assert len(plan["recovery_priority_sequence"]) == 14
        assert plan["recovery_priority_sequence"][0]["step"] == 1
        assert "Identity" in plan["recovery_priority_sequence"][0]["service"]
        assert plan["recovery_priority_sequence"][13]["step"] == 14

    def test_disaster_recovery_drill_execution(self):
        drill = DisasterRecoveryDrillManager.execute_drill(
            scenario_name="Primary DB Region Failover",
            simulated_failure="AWS us-east-1 DB Availability Zone Outage",
            target_subsystem="Database",
        )
        assert drill["status"] == DrillStatus.COMPLETED.value
        assert drill["fallback_triggered"] is True
        assert drill["data_loss_detected"] is False
        assert len(drill["findings"]) == 3

    def test_disaster_recovery_service_integration(self):
        service = DisasterRecoveryService()
        plan = service.get_dr_plan()
        assert plan["status"] == DRPlanStatus.ACTIVE.value
        assert "Disaster Recovery Plan" in plan["name"]


class TestOperationsDeploymentsAndFeatureFlags:
    """Test deployment sanity, automated rollbacks, and tenant feature flagging."""

    def test_deployment_recording(self):
        dep = DeploymentManager.record_deployment(
            version="1.43.0",
            deployed_by="ci-cd@agencyos.local",
            git_commit_sha="b7c8d9e0",
            release_notes="Phase 43 SRE & Reliability Release",
        )
        assert dep["version"] == "1.43.0"
        assert dep["status"] == DeploymentHealthStatus.HEALTHY.value
        assert dep["smoke_tests_passed"] is True
        assert dep["migrations_applied"] is True

    def test_rollback_trigger_evaluation(self):
        # Healthy metrics -> No rollback
        eval_healthy = RollbackManager.evaluate_rollback_triggers(
            error_rate_pct=0.1,
            p99_latency_ms=250.0,
            smoke_tests_passed=True,
        )
        assert eval_healthy["should_rollback"] is False

        # Breached metrics (Error rate 4.5% > 2.0%) -> Rollback recommended
        eval_breached = RollbackManager.evaluate_rollback_triggers(
            error_rate_pct=4.5,
            p99_latency_ms=1800.0,
            smoke_tests_passed=False,
        )
        assert eval_breached["should_rollback"] is True
        assert len(eval_breached["reasons"]) == 3

        # Execute rollback
        rb = RollbackManager.execute_rollback(
            current_version="1.43.0",
            target_version="1.42.9",
            initiated_by="sre-bot@agencyos.local",
            reason="Automated trigger: Error rate breached 2.0%",
        )
        assert rb["status"] == DeploymentHealthStatus.ROLLED_BACK.value
        assert rb["to_version"] == "1.42.9"
        assert rb["success"] is True
        assert len(rb["steps"]) == 5

    def test_tenant_feature_flags_and_kill_switches(self):
        ff = FeatureFlagManager()

        # Enabled flag for ENTERPRISE
        assert ff.is_enabled("ai_predictive_forecasting", tenant_id="tenant-alpha", tenant_tier="ENTERPRISE") is True

        # Tier restriction (STARTER not in allowed_tiers)
        assert ff.is_enabled("ai_predictive_forecasting", tenant_id="tenant-starter", tenant_tier="STARTER") is False

        # Percentage canary rollout
        ff.set_flag(
            flag_name="canary_beta_feature",
            enabled=True,
            percentage_rollout=50,
            allowed_tiers=["ENTERPRISE"],
        )
        # Check consistent hashing
        res1 = ff.is_enabled("canary_beta_feature", tenant_id="tenant-123", tenant_tier="ENTERPRISE")
        res2 = ff.is_enabled("canary_beta_feature", tenant_id="tenant-123", tenant_tier="ENTERPRISE")
        assert res1 == res2

        # Whitelist override
        ff.set_flag(
            flag_name="canary_beta_feature",
            enabled=True,
            percentage_rollout=0,
            tenant_whitelist=["tenant-vip"],
        )
        assert ff.is_enabled("canary_beta_feature", tenant_id="tenant-vip") is True
        assert ff.is_enabled("canary_beta_feature", tenant_id="tenant-regular") is False

        # Global kill-switch
        ff.set_flag("canary_beta_feature", enabled=False)
        assert ff.is_enabled("canary_beta_feature", tenant_id="tenant-vip") is False

    def test_operations_service_facade(self):
        ops = OperationsService()
        dep = ops.record_deployment(version="1.43.1", deployed_by="devops@agencyos.local")
        assert dep["version"] == "1.43.1"
        assert len(ops.list_deployments()) >= 2

        # Rollback evaluation through facade
        rb_res = ops.evaluate_and_rollback(
            current_version="1.43.1",
            target_version="1.43.0",
            error_rate_pct=5.0,
            p99_latency_ms=2000.0,
            smoke_tests_passed=False,
            initiated_by="sre@agencyos.local",
        )
        assert rb_res["triggered"] is True
        assert len(ops.list_rollbacks()) == 1


class TestPermissionsAndSecurityGuards:
    """Test permission guards and deny-by-default prohibited actions."""

    def test_permission_enum_members(self):
        assert AgentPermission.READ_HEALTH == "READ_HEALTH"
        assert AgentPermission.READ_CIRCUITS == "READ_CIRCUITS"
        assert AgentPermission.READ_SLOS == "READ_SLOS"
        assert AgentPermission.READ_RELIABILITY_INCIDENTS == "READ_RELIABILITY_INCIDENTS"
        assert AgentPermission.READ_BACKUPS == "READ_BACKUPS"
        assert AgentPermission.READ_DR_PLANS == "READ_DR_PLANS"

    def test_prohibited_actions_rejection(self):
        assert "EXECUTE_DR_FAILOVER" in PROHIBITED_PERMISSIONS
        assert "DELETE_BACKUP" in PROHIBITED_PERMISSIONS
        assert "FORCE_ROLLBACK_PRODUCTION" in PROHIBITED_PERMISSIONS
        assert "ALTER_CIRCUIT_STATE_MANUALLY" in PROHIBITED_PERMISSIONS

        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"READ_HEALTH", "EXECUTE_DR_FAILOVER"})

        with pytest.raises(AgentPermissionDeniedError):
            check_tool_permission({"READ_HEALTH"}, "DELETE_BACKUP")
