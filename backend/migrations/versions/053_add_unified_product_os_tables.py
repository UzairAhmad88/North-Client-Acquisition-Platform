"""add unified product os tables

Revision ID: 053
Revises: 052
Create Date: 2026-09-12 22:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '053'
down_revision = '052'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. product_portfolio_items
    op.create_table(
        'product_portfolio_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('product_line', sa.String(length=100), nullable=False, server_default='Core Platform'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('lifecycle_state', sa.String(length=50), nullable=False, server_default='DEVELOPMENT'),
        sa.Column('target_market', sa.String(length=255), nullable=True),
        sa.Column('owner', sa.String(length=100), nullable=False, server_default='product_lead'),
        sa.Column('arr_contribution_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('active_accounts_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. product_visions
    op.create_table(
        'product_visions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('vision_statement', sa.Text(), nullable=False),
        sa.Column('target_users', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('core_differentiator', sa.Text(), nullable=False),
        sa.Column('strategic_fit', sa.Text(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. product_strategies
    op.create_table(
        'product_strategies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('strategic_pillars', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('competitive_moat', sa.Text(), nullable=False),
        sa.Column('growth_motion', sa.String(length=50), nullable=False, server_default='PRODUCT_LED_SALES_ASSISTED'),
        sa.Column('product_bets', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. product_objectives
    op.create_table(
        'product_objectives',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('objective_title', sa.String(length=255), nullable=False),
        sa.Column('quarter', sa.String(length=50), nullable=False),
        sa.Column('key_results', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('progress_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='IN_PROGRESS'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. product_problems
    op.create_table(
        'product_problems',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='SET NULL'), nullable=True),
        sa.Column('statement', sa.Text(), nullable=False),
        sa.Column('target_segment', sa.String(length=100), nullable=False),
        sa.Column('validation_status', sa.String(length=50), nullable=False, server_default='VALIDATED'),
        sa.Column('evidence_type', sa.String(length=50), nullable=False, server_default='MEASURED'),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='HIGH'),
        sa.Column('cost_of_inaction_usd', sa.Float(), nullable=False, server_default='50000.0'),
        sa.Column('customer_mentions_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. product_feedback_items
    op.create_table(
        'product_feedback_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('problem_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_problems.id', ondelete='SET NULL'), nullable=True),
        sa.Column('customer_id', sa.String(length=100), nullable=False),
        sa.Column('source_channel', sa.String(length=50), nullable=False, server_default='SUPPORT'),
        sa.Column('feedback_text', sa.Text(), nullable=False),
        sa.Column('feedback_category', sa.String(length=50), nullable=False, server_default='USABILITY_ISSUE'),
        sa.Column('arr_impact_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 7. product_feedback_themes
    op.create_table(
        'product_feedback_themes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('theme_title', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='CORE_WORKFLOW'),
        sa.Column('frequency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('affected_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='MEDIUM'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. product_insights
    op.create_table(
        'product_insights',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('insight_text', sa.Text(), nullable=False),
        sa.Column('evidence_sources', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence_pct', sa.Float(), nullable=False, server_default='85.0'),
        sa.Column('impact_area', sa.String(length=100), nullable=False, server_default='User Activation'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. product_opportunities
    op.create_table(
        'product_opportunities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('problem_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_problems.id', ondelete='SET NULL'), nullable=True),
        sa.Column('customer_value_score', sa.Float(), nullable=False, server_default='8.0'),
        sa.Column('business_value_score', sa.Float(), nullable=False, server_default='8.5'),
        sa.Column('strategic_fit_score', sa.Float(), nullable=False, server_default='9.0'),
        sa.Column('estimated_arr_gain_usd', sa.Float(), nullable=False, server_default='100000.0'),
        sa.Column('composite_opportunity_score', sa.Float(), nullable=False, server_default='8.5'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='IDENTIFIED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 10. product_prioritization_scores
    op.create_table(
        'product_prioritization_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('opportunity_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_opportunities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('framework', sa.String(length=50), nullable=False, server_default='RICE'),
        sa.Column('reach', sa.Float(), nullable=False, server_default='1000.0'),
        sa.Column('impact', sa.Float(), nullable=False, server_default='3.0'),
        sa.Column('confidence_pct', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('effort_person_weeks', sa.Float(), nullable=False, server_default='4.0'),
        sa.Column('final_score', sa.Float(), nullable=False, server_default='600.0'),
        sa.Column('approved_by', sa.String(length=100), nullable=True),
        sa.Column('calculated_at', sa.DateTime(), nullable=False),
    )

    # 11. product_roadmaps
    op.create_table(
        'product_roadmaps',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 12. product_roadmap_items
    op.create_table(
        'product_roadmap_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('roadmap_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_roadmaps.id', ondelete='CASCADE'), nullable=False),
        sa.Column('opportunity_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_opportunities.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('horizon', sa.String(length=50), nullable=False, server_default='NOW'),
        sa.Column('quarter', sa.String(length=50), nullable=False, server_default='2026-Q4'),
        sa.Column('engineering_effort_weeks', sa.Float(), nullable=False, server_default='4.0'),
        sa.Column('dependencies', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('delivery_risk', sa.String(length=50), nullable=False, server_default='LOW'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PLANNED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 13. product_requirements
    op.create_table(
        'product_requirements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('roadmap_item_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_roadmap_items.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('requirement_type', sa.String(length=50), nullable=False, server_default='FUNCTIONAL'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('target_persona', sa.String(length=100), nullable=False, server_default='Managing Partner'),
        sa.Column('is_governance_reviewed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='SPECIFIED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 14. product_user_stories
    op.create_table(
        'product_user_stories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('requirement_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_requirements.id', ondelete='CASCADE'), nullable=False),
        sa.Column('story_narrative', sa.Text(), nullable=False),
        sa.Column('given_clause', sa.Text(), nullable=False),
        sa.Column('when_clause', sa.Text(), nullable=False),
        sa.Column('then_clause', sa.Text(), nullable=False),
        sa.Column('story_points', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='READY_FOR_DEV'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. product_feature_adoptions
    op.create_table(
        'product_feature_adoptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('feature_name', sa.String(length=255), nullable=False),
        sa.Column('eligible_users', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('active_users', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('adoption_rate_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('frequency_per_week', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('customer_value_rating', sa.Float(), nullable=False, server_default='4.5'),
        sa.Column('measured_at', sa.DateTime(), nullable=False),
    )

    # 16. product_health_scorecards
    op.create_table(
        'product_health_scorecards',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('composite_health_state', sa.String(length=50), nullable=False, server_default='HEALTHY'),
        sa.Column('adoption_score', sa.Float(), nullable=False, server_default='85.0'),
        sa.Column('retention_score', sa.Float(), nullable=False, server_default='92.0'),
        sa.Column('reliability_score', sa.Float(), nullable=False, server_default='99.9'),
        sa.Column('feedback_sentiment_score', sa.Float(), nullable=False, server_default='88.0'),
        sa.Column('support_efficiency_score', sa.Float(), nullable=False, server_default='90.0'),
        sa.Column('quality_score', sa.Float(), nullable=False, server_default='95.0'),
        sa.Column('economics_margin_score', sa.Float(), nullable=False, server_default='84.0'),
        sa.Column('measured_at', sa.DateTime(), nullable=False),
    )

    # 17. product_launch_plans
    op.create_table(
        'product_launch_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('release_version', sa.String(length=50), nullable=False),
        sa.Column('release_strategy', sa.String(length=50), nullable=False, server_default='FEATURE_FLAGGED_PHASED'),
        sa.Column('checklist', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_ready', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('approved_by', sa.String(length=100), nullable=True),
        sa.Column('scheduled_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 18. product_feature_flags
    op.create_table(
        'product_feature_flags',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('flag_key', sa.String(length=100), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('rollout_pct', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_environments', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('owner', sa.String(length=100), nullable=False, server_default='release_engineer'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 19. product_unit_economics
    op.create_table(
        'product_unit_economics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('arpu_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cogs_per_user_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('gross_margin_pct', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('support_cost_per_user_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('ltv_to_cac_ratio', sa.Float(), nullable=False, server_default='4.2'),
        sa.Column('calculated_at', sa.DateTime(), nullable=False),
    )

    # 20. product_forecasts
    op.create_table(
        'product_forecasts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('period', sa.String(length=50), nullable=False),
        sa.Column('scenario', sa.String(length=50), nullable=False, server_default='BASE'),
        sa.Column('p10_active_users', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p50_active_users', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p90_active_users', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('p50_arr_contribution_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('model_version', sa.String(length=50), nullable=False, server_default='v1.0-monte-carlo'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 21. product_risks
    op.create_table(
        'product_risks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product_portfolio_items.id', ondelete='SET NULL'), nullable=True),
        sa.Column('risk_category', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='MEDIUM'),
        sa.Column('mitigation_strategy', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('product_risks')
    op.drop_table('product_forecasts')
    op.drop_table('product_unit_economics')
    op.drop_table('product_feature_flags')
    op.drop_table('product_launch_plans')
    op.drop_table('product_health_scorecards')
    op.drop_table('product_feature_adoptions')
    op.drop_table('product_user_stories')
    op.drop_table('product_requirements')
    op.drop_table('product_roadmap_items')
    op.drop_table('product_roadmaps')
    op.drop_table('product_prioritization_scores')
    op.drop_table('product_opportunities')
    op.drop_table('product_insights')
    op.drop_table('product_feedback_themes')
    op.drop_table('product_feedback_items')
    op.drop_table('product_problems')
    op.drop_table('product_objectives')
    op.drop_table('product_strategies')
    op.drop_table('product_visions')
    op.drop_table('product_portfolio_items')
