"""add unified innovation tables

Revision ID: 048
Revises: 047
Create Date: 2026-09-10 03:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '048'
down_revision = '047'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. innovation_workspaces
    op.create_table(
        'innovation_workspaces',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('theme', sa.String(length=128), nullable=False, server_default='PRODUCT_INNOVATION'),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DISCOVERY'),
        sa.Column('owner_id', sa.String(length=128), nullable=False),
        sa.Column('target_market', sa.String(length=128), nullable=True),
        sa.Column('horizon', sa.String(length=16), nullable=False, server_default='H1'),
        sa.Column('stage_gate', sa.String(length=32), nullable=False, server_default='GATE_0_IDEA'),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='0.75'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. innovation_problems
    op.create_table(
        'innovation_problems',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('statement', sa.Text(), nullable=False),
        sa.Column('affected_users', sa.String(length=255), nullable=True),
        sa.Column('frequency', sa.String(length=64), nullable=False, server_default='DAILY'),
        sa.Column('severity', sa.String(length=32), nullable=False, server_default='HIGH'),
        sa.Column('existing_solutions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('willingness_to_pay_signal', sa.Float(), nullable=True),
        sa.Column('urgency_score', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='OBSERVED'),
        sa.Column('evidence_sources', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_problems_workspace_id'), 'innovation_problems', ['workspace_id'], unique=False)

    # 3. innovation_opportunities
    op.create_table(
        'innovation_opportunities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('market_potential', sa.String(length=32), nullable=False, server_default='HIGH'),
        sa.Column('revenue_potential_usd', sa.Float(), nullable=True),
        sa.Column('competitive_intensity', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('technical_feasibility', sa.String(length=32), nullable=False, server_default='FEASIBLE'),
        sa.Column('strategic_alignment_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('time_to_market_months', sa.Float(), nullable=False, server_default='3.0'),
        sa.Column('risk_level', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_opportunities_workspace_id'), 'innovation_opportunities', ['workspace_id'], unique=False)

    # 4. innovation_ideas
    op.create_table(
        'innovation_ideas',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('problem_id', sa.String(length=64), nullable=True),
        sa.Column('opportunity_id', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('origin_source', sa.String(length=128), nullable=False, server_default='HUMAN'),
        sa.Column('target_users', sa.String(length=255), nullable=True),
        sa.Column('proposed_value', sa.Text(), nullable=True),
        sa.Column('assumptions_summary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('customer_value_score', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('market_potential_score', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('strategic_fit_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('revenue_potential_score', sa.Float(), nullable=False, server_default='0.75'),
        sa.Column('profitability_score', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('differentiation_score', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('technical_feasibility_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('execution_complexity_score', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('risk_score', sa.Float(), nullable=False, server_default='0.4'),
        sa.Column('time_to_value_score', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('evidence_strength_score', sa.Float(), nullable=False, server_default='0.6'),
        sa.Column('composite_score', sa.Float(), nullable=False, server_default='0.76'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='IDEA'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_ideas_workspace_id'), 'innovation_ideas', ['workspace_id'], unique=False)

    # 5. innovation_hypotheses
    op.create_table(
        'innovation_hypotheses',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('idea_id', sa.String(length=64), sa.ForeignKey('innovation_ideas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('statement', sa.Text(), nullable=False),
        sa.Column('prediction', sa.Text(), nullable=False),
        sa.Column('metric_name', sa.String(length=128), nullable=False),
        sa.Column('baseline_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('target_value', sa.Float(), nullable=False, server_default='0.2'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DRAFTED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_hypotheses_workspace_id'), 'innovation_hypotheses', ['workspace_id'], unique=False)
    op.create_index(op.f('ix_innovation_hypotheses_idea_id'), 'innovation_hypotheses', ['idea_id'], unique=False)

    # 6. innovation_assumptions
    op.create_table(
        'innovation_assumptions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('hypothesis_id', sa.String(length=64), sa.ForeignKey('innovation_hypotheses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assumption_text', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False, server_default='CUSTOMER'),
        sa.Column('impact_level', sa.String(length=16), nullable=False, server_default='HIGH'),
        sa.Column('uncertainty_level', sa.String(length=16), nullable=False, server_default='HIGH'),
        sa.Column('validation_priority', sa.String(length=32), nullable=False, server_default='CRITICAL'),
        sa.Column('is_validated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_assumptions_hypothesis_id'), 'innovation_assumptions', ['hypothesis_id'], unique=False)

    # 7. innovation_experiments
    op.create_table(
        'innovation_experiments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('hypothesis_id', sa.String(length=64), sa.ForeignKey('innovation_hypotheses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('experiment_type', sa.String(length=64), nullable=False, server_default='PROTOTYPE'),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('target_population', sa.String(length=255), nullable=True),
        sa.Column('sample_size', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('duration_days', sa.Integer(), nullable=False, server_default='14'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DESIGNED'),
        sa.Column('risk_review_passed', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('governance_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('statistical_method', sa.String(length=64), nullable=False, server_default='TWO_SAMPLE_T_TEST'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_experiments_workspace_id'), 'innovation_experiments', ['workspace_id'], unique=False)
    op.create_index(op.f('ix_innovation_experiments_hypothesis_id'), 'innovation_experiments', ['hypothesis_id'], unique=False)

    # 8. innovation_experiment_results
    op.create_table(
        'innovation_experiment_results',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('experiment_id', sa.String(length=64), sa.ForeignKey('innovation_experiments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('observed_sample_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('control_mean', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('treatment_mean', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('delta_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p_value', sa.Float(), nullable=True),
        sa.Column('is_statistically_significant', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('conclusion', sa.String(length=32), nullable=False, server_default='SUPPORTED'),
        sa.Column('limitations', sa.Text(), nullable=True),
        sa.Column('raw_data_summary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_experiment_results_experiment_id'), 'innovation_experiment_results', ['experiment_id'], unique=False)

    # 9. innovation_learnings
    op.create_table(
        'innovation_learnings',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), nullable=False),
        sa.Column('hypothesis_id', sa.String(length=64), nullable=True),
        sa.Column('experiment_id', sa.String(length=64), nullable=True),
        sa.Column('insight_statement', sa.Text(), nullable=False),
        sa.Column('evidence_summary', sa.Text(), nullable=False),
        sa.Column('strategic_implication', sa.Text(), nullable=True),
        sa.Column('recorded_at_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_learnings_workspace_id'), 'innovation_learnings', ['workspace_id'], unique=False)

    # 10. innovation_product_concepts
    op.create_table(
        'innovation_product_concepts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('idea_id', sa.String(length=64), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('target_customer_persona', sa.String(length=255), nullable=False),
        sa.Column('value_proposition', sa.Text(), nullable=False),
        sa.Column('core_features', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('differentiators', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('business_model_type', sa.String(length=64), nullable=False, server_default='SUBSCRIPTION'),
        sa.Column('technical_architecture_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_product_concepts_workspace_id'), 'innovation_product_concepts', ['workspace_id'], unique=False)

    # 11. innovation_service_concepts
    op.create_table(
        'innovation_service_concepts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('idea_id', sa.String(length=64), nullable=True),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('target_client_profile', sa.String(length=255), nullable=False),
        sa.Column('service_deliverables', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('delivery_model', sa.String(length=64), nullable=False, server_default='HYBRID_AI_HUMAN'),
        sa.Column('pricing_model', sa.String(length=64), nullable=False, server_default='MONTHLY_RETAINER'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_service_concepts_workspace_id'), 'innovation_service_concepts', ['workspace_id'], unique=False)

    # 12. innovation_business_cases
    op.create_table(
        'innovation_business_cases',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('concept_id', sa.String(length=64), nullable=False),
        sa.Column('target_tam_usd', sa.Float(), nullable=False, server_default='1000000.0'),
        sa.Column('projected_year1_revenue_usd', sa.Float(), nullable=False, server_default='250000.0'),
        sa.Column('estimated_development_cost_usd', sa.Float(), nullable=False, server_default='50000.0'),
        sa.Column('estimated_cac_usd', sa.Float(), nullable=False, server_default='1200.0'),
        sa.Column('estimated_ltv_usd', sa.Float(), nullable=False, server_default='7200.0'),
        sa.Column('payback_months', sa.Float(), nullable=False, server_default='4.5'),
        sa.Column('break_even_customers_count', sa.Integer(), nullable=False, server_default='25'),
        sa.Column('gross_margin_percentage', sa.Float(), nullable=False, server_default='82.0'),
        sa.Column('recommendation', sa.String(length=32), nullable=False, server_default='PROCEED_TO_MVP'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_business_cases_workspace_id'), 'innovation_business_cases', ['workspace_id'], unique=False)

    # 13. innovation_economics
    op.create_table(
        'innovation_economics',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('concept_id', sa.String(length=64), nullable=False),
        sa.Column('price_per_unit_usd', sa.Float(), nullable=False, server_default='199.0'),
        sa.Column('direct_labor_cost_usd', sa.Float(), nullable=False, server_default='20.0'),
        sa.Column('ai_compute_cost_usd', sa.Float(), nullable=False, server_default='12.5'),
        sa.Column('infrastructure_cost_usd', sa.Float(), nullable=False, server_default='8.0'),
        sa.Column('gross_profit_per_unit_usd', sa.Float(), nullable=False, server_default='158.5'),
        sa.Column('gross_margin_percentage', sa.Float(), nullable=False, server_default='79.6'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_economics_concept_id'), 'innovation_economics', ['concept_id'], unique=False)

    # 14. innovation_prototypes
    op.create_table(
        'innovation_prototypes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('concept_id', sa.String(length=64), nullable=False),
        sa.Column('prototype_name', sa.String(length=255), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=False, server_default='v0.1'),
        sa.Column('prototype_url_or_repo', sa.String(length=255), nullable=True),
        sa.Column('user_feedback_summary', sa.Text(), nullable=True),
        sa.Column('usability_score', sa.Float(), nullable=False, server_default='8.5'),
        sa.Column('iteration_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_prototypes_concept_id'), 'innovation_prototypes', ['concept_id'], unique=False)

    # 15. innovation_prds
    op.create_table(
        'innovation_prds',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('concept_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('problem_summary', sa.Text(), nullable=False),
        sa.Column('target_personas', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('user_stories', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('functional_requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('non_functional_requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('security_privacy_requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('success_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('human_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_prds_concept_id'), 'innovation_prds', ['concept_id'], unique=False)

    # 16. innovation_gate_reviews
    op.create_table(
        'innovation_gate_reviews',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('innovation_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('gate_stage', sa.String(length=32), nullable=False),
        sa.Column('reviewer_id', sa.String(length=128), nullable=False),
        sa.Column('evidence_completeness_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('decision', sa.String(length=32), nullable=False, server_default='PENDING'),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('decision_timestamp', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_innovation_gate_reviews_workspace_id'), 'innovation_gate_reviews', ['workspace_id'], unique=False)

    # 17. innovation_portfolios
    op.create_table(
        'innovation_portfolios',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('portfolio_name', sa.String(length=255), nullable=False),
        sa.Column('horizon_1_budget_percentage', sa.Float(), nullable=False, server_default='70.0'),
        sa.Column('horizon_2_budget_percentage', sa.Float(), nullable=False, server_default='20.0'),
        sa.Column('horizon_3_budget_percentage', sa.Float(), nullable=False, server_default='10.0'),
        sa.Column('total_active_initiatives', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('portfolio_expected_roi', sa.Float(), nullable=False, server_default='3.4'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('innovation_portfolios')
    op.drop_table('innovation_gate_reviews')
    op.drop_table('innovation_prds')
    op.drop_table('innovation_prototypes')
    op.drop_table('innovation_economics')
    op.drop_table('innovation_business_cases')
    op.drop_table('innovation_service_concepts')
    op.drop_table('innovation_product_concepts')
    op.drop_table('innovation_learnings')
    op.drop_table('innovation_experiment_results')
    op.drop_table('innovation_experiments')
    op.drop_table('innovation_assumptions')
    op.drop_table('innovation_hypotheses')
    op.drop_table('innovation_ideas')
    op.drop_table('innovation_opportunities')
    op.drop_table('innovation_problems')
    op.drop_table('innovation_workspaces')
