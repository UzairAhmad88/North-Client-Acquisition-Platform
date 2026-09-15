"""add_enterprise_global_operations_orchestration_tables

Revision ID: 067
Revises: 066
Create Date: 2026-09-14 03:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '067'
down_revision = '066'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'ops_locations',
        'ops_facilities',
        'ops_demand',
        'ops_forecasts',
        'ops_supply_plans',
        'ops_suppliers',
        'ops_sourcing_events',
        'ops_purchase_orders',
        'ops_goods_receipts',
        'ops_inventory_items',
        'ops_warehouses',
        'ops_orders',
        'ops_shipments',
        'ops_vehicles',
        'ops_workforce_capacity',
        'ops_schedules',
        'ops_production_orders',
        'ops_quality_events',
        'ops_assets',
        'ops_digital_twin_nodes',
        'ops_simulations',
        'ops_exceptions',
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
        'ops_locations',
        'ops_facilities',
        'ops_demand',
        'ops_forecasts',
        'ops_supply_plans',
        'ops_suppliers',
        'ops_sourcing_events',
        'ops_purchase_orders',
        'ops_goods_receipts',
        'ops_inventory_items',
        'ops_warehouses',
        'ops_orders',
        'ops_shipments',
        'ops_vehicles',
        'ops_workforce_capacity',
        'ops_schedules',
        'ops_production_orders',
        'ops_quality_events',
        'ops_assets',
        'ops_digital_twin_nodes',
        'ops_simulations',
        'ops_exceptions',
    ]
    for table in reversed(tables):
        op.drop_table(table)
