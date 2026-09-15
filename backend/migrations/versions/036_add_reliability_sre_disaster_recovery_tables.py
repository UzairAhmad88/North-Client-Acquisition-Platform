"""add_reliability_sre_disaster_recovery_tables

Revision ID: 036
Revises: 035
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "036"
down_revision = "035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. system_health_snapshots
    op.create_table(
        "system_health_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="HEALTHY", index=True),
        sa.Column("active_circuit_breakers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("open_incidents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unhealthy_components", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("components_json", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 2. component_health_records
    op.create_table(
        "component_health_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("component_name", sa.String(length=100), nullable=False, index=True),
        sa.Column("component_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_critical", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("details_json", sa.JSON(), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 3. slo_definitions
    op.create_table(
        "slo_definitions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("slo_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_percentage", sa.Float(), nullable=False, server_default="99.9"),
        sa.Column("window_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("service_tier", sa.String(length=50), nullable=False, server_default="CRITICAL"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. slo_metric_snapshots
    op.create_table(
        "slo_metric_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("slo_id", sa.String(length=36), sa.ForeignKey("slo_definitions.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("slo_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("current_sli", sa.Float(), nullable=False),
        sa.Column("target_slo", sa.Float(), nullable=False),
        sa.Column("error_budget_remaining_pct", sa.Float(), nullable=False),
        sa.Column("burn_rate_1h", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("burn_rate_24h", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("budget_status", sa.String(length=50), nullable=False, server_default="HEALTHY", index=True),
        sa.Column("total_events", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("bad_events", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 5. reliability_incidents
    op.create_table(
        "reliability_incidents",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, index=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="TRIGGERED", index=True),
        sa.Column("affected_services", sa.JSON(), nullable=False),
        sa.Column("lead_responder", sa.String(length=255), nullable=True),
        sa.Column("responders", sa.JSON(), nullable=True),
        sa.Column("impact_summary", sa.Text(), nullable=False),
        sa.Column("timeline_events", sa.JSON(), nullable=True),
        sa.Column("mitigation_steps", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mitigated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. incident_postmortems
    op.create_table(
        "incident_postmortems",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("incident_id", sa.String(length=36), sa.ForeignKey("reliability_incidents.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("root_cause", sa.Text(), nullable=False),
        sa.Column("five_whys", sa.JSON(), nullable=True),
        sa.Column("timeline_events", sa.JSON(), nullable=True),
        sa.Column("what_went_well", sa.JSON(), nullable=True),
        sa.Column("what_could_improve", sa.JSON(), nullable=True),
        sa.Column("action_items", sa.JSON(), nullable=True),
        sa.Column("owner", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. system_backup_records
    op.create_table(
        "system_backup_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("backup_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED", index=True),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("storage_location", sa.String(length=512), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("retention_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 8. restore_verification_tests
    op.create_table(
        "restore_verification_tests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("backup_id", sa.String(length=36), sa.ForeignKey("system_backup_records.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="ISOLATED_SANDBOX"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED", index=True),
        sa.Column("rto_achieved_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("data_integrity_passed", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("tables_restored_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_verified_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("logs", sa.JSON(), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. disaster_recovery_plans
    op.create_table(
        "disaster_recovery_plans",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("plan_name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("scenario", sa.String(length=100), nullable=False),
        sa.Column("target_rpo_minutes", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("target_rto_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("primary_region", sa.String(length=50), nullable=False, server_default="us-east-1"),
        sa.Column("secondary_region", sa.String(length=50), nullable=False, server_default="us-west-2"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="READY"),
        sa.Column("recovery_steps", sa.JSON(), nullable=False),
        sa.Column("last_tested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. disaster_recovery_drills
    op.create_table(
        "disaster_recovery_drills",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("plan_id", sa.String(length=36), sa.ForeignKey("disaster_recovery_plans.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("scenario", sa.String(length=100), nullable=False),
        sa.Column("initiated_by", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED", index=True),
        sa.Column("actual_rto_minutes", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("data_loss_minutes", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("step_results", sa.JSON(), nullable=False),
        sa.Column("observations", sa.Text(), nullable=True),
        sa.Column("lessons_learned", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 11. deployment_records
    op.create_table(
        "deployment_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version", sa.String(length=50), nullable=False, index=True),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="PRODUCTION", index=True),
        sa.Column("deployed_by", sa.String(length=255), nullable=False),
        sa.Column("git_commit_sha", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("smoke_tests_passed", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("migrations_applied", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("release_notes", sa.Text(), nullable=True),
        sa.Column("deployed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. feature_flags
    op.create_table(
        "feature_flags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("percentage_rollout", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("allowed_tiers", sa.JSON(), nullable=True),
        sa.Column("tenant_whitelist", sa.JSON(), nullable=True),
        sa.Column("tenant_blacklist", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. circuit_breaker_states
    op.create_table(
        "circuit_breaker_states",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("service_name", sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column("state", sa.String(length=50), nullable=False, server_default="CLOSED"),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_failure_reason", sa.Text(), nullable=True),
        sa.Column("last_state_change", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. idempotency_records
    op.create_table(
        "idempotency_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("action_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PROCESSING"),
        sa.Column("response_payload", sa.JSON(), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("idempotency_records")
    op.drop_table("circuit_breaker_states")
    op.drop_table("feature_flags")
    op.drop_table("deployment_records")
    op.drop_table("disaster_recovery_drills")
    op.drop_table("disaster_recovery_plans")
    op.drop_table("restore_verification_tests")
    op.drop_table("system_backup_records")
    op.drop_table("incident_postmortems")
    op.drop_table("reliability_incidents")
    op.drop_table("slo_metric_snapshots")
    op.drop_table("slo_definitions")
    op.drop_table("component_health_records")
    op.drop_table("system_health_snapshots")
