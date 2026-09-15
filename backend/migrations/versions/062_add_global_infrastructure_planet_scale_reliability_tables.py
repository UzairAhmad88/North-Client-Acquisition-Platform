"""add_global_infrastructure_planet_scale_reliability_tables

Revision ID: 062
Revises: 061
Create Date: 2026-09-13 22:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '062'
down_revision = '061'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'global_locations',
        'global_regions',
        'global_data_centers',
        'global_racks',
        'global_hardware_assets',
        'global_hardware_health',
        'global_edge_locations',
        'global_edge_nodes',
        'global_edge_workloads',
        'global_device_fleets',
        'global_device_updates',
        'global_network_paths',
        'global_traffic_metrics',
        'global_routing_policies',
        'global_dns_zones',
        'global_cdn_edges',
        'global_service_topologies',
        'global_latency_telemetry',
        'global_capacity',
        'global_workload_placements',
        'global_workload_migrations',
        'global_replication_states',
        'global_partition_events',
        'global_disaster_recovery_plans',
        'global_failover_events',
        'global_chaos_experiments',
        'global_incident_records',
        'global_root_cause_analysis',
        'global_digital_twins',
        'global_audit_events'
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
        'global_audit_events',
        'global_digital_twins',
        'global_root_cause_analysis',
        'global_incident_records',
        'global_chaos_experiments',
        'global_failover_events',
        'global_disaster_recovery_plans',
        'global_partition_events',
        'global_replication_states',
        'global_workload_migrations',
        'global_workload_placements',
        'global_capacity',
        'global_latency_telemetry',
        'global_service_topologies',
        'global_cdn_edges',
        'global_dns_zones',
        'global_routing_policies',
        'global_traffic_metrics',
        'global_network_paths',
        'global_device_updates',
        'global_device_fleets',
        'global_edge_workloads',
        'global_edge_nodes',
        'global_edge_locations',
        'global_hardware_health',
        'global_hardware_assets',
        'global_racks',
        'global_data_centers',
        'global_regions',
        'global_locations'
    ]
    for tbl in tables:
        op.drop_table(tbl)
