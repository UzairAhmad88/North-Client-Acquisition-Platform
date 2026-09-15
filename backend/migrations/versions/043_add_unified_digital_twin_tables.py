"""add_unified_digital_twin_tables

Revision ID: 043
Revises: 042
Create Date: 2026-09-10
"""

import alembic.op as op
import sqlalchemy as sa

revision = "043"
down_revision = "042"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. digital_twin_models
    op.create_table(
        "digital_twin_models",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("organization_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("model_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("scope", sa.String(length=100), nullable=False, server_default="ORGANIZATION"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="ACTIVE"),
        sa.Column("default_time_horizon", sa.String(length=50), nullable=False, server_default="12_MONTHS"),
        sa.Column("simulation_methods_supported", sa.JSON(), nullable=False),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. digital_twin_model_versions
    op.create_table(
        "digital_twin_model_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("model_payload", sa.JSON(), nullable=False),
        sa.Column("change_reason", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. digital_twin_entities
    op.create_table(
        "digital_twin_entities",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entity_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("entity_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_domain", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_entity_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("state_payload", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. digital_twin_entity_versions
    op.create_table(
        "digital_twin_entity_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("entity_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("state_payload", sa.JSON(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. digital_twin_state_snapshots
    op.create_table(
        "digital_twin_state_snapshots",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("snapshot_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("snapshot_timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("commercial_state", sa.JSON(), nullable=False),
        sa.Column("delivery_state", sa.JSON(), nullable=False),
        sa.Column("operational_state", sa.JSON(), nullable=False),
        sa.Column("financial_state", sa.JSON(), nullable=False),
        sa.Column("ai_state", sa.JSON(), nullable=False),
        sa.Column("reliability_state", sa.JSON(), nullable=False),
        sa.Column("risk_state", sa.JSON(), nullable=False),
        sa.Column("composite_health_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("state_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. digital_twin_relationships
    op.create_table(
        "digital_twin_relationships",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_entity_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target_entity_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("relationship_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("properties", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. digital_twin_parameters
    op.create_table(
        "digital_twin_parameters",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("parameter_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("current_value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default="RATIO"),
        sa.Column("min_bound", sa.Float(), nullable=True),
        sa.Column("max_bound", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. digital_twin_parameter_versions
    op.create_table(
        "digital_twin_parameter_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("parameter_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_parameters.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("calibration_reason", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. digital_twin_assumptions
    op.create_table(
        "digital_twin_assumptions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("assumption_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("parameter_code", sa.String(length=100), nullable=False),
        sa.Column("baseline_value", sa.Float(), nullable=False),
        sa.Column("assumed_value", sa.Float(), nullable=False),
        sa.Column("delta_percentage", sa.Float(), nullable=False),
        sa.Column("source_basis", sa.String(length=100), nullable=False, server_default="HISTORICAL_ANALYTICS"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.8"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. digital_twin_constraints
    op.create_table(
        "digital_twin_constraints",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("constraint_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("threshold_value", sa.Float(), nullable=False),
        sa.Column("is_hard_constraint", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. digital_twin_scenarios
    op.create_table(
        "digital_twin_scenarios",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("twin_model_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("scenario_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("scenario_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("time_horizon", sa.String(length=50), nullable=False, server_default="12_MONTHS"),
        sa.Column("simulation_method", sa.String(length=50), nullable=False, server_default="MONTE_CARLO"),
        sa.Column("baseline_snapshot_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_state_snapshots.id", ondelete="SET NULL"), nullable=True),
        sa.Column("parameter_overrides", sa.JSON(), nullable=False),
        sa.Column("assumptions_payload", sa.JSON(), nullable=False),
        sa.Column("constraints_payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="CONFIGURED"),
        sa.Column("created_by", sa.String(length=100), nullable=False, server_default="system"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. digital_twin_scenario_versions
    op.create_table(
        "digital_twin_scenario_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("scenario_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("scenario_payload", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. digital_twin_simulations
    op.create_table(
        "digital_twin_simulations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("scenario_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("simulation_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("method", sa.String(length=50), nullable=False),
        sa.Column("iterations", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("runtime_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED"),
        sa.Column("metrics_summary", sa.JSON(), nullable=False),
        sa.Column("uncertainty_distribution", sa.JSON(), nullable=False),
        sa.Column("constraint_violations", sa.JSON(), nullable=False),
        sa.Column("is_sandboxed", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. digital_twin_simulation_runs
    op.create_table(
        "digital_twin_simulation_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("simulation_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_simulations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("run_index", sa.Integer(), nullable=False),
        sa.Column("simulated_revenue", sa.Float(), nullable=False),
        sa.Column("simulated_profit", sa.Float(), nullable=False),
        sa.Column("simulated_margin", sa.Float(), nullable=False),
        sa.Column("simulated_capacity_utilization", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. digital_twin_simulation_results
    op.create_table(
        "digital_twin_simulation_results",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("simulation_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_simulations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("expected_value", sa.Float(), nullable=False),
        sa.Column("p10_value", sa.Float(), nullable=False),
        sa.Column("p50_value", sa.Float(), nullable=False),
        sa.Column("p90_value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default="USD"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. digital_twin_sensitivity_results
    op.create_table(
        "digital_twin_sensitivity_results",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("scenario_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("parameter_code", sa.String(length=100), nullable=False),
        sa.Column("target_metric", sa.String(length=100), nullable=False, server_default="REVENUE"),
        sa.Column("sensitivity_score", sa.Float(), nullable=False),
        sa.Column("impact_level", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("low_impact_value", sa.Float(), nullable=False),
        sa.Column("high_impact_value", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. digital_twin_counterfactuals
    op.create_table(
        "digital_twin_counterfactuals",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("counterfactual_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("historical_event_id", sa.String(length=100), nullable=False),
        sa.Column("hypothetical_condition", sa.Text(), nullable=False),
        sa.Column("historical_actual", sa.JSON(), nullable=False),
        sa.Column("simulated_alternative", sa.JSON(), nullable=False),
        sa.Column("divergence_summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 18. digital_twin_decision_options
    op.create_table(
        "digital_twin_decision_options",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("option_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("scenario_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("expected_benefit_usd", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("expected_cost_usd", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.85"),
        sa.Column("tradeoff_summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 19. digital_twin_decision_records
    op.create_table(
        "digital_twin_decision_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("selected_option_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_decision_options.id", ondelete="SET NULL"), nullable=True),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("decision_owner", sa.String(length=100), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("scenario_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="APPROVED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 20. digital_twin_outcomes
    op.create_table(
        "digital_twin_outcomes",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_decision_records.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("scenario_id", sa.Uuid(as_uuid=True), sa.ForeignKey("digital_twin_scenarios.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("observed_period", sa.String(length=100), nullable=False),
        sa.Column("predicted_metrics", sa.JSON(), nullable=False),
        sa.Column("actual_metrics", sa.JSON(), nullable=False),
        sa.Column("variance_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 21. digital_twin_calibration_records
    op.create_table(
        "digital_twin_calibration_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("parameter_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("old_value", sa.Float(), nullable=False),
        sa.Column("calibrated_value", sa.Float(), nullable=False),
        sa.Column("calibration_basis", sa.Text(), nullable=False),
        sa.Column("calibrated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("model_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("digital_twin_calibration_records")
    op.drop_table("digital_twin_outcomes")
    op.drop_table("digital_twin_decision_records")
    op.drop_table("digital_twin_decision_options")
    op.drop_table("digital_twin_counterfactuals")
    op.drop_table("digital_twin_sensitivity_results")
    op.drop_table("digital_twin_simulation_results")
    op.drop_table("digital_twin_simulation_runs")
    op.drop_table("digital_twin_simulations")
    op.drop_table("digital_twin_scenario_versions")
    op.drop_table("digital_twin_scenarios")
    op.drop_table("digital_twin_constraints")
    op.drop_table("digital_twin_assumptions")
    op.drop_table("digital_twin_parameter_versions")
    op.drop_table("digital_twin_parameters")
    op.drop_table("digital_twin_relationships")
    op.drop_table("digital_twin_state_snapshots")
    op.drop_table("digital_twin_entity_versions")
    op.drop_table("digital_twin_entities")
    op.drop_table("digital_twin_model_versions")
    op.drop_table("digital_twin_models")
