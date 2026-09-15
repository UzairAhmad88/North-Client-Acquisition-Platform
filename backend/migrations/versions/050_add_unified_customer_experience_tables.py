"""add unified customer experience tables

Revision ID: 050
Revises: 049
Create Date: 2026-09-10 03:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '050'
down_revision = '049'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. customer_journeys
    op.create_table(
        'customer_journeys',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('customer_name', sa.String(length=255), nullable=True),
        sa.Column('journey_type', sa.String(length=64), nullable=False, server_default='sales'),
        sa.Column('current_stage', sa.String(length=64), nullable=False, server_default='discovery'),
        sa.Column('lifecycle_status', sa.String(length=64), nullable=False, server_default='active'),
        sa.Column('health_status', sa.String(length=64), nullable=False, server_default='healthy'),
        sa.Column('completion_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('effort_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('sentiment_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('stage_history', sa.JSON(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 2. customer_journey_stages
    op.create_table(
        'customer_journey_stages',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('journey_id', sa.String(length=64), sa.ForeignKey('customer_journeys.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('stage_name', sa.String(length=64), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='pending'),
        sa.Column('entered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('dropoff_risk', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('touchpoint_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 3. customer_journey_events
    op.create_table(
        'customer_journey_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('journey_id', sa.String(length=64), sa.ForeignKey('customer_journeys.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('stage', sa.String(length=64), nullable=False),
        sa.Column('channel', sa.String(length=64), nullable=False, server_default='web'),
        sa.Column('actor_type', sa.String(length=64), nullable=False, server_default='customer'),
        sa.Column('actor_id', sa.String(length=64), nullable=True),
        sa.Column('provenance_source', sa.String(length=255), nullable=True),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 4. customer_touchpoints
    op.create_table(
        'customer_touchpoints',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('journey_id', sa.String(length=64), sa.ForeignKey('customer_journeys.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('channel', sa.String(length=64), nullable=False),
        sa.Column('touchpoint_type', sa.String(length=64), nullable=False),
        sa.Column('purpose', sa.String(length=255), nullable=True),
        sa.Column('outcome', sa.String(length=64), nullable=False, server_default='completed'),
        sa.Column('sentiment', sa.String(length=64), nullable=False, server_default='neutral'),
        sa.Column('friction_detected', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('duration_seconds', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('interaction_metadata', sa.JSON(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 5. customer_journey_variants
    op.create_table(
        'customer_journey_variants',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('variant_name', sa.String(length=255), nullable=False),
        sa.Column('journey_type', sa.String(length=64), nullable=False),
        sa.Column('stage_sequence', sa.JSON(), nullable=False),
        sa.Column('frequency_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('conversion_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('avg_completion_time_hours', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('friction_frequency', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_optimal', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 6. customer_friction_points
    op.create_table(
        'customer_friction_points',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('journey_id', sa.String(length=64), nullable=True),
        sa.Column('stage', sa.String(length=64), nullable=False),
        sa.Column('friction_type', sa.String(length=64), nullable=False),
        sa.Column('severity', sa.String(length=64), nullable=False, server_default='medium'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('customer_impact', sa.Text(), nullable=True),
        sa.Column('business_impact', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('resolution_status', sa.String(length=64), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 7. customer_effort_records
    op.create_table(
        'customer_effort_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('journey_id', sa.String(length=64), nullable=True),
        sa.Column('stage', sa.String(length=64), nullable=False),
        sa.Column('ces_score', sa.Float(), nullable=False, server_default='2.0'),
        sa.Column('effort_tier', sa.String(length=64), nullable=False, server_default='low_effort'),
        sa.Column('step_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('form_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('repeated_info_instances', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('waiting_time_minutes', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('support_contacts_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 8. customer_sentiment_records
    op.create_table(
        'customer_sentiment_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_channel', sa.String(length=64), nullable=False),
        sa.Column('sentiment', sa.String(length=64), nullable=False, server_default='neutral'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('model_version', sa.String(length=64), nullable=False, server_default='cx-sentiment-v1'),
        sa.Column('detected_emotions', sa.JSON(), nullable=True),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('is_customer_stated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 9. customer_goals
    op.create_table(
        'customer_goals',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('goal_type', sa.String(length=64), nullable=False, server_default='business_goal'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('baseline_value', sa.String(length=255), nullable=True),
        sa.Column('target_value', sa.String(length=255), nullable=True),
        sa.Column('current_value', sa.String(length=255), nullable=True),
        sa.Column('progress_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='in_progress'),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('target_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 10. customer_experience_health
    op.create_table(
        'customer_experience_health',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column('overall_health_score', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('health_state', sa.String(length=64), nullable=False, server_default='healthy'),
        sa.Column('factor_breakdown', sa.JSON(), nullable=True),
        sa.Column('churn_probability', sa.Float(), nullable=False, server_default='0.1'),
        sa.Column('expansion_readiness', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('last_evaluated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 11. customer_churn_predictions
    op.create_table(
        'customer_churn_predictions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('churn_probability', sa.Float(), nullable=False),
        sa.Column('risk_level', sa.String(length=64), nullable=False, server_default='low'),
        sa.Column('primary_drivers', sa.JSON(), nullable=True),
        sa.Column('recommended_interventions', sa.JSON(), nullable=True),
        sa.Column('model_name', sa.String(length=64), nullable=False, server_default='gradient-boosted-churn-v2'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('is_confirmed_by_human', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('predicted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 12. customer_retention_opportunities
    op.create_table(
        'customer_retention_opportunities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('trigger_reason', sa.Text(), nullable=False),
        sa.Column('proposed_action', sa.Text(), nullable=False),
        sa.Column('impact_estimate', sa.String(length=64), nullable=False, server_default='high'),
        sa.Column('effort_required', sa.String(length=64), nullable=False, server_default='medium'),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='open'),
        sa.Column('requires_governance_approval', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 13. customer_expansion_opportunities
    op.create_table(
        'customer_expansion_opportunities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('expansion_type', sa.String(length=64), nullable=False, server_default='additional_capacity'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('estimated_arr_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('evidence_signals', sa.JSON(), nullable=True),
        sa.Column('stage', sa.String(length=64), nullable=False, server_default='discovery'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 14. customer_advocacy_records
    op.create_table(
        'customer_advocacy_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('advocacy_type', sa.String(length=64), nullable=False, server_default='testimonial'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('permission_granted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('publication_status', sa.String(length=64), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 15. customer_referrals
    op.create_table(
        'customer_referrals',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('referrer_customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('referred_company_name', sa.String(length=255), nullable=False),
        sa.Column('referred_contact_email', sa.String(length=255), nullable=True),
        sa.Column('relationship_context', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='submitted'),
        sa.Column('conversion_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 16. customer_segments
    op.create_table(
        'customer_segments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('criteria', sa.JSON(), nullable=True),
        sa.Column('member_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_health_score', sa.Float(), nullable=False, server_default='75.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 17. customer_personas
    op.create_table(
        'customer_personas',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('persona_name', sa.String(length=255), nullable=False),
        sa.Column('role_category', sa.String(length=64), nullable=False),
        sa.Column('primary_goals', sa.JSON(), nullable=True),
        sa.Column('common_pain_points', sa.JSON(), nullable=True),
        sa.Column('preferred_channels', sa.JSON(), nullable=True),
        sa.Column('evidence_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_ai_hypothesis', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 18. customer_voice_records
    op.create_table(
        'customer_voice_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_channel', sa.String(length=64), nullable=False),
        sa.Column('quote_text', sa.Text(), nullable=False),
        sa.Column('feedback_category', sa.String(length=64), nullable=False, server_default='need'),
        sa.Column('extracted_topics', sa.JSON(), nullable=True),
        sa.Column('sentiment', sa.String(length=64), nullable=False, server_default='neutral'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 19. customer_voice_themes
    op.create_table(
        'customer_voice_themes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('theme_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('frequency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('severity', sa.String(length=64), nullable=False, server_default='medium'),
        sa.Column('trend_direction', sa.String(length=64), nullable=False, server_default='stable'),
        sa.Column('affected_stages', sa.JSON(), nullable=True),
        sa.Column('sample_quotes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 20. customer_expectation_gaps
    op.create_table(
        'customer_expectation_gaps',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('area', sa.String(length=255), nullable=False),
        sa.Column('promised_capability', sa.Text(), nullable=False),
        sa.Column('customer_expected', sa.Text(), nullable=False),
        sa.Column('delivered_reality', sa.Text(), nullable=False),
        sa.Column('gap_severity', sa.String(length=64), nullable=False, server_default='moderate'),
        sa.Column('evidence_source', sa.String(length=255), nullable=True),
        sa.Column('remediation_action', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='identified'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 21. customer_experience_experiments
    op.create_table(
        'customer_experience_experiments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('experiment_type', sa.String(length=64), nullable=False, server_default='onboarding_flow'),
        sa.Column('hypothesis', sa.Text(), nullable=False),
        sa.Column('control_variant', sa.JSON(), nullable=False),
        sa.Column('treatment_variant', sa.JSON(), nullable=False),
        sa.Column('target_stage', sa.String(length=64), nullable=False),
        sa.Column('primary_metric', sa.String(length=64), nullable=False, server_default='conversion_rate'),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='draft'),
        sa.Column('sample_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('results_summary', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 22. customer_experience_alerts
    op.create_table(
        'customer_experience_alerts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('customer_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('alert_type', sa.String(length=64), nullable=False),
        sa.Column('severity', sa.String(length=64), nullable=False, server_default='warning'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('evidence_signals', sa.JSON(), nullable=True),
        sa.Column('recommended_action', sa.Text(), nullable=True),
        sa.Column('is_resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('customer_experience_alerts')
    op.drop_table('customer_experience_experiments')
    op.drop_table('customer_expectation_gaps')
    op.drop_table('customer_voice_themes')
    op.drop_table('customer_voice_records')
    op.drop_table('customer_personas')
    op.drop_table('customer_segments')
    op.drop_table('customer_referrals')
    op.drop_table('customer_advocacy_records')
    op.drop_table('customer_expansion_opportunities')
    op.drop_table('customer_retention_opportunities')
    op.drop_table('customer_churn_predictions')
    op.drop_table('customer_experience_health')
    op.drop_table('customer_goals')
    op.drop_table('customer_sentiment_records')
    op.drop_table('customer_effort_records')
    op.drop_table('customer_friction_points')
    op.drop_table('customer_journey_variants')
    op.drop_table('customer_touchpoints')
    op.drop_table('customer_journey_events')
    op.drop_table('customer_journey_stages')
    op.drop_table('customer_journeys')
