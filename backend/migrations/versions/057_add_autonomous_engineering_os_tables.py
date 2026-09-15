"""add autonomous engineering os tables

Revision ID: 057
Revises: 056
Create Date: 2026-09-12 23:28:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '057'
down_revision = '056'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. eng_project_workspaces
    op.create_table(
        'eng_project_workspaces',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('team', sa.String(length=128), nullable=False),
        sa.Column('repository_url', sa.String(length=512), nullable=True),
        sa.Column('tech_stack', sa.JSON(), nullable=True),
        sa.Column('budget_allocated_usd', sa.Float(), nullable=True),
        sa.Column('budget_spent_usd', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. eng_requirements
    op.create_table(
        'eng_requirements',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('eng_project_workspaces.id'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('requirement_type', sa.String(length=64), nullable=True),
        sa.Column('priority', sa.String(length=32), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('ambiguity_score', sa.Float(), nullable=True),
        sa.Column('dependencies', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. eng_acceptance_criteria
    op.create_table(
        'eng_acceptance_criteria',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('requirement_id', sa.String(length=64), sa.ForeignKey('eng_requirements.id'), nullable=False),
        sa.Column('given_clause', sa.Text(), nullable=False),
        sa.Column('when_clause', sa.Text(), nullable=False),
        sa.Column('then_clause', sa.Text(), nullable=False),
        sa.Column('is_automated_test_created', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. eng_architecture_components
    op.create_table(
        'eng_architecture_components',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('eng_project_workspaces.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('component_type', sa.String(length=64), nullable=False),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('runtime_environment', sa.String(length=64), nullable=True),
        sa.Column('slo_target_latency_p95_ms', sa.Float(), nullable=True),
        sa.Column('slo_target_availability_pct', sa.Float(), nullable=True),
        sa.Column('dependencies_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. eng_code_repositories
    op.create_table(
        'eng_code_repositories',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('organization', sa.String(length=128), nullable=True),
        sa.Column('provider', sa.String(length=64), nullable=True),
        sa.Column('default_branch', sa.String(length=64), nullable=True),
        sa.Column('language', sa.String(length=64), nullable=True),
        sa.Column('indexed_files_count', sa.Integer(), nullable=True),
        sa.Column('indexed_symbols_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. eng_code_symbols
    op.create_table(
        'eng_code_symbols',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('repository_id', sa.String(length=64), sa.ForeignKey('eng_code_repositories.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('symbol_type', sa.String(length=64), nullable=True),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('line_start', sa.Integer(), nullable=True),
        sa.Column('line_end', sa.Integer(), nullable=True),
        sa.Column('docstring', sa.Text(), nullable=True),
        sa.Column('called_by_symbols', sa.JSON(), nullable=True),
        sa.Column('calls_symbols', sa.JSON(), nullable=True),
    )

    # 7. eng_tasks
    op.create_table(
        'eng_tasks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('requirement_id', sa.String(length=64), sa.ForeignKey('eng_requirements.id'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('task_type', sa.String(length=64), nullable=True),
        sa.Column('priority', sa.String(length=32), nullable=True),
        sa.Column('assigned_agent', sa.String(length=128), nullable=True),
        sa.Column('assigned_human_reviewer', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('branch_name', sa.String(length=128), nullable=True),
        sa.Column('estimated_tokens', sa.Integer(), nullable=True),
        sa.Column('tokens_consumed', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. eng_agent_coding_sessions
    op.create_table(
        'eng_agent_coding_sessions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('task_id', sa.String(length=64), sa.ForeignKey('eng_tasks.id'), nullable=False),
        sa.Column('agent_id', sa.String(length=64), nullable=True),
        sa.Column('sandbox_workspace_path', sa.String(length=512), nullable=False),
        sa.Column('branch_created', sa.String(length=128), nullable=False),
        sa.Column('files_modified', sa.JSON(), nullable=True),
        sa.Column('diff_stat_additions', sa.Integer(), nullable=True),
        sa.Column('diff_stat_deletions', sa.Integer(), nullable=True),
        sa.Column('unit_tests_passed', sa.Boolean(), nullable=True),
        sa.Column('security_checks_passed', sa.Boolean(), nullable=True),
        sa.Column('generated_pr_id', sa.String(length=64), nullable=True),
        sa.Column('session_cost_usd', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. eng_pull_requests
    op.create_table(
        'eng_pull_requests',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('repository_id', sa.String(length=64), sa.ForeignKey('eng_code_repositories.id'), nullable=False),
        sa.Column('task_id', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('source_branch', sa.String(length=128), nullable=False),
        sa.Column('target_branch', sa.String(length=128), nullable=True),
        sa.Column('author', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('risk_score_composite', sa.Float(), nullable=True),
        sa.Column('risk_breakdown_json', sa.JSON(), nullable=True),
        sa.Column('ci_pipeline_status', sa.String(length=32), nullable=True),
        sa.Column('is_merged', sa.Boolean(), nullable=True),
        sa.Column('merged_by', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 10. eng_ci_pipelines
    op.create_table(
        'eng_ci_pipelines',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('repository_id', sa.String(length=64), sa.ForeignKey('eng_code_repositories.id'), nullable=False),
        sa.Column('pipeline_name', sa.String(length=255), nullable=False),
        sa.Column('trigger_event', sa.String(length=64), nullable=True),
        sa.Column('stages_json', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 11. eng_ci_build_runs
    op.create_table(
        'eng_ci_build_runs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('pipeline_id', sa.String(length=64), sa.ForeignKey('eng_ci_pipelines.id'), nullable=False),
        sa.Column('commit_sha', sa.String(length=64), nullable=False),
        sa.Column('branch', sa.String(length=128), nullable=False),
        sa.Column('build_number', sa.Integer(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('logs_uri', sa.String(length=512), nullable=True),
        sa.Column('artifacts_generated', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 12. eng_test_suites
    op.create_table(
        'eng_test_suites',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('repository_id', sa.String(length=64), sa.ForeignKey('eng_code_repositories.id'), nullable=False),
        sa.Column('suite_name', sa.String(length=255), nullable=False),
        sa.Column('suite_type', sa.String(length=64), nullable=True),
        sa.Column('total_tests_count', sa.Integer(), nullable=True),
        sa.Column('passed_tests_count', sa.Integer(), nullable=True),
        sa.Column('failed_tests_count', sa.Integer(), nullable=True),
        sa.Column('flaky_rate_pct', sa.Float(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=False),
    )

    # 13. eng_sbom_packages
    op.create_table(
        'eng_sbom_packages',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('repository_id', sa.String(length=64), sa.ForeignKey('eng_code_repositories.id'), nullable=False),
        sa.Column('package_name', sa.String(length=255), nullable=False),
        sa.Column('version', sa.String(length=64), nullable=False),
        sa.Column('license_type', sa.String(length=64), nullable=True),
        sa.Column('is_license_compliant', sa.Boolean(), nullable=True),
        sa.Column('vulnerabilities_count', sa.Integer(), nullable=True),
        sa.Column('scanned_at', sa.DateTime(), nullable=False),
    )

    # 14. eng_deployments
    op.create_table(
        'eng_deployments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('environment', sa.String(length=32), nullable=True),
        sa.Column('strategy', sa.String(length=32), nullable=True),
        sa.Column('version', sa.String(length=64), nullable=False),
        sa.Column('traffic_weight_pct', sa.Float(), nullable=True),
        sa.Column('verification_status', sa.String(length=32), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('rollback_target_version', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. eng_service_catalog
    op.create_table(
        'eng_service_catalog',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('repository_id', sa.String(length=64), nullable=True),
        sa.Column('slo_target_availability_pct', sa.Float(), nullable=True),
        sa.Column('current_availability_pct', sa.Float(), nullable=True),
        sa.Column('error_budget_remaining_pct', sa.Float(), nullable=True),
        sa.Column('p95_latency_ms', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 16. eng_incidents
    op.create_table(
        'eng_incidents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('severity', sa.String(length=16), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('correlated_root_cause_hypothesis', sa.Text(), nullable=True),
        sa.Column('remediation_status', sa.String(length=32), nullable=True),
        sa.Column('mitigation_action_taken', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 17. eng_self_healing_runbooks
    op.create_table(
        'eng_self_healing_runbooks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('trigger_condition', sa.String(length=128), nullable=False),
        sa.Column('target_service', sa.String(length=255), nullable=False),
        sa.Column('action_type', sa.String(length=64), nullable=True),
        sa.Column('is_autonomous_approved', sa.Boolean(), nullable=True),
        sa.Column('executions_count', sa.Integer(), nullable=True),
        sa.Column('success_rate_pct', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 18. eng_finops_costs
    op.create_table(
        'eng_finops_costs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('eng_project_workspaces.id'), nullable=False),
        sa.Column('cost_category', sa.String(length=64), nullable=True),
        sa.Column('amount_usd', sa.Float(), nullable=True),
        sa.Column('units_consumed', sa.Float(), nullable=True),
        sa.Column('period_date', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('eng_finops_costs')
    op.drop_table('eng_self_healing_runbooks')
    op.drop_table('eng_incidents')
    op.drop_table('eng_service_catalog')
    op.drop_table('eng_deployments')
    op.drop_table('eng_sbom_packages')
    op.drop_table('eng_test_suites')
    op.drop_table('eng_ci_build_runs')
    op.drop_table('eng_ci_pipelines')
    op.drop_table('eng_pull_requests')
    op.drop_table('eng_agent_coding_sessions')
    op.drop_table('eng_tasks')
    op.drop_table('eng_code_symbols')
    op.drop_table('eng_code_repositories')
    op.drop_table('eng_architecture_components')
    op.drop_table('eng_acceptance_criteria')
    op.drop_table('eng_requirements')
    op.drop_table('eng_project_workspaces')
