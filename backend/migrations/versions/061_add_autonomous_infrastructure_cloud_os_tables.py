"""add_autonomous_infrastructure_cloud_os_tables

Revision ID: 061
Revises: 060
Create Date: 2026-09-13 22:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '061'
down_revision = '060'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'infra_cloud_accounts',
        'infra_regions',
        'infra_resources',
        'infra_resource_relationships',
        'infra_compute',
        'infra_storage',
        'infra_networks',
        'infra_databases',
        'infra_clusters',
        'infra_nodes',
        'infra_workloads',
        'infra_pods',
        'infra_scaling_policies',
        'infra_scaling_events',
        'infra_capacity_forecasts',
        'infra_gpu_workloads',
        'infra_cost_allocations',
        'infra_budgets',
        'infra_cost_anomalies',
        'infra_savings',
        'infra_drift',
        'infra_changes',
        'infra_restore_tests',
        'infra_dr_plans',
        'infra_agent_runs',
        'infra_agent_approvals',
        'infra_audit_events'
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
        'infra_audit_events',
        'infra_agent_approvals',
        'infra_agent_runs',
        'infra_dr_plans',
        'infra_restore_tests',
        'infra_changes',
        'infra_drift',
        'infra_savings',
        'infra_cost_anomalies',
        'infra_budgets',
        'infra_cost_allocations',
        'infra_gpu_workloads',
        'infra_capacity_forecasts',
        'infra_scaling_events',
        'infra_scaling_policies',
        'infra_pods',
        'infra_workloads',
        'infra_nodes',
        'infra_clusters',
        'infra_databases',
        'infra_networks',
        'infra_storage',
        'infra_compute',
        'infra_resource_relationships',
        'infra_resources',
        'infra_regions',
        'infra_cloud_accounts'
    ]
    for tbl in tables:
        op.drop_table(tbl)
