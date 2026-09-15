"""add unified marketing tables

Revision ID: 052
Revises: 051
Create Date: 2026-09-12 22:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '052'
down_revision = '051'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. marketing_audiences
    op.create_table(
        'marketing_audiences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_icp', sa.String(length=255), nullable=True),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('company_size_tier', sa.String(length=50), nullable=True),
        sa.Column('buying_context', sa.String(length=255), nullable=True),
        sa.Column('primary_pain_points', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('channel_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('total_market_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reachable_market_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. marketing_segments
    op.create_table(
        'marketing_segments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('segment_type', sa.String(length=50), nullable=False, server_default='BEHAVIORAL'),
        sa.Column('criteria', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('account_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_revenue_potential_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. marketing_personas
    op.create_table(
        'marketing_personas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('role_type', sa.String(length=50), nullable=False, server_default='DECISION_MAKER'),
        sa.Column('assumption_status', sa.String(length=50), nullable=False, server_default='OBSERVED'),
        sa.Column('core_responsibilities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('top_priorities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('key_objections', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('preferred_content_formats', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. marketing_positioning
    op.create_table(
        'marketing_positioning',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_customer', sa.String(length=255), nullable=False),
        sa.Column('problem_statement', sa.Text(), nullable=False),
        sa.Column('alternative_solution', sa.Text(), nullable=False),
        sa.Column('our_solution', sa.Text(), nullable=False),
        sa.Column('key_differentiators', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('value_statement', sa.Text(), nullable=False),
        sa.Column('proof_points', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('approved_by', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. marketing_message_houses
    op.create_table(
        'marketing_message_houses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('positioning_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_positioning.id', ondelete='CASCADE'), nullable=False),
        sa.Column('core_message', sa.Text(), nullable=False),
        sa.Column('pillar_1', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('pillar_2', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('pillar_3', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('call_to_action', sa.String(length=255), nullable=False),
        sa.Column('forbidden_terms', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('preferred_terms', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. content_assets
    op.create_table(
        'content_assets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False, server_default='ARTICLE'),
        sa.Column('journey_stage', sa.String(length=50), nullable=False, server_default='AWARENESS'),
        sa.Column('target_audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('current_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('body_markdown', sa.Text(), nullable=False),
        sa.Column('primary_cta', sa.String(length=255), nullable=True),
        sa.Column('revenue_influenced_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('views_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('conversions_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 7. content_asset_versions
    op.create_table(
        'content_asset_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body_markdown', sa.Text(), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=False, server_default='system'),
        sa.Column('change_summary', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. content_briefs
    op.create_table(
        'content_briefs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('target_topic', sa.String(length=255), nullable=False),
        sa.Column('target_audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('journey_stage', sa.String(length=50), nullable=False, server_default='AWARENESS'),
        sa.Column('search_intent', sa.String(length=50), nullable=False, server_default='INFORMATIONAL'),
        sa.Column('key_takeaways', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('primary_keywords', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('required_evidence_sources', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. content_claims
    op.create_table(
        'content_claims',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('claim_text', sa.Text(), nullable=False),
        sa.Column('source_reference', sa.String(length=255), nullable=False),
        sa.Column('source_date', sa.String(length=50), nullable=True),
        sa.Column('confidence_pct', sa.Float(), nullable=False, server_default='85.0'),
        sa.Column('verification_status', sa.String(length=50), nullable=False, server_default='VERIFIED'),
        sa.Column('reviewer_notes', sa.Text(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 10. content_approvals
    op.create_table(
        'content_approvals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content_assets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('approver', sa.String(length=100), nullable=False),
        sa.Column('approval_type', sa.String(length=50), nullable=False, server_default='EDITORIAL'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='APPROVED'),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 11. content_gaps
    op.create_table(
        'content_gaps',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('target_audience', sa.String(length=100), nullable=False),
        sa.Column('journey_stage', sa.String(length=50), nullable=False),
        sa.Column('demand_volume', sa.String(length=50), nullable=False, server_default='HIGH'),
        sa.Column('revenue_potential_usd', sa.Float(), nullable=False, server_default='50000.0'),
        sa.Column('effort_tier', sa.String(length=50), nullable=False, server_default='MEDIUM'),
        sa.Column('priority_score', sa.Float(), nullable=False, server_default='8.5'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 12. brand_voice_profiles
    op.create_table(
        'brand_voice_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, server_default='Default Brand Voice'),
        sa.Column('primary_tone', sa.String(length=50), nullable=False, server_default='AUTHORITATIVE_EMPATHETIC'),
        sa.Column('reading_level', sa.String(length=50), nullable=False, server_default='PROFESSIONAL'),
        sa.Column('prohibited_claims', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('preferred_vocab', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 13. marketing_campaigns
    op.create_table(
        'marketing_campaigns',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('campaign_type', sa.String(length=50), nullable=False, server_default='DEMAND_GENERATION'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('target_audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('allocated_budget_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('actual_spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('leads_generated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mql_generated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('sql_generated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('opportunities_influenced', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('pipeline_influenced_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('revenue_attributed_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('channels', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('owner', sa.String(length=100), nullable=False, server_default='growth_lead'),
        sa.Column('is_governance_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 14. marketing_campaign_versions
    op.create_table(
        'marketing_campaign_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('snapshot', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. marketing_channels
    op.create_table(
        'marketing_channels',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('channel_type', sa.String(length=50), nullable=False, server_default='ORGANIC_SEARCH'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('total_spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_revenue_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('avg_cac_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('avg_roas', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 16. marketing_channel_metrics
    op.create_table(
        'marketing_channel_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('channel_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_channels.id', ondelete='CASCADE'), nullable=False),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('impressions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('clicks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mql', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('revenue_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 17. email_campaigns
    op.create_table(
        'email_campaigns',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_campaigns.id', ondelete='SET NULL'), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('subject_line', sa.String(length=255), nullable=False),
        sa.Column('preview_text', sa.String(length=255), nullable=True),
        sa.Column('sender_name', sa.String(length=100), nullable=False, server_default="North's Advisory"),
        sa.Column('sender_email', sa.String(length=150), nullable=False, server_default='insights@norths.io'),
        sa.Column('recipients_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('delivered_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('opened_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('clicked_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('unsubscribed_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 18. email_templates
    op.create_table(
        'email_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='NURTURE'),
        sa.Column('body_html', sa.Text(), nullable=False),
        sa.Column('body_text', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 19. email_sequences
    op.create_table(
        'email_sequences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('target_audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('steps', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('enrolled_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completed_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 20. email_suppressions
    op.create_table(
        'email_suppressions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('reason', sa.String(length=50), nullable=False, server_default='UNSUBSCRIBE'),
        sa.Column('source', sa.String(length=100), nullable=False, server_default='user_opt_out'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 21. marketing_leads
    op.create_table(
        'marketing_leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, index=True),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('source_channel', sa.String(length=100), nullable=False, server_default='ORGANIC_SEARCH'),
        sa.Column('first_touch_campaign', sa.String(length=255), nullable=True),
        sa.Column('last_touch_campaign', sa.String(length=255), nullable=True),
        sa.Column('fit_score', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('engagement_score', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('intent_score', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('composite_lead_score', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('qualification_stage', sa.String(length=50), nullable=False, server_default='NEW'),
        sa.Column('consent_obtained', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_suppressed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 22. marketing_lead_scores
    op.create_table(
        'marketing_lead_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_leads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('fit_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('engagement_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('intent_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('calculated_at', sa.DateTime(), nullable=False),
    )

    # 23. marketing_nurture_programs
    op.create_table(
        'marketing_nurture_programs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('goal', sa.String(length=255), nullable=False),
        sa.Column('entry_conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('exit_conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('active_leads_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('converted_leads_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 24. marketing_funnel_metrics
    op.create_table(
        'marketing_funnel_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('impressions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('visitors', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mql', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('sql', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('opportunities', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('deals_won', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('conversion_rate_lead_to_mql_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('conversion_rate_mql_to_sql_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('conversion_rate_sql_to_won_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('avg_funnel_velocity_days', sa.Float(), nullable=False, server_default='28.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 25. marketing_attribution_records
    op.create_table(
        'marketing_attribution_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=100), nullable=True),
        sa.Column('deal_value_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('attribution_model', sa.String(length=50), nullable=False, server_default='MULTI_TOUCH_W_SHAPED'),
        sa.Column('touches', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('campaign_credits', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('channel_credits', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('calculated_at', sa.DateTime(), nullable=False),
    )

    # 26. marketing_budgets
    op.create_table(
        'marketing_budgets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('total_planned_budget_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_committed_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_spent_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('channel_allocations', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('approved_by', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 27. marketing_roi_records
    op.create_table(
        'marketing_roi_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('total_spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_attributed_revenue_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cost_per_lead_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cost_per_mql_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cost_per_acquisition_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('roas', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('roi_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 28. marketing_experiments
    op.create_table(
        'marketing_experiments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('experiment_type', sa.String(length=50), nullable=False, server_default='LANDING_PAGE_CTA'),
        sa.Column('hypothesis', sa.Text(), nullable=False),
        sa.Column('variants', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('sample_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('confidence_level_pct', sa.Float(), nullable=False, server_default='95.0'),
        sa.Column('winner_variant', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='RUNNING'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 29. landing_pages
    op.create_table(
        'landing_pages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('slug', sa.String(length=255), nullable=False, unique=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('target_campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_campaigns.id', ondelete='SET NULL'), nullable=True),
        sa.Column('visitors_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('submissions_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('conversion_rate_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 30. seo_keywords
    op.create_table(
        'seo_keywords',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('keyword', sa.String(length=255), nullable=False, unique=True),
        sa.Column('monthly_search_volume', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('keyword_difficulty', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('search_intent', sa.String(length=50), nullable=False, server_default='INFORMATIONAL'),
        sa.Column('current_ranking', sa.Integer(), nullable=True),
        sa.Column('target_content_asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('content_assets.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 31. marketing_events
    op.create_table(
        'marketing_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False, server_default='WEBINAR'),
        sa.Column('registrations_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('attendees_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('leads_generated_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('scheduled_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 32. marketing_calendar_events
    op.create_table(
        'marketing_calendar_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False, server_default='CAMPAIGN_LAUNCH'),
        sa.Column('channel', sa.String(length=50), nullable=False, server_default='EMAIL'),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('has_conflict', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 33. marketing_forecasts
    op.create_table(
        'marketing_forecasts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('scenario', sa.String(length=50), nullable=False, server_default='BASE'),
        sa.Column('p10_leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p25_leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p50_leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p75_leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p90_leads', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p50_pipeline_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p50_revenue_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('model_version', sa.String(length=50), nullable=False, server_default='v1.0-monte-carlo'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 34. marketing_risks
    op.create_table(
        'marketing_risks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('risk_category', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='MEDIUM'),
        sa.Column('mitigation_strategy', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 35. marketing_fatigue_records
    op.create_table(
        'marketing_fatigue_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('audience_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('marketing_audiences.id', ondelete='SET NULL'), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=False),
        sa.Column('weekly_frequency', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('unsubscribe_rate_pct', sa.Float(), nullable=False, server_default='0.2'),
        sa.Column('engagement_decay_pct', sa.Float(), nullable=False, server_default='5.0'),
        sa.Column('fatigue_level', sa.String(length=50), nullable=False, server_default='NORMAL'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('marketing_fatigue_records')
    op.drop_table('marketing_risks')
    op.drop_table('marketing_forecasts')
    op.drop_table('marketing_calendar_events')
    op.drop_table('marketing_events')
    op.drop_table('seo_keywords')
    op.drop_table('landing_pages')
    op.drop_table('marketing_experiments')
    op.drop_table('marketing_roi_records')
    op.drop_table('marketing_budgets')
    op.drop_table('marketing_attribution_records')
    op.drop_table('marketing_funnel_metrics')
    op.drop_table('marketing_nurture_programs')
    op.drop_table('marketing_lead_scores')
    op.drop_table('marketing_leads')
    op.drop_table('email_suppressions')
    op.drop_table('email_sequences')
    op.drop_table('email_templates')
    op.drop_table('email_campaigns')
    op.drop_table('marketing_channel_metrics')
    op.drop_table('marketing_channels')
    op.drop_table('marketing_campaign_versions')
    op.drop_table('marketing_campaigns')
    op.drop_table('brand_voice_profiles')
    op.drop_table('content_gaps')
    op.drop_table('content_approvals')
    op.drop_table('content_claims')
    op.drop_table('content_briefs')
    op.drop_table('content_asset_versions')
    op.drop_table('content_assets')
    op.drop_table('marketing_message_houses')
    op.drop_table('marketing_positioning')
    op.drop_table('marketing_personas')
    op.drop_table('marketing_segments')
    op.drop_table('marketing_audiences')
