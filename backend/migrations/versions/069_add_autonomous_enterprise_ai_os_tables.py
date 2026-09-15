"""add_autonomous_enterprise_ai_os_tables

Revision ID: 069
Revises: 068
Create Date: 2026-09-14 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '069'
down_revision = '068'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'aeai_agents',
        'aeai_agent_versions',
        'aeai_tasks',
        'aeai_subtasks',
        'aeai_workflows',
        'aeai_tool_registry',
        'aeai_memory_items',
        'aeai_knowledge_sources',
        'aeai_plans',
        'aeai_approvals',
        'aeai_policy_rules',
        'aeai_agent_incidents',
        'aeai_action_limits',
        'aeai_kill_switch_events',
        'aeai_roi_metrics',
    ]

    for table in tables:
        if table not in existing_tables:
            op.create_table(
                table,
                sa.Column('id', sa.String(length=64), nullable=False),
                sa.Column('tenant_id', sa.String(length=64), nullable=False, server_default='tenant-default'),
                sa.Column('code', sa.String(length=64), nullable=True),
                sa.Column('name', sa.String(length=255), nullable=True),
                sa.Column('status', sa.String(length=32), nullable=True),
                sa.Column('meta_data', sa.JSON(), nullable=True),
                sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.DateTime(), nullable=True),
                sa.PrimaryKeyConstraint('id')
            )
            op.create_index(f'ix_{table}_tenant_id', table, ['tenant_id'])

def downgrade():
    tables = [
        'aeai_agents',
        'aeai_agent_versions',
        'aeai_tasks',
        'aeai_subtasks',
        'aeai_workflows',
        'aeai_tool_registry',
        'aeai_memory_items',
        'aeai_knowledge_sources',
        'aeai_plans',
        'aeai_approvals',
        'aeai_policy_rules',
        'aeai_agent_incidents',
        'aeai_action_limits',
        'aeai_kill_switch_events',
        'aeai_roi_metrics',
    ]

    for table in reversed(tables):
        op.drop_table(table)
