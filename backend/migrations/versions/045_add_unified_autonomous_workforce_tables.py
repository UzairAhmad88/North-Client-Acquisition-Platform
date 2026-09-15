"""add unified autonomous workforce tables

Revision ID: 045
Revises: 044
Create Date: 2026-09-10 02:22:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '045'
down_revision = '044'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. ai_workers
    op.create_table(
        'ai_workers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('worker_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('role', sa.String(length=64), nullable=False),
        sa.Column('specialization', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ACTIVE'),
        sa.Column('supervision_level', sa.Integer(), nullable=False, server_default='2'),
        sa.Column('agent_version', sa.String(length=32), nullable=False, server_default='1.0'),
        sa.Column('model_name', sa.String(length=64), nullable=False, server_default='gemini-1.5-pro'),
        sa.Column('owner', sa.String(length=64), nullable=False, server_default='system_admin'),
        sa.Column('capabilities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('tool_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('knowledge_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('permission_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('budget_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('communication_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('total_tasks_completed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_tasks_failed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_cost_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('average_latency_seconds', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('grounding_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_workers_worker_code', 'ai_workers', ['worker_code'], unique=True)
    op.create_index('ix_ai_workers_org_id', 'ai_workers', ['organization_id'])
    op.create_index('ix_ai_workers_specialization', 'ai_workers', ['specialization'])
    op.create_index('ix_ai_workers_status', 'ai_workers', ['status'])

    # 2. ai_departments
    op.create_table(
        'ai_departments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('department_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('head_worker_code', sa.String(length=64), nullable=True),
        sa.Column('monthly_budget_usd', sa.Float(), nullable=False, server_default='500.0'),
        sa.Column('current_spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_departments_code', 'ai_departments', ['department_code'], unique=True)
    op.create_index('ix_ai_departments_org', 'ai_departments', ['organization_id'])

    # 3. ai_teams
    op.create_table(
        'ai_teams',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('team_code', sa.String(length=64), nullable=False),
        sa.Column('department_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('purpose', sa.Text(), nullable=True),
        sa.Column('manager_worker_code', sa.String(length=64), nullable=True),
        sa.Column('workflow_template', sa.String(length=64), nullable=False, server_default='PARALLEL_REVIEW'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='ACTIVE'),
        sa.Column('budget_limit_usd', sa.Float(), nullable=False, server_default='150.0'),
        sa.Column('current_spend_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_teams_code', 'ai_teams', ['team_code'], unique=True)
    op.create_index('ix_ai_teams_dept', 'ai_teams', ['department_code'])
    op.create_index('ix_ai_teams_org', 'ai_teams', ['organization_id'])

    # 4. ai_team_members
    op.create_table(
        'ai_team_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('team_code', sa.String(length=64), nullable=False),
        sa.Column('worker_code', sa.String(length=64), nullable=False),
        sa.Column('role_in_team', sa.String(length=64), nullable=False, server_default='SPECIALIST'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_team_members_team', 'ai_team_members', ['team_code'])
    op.create_index('ix_ai_team_members_worker', 'ai_team_members', ['worker_code'])

    # 5. ai_work_tasks
    op.create_table(
        'ai_work_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('parent_task_code', sa.String(length=64), nullable=True),
        sa.Column('objective', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('worker_code', sa.String(length=64), nullable=True),
        sa.Column('team_code', sa.String(length=64), nullable=True),
        sa.Column('priority', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='CREATED'),
        sa.Column('supervision_level', sa.Integer(), nullable=False, server_default='2'),
        sa.Column('risk_level', sa.String(length=32), nullable=False, server_default='LOW'),
        sa.Column('inputs', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('result_summary', sa.Text(), nullable=True),
        sa.Column('result_artifacts', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('evidence', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('assumptions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('cost_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('token_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('runtime_seconds', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_ai_work_tasks_code', 'ai_work_tasks', ['task_code'], unique=True)
    op.create_index('ix_ai_work_tasks_org', 'ai_work_tasks', ['organization_id'])
    op.create_index('ix_ai_work_tasks_worker', 'ai_work_tasks', ['worker_code'])
    op.create_index('ix_ai_work_tasks_status', 'ai_work_tasks', ['status'])

    # 6. ai_work_task_dependencies
    op.create_table(
        'ai_work_task_dependencies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('predecessor_task_code', sa.String(length=64), nullable=False),
        sa.Column('successor_task_code', sa.String(length=64), nullable=False),
        sa.Column('is_hard_dependency', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_task_deps_pred', 'ai_work_task_dependencies', ['predecessor_task_code'])
    op.create_index('ix_task_deps_succ', 'ai_work_task_dependencies', ['successor_task_code'])

    # 7. ai_handoffs
    op.create_table(
        'ai_handoffs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('handoff_code', sa.String(length=64), nullable=False),
        sa.Column('from_worker_code', sa.String(length=64), nullable=False),
        sa.Column('to_worker_code', sa.String(length=64), nullable=False),
        sa.Column('task_code', sa.String(length=64), nullable=False),
        sa.Column('context_summary', sa.Text(), nullable=False),
        sa.Column('artifacts', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('evidence', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('assumptions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('unknowns', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('expected_next_action', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DELIVERED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_handoffs_code', 'ai_handoffs', ['handoff_code'], unique=True)
    op.create_index('ix_ai_handoffs_task', 'ai_handoffs', ['task_code'])

    # 8. ai_consensus_runs
    op.create_table(
        'ai_consensus_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('consensus_code', sa.String(length=64), nullable=False),
        sa.Column('topic', sa.String(length=256), nullable=False),
        sa.Column('participating_workers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('worker_opinions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('consensus_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('has_conflicts', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('synthesized_conclusion', sa.Text(), nullable=False),
        sa.Column('dissenting_views', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_consensus_code', 'ai_consensus_runs', ['consensus_code'], unique=True)

    # 9. ai_review_runs
    op.create_table(
        'ai_review_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('review_code', sa.String(length=64), nullable=False),
        sa.Column('target_task_code', sa.String(length=64), nullable=False),
        sa.Column('author_worker_code', sa.String(length=64), nullable=False),
        sa.Column('critic_worker_code', sa.String(length=64), nullable=False),
        sa.Column('review_type', sa.String(length=64), nullable=False, server_default='FACT_AND_RISK'),
        sa.Column('critique_summary', sa.Text(), nullable=False),
        sa.Column('findings', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('quality_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('is_approved_by_critic', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_reviews_code', 'ai_review_runs', ['review_code'], unique=True)
    op.create_index('ix_ai_reviews_task', 'ai_review_runs', ['target_task_code'])

    # 10. ai_worker_budgets
    op.create_table(
        'ai_worker_budgets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('worker_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('period_end', sa.DateTime(timezone=True), nullable=False),
        sa.Column('daily_cost_limit_usd', sa.Float(), nullable=False, server_default='10.0'),
        sa.Column('daily_cost_spent_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('monthly_cost_limit_usd', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('monthly_cost_spent_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_exceeded', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_worker_budgets_worker', 'ai_worker_budgets', ['worker_code'])
    op.create_index('ix_worker_budgets_org', 'ai_worker_budgets', ['organization_id'])

    # 11. ai_worker_metrics
    op.create_table(
        'ai_worker_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('worker_code', sa.String(length=64), nullable=False),
        sa.Column('period', sa.String(length=32), nullable=False, server_default='CURRENT_WEEK'),
        sa.Column('task_success_rate', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('factuality_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('grounding_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('policy_compliance_rate', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('human_override_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('average_latency_sec', sa.Float(), nullable=False, server_default='1.5'),
        sa.Column('total_tokens_consumed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_worker_metrics_worker', 'ai_worker_metrics', ['worker_code'])

    # 12. ai_workforce_plans
    op.create_table(
        'ai_workforce_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('plan_code', sa.String(length=64), nullable=False),
        sa.Column('organization_id', sa.String(length=64), nullable=False),
        sa.Column('strategic_objective_id', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('required_departments', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('required_workers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('estimated_monthly_cost_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('estimated_human_hours_saved', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_workforce_plans_code', 'ai_workforce_plans', ['plan_code'], unique=True)
    op.create_index('ix_workforce_plans_org', 'ai_workforce_plans', ['organization_id'])


def downgrade() -> None:
    op.drop_table('ai_workforce_plans')
    op.drop_table('ai_worker_metrics')
    op.drop_table('ai_worker_budgets')
    op.drop_table('ai_review_runs')
    op.drop_table('ai_consensus_runs')
    op.drop_table('ai_handoffs')
    op.drop_table('ai_work_task_dependencies')
    op.drop_table('ai_work_tasks')
    op.drop_table('ai_team_members')
    op.drop_table('ai_teams')
    op.drop_table('ai_departments')
    op.drop_table('ai_workers')
