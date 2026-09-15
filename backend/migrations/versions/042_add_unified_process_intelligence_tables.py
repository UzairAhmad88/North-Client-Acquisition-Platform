"""add_unified_process_intelligence_tables

Revision ID: 042
Revises: 041
Create Date: 2026-09-10
"""

import alembic.op as op
import sqlalchemy as sa

revision = "042"
down_revision = "041"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. process_definitions
    op.create_table(
        "process_definitions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("organization_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("process_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("domain", sa.String(length=100), nullable=False, index=True),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="ACTIVE"),
        sa.Column("scope", sa.String(length=100), nullable=False, server_default="ORGANIZATION"),
        sa.Column("trigger_type", sa.String(length=100), nullable=False, server_default="EVENT"),
        sa.Column("expected_outcome", sa.Text(), nullable=True),
        sa.Column("workflow_definition_id", sa.String(length=100), nullable=True),
        sa.Column("policy_requirements", sa.JSON(), nullable=False),
        sa.Column("governance_controls", sa.JSON(), nullable=False),
        sa.Column("kpis", sa.JSON(), nullable=False),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. process_definition_versions
    op.create_table(
        "process_definition_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("definition_payload", sa.JSON(), nullable=False),
        sa.Column("change_reason", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. process_cases
    op.create_table(
        "process_cases",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("case_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entity_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("entity_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cycle_time_seconds", sa.Float(), nullable=True),
        sa.Column("waiting_time_seconds", sa.Float(), nullable=True),
        sa.Column("processing_time_seconds", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="ACTIVE"),
        sa.Column("outcome", sa.String(length=100), nullable=True),
        sa.Column("owner_id", sa.String(length=100), nullable=True),
        sa.Column("variant_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("attributes", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. process_case_attributes
    op.create_table(
        "process_case_attributes",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("case_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_cases.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("attribute_name", sa.String(length=100), nullable=False),
        sa.Column("attribute_value", sa.Text(), nullable=False),
        sa.Column("data_type", sa.String(length=50), nullable=False, server_default="STRING"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. process_event_logs
    op.create_table(
        "process_event_logs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("event_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("case_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("activity", sa.String(length=255), nullable=False, index=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("actor", sa.String(length=100), nullable=False, server_default="system"),
        sa.Column("actor_type", sa.String(length=50), nullable=False, server_default="SYSTEM"),
        sa.Column("resource", sa.String(length=100), nullable=True),
        sa.Column("entity_type", sa.String(length=100), nullable=True),
        sa.Column("entity_id", sa.String(length=255), nullable=True),
        sa.Column("workflow_id", sa.String(length=100), nullable=True),
        sa.Column("task_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED"),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("attributes", sa.JSON(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False, server_default="SYSTEM_TELEMETRY"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. process_variants
    op.create_table(
        "process_variants",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("variant_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("event_sequence", sa.JSON(), nullable=False),
        sa.Column("sequence_hash", sa.String(length=64), nullable=False, index=True),
        sa.Column("frequency", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("average_cycle_time_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("conversion_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("failure_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("rework_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_conforming", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. process_variant_events
    op.create_table(
        "process_variant_events",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("variant_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_variants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("activity_name", sa.String(length=255), nullable=False),
        sa.Column("average_duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. process_maps
    op.create_table(
        "process_maps",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("map_type", sa.String(length=50), nullable=False, server_default="OBSERVED"),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("nodes_payload", sa.JSON(), nullable=False),
        sa.Column("edges_payload", sa.JSON(), nullable=False),
        sa.Column("metrics_summary", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. process_transitions
    op.create_table(
        "process_transitions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_activity", sa.String(length=255), nullable=False, index=True),
        sa.Column("target_activity", sa.String(length=255), nullable=False, index=True),
        sa.Column("transition_frequency", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("average_latency_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("median_latency_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. process_conformance_rules
    op.create_table(
        "process_conformance_rules",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("rule_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("rule_type", sa.String(length=50), nullable=False),
        sa.Column("source_activity", sa.String(length=255), nullable=True),
        sa.Column("target_activity", sa.String(length=255), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. process_conformance_violations
    op.create_table(
        "process_conformance_violations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("case_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("rule_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_conformance_rules.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("violation_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("violation_type", sa.String(length=50), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("activity_involved", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DETECTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. process_bottlenecks
    op.create_table(
        "process_bottlenecks",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("bottleneck_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("activity_name", sa.String(length=255), nullable=False, index=True),
        sa.Column("bottleneck_type", sa.String(length=50), nullable=False, server_default="WAIT_TIME"),
        sa.Column("average_wait_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("average_processing_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("queue_depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("frequency", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("affected_cases_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("root_cause_summary", sa.Text(), nullable=False),
        sa.Column("business_impact", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("recommendation", sa.Text(), nullable=True),
        sa.Column("evidence_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. process_rework_records
    op.create_table(
        "process_rework_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("case_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("activity_name", sa.String(length=255), nullable=False),
        sa.Column("repetition_count", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("wasted_duration_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("probable_driver", sa.String(length=100), nullable=False, server_default="SCOPE_INSTABILITY"),
        sa.Column("evidence_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. process_handoff_records
    op.create_table(
        "process_handoff_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_role", sa.String(length=100), nullable=False),
        sa.Column("target_role", sa.String(length=100), nullable=False),
        sa.Column("handoff_type", sa.String(length=100), nullable=False, server_default="DEPARTMENTAL"),
        sa.Column("average_delay_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("handoff_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("friction_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("common_issues", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. process_resource_metrics
    op.create_table(
        "process_resource_metrics",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("resource_type", sa.String(length=50), nullable=False, server_default="ROLE"),
        sa.Column("resource_identifier", sa.String(length=100), nullable=False, index=True),
        sa.Column("active_cases_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("utilization_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("average_handling_time_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("blocked_time_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("snapshot_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. process_automation_candidates
    op.create_table(
        "process_automation_candidates",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("candidate_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("task_name", sa.String(length=255), nullable=False),
        sa.Column("frequency_per_month", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("average_duration_minutes", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("error_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("reversibility", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("suitability_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="REVIEW_REQUIRED"),
        sa.Column("expected_savings_hours_month", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="IDENTIFIED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. process_optimization_proposals
    op.create_table(
        "process_optimization_proposals",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("proposal_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("proposed_version", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("problem_statement", sa.Text(), nullable=False),
        sa.Column("evidence_summary", sa.Text(), nullable=False),
        sa.Column("proposed_changes", sa.JSON(), nullable=False),
        sa.Column("tradeoff_scorecard", sa.JSON(), nullable=False),
        sa.Column("expected_benefits", sa.JSON(), nullable=False),
        sa.Column("expected_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("rollback_plan", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False, server_default="system"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 18. process_simulation_runs
    op.create_table(
        "process_simulation_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("simulation_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("proposal_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_optimization_proposals.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("scenario_type", sa.String(length=50), nullable=False, server_default="OPTIMIZED"),
        sa.Column("iterations", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column("assumptions_payload", sa.JSON(), nullable=False),
        sa.Column("predicted_throughput", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("predicted_cycle_time_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("predicted_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("predicted_failure_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("predicted_rework_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("results_summary", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 19. process_simulation_assumptions
    op.create_table(
        "process_simulation_assumptions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("simulation_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_simulation_runs.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("assumption_key", sa.String(length=100), nullable=False),
        sa.Column("assumption_value", sa.String(length=255), nullable=False),
        sa.Column("source_basis", sa.String(length=100), nullable=False, server_default="HISTORICAL_LOG"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 20. process_experiments
    op.create_table(
        "process_experiments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("experiment_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("variant_a_definition", sa.JSON(), nullable=False),
        sa.Column("variant_b_definition", sa.JSON(), nullable=False),
        sa.Column("allocation_percentage_b", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PLANNED"),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("results_summary", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 21. process_deployments
    op.create_table(
        "process_deployments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("deployment_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("proposal_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_optimization_proposals.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("strategy", sa.String(length=50), nullable=False, server_default="CANARY"),
        sa.Column("rollout_percentage", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("target_version", sa.Integer(), nullable=False),
        sa.Column("approved_by", sa.String(length=100), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("health_status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("canary_metrics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 22. process_health_snapshots
    op.create_table(
        "process_health_snapshots",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("health_status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("cycle_time_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("conformance_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("failure_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("rework_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("slo_compliance_rate", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("factors_summary", sa.JSON(), nullable=False),
        sa.Column("snapshot_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 23. process_risk_assessments
    op.create_table(
        "process_risk_assessments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("process_id", sa.Uuid(as_uuid=True), sa.ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("security_risk", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("compliance_risk", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("operational_risk", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("financial_risk", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("customer_risk", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("composite_risk_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_tier", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("findings", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("process_risk_assessments")
    op.drop_table("process_health_snapshots")
    op.drop_table("process_deployments")
    op.drop_table("process_experiments")
    op.drop_table("process_simulation_assumptions")
    op.drop_table("process_simulation_runs")
    op.drop_table("process_optimization_proposals")
    op.drop_table("process_automation_candidates")
    op.drop_table("process_resource_metrics")
    op.drop_table("process_handoff_records")
    op.drop_table("process_rework_records")
    op.drop_table("process_bottlenecks")
    op.drop_table("process_conformance_violations")
    op.drop_table("process_conformance_rules")
    op.drop_table("process_transitions")
    op.drop_table("process_maps")
    op.drop_table("process_variant_events")
    op.drop_table("process_variants")
    op.drop_table("process_event_logs")
    op.drop_table("process_case_attributes")
    op.drop_table("process_cases")
    op.drop_table("process_definition_versions")
    op.drop_table("process_definitions")
