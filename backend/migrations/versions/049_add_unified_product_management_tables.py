"""add unified product management tables

Revision ID: 049
Revises: 048
Create Date: 2026-09-10 03:22:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '049'
down_revision = '048'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. products
    op.create_table(
        'products',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('product_type', sa.String(length=64), nullable=False, server_default='SOFTWARE_PRODUCT'),
        sa.Column('lifecycle_stage', sa.String(length=64), nullable=False, server_default='DISCOVERY'),
        sa.Column('owner_id', sa.String(length=128), nullable=False),
        sa.Column('team_name', sa.String(length=128), nullable=True),
        sa.Column('vision_statement', sa.Text(), nullable=True),
        sa.Column('target_market', sa.String(length=255), nullable=True),
        sa.Column('customer_segments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('north_star_metric', sa.String(length=255), nullable=True),
        sa.Column('health_status', sa.String(length=32), nullable=False, server_default='HEALTHY'),
        sa.Column('health_score', sa.Float(), nullable=False, server_default='0.88'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ACTIVE'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. product_objectives
    op.create_table(
        'product_objectives',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('metric_name', sa.String(length=128), nullable=False),
        sa.Column('baseline_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('target_value', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('current_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('unit', sa.String(length=32), nullable=True, server_default='%'),
        sa.Column('time_window', sa.String(length=64), nullable=True, server_default='Q3 2026'),
        sa.Column('owner_id', sa.String(length=128), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ON_TRACK'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_objectives_product_id'), 'product_objectives', ['product_id'], unique=False)

    # 3. product_metrics
    op.create_table(
        'product_metrics',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False, server_default='ENGAGEMENT'),
        sa.Column('definition', sa.Text(), nullable=True),
        sa.Column('formula', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=128), nullable=True),
        sa.Column('current_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('target_value', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=32), nullable=True, server_default='count'),
        sa.Column('time_window', sa.String(length=64), nullable=True, server_default='30d'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_metrics_product_id'), 'product_metrics', ['product_id'], unique=False)

    # 4. product_feedback
    op.create_table(
        'product_feedback',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source', sa.String(length=64), nullable=False, server_default='CLIENT'),
        sa.Column('feedback_type', sa.String(length=64), nullable=False, server_default='FEATURE_REQUEST'),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('customer_segment', sa.String(length=128), nullable=True),
        sa.Column('revenue_impact_usd', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('sentiment_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('theme_cluster', sa.String(length=128), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='NEW'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_feedback_product_id'), 'product_feedback', ['product_id'], unique=False)

    # 5. product_requirements
    op.create_table(
        'product_requirements',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('requirement_code', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False, server_default='FUNCTIONAL'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(length=32), nullable=False, server_default='HIGH'),
        sa.Column('acceptance_criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('source_evidence', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('dependencies', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('linked_problem_id', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DRAFT'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_requirements_product_id'), 'product_requirements', ['product_id'], unique=False)

    # 6. product_epics
    op.create_table(
        'product_epics',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('target_release_id', sa.String(length=64), nullable=True),
        sa.Column('business_value_score', sa.Float(), nullable=False, server_default='8.0'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PLANNED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_epics_product_id'), 'product_epics', ['product_id'], unique=False)

    # 7. product_features
    op.create_table(
        'product_features',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('epic_id', sa.String(length=64), sa.ForeignKey('product_epics.id', ondelete='CASCADE'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_story', sa.Text(), nullable=True),
        sa.Column('acceptance_criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('effort_points', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('priority', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='READY'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_features_product_id'), 'product_features', ['product_id'], unique=False)

    # 8. product_backlog_items
    op.create_table(
        'product_backlog_items',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('item_type', sa.String(length=32), nullable=False, server_default='STORY'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('business_value', sa.Float(), nullable=False, server_default='7.0'),
        sa.Column('customer_value', sa.Float(), nullable=False, server_default='7.0'),
        sa.Column('effort_estimate', sa.Float(), nullable=False, server_default='3.0'),
        sa.Column('risk_score', sa.Float(), nullable=False, server_default='2.0'),
        sa.Column('assigned_sprint_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='BACKLOG'),
        sa.Column('assignee_id', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_backlog_items_product_id'), 'product_backlog_items', ['product_id'], unique=False)

    # 9. product_prioritization_scores
    op.create_table(
        'product_prioritization_scores',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('item_id', sa.String(length=64), nullable=False),
        sa.Column('framework', sa.String(length=32), nullable=False, server_default='RICE'),
        sa.Column('score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('formula_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('calculated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_prioritization_scores_item_id'), 'product_prioritization_scores', ['item_id'], unique=False)

    # 10. product_roadmaps
    op.create_table(
        'product_roadmaps',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('scenario_type', sa.String(length=64), nullable=False, server_default='BASE_PLAN'),
        sa.Column('confidence_level', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_roadmaps_product_id'), 'product_roadmaps', ['product_id'], unique=False)

    # 11. product_roadmap_items
    op.create_table(
        'product_roadmap_items',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('roadmap_id', sa.String(length=64), sa.ForeignKey('product_roadmaps.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('horizon', sa.String(length=32), nullable=False, server_default='NOW'),
        sa.Column('theme', sa.String(length=128), nullable=True),
        sa.Column('expected_outcome', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.80'),
        sa.Column('dependencies', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('estimated_weeks', sa.Integer(), nullable=False, server_default='4'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_roadmap_items_roadmap_id'), 'product_roadmap_items', ['roadmap_id'], unique=False)

    # 12. product_capacity_plans
    op.create_table(
        'product_capacity_plans',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), nullable=False),
        sa.Column('engineering_fte', sa.Float(), nullable=False, server_default='4.0'),
        sa.Column('design_fte', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('qa_fte', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('ai_ml_fte', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('devops_fte', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('bottleneck_role', sa.String(length=64), nullable=True),
        sa.Column('utilization_rate', sa.Float(), nullable=False, server_default='0.82'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_capacity_plans_product_id'), 'product_capacity_plans', ['product_id'], unique=False)

    # 13. product_sprints
    op.create_table(
        'product_sprints',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('sprint_goal', sa.Text(), nullable=True),
        sa.Column('capacity_points', sa.Integer(), nullable=False, server_default='40'),
        sa.Column('committed_points', sa.Integer(), nullable=False, server_default='36'),
        sa.Column('completed_points', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PLANNING'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_sprints_product_id'), 'product_sprints', ['product_id'], unique=False)

    # 14. product_releases
    op.create_table(
        'product_releases',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_tag', sa.String(length=64), nullable=False),
        sa.Column('release_name', sa.String(length=255), nullable=False),
        sa.Column('scope_summary', sa.Text(), nullable=True),
        sa.Column('readiness_status', sa.String(length=32), nullable=False, server_default='IN_PROGRESS'),
        sa.Column('readiness_score', sa.Float(), nullable=False, server_default='0.70'),
        sa.Column('critical_defects_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('qa_sign_off', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('security_sign_off', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('rollback_plan', sa.Text(), nullable=True),
        sa.Column('released_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_releases_product_id'), 'product_releases', ['product_id'], unique=False)

    # 15. product_feature_flags
    op.create_table(
        'product_feature_flags',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('flag_key', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('state', sa.String(length=32), nullable=False, server_default='OFF'),
        sa.Column('rollout_percentage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_segments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_feature_flags_product_id'), 'product_feature_flags', ['product_id'], unique=False)

    # 16. product_launches
    op.create_table(
        'product_launches',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('launch_name', sa.String(length=255), nullable=False),
        sa.Column('target_audience', sa.String(length=255), nullable=True),
        sa.Column('value_messaging', sa.Text(), nullable=True),
        sa.Column('checklist_status', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('is_launch_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('approved_by', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PREPARING'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_launches_product_id'), 'product_launches', ['product_id'], unique=False)

    # 17. product_experiments
    op.create_table(
        'product_experiments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('hypothesis', sa.Text(), nullable=False),
        sa.Column('primary_metric', sa.String(length=128), nullable=False),
        sa.Column('guardrail_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('control_variant', sa.String(length=128), nullable=False, server_default='Control'),
        sa.Column('treatment_variants', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('p_value', sa.Float(), nullable=True),
        sa.Column('is_statistically_significant', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='RUNNING'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_experiments_product_id'), 'product_experiments', ['product_id'], unique=False)

    # 18. product_health_records
    op.create_table(
        'product_health_records',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('health_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('adoption_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('satisfaction_score', sa.Float(), nullable=False, server_default='0.90'),
        sa.Column('reliability_score', sa.Float(), nullable=False, server_default='0.99'),
        sa.Column('security_score', sa.Float(), nullable=False, server_default='0.95'),
        sa.Column('delivery_score', sa.Float(), nullable=False, server_default='0.80'),
        sa.Column('health_state', sa.String(length=32), nullable=False, server_default='HEALTHY'),
        sa.Column('findings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_health_records_product_id'), 'product_health_records', ['product_id'], unique=False)

    # 19. product_sunset_plans
    op.create_table(
        'product_sunset_plans',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('product_id', sa.String(length=64), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sunset_reason', sa.Text(), nullable=False),
        sa.Column('migration_target_product_id', sa.String(length=64), nullable=True),
        sa.Column('affected_customers_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('financial_impact_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('deprecation_date', sa.DateTime(), nullable=True),
        sa.Column('sunset_date', sa.DateTime(), nullable=True),
        sa.Column('governance_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ANALYSIS'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_product_sunset_plans_product_id'), 'product_sunset_plans', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_table('product_sunset_plans')
    op.drop_table('product_health_records')
    op.drop_table('product_experiments')
    op.drop_table('product_launches')
    op.drop_table('product_feature_flags')
    op.drop_table('product_releases')
    op.drop_table('product_sprints')
    op.drop_table('product_capacity_plans')
    op.drop_table('product_roadmap_items')
    op.drop_table('product_roadmaps')
    op.drop_table('product_prioritization_scores')
    op.drop_table('product_backlog_items')
    op.drop_table('product_features')
    op.drop_table('product_epics')
    op.drop_table('product_requirements')
    op.drop_table('product_feedback')
    op.drop_table('product_metrics')
    op.drop_table('product_objectives')
    op.drop_table('products')
