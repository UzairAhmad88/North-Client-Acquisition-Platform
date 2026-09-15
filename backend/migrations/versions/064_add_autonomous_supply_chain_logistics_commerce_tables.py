"""add_autonomous_supply_chain_logistics_commerce_tables

Revision ID: 064
Revises: 063
Create Date: 2026-09-13 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '064'
down_revision = '063'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'sc_suppliers',
        'sc_supplier_contracts',
        'sc_products',
        'sc_bill_of_materials',
        'sc_purchase_orders',
        'sc_inventory_items',
        'sc_inventory_movements',
        'sc_demand_forecasts',
        'sc_warehouses',
        'sc_pick_tasks',
        'sc_carriers',
        'sc_vehicles',
        'sc_shipments',
        'sc_sales_orders',
        'sc_return_requests',
        'sc_disruptions',
        'sc_digital_twins',
        'sc_agent_runs',
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
            op.create_index(f'ix_{tbl}_tenant_id', tbl, ['tenant_id'], unique=False)

def downgrade():
    tables = [
        'sc_suppliers',
        'sc_supplier_contracts',
        'sc_products',
        'sc_bill_of_materials',
        'sc_purchase_orders',
        'sc_inventory_items',
        'sc_inventory_movements',
        'sc_demand_forecasts',
        'sc_warehouses',
        'sc_pick_tasks',
        'sc_carriers',
        'sc_vehicles',
        'sc_shipments',
        'sc_sales_orders',
        'sc_return_requests',
        'sc_disruptions',
        'sc_digital_twins',
        'sc_agent_runs',
    ]
    for tbl in tables:
        op.drop_table(tbl)
