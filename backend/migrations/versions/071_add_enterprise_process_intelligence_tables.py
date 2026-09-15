"""add_enterprise_process_intelligence_tables

Revision ID: 071
Revises: 070
Create Date: 2026-09-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '071'
down_revision = '070'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'epi_process_catalog',
        'epi_process_versions',
        'epi_process_hierarchies',
        'epi_value_streams',
        'epi_event_logs',
        'epi_process_events',
        'epi_process_cases',
        'epi_process_case_events',
        'epi_process_models',
        'epi_process_model_versions',
        'epi_process_model_nodes',
        'epi_process_model_edges',
        'epi_process_variants',
        'epi_process_variant_metrics',
        'epi_conformance_runs',
        'epi_conformance_results',
        'epi_performance_metrics',
        'epi_bottlenecks',
        'epi_root_causes',
        'epi_process_waste',
        'epi_activity_costs',
        'epi_process_costs',
        'epi_process_slas',
        'epi_sla_events',
        'epi_sla_predictions',
        'epi_process_risks',
        'epi_process_controls',
        'epi_process_control_executions',
        'epi_sod_violations',
        'epi_process_simulations',
        'epi_process_simulation_runs',
        'epi_process_simulation_results',
        'epi_process_optimizations',
        'epi_process_optimization_runs',
        'epi_process_optimization_results',
        'epi_automation_opportunities',
        'epi_automation_scores',
        'epi_automation_roi',
        'epi_process_change_requests',
        'epi_process_change_approvals',
        'epi_process_change_deployments',
        'epi_process_change_rollbacks',
        'epi_process_dependencies',
        'epi_process_criticality',
        'epi_process_resilience',
        'epi_process_anomalies',
        'epi_process_drift_events',
        'epi_process_alerts',
        'epi_process_lessons',
        'epi_process_benchmarks',
        'epi_process_kpis',
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
        'epi_process_catalog',
        'epi_process_versions',
        'epi_process_hierarchies',
        'epi_value_streams',
        'epi_event_logs',
        'epi_process_events',
        'epi_process_cases',
        'epi_process_case_events',
        'epi_process_models',
        'epi_process_model_versions',
        'epi_process_model_nodes',
        'epi_process_model_edges',
        'epi_process_variants',
        'epi_process_variant_metrics',
        'epi_conformance_runs',
        'epi_conformance_results',
        'epi_performance_metrics',
        'epi_bottlenecks',
        'epi_root_causes',
        'epi_process_waste',
        'epi_activity_costs',
        'epi_process_costs',
        'epi_process_slas',
        'epi_sla_events',
        'epi_sla_predictions',
        'epi_process_risks',
        'epi_process_controls',
        'epi_process_control_executions',
        'epi_sod_violations',
        'epi_process_simulations',
        'epi_process_simulation_runs',
        'epi_process_simulation_results',
        'epi_process_optimizations',
        'epi_process_optimization_runs',
        'epi_process_optimization_results',
        'epi_automation_opportunities',
        'epi_automation_scores',
        'epi_automation_roi',
        'epi_process_change_requests',
        'epi_process_change_approvals',
        'epi_process_change_deployments',
        'epi_process_change_rollbacks',
        'epi_process_dependencies',
        'epi_process_criticality',
        'epi_process_resilience',
        'epi_process_anomalies',
        'epi_process_drift_events',
        'epi_process_alerts',
        'epi_process_lessons',
        'epi_process_benchmarks',
        'epi_process_kpis',
    ]

    for table in tables:
        op.drop_table(table)
