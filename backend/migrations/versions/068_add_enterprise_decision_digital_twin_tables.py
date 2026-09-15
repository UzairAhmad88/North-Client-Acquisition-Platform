"""add_enterprise_decision_digital_twin_tables

Revision ID: 068
Revises: 067
Create Date: 2026-09-14 03:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '068'
down_revision = '067'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'dtwin_entities',
        'dtwin_relationships',
        'dtwin_models',
        'dtwin_forecasts',
        'dtwin_scenarios',
        'dtwin_simulations',
        'dtwin_optimizations',
        'dtwin_decision_records',
        'dtwin_okrs',
        'dtwin_early_warnings',
        'dtwin_crisis_cases',
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
        'dtwin_entities',
        'dtwin_relationships',
        'dtwin_models',
        'dtwin_forecasts',
        'dtwin_scenarios',
        'dtwin_simulations',
        'dtwin_optimizations',
        'dtwin_decision_records',
        'dtwin_okrs',
        'dtwin_early_warnings',
        'dtwin_crisis_cases',
    ]
    for table in reversed(tables):
        op.drop_table(table)
