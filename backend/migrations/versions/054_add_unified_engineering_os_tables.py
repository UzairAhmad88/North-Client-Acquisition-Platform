"""add unified engineering os tables

Revision ID: 054
Revises: 053
Create Date: 2026-09-12 22:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '054'
down_revision = '053'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. engineering_organizations
    op.create_table(
        'engineering_organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('head_of_engineering_email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. engineering_teams
    op.create_table(
        'engineering_teams',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_organizations.id', ondelete='CASCADE'), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('team_type', sa.String(length=50), nullable=False, server_default='BACKEND'),
        sa.Column('lead_email', sa.String(length=255), nullable=True),
        sa.Column('member_count', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. engineering_projects
    op.create_table(
        'engineering_projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_teams.id', ondelete='SET NULL'), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('key', sa.String(length=50), nullable=False, unique=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'),
        sa.Column('linked_product_initiative_id', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. engineering_repositories
    op.create_table(
        'engineering_repositories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_projects.id', ondelete='CASCADE'), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False, server_default='GITHUB'),
        sa.Column('default_branch', sa.String(length=100), nullable=False, server_default='main'),
        sa.Column('primary_language', sa.String(length=100), nullable=False, server_default='Python'),
        sa.Column('is_private', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. engineering_pull_requests
    op.create_table(
        'engineering_pull_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('repository_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_repositories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('pr_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('source_branch', sa.String(length=100), nullable=False),
        sa.Column('target_branch', sa.String(length=100), nullable=False, server_default='main'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('risk_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('linked_work_item', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('merged_at', sa.DateTime(), nullable=True),
    )

    # 6. engineering_services
    op.create_table(
        'engineering_services',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('service_tier', sa.String(length=20), nullable=False, server_default='TIER_1'),
        sa.Column('owner_team', sa.String(length=100), nullable=False, server_default='Core Platform'),
        sa.Column('runtime', sa.String(length=50), nullable=False, server_default='FASTAPI_PYTHON'),
        sa.Column('target_slo_availability', sa.Float(), nullable=False, server_default='99.9'),
        sa.Column('current_health_state', sa.String(length=50), nullable=False, server_default='HEALTHY'),
        sa.Column('dependencies', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 7. engineering_apis
    op.create_table(
        'engineering_apis',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('service_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_services.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False, server_default='v1'),
        sa.Column('protocol', sa.String(length=50), nullable=False, server_default='REST_OPENAPI'),
        sa.Column('is_deprecated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('auth_mechanism', sa.String(length=100), nullable=False, server_default='BEARER_JWT'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. engineering_environments
    op.create_table(
        'engineering_environments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('is_production', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('cluster_region', sa.String(length=100), nullable=False, server_default='us-east-1'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='READY'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. engineering_pipelines
    op.create_table(
        'engineering_pipelines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('repository_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_repositories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('pipeline_type', sa.String(length=50), nullable=False, server_default='CI_BUILD_TEST'),
        sa.Column('last_status', sa.String(length=50), nullable=False, server_default='SUCCESS'),
        sa.Column('duration_seconds', sa.Float(), nullable=False, server_default='120.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 10. engineering_deployments
    op.create_table(
        'engineering_deployments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('service_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('engineering_services.id', ondelete='CASCADE'), nullable=False),
        sa.Column('environment', sa.String(length=50), nullable=False, server_default='PRODUCTION'),
        sa.Column('strategy', sa.String(length=50), nullable=False, server_default='CANARY'),
        sa.Column('version_tag', sa.String(length=100), nullable=False),
        sa.Column('commit_sha', sa.String(length=64), nullable=False),
        sa.Column('operator_email', sa.String(length=255), nullable=False),
        sa.Column('approved_by', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DEPLOYED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 11. engineering_incidents
    op.create_table(
        'engineering_incidents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False, server_default='SEV2'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DETECTED'),
        sa.Column('affected_service', sa.String(length=100), nullable=False),
        sa.Column('root_cause_summary', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Float(), nullable=False, server_default='30.0'),
        sa.Column('incident_commander', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
    )

    # 12. engineering_changes
    op.create_table(
        'engineering_changes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('change_type', sa.String(length=50), nullable=False, server_default='INFRASTRUCTURE_UPDATE'),
        sa.Column('risk_level', sa.String(length=20), nullable=False, server_default='HIGH'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING_APPROVAL'),
        sa.Column('rollback_plan', sa.Text(), nullable=False),
        sa.Column('approver', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 13. engineering_vulnerabilities
    op.create_table(
        'engineering_vulnerabilities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('cve_id', sa.String(length=50), nullable=False),
        sa.Column('package_name', sa.String(length=100), nullable=False),
        sa.Column('current_version', sa.String(length=50), nullable=False),
        sa.Column('fixed_version', sa.String(length=50), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False, server_default='HIGH'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 14. engineering_technical_debt
    op.create_table(
        'engineering_technical_debt',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('area', sa.String(length=100), nullable=False, server_default='ARCHITECTURE'),
        sa.Column('severity', sa.String(length=20), nullable=False, server_default='MEDIUM'),
        sa.Column('effort_person_days', sa.Float(), nullable=False, server_default='5.0'),
        sa.Column('remediation_status', sa.String(length=50), nullable=False, server_default='LOGGED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. engineering_cloud_costs
    op.create_table(
        'engineering_cloud_costs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('service_name', sa.String(length=100), nullable=False),
        sa.Column('environment', sa.String(length=50), nullable=False, server_default='PRODUCTION'),
        sa.Column('monthly_cost_usd', sa.Float(), nullable=False, server_default='1200.0'),
        sa.Column('waste_estimate_usd', sa.Float(), nullable=False, server_default='150.0'),
        sa.Column('cost_trend_pct', sa.Float(), nullable=False, server_default='3.5'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 16. engineering_risks
    op.create_table(
        'engineering_risks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(length=100), nullable=False, server_default='default_tenant', index=True),
        sa.Column('category', sa.String(length=100), nullable=False, server_default='DELIVERY'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('probability', sa.Float(), nullable=False, server_default='0.3'),
        sa.Column('impact_score', sa.Float(), nullable=False, server_default='7.0'),
        sa.Column('exposure_score', sa.Float(), nullable=False, server_default='2.1'),
        sa.Column('severity', sa.String(length=20), nullable=False, server_default='HIGH'),
        sa.Column('mitigation_strategy', sa.Text(), nullable=True),
        sa.Column('owner', sa.String(length=255), nullable=False, server_default='lead-eng@uzaii.com'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('engineering_risks')
    op.drop_table('engineering_cloud_costs')
    op.drop_table('engineering_technical_debt')
    op.drop_table('engineering_vulnerabilities')
    op.drop_table('engineering_changes')
    op.drop_table('engineering_incidents')
    op.drop_table('engineering_deployments')
    op.drop_table('engineering_pipelines')
    op.drop_table('engineering_environments')
    op.drop_table('engineering_apis')
    op.drop_table('engineering_services')
    op.drop_table('engineering_pull_requests')
    op.drop_table('engineering_repositories')
    op.drop_table('engineering_projects')
    op.drop_table('engineering_teams')
    op.drop_table('engineering_organizations')
