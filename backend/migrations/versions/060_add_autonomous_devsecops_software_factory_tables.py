"""add_autonomous_devsecops_software_factory_tables

Revision ID: 060
Revises: 059
Create Date: 2026-09-13 22:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '060'
down_revision = '059'
branch_labels = None
depends_on = None

def upgrade():
    # Helper to check if table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'dsops_factory_projects',
        'dsops_repositories',
        'dsops_codebase_graphs',
        'dsops_engineering_agents',
        'dsops_agent_approvals',
        'dsops_task_plans',
        'dsops_review_findings',
        'dsops_test_intelligence',
        'dsops_pipelines',
        'dsops_builds',
        'dsops_artifacts',
        'dsops_releases',
        'dsops_deployments',
        'dsops_environments',
        'dsops_services',
        'dsops_slos',
        'dsops_incidents',
        'dsops_runbooks',
        'dsops_technical_debt',
        'dsops_dora_metrics',
        'dsops_audit_events'
    ]

    for tbl in tables:
        if tbl not in existing_tables:
            op.create_table(
                tbl,
                sa.Column('id', sa.String(length=64), nullable=False),
                sa.Column('tenant_id', sa.String(length=64), nullable=False),
                sa.Column('created_at', sa.DateTime(), nullable=True),
                sa.PrimaryKeyConstraint('id')
            )
            op.create_index(f'ix_{tbl}_id', tbl, ['id'], unique=False)
            op.create_index(f'ix_{tbl}_tenant_id', tbl, ['tenant_id'], unique=False)

def downgrade():
    tables = [
        'dsops_audit_events',
        'dsops_dora_metrics',
        'dsops_technical_debt',
        'dsops_runbooks',
        'dsops_incidents',
        'dsops_slos',
        'dsops_services',
        'dsops_environments',
        'dsops_deployments',
        'dsops_releases',
        'dsops_artifacts',
        'dsops_builds',
        'dsops_pipelines',
        'dsops_test_intelligence',
        'dsops_review_findings',
        'dsops_task_plans',
        'dsops_agent_approvals',
        'dsops_engineering_agents',
        'dsops_codebase_graphs',
        'dsops_repositories',
        'dsops_factory_projects'
    ]
    for tbl in tables:
        op.drop_table(tbl)
