"""add_cyber_physical_systems_iot_robotics_tables

Revision ID: 063
Revises: 062
Create Date: 2026-09-13 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '063'
down_revision = '062'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'cps_facilities',
        'cps_zones',
        'cps_assets',
        'cps_asset_relationships',
        'cps_devices',
        'cps_device_identity',
        'cps_device_shadow',
        'cps_sensors',
        'cps_sensor_readings',
        'cps_actuators',
        'cps_commands',
        'cps_robots',
        'cps_robot_missions',
        'cps_machine_health',
        'cps_maintenance',
        'cps_spare_parts',
        'cps_energy',
        'cps_digital_twins',
        'cps_twin_simulations',
        'cps_safety_policies',
        'cps_safety_events',
        'cps_field_operations',
        'cps_agent_runs'
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
        'cps_facilities',
        'cps_zones',
        'cps_assets',
        'cps_asset_relationships',
        'cps_devices',
        'cps_device_identity',
        'cps_device_shadow',
        'cps_sensors',
        'cps_sensor_readings',
        'cps_actuators',
        'cps_commands',
        'cps_robots',
        'cps_robot_missions',
        'cps_machine_health',
        'cps_maintenance',
        'cps_spare_parts',
        'cps_energy',
        'cps_digital_twins',
        'cps_twin_simulations',
        'cps_safety_policies',
        'cps_safety_events',
        'cps_field_operations',
        'cps_agent_runs'
    ]
    for tbl in tables:
        op.drop_table(tbl)
