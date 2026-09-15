"""add unified revenue growth tables

Revision ID: 051
Revises: 050
Create Date: 2026-09-12 21:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '051'
down_revision = '050'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. gtm_strategies
    op.create_table(
        'gtm_strategies',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('target_market', sa.String(length=255), nullable=False),
        sa.Column('sales_motion', sa.String(length=64), nullable=False, server_default='consultative'),
        sa.Column('positioning', sa.Text(), nullable=True),
        sa.Column('value_proposition', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='active'),
        sa.Column('channels', sa.JSON(), nullable=True),
        sa.Column('metrics_targets', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 2. gtm_segments
    op.create_table(
        'gtm_segments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('strategy_id', sa.String(length=64), sa.ForeignKey('gtm_strategies.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('industry', sa.String(length=128), nullable=True),
        sa.Column('company_size_tier', sa.String(length=64), nullable=False, server_default='mid_market'),
        sa.Column('estimated_tam_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('estimated_sam_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('priority_tier', sa.String(length=32), nullable=False, server_default='tier_1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 3. gtm_icps
    op.create_table(
        'gtm_icps',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('segment_id', sa.String(length=64), sa.ForeignKey('gtm_segments.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('target_industries', sa.JSON(), nullable=True),
        sa.Column('min_employee_count', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('max_employee_count', sa.Integer(), nullable=False, server_default='5000'),
        sa.Column('min_arr_usd', sa.Float(), nullable=False, server_default='5000000.0'),
        sa.Column('required_tech_profile', sa.JSON(), nullable=True),
        sa.Column('pain_points', sa.JSON(), nullable=True),
        sa.Column('buying_signals', sa.JSON(), nullable=True),
        sa.Column('exclusions', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 4. target_accounts
    op.create_table(
        'target_accounts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=True, index=True),
        sa.Column('industry', sa.String(length=128), nullable=True),
        sa.Column('employee_count', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('estimated_annual_revenue', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('country', sa.String(length=64), nullable=True),
        sa.Column('icp_fit_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('priority_level', sa.String(length=32), nullable=False, server_default='medium'),
        sa.Column('coverage_status', sa.String(length=64), nullable=False, server_default='discovered'),
        sa.Column('assigned_rep', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 5. target_account_scores
    op.create_table(
        'target_account_scores',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('account_id', sa.String(length=64), sa.ForeignKey('target_accounts.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('icp_fit', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('business_need', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('digital_gap', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('revenue_potential', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('buying_signal', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('composite_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 6. market_coverage_records
    op.create_table(
        'market_coverage_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('segment', sa.String(length=128), nullable=False),
        sa.Column('territory', sa.String(length=128), nullable=False),
        sa.Column('accounts_discovered', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('accounts_researched', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('qualified_accounts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('contacted_accounts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('active_opportunities', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('won_accounts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('coverage_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 7. territory_definitions
    op.create_table(
        'territory_definitions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('geography', sa.String(length=128), nullable=False),
        sa.Column('industry_focus', sa.JSON(), nullable=True),
        sa.Column('account_tier', sa.String(length=64), nullable=False, server_default='tier_1'),
        sa.Column('owner_name', sa.String(length=128), nullable=True),
        sa.Column('revenue_potential_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 8. sales_pipelines
    op.create_table(
        'sales_pipelines',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('pipeline_type', sa.String(length=64), nullable=False, server_default='enterprise_new_business'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('stages', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 9. sales_opportunities
    op.create_table(
        'sales_opportunities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('account_id', sa.String(length=64), sa.ForeignKey('target_accounts.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('pipeline_id', sa.String(length=64), sa.ForeignKey('sales_pipelines.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('stage', sa.String(length=64), nullable=False, server_default='qualified'),
        sa.Column('estimated_arr_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('win_probability', sa.Float(), nullable=False, server_default='0.2'),
        sa.Column('weighted_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('expected_close_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('owner_name', sa.String(length=128), nullable=False, server_default='Account Executive'),
        sa.Column('sales_motion', sa.String(length=64), nullable=False, server_default='consultative'),
        sa.Column('primary_need', sa.Text(), nullable=True),
        sa.Column('risk_status', sa.String(length=32), nullable=False, server_default='healthy'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 10. sales_opportunity_health
    op.create_table(
        'sales_opportunity_health',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('engagement_score', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('decision_access_score', sa.Float(), nullable=False, server_default='75.0'),
        sa.Column('budget_evidence_score', sa.Float(), nullable=False, server_default='85.0'),
        sa.Column('overall_health_score', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('health_state', sa.String(length=32), nullable=False, server_default='healthy'),
        sa.Column('evaluated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 11. sales_activities
    op.create_table(
        'sales_activities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('activity_type', sa.String(length=64), nullable=False, server_default='meeting'),
        sa.Column('summary', sa.String(length=255), nullable=False),
        sa.Column('outcome', sa.String(length=128), nullable=True),
        sa.Column('actor_name', sa.String(length=128), nullable=False, server_default='Sales Rep'),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 12. sales_forecasts
    op.create_table(
        'sales_forecasts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('forecast_period', sa.String(length=64), nullable=False),
        sa.Column('model_version', sa.String(length=64), nullable=False, server_default='probabilistic-ensemble-v3'),
        sa.Column('p10_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p25_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p50_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p75_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p90_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('pipeline_total_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('weighted_pipeline_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('scenario', sa.String(length=64), nullable=False, server_default='base'),
        sa.Column('assumptions', sa.JSON(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 13. revenue_targets
    op.create_table(
        'revenue_targets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('period', sa.String(length=64), nullable=False),
        sa.Column('target_type', sa.String(length=64), nullable=False, server_default='company_arr'),
        sa.Column('target_amount_usd', sa.Float(), nullable=False),
        sa.Column('actual_amount_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('variance_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('variance_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 14. sales_capacity_plans
    op.create_table(
        'sales_capacity_plans',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('period', sa.String(length=64), nullable=False),
        sa.Column('rep_count', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('quota_per_rep_usd', sa.Float(), nullable=False, server_default='500000.0'),
        sa.Column('total_capacity_usd', sa.Float(), nullable=False, server_default='2500000.0'),
        sa.Column('ramp_factor', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('effective_capacity_usd', sa.Float(), nullable=False, server_default='2125000.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 15. pricing_intelligence
    op.create_table(
        'pricing_intelligence',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_or_service', sa.String(length=255), nullable=False),
        sa.Column('tier_name', sa.String(length=128), nullable=False),
        sa.Column('list_price_usd', sa.Float(), nullable=False),
        sa.Column('billing_frequency', sa.String(length=32), nullable=False, server_default='annual'),
        sa.Column('average_discount_pct', sa.Float(), nullable=False, server_default='10.0'),
        sa.Column('target_gross_margin_pct', sa.Float(), nullable=False, server_default='75.0'),
        sa.Column('willingness_to_pay_evidence', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 16. discount_requests
    op.create_table(
        'discount_requests',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('requested_discount_pct', sa.Float(), nullable=False),
        sa.Column('original_price_usd', sa.Float(), nullable=False),
        sa.Column('proposed_price_usd', sa.Float(), nullable=False),
        sa.Column('margin_impact_pct', sa.Float(), nullable=False),
        sa.Column('justification', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='pending_approval'),
        sa.Column('approver_name', sa.String(length=128), nullable=True),
        sa.Column('approval_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 17. deal_risks
    op.create_table(
        'deal_risks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('risk_category', sa.String(length=64), nullable=False, server_default='decision_maker'),
        sa.Column('severity', sa.String(length=32), nullable=False, server_default='medium'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('mitigation_strategy', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 18. next_best_actions
    op.create_table(
        'next_best_actions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recommended_action', sa.String(length=255), nullable=False),
        sa.Column('action_type', sa.String(length=64), nullable=False, server_default='schedule_technical_deep_dive'),
        sa.Column('rationale', sa.Text(), nullable=False),
        sa.Column('evidence_signals', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.88'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='recommended'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 19. lead_routing_rules
    op.create_table(
        'lead_routing_rules',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('rule_name', sa.String(length=255), nullable=False),
        sa.Column('criteria', sa.JSON(), nullable=False),
        sa.Column('target_rep_or_team', sa.String(length=128), nullable=False),
        sa.Column('priority_order', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 20. channel_definitions
    op.create_table(
        'channel_definitions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('channel_type', sa.String(length=64), nullable=False, server_default='outbound_direct'),
        sa.Column('leads_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('opportunities_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('revenue_won_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cac_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('conversion_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 21. attribution_records
    op.create_table(
        'attribution_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_id', sa.String(length=64), sa.ForeignKey('sales_opportunities.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('attribution_model', sa.String(length=64), nullable=False, server_default='multi_touch_w_shaped'),
        sa.Column('touchpoints_breakdown', sa.JSON(), nullable=False),
        sa.Column('evaluated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 22. customer_acquisition_economics
    op.create_table(
        'customer_acquisition_economics',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('period', sa.String(length=64), nullable=False),
        sa.Column('blended_cac_usd', sa.Float(), nullable=False, server_default='8500.0'),
        sa.Column('average_ltv_usd', sa.Float(), nullable=False, server_default='48000.0'),
        sa.Column('ltv_to_cac_ratio', sa.Float(), nullable=False, server_default='5.65'),
        sa.Column('payback_period_months', sa.Float(), nullable=False, server_default='6.5'),
        sa.Column('gross_margin_pct', sa.Float(), nullable=False, server_default='78.0'),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 23. revenue_waterfalls
    op.create_table(
        'revenue_waterfalls',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('period', sa.String(length=64), nullable=False),
        sa.Column('beginning_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('new_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('expansion_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('contraction_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('churn_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('ending_arr_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('net_retention_pct', sa.Float(), nullable=False, server_default='112.0'),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 24. revenue_risk_records
    op.create_table(
        'revenue_risk_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('risk_type', sa.String(length=64), nullable=False, server_default='customer_concentration'),
        sa.Column('severity', sa.String(length=32), nullable=False, server_default='medium'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('potential_revenue_impact_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('evidence_data', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 25. revenue_growth_opportunities
    op.create_table(
        'revenue_growth_opportunities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('opportunity_type', sa.String(length=64), nullable=False, server_default='cross_sell_ai_workforce'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('estimated_arr_potential_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('target_segment', sa.String(length=128), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='identified'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # 26. partner_profiles
    op.create_table(
        'partner_profiles',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('partner_name', sa.String(length=255), nullable=False),
        sa.Column('partner_type', sa.String(length=64), nullable=False, server_default='solution_integrator'),
        sa.Column('region', sa.String(length=128), nullable=True),
        sa.Column('referred_leads_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('influenced_revenue_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('tier', sa.String(length=32), nullable=False, server_default='gold'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('partner_profiles')
    op.drop_table('revenue_growth_opportunities')
    op.drop_table('revenue_risk_records')
    op.drop_table('revenue_waterfalls')
    op.drop_table('customer_acquisition_economics')
    op.drop_table('attribution_records')
    op.drop_table('channel_definitions')
    op.drop_table('lead_routing_rules')
    op.drop_table('next_best_actions')
    op.drop_table('deal_risks')
    op.drop_table('discount_requests')
    op.drop_table('pricing_intelligence')
    op.drop_table('sales_capacity_plans')
    op.drop_table('revenue_targets')
    op.drop_table('sales_forecasts')
    op.drop_table('sales_activities')
    op.drop_table('sales_opportunity_health')
    op.drop_table('sales_opportunities')
    op.drop_table('sales_pipelines')
    op.drop_table('territory_definitions')
    op.drop_table('market_coverage_records')
    op.drop_table('target_account_scores')
    op.drop_table('target_accounts')
    op.drop_table('gtm_icps')
    op.drop_table('gtm_segments')
    op.drop_table('gtm_strategies')
