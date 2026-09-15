"""add_platform_administration_configuration_tables

Revision ID: 038
Revises: 037
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "038"
down_revision = "037"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. configuration_definitions
    op.create_table(
        "configuration_definitions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("config_type", sa.String(length=50), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("scope", sa.String(length=50), nullable=False, server_default="GLOBAL"),
        sa.Column("default_value_json", sa.JSON(), nullable=True),
        sa.Column("current_value_json", sa.JSON(), nullable=True),
        sa.Column("validation_rules_json", sa.JSON(), nullable=True),
        sa.Column("sensitive", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mutable", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("restart_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("policy_controlled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. configuration_versions
    op.create_table(
        "configuration_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("config_key", sa.String(length=100), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("value_json", sa.JSON(), nullable=True),
        sa.Column("changed_by", sa.String(length=100), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 3. configuration_values (scoped overrides)
    op.create_table(
        "configuration_values",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("config_key", sa.String(length=100), nullable=False, index=True),
        sa.Column("scope", sa.String(length=50), nullable=False),
        sa.Column("scope_identifier", sa.String(length=100), nullable=False, index=True),
        sa.Column("value_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. configuration_change_requests
    op.create_table(
        "configuration_change_requests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("change_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("config_key", sa.String(length=100), nullable=False, index=True),
        sa.Column("old_value_json", sa.JSON(), nullable=True),
        sa.Column("new_value_json", sa.JSON(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("requested_by", sa.String(length=100), nullable=False),
        sa.Column("reviewed_by", sa.String(length=100), nullable=True),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING_APPROVAL", index=True),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 5. platform_policies
    op.create_table(
        "platform_policies",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("policy_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=50), nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("scope", sa.String(length=50), nullable=False, server_default="GLOBAL"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE", index=True),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_by", sa.String(length=100), nullable=False, server_default="system"),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. platform_policy_versions
    op.create_table(
        "platform_policy_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("policy_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("policy_json", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. platform_policy_rules
    op.create_table(
        "platform_policy_rules",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("rule_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("policy_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("condition", sa.Text(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("is_mandatory_security", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    # 8. admin_feature_flags
    op.create_table(
        "admin_feature_flags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DISABLED", index=True),
        sa.Column("rollout_type", sa.String(length=50), nullable=False, server_default="BOOLEAN"),
        sa.Column("rollout_percentage", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("allowed_tiers_json", sa.JSON(), nullable=True),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="PRODUCTION"),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="admin"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. admin_feature_flag_rules
    op.create_table(
        "admin_feature_flag_rules",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("flag_key", sa.String(length=100), nullable=False, index=True),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_value", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    # 10. environment_records
    op.create_table(
        "environment_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("env_id", sa.String(length=50), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("env_type", sa.String(length=50), nullable=False),
        sa.Column("is_production", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("allow_mock_providers", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("allow_chaos_testing", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("allow_real_financial_execution", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("active_version", sa.String(length=50), nullable=False, server_default="v1.0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. integration_registry
    op.create_table(
        "integration_registry",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("provider_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("base_url", sa.String(length=255), nullable=False),
        sa.Column("secret_reference", sa.String(length=255), nullable=False),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("max_retries", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("rate_limit_rpm", sa.Integer(), nullable=False, server_default="600"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("health_status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("error_rate_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("last_health_check", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. secret_references
    op.create_table(
        "secret_references",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("secret_uri", sa.String(length=255), unique=True, nullable=False, index=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("provider_name", sa.String(length=100), nullable=False),
        sa.Column("last_rotated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("rotation_period_days", sa.Integer(), nullable=False, server_default="90"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
    )

    # 13. maintenance_windows
    op.create_table(
        "maintenance_windows",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("window_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("mode", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("false"), index=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("internal_banner", sa.Text(), nullable=True),
        sa.Column("client_portal_banner", sa.Text(), nullable=True),
        sa.Column("initiated_by", sa.String(length=100), nullable=False),
        sa.Column("affected_services_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. system_control_states
    op.create_table(
        "system_control_states",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("switch_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("target_identifier", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=50), nullable=False, server_default="DISARMED", index=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("activated_by", sa.String(length=100), nullable=True),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 15. administrative_audit_events
    op.create_table(
        "administrative_audit_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("actor", sa.String(length=100), nullable=False, index=True),
        sa.Column("actor_type", sa.String(length=50), nullable=False, server_default="USER"),
        sa.Column("action", sa.String(length=100), nullable=False, index=True),
        sa.Column("resource_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("resource_id", sa.String(length=100), nullable=False),
        sa.Column("old_value_json", sa.JSON(), nullable=True),
        sa.Column("new_value_json", sa.JSON(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("authorization_status", sa.String(length=50), nullable=False, server_default="AUTHORIZED"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 16. configuration_drift_records
    op.create_table(
        "configuration_drift_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("drift_id", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("config_key", sa.String(length=100), nullable=False, index=True),
        sa.Column("expected_value_json", sa.JSON(), nullable=True),
        sa.Column("actual_value_json", sa.JSON(), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="WARNING"),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="PRODUCTION"),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.text("false"), index=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )


def downgrade() -> None:
    op.drop_table("configuration_drift_records")
    op.drop_table("administrative_audit_events")
    op.drop_table("system_control_states")
    op.drop_table("maintenance_windows")
    op.drop_table("secret_references")
    op.drop_table("integration_registry")
    op.drop_table("environment_records")
    op.drop_table("admin_feature_flag_rules")
    op.drop_table("admin_feature_flags")
    op.drop_table("platform_policy_rules")
    op.drop_table("platform_policy_versions")
    op.drop_table("platform_policies")
    op.drop_table("configuration_change_requests")
    op.drop_table("configuration_values")
    op.drop_table("configuration_versions")
    op.drop_table("configuration_definitions")
