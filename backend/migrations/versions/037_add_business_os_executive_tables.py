"""add_business_os_executive_tables

Revision ID: 037
Revises: 036
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "037"
down_revision = "036"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. strategic_objectives
    op.create_table(
        "strategic_objectives",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), nullable=False, server_default="default_org", index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("timeframe", sa.String(length=50), nullable=False, server_default="FY2026"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="P1_HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE", index=True),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="Executive Team"),
        sa.Column("progress_pct", sa.Numeric(precision=5, scale=2), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. key_results
    op.create_table(
        "key_results",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("objective_id", sa.String(length=36), sa.ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("target_value", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("current_value", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.0"),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default="%"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="NOT_STARTED"),
        sa.Column("owner", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. initiatives
    op.create_table(
        "initiatives",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("objective_id", sa.String(length=36), sa.ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("budget", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.0"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="P1_HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PLANNED", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. initiative_milestones
    op.create_table(
        "initiative_milestones",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("initiative_id", sa.String(length=36), sa.ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("due_date", sa.String(length=50), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. initiative_dependencies
    op.create_table(
        "initiative_dependencies",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("initiative_id", sa.String(length=36), sa.ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("dependency_type", sa.String(length=50), nullable=False),
        sa.Column("state", sa.String(length=50), nullable=False, server_default="AVAILABLE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. kpi_definitions
    op.create_table(
        "kpi_definitions",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="PKR"),
        sa.Column("source_domain", sa.String(length=100), nullable=False),
        sa.Column("formula", sa.Text(), nullable=False),
        sa.Column("target_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("warning_threshold", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("critical_threshold", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("freshness_max_seconds", sa.Integer(), nullable=False, server_default="3600"),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("is_higher_better", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. kpi_value_snapshots
    op.create_table(
        "kpi_value_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("kpi_id", sa.String(length=100), sa.ForeignKey("kpi_definitions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("value", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("target_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("variance", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ON_TRACK"),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 8. scorecard_records
    op.create_table(
        "scorecard_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("department_name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, index=True),
        sa.Column("overall_status", sa.String(length=50), nullable=False, server_default="ON_TRACK"),
        sa.Column("scorecard_items_json", sa.JSON(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 9. business_health_snapshots
    op.create_table(
        "business_health_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("overall_health_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("overall_status", sa.String(length=50), nullable=False, server_default="HEALTHY", index=True),
        sa.Column("dimensions_json", sa.JSON(), nullable=False),
        sa.Column("key_strengths_json", sa.JSON(), nullable=True),
        sa.Column("critical_risks_json", sa.JSON(), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 10. organizational_risks
    op.create_table(
        "organizational_risks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, index=True),
        sa.Column("probability", sa.String(length=50), nullable=False, server_default="POSSIBLE"),
        sa.Column("impact", sa.String(length=50), nullable=False, server_default="MODERATE"),
        sa.Column("risk_score", sa.Integer(), nullable=False, server_default="9"),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="MEDIUM", index=True),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ASSESSED", index=True),
        sa.Column("evidence_signals_json", sa.JSON(), nullable=True),
        sa.Column("mitigation_strategy", sa.Text(), nullable=True),
        sa.Column("contingency_plan", sa.Text(), nullable=True),
        sa.Column("due_date", sa.String(length=50), nullable=True),
        sa.Column("identified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. decision_records
    op.create_table(
        "decision_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("business_question", sa.Text(), nullable=False),
        sa.Column("context_summary", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="P1_HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DECISION_REQUIRED", index=True),
        sa.Column("ai_recommendation", sa.Text(), nullable=True),
        sa.Column("ai_recommendation_rationale", sa.Text(), nullable=True),
        sa.Column("chosen_option_id", sa.String(length=50), nullable=True),
        sa.Column("chosen_option_title", sa.String(length=255), nullable=True),
        sa.Column("decision_rationale", sa.Text(), nullable=True),
        sa.Column("decided_by", sa.String(length=100), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expected_outcome", sa.Text(), nullable=True),
        sa.Column("actual_outcome", sa.Text(), nullable=True),
        sa.Column("outcome_variance_analysis", sa.Text(), nullable=True),
        sa.Column("lessons_learned_json", sa.JSON(), nullable=True),
        sa.Column("evidence_signals_json", sa.JSON(), nullable=True),
        sa.Column("review_due_date", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. scenario_models
    op.create_table(
        "scenario_models",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("scenario_type", sa.String(length=50), nullable=False, server_default="CUSTOM"),
        sa.Column("simulated_revenue", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("simulated_profit", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("simulated_margin_pct", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("capacity_utilization_pct", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("cash_requirement", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("assumptions_json", sa.JSON(), nullable=True),
        sa.Column("sensitivity_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. executive_briefings
    op.create_table(
        "executive_briefings",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("frequency", sa.String(length=50), nullable=False, server_default="DAILY", index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary_paragraph", sa.Text(), nullable=False),
        sa.Column("key_metrics_json", sa.JSON(), nullable=True),
        sa.Column("what_changed_json", sa.JSON(), nullable=True),
        sa.Column("top_decisions_json", sa.JSON(), nullable=True),
        sa.Column("critical_risks_json", sa.JSON(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    # 14. business_calendar_events
    op.create_table(
        "business_calendar_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("event_date", sa.String(length=50), nullable=False, index=True),
        sa.Column("related_entity_id", sa.String(length=100), nullable=False),
        sa.Column("related_entity_name", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("owner", sa.String(length=100), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. executive_alerts
    op.create_table(
        "executive_alerts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="HIGH", index=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="TRIGGERED", index=True),
        sa.Column("source_domain", sa.String(length=100), nullable=False),
        sa.Column("acknowledged_by", sa.String(length=100), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )


def downgrade() -> None:
    op.drop_table("executive_alerts")
    op.drop_table("business_calendar_events")
    op.drop_table("executive_briefings")
    op.drop_table("scenario_models")
    op.drop_table("decision_records")
    op.drop_table("organizational_risks")
    op.drop_table("business_health_snapshots")
    op.drop_table("scorecard_records")
    op.drop_table("kpi_value_snapshots")
    op.drop_table("kpi_definitions")
    op.drop_table("initiative_dependencies")
    op.drop_table("initiative_milestones")
    op.drop_table("initiatives")
    op.drop_table("key_results")
    op.drop_table("strategic_objectives")
