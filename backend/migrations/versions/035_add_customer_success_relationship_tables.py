"""add_customer_success_relationship_tables

Revision ID: 035
Revises: 034
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "035"
down_revision = "034"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. client_profiles
    op.create_table(
        "client_profiles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_account_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("business_id", sa.String(length=36), nullable=True, index=True),
        sa.Column("business_name", sa.String(length=255), nullable=False),
        sa.Column("lifecycle_stage", sa.String(length=50), nullable=False, server_default="ACTIVE", index=True),
        sa.Column("relationship_strength", sa.String(length=50), nullable=False, server_default="ESTABLISHED"),
        sa.Column("relationship_owner_id", sa.String(length=36), nullable=True),
        sa.Column("sales_owner_id", sa.String(length=36), nullable=True),
        sa.Column("project_owner_id", sa.String(length=36), nullable=True),
        sa.Column("cs_owner_id", sa.String(length=36), nullable=True),
        sa.Column("target_contract_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("ltv_estimate", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("churn_risk_band", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 2. client_relationships
    op.create_table(
        "client_relationships",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("contact_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("contact_name", sa.String(length=255), nullable=False),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("role_title", sa.String(length=100), nullable=True),
        sa.Column("decision_role", sa.String(length=50), nullable=False, server_default="USER"),
        sa.Column("relationship_strength", sa.String(length=50), nullable=False, server_default="ESTABLISHED"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 3. client_timeline_events
    op.create_table(
        "client_timeline_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("event_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("actor_type", sa.String(length=50), nullable=False, server_default="SYSTEM"),
        sa.Column("actor_id", sa.String(length=36), nullable=True),
        sa.Column("source_entity_type", sa.String(length=100), nullable=True),
        sa.Column("source_entity_id", sa.String(length=36), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"), index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 4. client_goals
    op.create_table(
        "client_goals",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="IN_PROGRESS"),
        sa.Column("success_metric", sa.String(length=255), nullable=True),
        sa.Column("target_value", sa.String(length=100), nullable=True),
        sa.Column("current_value", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 5. client_success_plans
    op.create_table(
        "client_success_plans",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("target_completion_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 6. client_success_tasks
    op.create_table(
        "client_success_tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("plan_id", sa.String(length=36), sa.ForeignKey("client_success_plans.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("goal_id", sa.String(length=36), nullable=True),
        sa.Column("client_profile_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("assigned_to_user_id", sa.String(length=36), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 7. client_health_scores
    op.create_table(
        "client_health_scores",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("overall_score", sa.Numeric(precision=5, scale=2), nullable=False, server_default="0.00"),
        sa.Column("health_band", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("trend", sa.String(length=50), nullable=False, server_default="STABLE"),
        sa.Column("engagement_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("project_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("support_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("finance_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("satisfaction_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("relationship_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("goal_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("positive_factors", sa.JSON(), nullable=True),
        sa.Column("risk_factors", sa.JSON(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 8. client_health_history
    op.create_table(
        "client_health_history",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("health_band", sa.String(length=50), nullable=False),
        sa.Column("trend", sa.String(length=50), nullable=False),
        sa.Column("factor_breakdown", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"), index=True),
    )

    # 9. client_surveys
    op.create_table(
        "client_surveys",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("survey_type", sa.String(length=50), nullable=False, server_default="CSAT"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("responses_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avg_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 10. client_survey_responses
    op.create_table(
        "client_survey_responses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("survey_id", sa.String(length=36), sa.ForeignKey("client_surveys.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("contact_id", sa.String(length=36), nullable=True),
        sa.Column("score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("csat", sa.Integer(), nullable=True),
        sa.Column("nps", sa.Integer(), nullable=True),
        sa.Column("ces", sa.Integer(), nullable=True),
        sa.Column("raw_feedback", sa.Text(), nullable=True),
        sa.Column("sentiment", sa.String(length=50), nullable=False, server_default="NEUTRAL"),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 11. client_sentiment_analyses
    op.create_table(
        "client_sentiment_analyses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_message_id", sa.String(length=36), nullable=True),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default="MESSAGE"),
        sa.Column("sentiment_label", sa.String(length=50), nullable=False, server_default="NEUTRAL"),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("model_version", sa.String(length=50), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 12. client_risks
    op.create_table(
        "client_risks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("risk_category", sa.String(length=50), nullable=False, server_default="RELATIONSHIP"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("recommended_action", sa.Text(), nullable=True),
        sa.Column("assigned_to_user_id", sa.String(length=36), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 13. client_opportunities
    op.create_table(
        "client_opportunities",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("opportunity_type", sa.String(length=50), nullable=False, server_default="EXPANSION"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("estimated_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="IDENTIFIED"),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("recommended_next_step", sa.Text(), nullable=True),
        sa.Column("linked_requirement_id", sa.String(length=36), nullable=True),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 14. client_renewals
    op.create_table(
        "client_renewals",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("renewal_window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("renewal_window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("contract_value", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="UPCOMING"),
        sa.Column("probability_pct", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 15. client_referrals
    op.create_table(
        "client_referrals",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("referred_business_name", sa.String(length=255), nullable=False),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("contact_phone", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="IDENTIFIED"),
        sa.Column("lead_id", sa.String(length=36), nullable=True),
        sa.Column("converted_revenue", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 16. client_segments
    op.create_table(
        "client_segments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("segment_name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rules", sa.JSON(), nullable=False),
        sa.Column("is_dynamic", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 17. client_account_plans
    op.create_table(
        "client_account_plans",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("relationship_map", sa.JSON(), nullable=True),
        sa.Column("service_summary", sa.Text(), nullable=True),
        sa.Column("risk_summary", sa.Text(), nullable=True),
        sa.Column("opportunity_summary", sa.Text(), nullable=True),
        sa.Column("next_steps", sa.Text(), nullable=True),
        sa.Column("review_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # 18. client_reviews
    op.create_table(
        "client_reviews",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("client_profile_id", sa.String(length=36), sa.ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("review_type", sa.String(length=50), nullable=False, server_default="QBR"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("summary_notes", sa.Text(), nullable=True),
        sa.Column("action_items", sa.JSON(), nullable=True),
        sa.Column("attendees", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SCHEDULED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("client_reviews")
    op.drop_table("client_account_plans")
    op.drop_table("client_segments")
    op.drop_table("client_referrals")
    op.drop_table("client_renewals")
    op.drop_table("client_opportunities")
    op.drop_table("client_risks")
    op.drop_table("client_sentiment_analyses")
    op.drop_table("client_survey_responses")
    op.drop_table("client_surveys")
    op.drop_table("client_health_history")
    op.drop_table("client_health_scores")
    op.drop_table("client_success_tasks")
    op.drop_table("client_success_plans")
    op.drop_table("client_goals")
    op.drop_table("client_timeline_events")
    op.drop_table("client_relationships")
    op.drop_table("client_profiles")
