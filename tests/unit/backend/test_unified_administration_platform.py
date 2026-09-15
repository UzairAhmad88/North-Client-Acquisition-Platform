"""Unit tests for Phase 44 — Platform Administration, System Controls, Dynamic Policies & Global Operations."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import pytest

from app.administration.base import (
    AdminHealthReport,
    AdminHealthStatus,
    ApprovalStatus,
    ChangeRiskLevel,
    ChangeStatus,
    ConfigItem,
    ConfigScope,
    ConfigStatus,
    ConfigType,
    DriftItem,
    DriftSeverity,
    EnvironmentType,
    FeatureFlagItem,
    FlagStatus,
    KillSwitchItem,
    KillSwitchLevel,
    KillSwitchState,
    MaintenanceMode,
    PolicyDomain,
    PolicyEvaluationResult,
    PolicyItem,
    PolicyRule,
    PolicyScope,
    PolicyStatus,
    RolloutType,
)
from app.administration.configuration import (
    ConfigurationManager,
    ConfigurationValidationError,
    ImmutableConfigError,
)
from app.administration.drift import ConfigurationDriftDetector
from app.administration.environments import (
    EnvironmentDefinition,
    EnvironmentManager,
    EnvironmentPromotionRequest,
)
from app.administration.feature_flags import AdminFeatureFlagManager
from app.administration.health import AdminHealthEngine
from app.administration.integrations import IntegrationManager, ProviderConfiguration
from app.administration.maintenance import MaintenanceManager, MaintenanceWindow
from app.administration.policies import PolicyConflictError, PolicyEngine
from app.administration.service import PlatformAdministrationService
from app.administration.system_controls import SystemControlManager

from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
    check_tool_permission,
)
from agents.core.errors import AgentPermissionDeniedError


class TestConfigurationManager:
    """Tests for dynamic configuration registry, type validation, immutability, and change workflow."""

    def test_default_configs_loaded(self):
        mgr = ConfigurationManager()
        configs = mgr.list_configs()
        assert len(configs) >= 7
        keys = {c.key for c in configs}
        assert "AI_MAX_DAILY_COST" in keys
        assert "SESSION_INACTIVITY_TIMEOUT_MINUTES" in keys

    def test_register_and_get_config(self):
        mgr = ConfigurationManager()
        cfg = mgr.register_config(
            ConfigItem(
                key="STORAGE_MAX_UPLOAD_SIZE_MB",
                display_name="Max Upload Size (MB)",
                description="Maximum payload upload size in megabytes",
                config_type=ConfigType.INTEGER,
                category="Storage",
                default_value=50,
                current_value=50,
                validation_rules={"min": 1, "max": 500},
            )
        )
        assert cfg.key == "STORAGE_MAX_UPLOAD_SIZE_MB"
        assert cfg.current_value == 50
        assert mgr.get_config("STORAGE_MAX_UPLOAD_SIZE_MB").current_value == 50

    def test_type_and_rule_validation(self):
        mgr = ConfigurationManager()
        mgr.register_config(
            ConfigItem(
                key="SECURITY_RATE_LIMIT",
                display_name="Rate Limit",
                description="Per-minute rate limit",
                config_type=ConfigType.INTEGER,
                category="Security",
                default_value=60,
                current_value=60,
                validation_rules={"min": 10, "max": 1000},
            )
        )
        # Invalid type
        with pytest.raises(ConfigurationValidationError):
            mgr.create_change_request(
                key="SECURITY_RATE_LIMIT",
                new_value="not-an-integer",
                reason="Invalid update",
                requested_by="admin",
            )
        # Out of bounds
        with pytest.raises(ConfigurationValidationError):
            mgr.create_change_request(
                key="SECURITY_RATE_LIMIT",
                new_value=5000,
                reason="Too high",
                requested_by="admin",
            )

    def test_immutability_guard(self):
        mgr = ConfigurationManager()
        mgr.register_config(
            ConfigItem(
                key="SECURITY_ROOT_CA_FINGERPRINT",
                display_name="Root CA",
                description="Immutable root fingerprint",
                config_type=ConfigType.STRING,
                category="Security",
                default_value="sha256:abcd1234",
                current_value="sha256:abcd1234",
                mutable=False,
            )
        )
        with pytest.raises(ImmutableConfigError):
            mgr.create_change_request(
                key="SECURITY_ROOT_CA_FINGERPRINT",
                new_value="sha256:newprint",
                reason="Attempt change",
                requested_by="admin",
            )

    def test_change_request_approval_and_version_history(self):
        mgr = ConfigurationManager()
        cr = mgr.create_change_request(
            key="AI_MAX_DAILY_COST",
            new_value=150.0,
            reason="Upgrade tier limit",
            requested_by="engineer_alice",
        )
        assert cr.status == ChangeStatus.PENDING_APPROVAL
        assert mgr.get_config("AI_MAX_DAILY_COST").current_value == 50.0  # Value not updated yet

        # Approve change
        approved_cfg = mgr.approve_and_apply_change(cr.change_id, approved_by="admin_bob")
        assert approved_cfg.current_value == 150.0
        assert approved_cfg.version == 2
        history = mgr._history["AI_MAX_DAILY_COST"]
        assert len(history) == 2
        assert history[0].current_value == 50.0
        assert history[1].current_value == 150.0

    def test_config_diff(self):
        mgr = ConfigurationManager()
        cr = mgr.create_change_request(
            key="AI_TIMEOUT_SECONDS",
            new_value=60,
            reason="Increase timeout",
            requested_by="sre_lead",
        )
        mgr.approve_and_apply_change(cr.change_id, approved_by="admin")
        diff = mgr.compute_diff("AI_TIMEOUT_SECONDS", v_from=1, v_to=2)
        assert diff["key"] == "AI_TIMEOUT_SECONDS"
        assert diff["version_from"] == 1
        assert diff["version_to"] == 2
        assert diff["old_value"] == 30
        assert diff["new_value"] == 60
        assert diff["has_drift"] is True

    def test_scoped_override_resolution(self):
        mgr = ConfigurationManager()
        mgr.set_scoped_override(
            scope=ConfigScope.ORGANIZATION,
            scope_identifier="org_enterprise_1",
            key="AI_MAX_DAILY_COST",
            value=500.0,
        )
        # Global resolution
        assert mgr.resolve_value("AI_MAX_DAILY_COST") == 50.0
        # Scoped organization resolution
        assert mgr.resolve_value("AI_MAX_DAILY_COST", organization="org_enterprise_1") == 500.0


class TestPolicyEngine:
    """Tests for dynamic enterprise policy engine, rule priority, and evaluation."""

    def test_default_policies_exist(self):
        engine = PolicyEngine()
        policies = engine.list_policies()
        assert len(policies) >= 4
        domains = {p.domain for p in policies}
        assert PolicyDomain.SECURITY in domains
        assert PolicyDomain.AI in domains
        assert PolicyDomain.FINANCE in domains

    def test_security_policy_cross_tenant_block(self):
        engine = PolicyEngine()
        decision, reason = engine.evaluate_action(
            domain=PolicyDomain.SECURITY,
            action="read_lead_record",
            actor_type="user",
            context={"cross_tenant_access": True},
        )
        assert decision == PolicyEvaluationResult.BLOCK
        assert "Cross-tenant access is strictly prohibited" in reason

    def test_ai_policy_irreversible_action_block(self):
        engine = PolicyEngine()
        decision, reason = engine.evaluate_action(
            domain=PolicyDomain.AI,
            action="payment.execute",
            actor_type="ai_agent",
            context={"autonomous": True},
        )
        assert decision == PolicyEvaluationResult.BLOCK
        assert "AI agents are strictly forbidden" in reason

    def test_finance_dual_approval_policy(self):
        engine = PolicyEngine()
        # Large refund without dual approval -> REVIEW
        decision, reason = engine.evaluate_action(
            domain=PolicyDomain.FINANCE,
            action="refund.issue",
            amount=5000.0,
            context={"dual_approved": False},
        )
        assert decision == PolicyEvaluationResult.REVIEW
        assert "Refunds exceeding $1,000 require dual managerial sign-off" in reason

        # Small refund -> ALLOW
        decision_small, _ = engine.evaluate_action(
            domain=PolicyDomain.FINANCE,
            action="refund.issue",
            amount=200.0,
            context={"dual_approved": False},
        )
        assert decision_small == PolicyEvaluationResult.ALLOW

    def test_prevent_weakening_mandatory_security(self):
        engine = PolicyEngine()
        weak_policy = PolicyItem(
            policy_id="POL-WEAK-SEC",
            name="Weak Tenant Access",
            domain=PolicyDomain.SECURITY,
            description="Attempting to bypass tenant check",
            scope=PolicyScope.ORGANIZATION,
            rules=[
                PolicyRule(
                    rule_id="RULE-WEAK",
                    name="Allow Cross Tenant",
                    condition="context.cross_tenant_access == True",
                    action=PolicyEvaluationResult.ALLOW,
                    reason="Permit bypass",
                    is_mandatory_security=True,
                )
            ],
        )
        with pytest.raises(PolicyConflictError):
            engine.register_policy(weak_policy)


class TestSystemControlManager:
    """Tests for global and granular emergency kill switches."""

    def test_default_kill_switches(self):
        mgr = SystemControlManager()
        switches = mgr.list_switches()
        assert len(switches) >= 7
        switch_ids = {s.switch_id for s in switches}
        assert "GLOBAL_AI_OFF" in switch_ids
        assert "GLOBAL_COMMUNICATION_OFF" in switch_ids
        assert "GLOBAL_PAYMENTS_OFF" in switch_ids

    def test_engage_and_release_kill_switch(self):
        mgr = SystemControlManager()
        assert not mgr.is_kill_switch_active("GLOBAL_AI_OFF")

        # Activate switch
        activated = mgr.activate_kill_switch(
            switch_id="GLOBAL_AI_OFF",
            activated_by="lead_sre",
            reason="Anomaly in LLM response pipeline",
        )
        assert activated.state == KillSwitchState.ACTIVE
        assert mgr.is_kill_switch_active("GLOBAL_AI_OFF")

        # Release switch
        released = mgr.release_kill_switch("GLOBAL_AI_OFF", released_by="lead_sre")
        assert released.state == KillSwitchState.DISARMED
        assert not mgr.is_kill_switch_active("GLOBAL_AI_OFF")


class TestAdminFeatureFlagManager:
    """Tests for feature flags, canary percentages, and tenant tier gating."""

    def test_default_flags(self):
        mgr = AdminFeatureFlagManager()
        flags = mgr.list_flags()
        assert len(flags) >= 4
        keys = {f.key for f in flags}
        assert "AI_EXECUTIVE_COPILOT" in keys
        assert "ADVANCED_VECTOR_SEARCH" in keys

    def test_boolean_flag_evaluation(self):
        mgr = AdminFeatureFlagManager()
        # Initially disabled
        assert mgr.is_enabled("REAL_TIME_STRIPE_PAYMENTS") is False

        # Enable flag
        mgr.set_flag_status("REAL_TIME_STRIPE_PAYMENTS", FlagStatus.ENABLED)
        assert mgr.is_enabled("REAL_TIME_STRIPE_PAYMENTS") is True

    def test_percentage_canary_evaluation(self):
        mgr = AdminFeatureFlagManager()
        # ADVANCED_VECTOR_SEARCH has 25% canary
        user_1_res = mgr.is_enabled("ADVANCED_VECTOR_SEARCH", user_id="user_abc_123")
        user_1_repeat = mgr.is_enabled("ADVANCED_VECTOR_SEARCH", user_id="user_abc_123")
        assert user_1_res == user_1_repeat

    def test_tenant_tier_evaluation(self):
        mgr = AdminFeatureFlagManager()
        # AI_EXECUTIVE_COPILOT allowed for ENTERPRISE, PRO
        assert mgr.is_enabled("AI_EXECUTIVE_COPILOT", tenant_tier="ENTERPRISE") is True
        assert mgr.is_enabled("AI_EXECUTIVE_COPILOT", tenant_tier="PRO") is True
        assert mgr.is_enabled("AI_EXECUTIVE_COPILOT", tenant_tier="FREE") is False


class TestEnvironmentManager:
    """Tests for multi-environment isolation, safeguards, and config promotion."""

    def test_environment_definitions(self):
        mgr = EnvironmentManager()
        envs = mgr.list_environments()
        assert len(envs) >= 3
        types = {e.env_type for e in envs}
        assert EnvironmentType.PRODUCTION in types
        assert EnvironmentType.STAGING in types
        assert EnvironmentType.DEVELOPMENT in types

    def test_production_safeguards(self):
        mgr = EnvironmentManager()
        prod = mgr.get_environment(EnvironmentType.PRODUCTION)
        assert prod.is_production is True
        assert prod.requires_approval_for_changes is True
        assert prod.allow_mock_providers is False
        assert prod.allow_chaos_testing is False
        assert prod.allow_real_financial_execution is True

    def test_environment_config_promotion(self):
        mgr = EnvironmentManager()
        req = mgr.create_promotion_request(
            source_env=EnvironmentType.STAGING,
            target_env=EnvironmentType.PRODUCTION,
            keys=["AI_MAX_DAILY_COST", "SESSION_INACTIVITY_TIMEOUT_MINUTES"],
            requested_by="devops_sam",
        )
        assert req.status == "PENDING_APPROVAL"
        assert len(req.configuration_keys) == 2

        # Approve promotion
        approved = mgr.approve_promotion(req.promotion_id, approved_by="admin_lead")
        assert approved.status == "APPLIED"
        assert approved.approved_by == "admin_lead"


class TestIntegrationManager:
    """Tests for third-party provider registry, secret masking, and health telemetry."""

    def test_default_providers(self):
        mgr = IntegrationManager()
        providers = mgr.list_providers()
        assert len(providers) >= 5
        provider_ids = {p.provider_id for p in providers}
        assert "PROV-OPENAI" in provider_ids
        assert "PROV-ANTHROPIC" in provider_ids
        assert "PROV-SENDGRID" in provider_ids

    def test_secret_reference_never_exposes_raw_tokens(self):
        mgr = IntegrationManager()
        prov = mgr.get_provider("PROV-OPENAI")
        assert prov.secret_reference == "secret://production/ai/openai-api-key"
        assert not prov.secret_reference.startswith("sk-")

    def test_update_health_telemetry(self):
        mgr = IntegrationManager()
        mgr.record_health_probe(
            provider_id="PROV-OPENAI",
            is_healthy=True,
            latency_ms=145.0,
            error_rate=0.01,
        )
        prov = mgr.get_provider("PROV-OPENAI")
        assert prov.latency_ms == 145.0
        assert prov.error_rate_percentage == 0.01
        assert prov.health_status == "HEALTHY"


class TestMaintenanceManager:
    """Tests for platform maintenance states and read-only mode enforcement."""

    def test_default_normal_mode(self):
        mgr = MaintenanceManager()
        assert mgr.get_current_mode() == MaintenanceMode.NORMAL
        assert mgr.is_mutation_allowed() is True

    def test_start_and_end_maintenance_window(self):
        mgr = MaintenanceManager()
        win = mgr.start_maintenance(
            mode=MaintenanceMode.MAINTENANCE,
            title="Database Schema Upgrade",
            description="Upgrading tables to Phase 44",
            internal_banner="System in maintenance mode. Mutations disabled.",
            client_banner="Maintenance in progress.",
            affected_services=["database", "api"],
            initiated_by="dba_admin",
        )
        assert win.is_active is True
        assert mgr.get_current_mode() == MaintenanceMode.MAINTENANCE
        assert mgr.is_mutation_allowed() is False

        # End maintenance
        res = mgr.end_maintenance(ended_by="dba_admin")
        assert res == MaintenanceMode.NORMAL
        assert mgr.get_current_mode() == MaintenanceMode.NORMAL
        assert mgr.is_mutation_allowed() is True


class TestConfigurationDriftDetector:
    """Tests for runtime vs declared configuration drift detection and reconciliation."""

    def test_drift_detection(self):
        cfg_mgr = ConfigurationManager()
        detector = ConfigurationDriftDetector(cfg_mgr)
        runtime_snapshot = {
            "AI_MAX_DAILY_COST": 100.0,  # Declared is 50.0
            "SESSION_INACTIVITY_TIMEOUT_MINUTES": 60,  # Matches declared
        }
        drifts = detector.scan_for_drift(runtime_snapshot, env=EnvironmentType.PRODUCTION)
        assert len(drifts) == 1
        assert drifts[0].key == "AI_MAX_DAILY_COST"
        assert drifts[0].expected_value == 50.0
        assert drifts[0].actual_value == 100.0
        assert drifts[0].resolved is False

    def test_drift_reconciliation(self):
        cfg_mgr = ConfigurationManager()
        detector = ConfigurationDriftDetector(cfg_mgr)
        drifts = detector.scan_for_drift(
            {"AI_MAX_DAILY_COST": 100.0},
            env=EnvironmentType.PRODUCTION,
        )
        drift_id = drifts[0].drift_id
        resolved = detector.resolve_drift(drift_id, resolved_by="admin_sre")
        assert resolved.resolved is True
        assert len(detector.list_unresolved_drifts()) == 0


class TestPlatformAdministrationService:
    """Tests for unified Administration orchestration service and composite health."""

    def test_service_initialization_and_health_report(self):
        svc = PlatformAdministrationService()
        health = svc.health_engine.compute_health_report()
        assert health.status in [AdminHealthStatus.HEALTHY, AdminHealthStatus.STABLE]
        assert health.configuration_validity_score >= 90
        assert health.policy_consistency_score >= 90
        assert health.integration_health_score >= 90
        assert health.drift_count == 0

    def test_full_admin_overview(self):
        svc = PlatformAdministrationService()
        overview = svc.get_overview()
        assert "health" in overview
        assert overview["configs_count"] >= 7
        assert overview["policies_count"] >= 4
        assert overview["feature_flags_count"] >= 4
        assert overview["providers_count"] >= 5
        assert overview["environments_count"] >= 3
        assert overview["kill_switches_count"] >= 7


class TestPhase44PermissionsAndProhibitions:
    """Tests ensuring agents cannot execute prohibited administrative operations autonomously."""

    def test_prohibited_permissions_include_phase_44(self):
        assert "APPLY_CONFIG_CHANGE_AUTONOMOUSLY" in PROHIBITED_PERMISSIONS
        assert "ALTER_MANDATORY_SECURITY_POLICY" in PROHIBITED_PERMISSIONS
        assert "ENGAGE_EMERGENCY_KILL_SWITCH_AUTONOMOUSLY" in PROHIBITED_PERMISSIONS
        assert "OVERWRITE_ENVIRONMENT_PROMOTION_CHECKS" in PROHIBITED_PERMISSIONS
        assert "UNAUTHORIZED_MAINTENANCE_TRIGGER" in PROHIBITED_PERMISSIONS

    def test_agent_cannot_be_assigned_phase_44_prohibited_permission(self):
        invalid_perms = {"READ_BUSINESS", "APPLY_CONFIG_CHANGE_AUTONOMOUSLY"}
        with pytest.raises(AgentPermissionDeniedError) as exc_info:
            validate_agent_permissions(invalid_perms)
        assert "prohibited" in str(exc_info.value).lower()

    def test_tool_permission_enforcement(self):
        agent_perms = {"READ_BUSINESS", "READ_SERVICES"}
        # Required permission granted
        check_tool_permission(agent_perms, "READ_BUSINESS")

        # Missing permission rejected
        with pytest.raises(AgentPermissionDeniedError):
            check_tool_permission(agent_perms, "CREATE_DRAFT")
