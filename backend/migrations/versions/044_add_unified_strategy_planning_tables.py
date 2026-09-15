"""add_unified_strategy_planning_tables

Revision ID: 044
Revises: 043
Create Date: 2026-09-10
"""

import alembic.op as op
import sqlalchemy as sa

revision = "044"
down_revision = "043"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. strategic_pillars
    op.create_table(
        "strategic_pillars",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("pillar_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. strategic_plans
    op.create_table(
        "strategic_plans",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("organization_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("plan_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("vision_statement", sa.Text(), nullable=False),
        sa.Column("mission_statement", sa.Text(), nullable=True),
        sa.Column("planning_horizon", sa.String(length=50), nullable=False, server_default="MEDIUM_TERM"),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="DRAFT"),
        sa.Column("total_budget_usd", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. strategic_plan_versions
    op.create_table(
        "strategic_plan_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("plan_snapshot", sa.JSON(), nullable=False),
        sa.Column("change_reason", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. strategic_objectives
    op.create_table(
        "strategic_objectives",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("pillar_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_pillars.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("objective_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("strategic_pillar", sa.String(length=100), nullable=False, server_default="GROWTH"),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="executive_team"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("baseline_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("target_value", sa.Float(), nullable=False),
        sa.Column("current_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="ACTIVE"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("progress_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("evidence_summary", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. key_results
    op.create_table(
        "key_results",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("objective_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("kr_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("baseline_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("target_value", sa.Float(), nullable=False),
        sa.Column("current_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default="PERCENT"),
        sa.Column("progress_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("measurement_method", sa.String(length=100), nullable=False, server_default="AUTOMATED_TELEMETRY"),
        sa.Column("source_metric", sa.String(length=100), nullable=True),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. strategic_initiatives
    op.create_table(
        "strategic_initiatives",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("primary_objective_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_objectives.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("initiative_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False, server_default="GROWTH"),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="IDEA"),
        sa.Column("expected_value_usd", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("estimated_cost_usd", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("required_fte_capacity", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("estimated_duration_weeks", sa.Float(), nullable=False, server_default="4.0"),
        sa.Column("priority_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("feasibility_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("is_funded", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. initiative_dependencies
    op.create_table(
        "initiative_dependencies",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_initiative_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target_initiative_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("dependency_type", sa.String(length=50), nullable=False, server_default="FINISH_TO_START"),
        sa.Column("is_critical_path", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("lag_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. strategic_constraints
    op.create_table(
        "strategic_constraints",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("constraint_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, server_default="BUDGET"),
        sa.Column("metric", sa.String(length=100), nullable=False),
        sa.Column("operator", sa.String(length=20), nullable=False, server_default="LTE"),
        sa.Column("threshold_value", sa.Float(), nullable=False),
        sa.Column("is_hard_constraint", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. strategic_assumptions
    op.create_table(
        "strategic_assumptions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("assumption_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("parameter_name", sa.String(length=100), nullable=False),
        sa.Column("baseline_value", sa.Float(), nullable=False),
        sa.Column("assumed_value", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.8"),
        sa.Column("source_basis", sa.String(length=100), nullable=False, server_default="HISTORICAL_ANALYTICS"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. optimization_runs
    op.create_table(
        "optimization_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("run_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("optimization_type", sa.String(length=100), nullable=False, server_default="MULTI_OBJECTIVE_LINEAR"),
        sa.Column("objective_weights", sa.JSON(), nullable=False),
        sa.Column("solver_name", sa.String(length=100), nullable=False, server_default="EXACT_SIMPLEX_HEURISTIC"),
        sa.Column("runtime_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED"),
        sa.Column("score_achieved", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("selected_initiative_ids", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. pareto_frontiers
    op.create_table(
        "pareto_frontiers",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("optimization_run_id", sa.Uuid(as_uuid=True), sa.ForeignKey("optimization_runs.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("frontier_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("plans_payload", sa.JSON(), nullable=False),
        sa.Column("tradeoff_summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. strategy_risk_assessments
    op.create_table(
        "strategy_risk_assessments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("initiative_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("risk_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("category", sa.String(length=100), nullable=False, server_default="OPERATIONAL"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("likelihood", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("impact", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.1"),
        sa.Column("mitigation_strategy", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. strategy_scorecards
    op.create_table(
        "strategy_scorecards",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("scorecard_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("period", sa.String(length=50), nullable=False, server_default="CURRENT_QUARTER"),
        sa.Column("composite_health_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("growth_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("profitability_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("delivery_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("ai_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("security_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("compliance_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("reliability_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("dimensions_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. strategy_alerts
    op.create_table(
        "strategy_alerts",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("alert_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("alert_type", sa.String(length=100), nullable=False, server_default="STRATEGIC_DRIFT"),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="WARNING"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("affected_objective_ids", sa.JSON(), nullable=False),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. strategy_decisions
    op.create_table(
        "strategy_decisions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("question", sa.String(length=255), nullable=False),
        sa.Column("context_summary", sa.Text(), nullable=False),
        sa.Column("selected_option", sa.JSON(), nullable=False),
        sa.Column("rejected_options", sa.JSON(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("decision_owner", sa.String(length=100), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("plan_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. strategy_outcomes
    op.create_table(
        "strategy_outcomes",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision_id", sa.Uuid(as_uuid=True), sa.ForeignKey("strategy_decisions.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("outcome_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("observed_period", sa.String(length=50), nullable=False),
        sa.Column("planned_metrics", sa.JSON(), nullable=False),
        sa.Column("actual_metrics", sa.JSON(), nullable=False),
        sa.Column("variance_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("model_prediction_error", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. strategy_drift_events
    op.create_table(
        "strategy_drift_events",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("drift_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("expected_value", sa.Float(), nullable=False),
        sa.Column("actual_value", sa.Float(), nullable=False),
        sa.Column("drift_percentage", sa.Float(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("is_adapted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("strategy_drift_events")
    op.drop_table("strategy_outcomes")
    op.drop_table("strategy_decisions")
    op.drop_table("strategy_alerts")
    op.drop_table("strategy_scorecards")
    op.drop_table("strategy_risk_assessments")
    op.drop_table("pareto_frontiers")
    op.drop_table("optimization_runs")
    op.drop_table("strategic_assumptions")
    op.drop_table("strategic_constraints")
    op.drop_table("initiative_dependencies")
    op.drop_table("strategic_initiatives")
    op.drop_table("key_results")
    op.drop_table("strategic_objectives")
    op.drop_table("strategic_plan_versions")
    op.drop_table("strategic_plans")
    op.drop_table("strategic_pillars")
