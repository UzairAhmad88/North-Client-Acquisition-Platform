"""add unified enterprise data os tables

Revision ID: 055
Revises: 054
Create Date: 2026-09-12 22:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '055'
down_revision = '054'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. data_domains
    op.create_table(
        'data_domains',
        sa.Column('domain_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('slug', sa.String(length=128), nullable=False),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('lead_steward_email', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 2. data_sources
    op.create_table(
        'data_sources',
        sa.Column('source_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('source_type', sa.String(length=64), nullable=False),
        sa.Column('provider', sa.String(length=64), nullable=False),
        sa.Column('domain_id', sa.String(length=64), nullable=True),
        sa.Column('connection_endpoint', sa.String(length=256), nullable=False),
        sa.Column('auth_type', sa.String(length=64), nullable=False),
        sa.Column('data_classification', sa.String(length=64), server_default='INTERNAL'),
        sa.Column('status', sa.String(length=64), server_default='ACTIVE'),
        sa.Column('reliability_score', sa.Float(), server_default='99.9'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. data_ingestion_jobs
    op.create_table(
        'data_ingestion_jobs',
        sa.Column('job_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('target_dataset_id', sa.String(length=64), nullable=False),
        sa.Column('ingestion_mode', sa.String(length=64), server_default='BATCH'),
        sa.Column('schedule_cron', sa.String(length=64), nullable=True),
        sa.Column('watermark_offset', sa.String(length=128), nullable=True),
        sa.Column('records_processed_count', sa.Integer(), server_default='0'),
        sa.Column('latency_ms', sa.Float(), server_default='0.0'),
        sa.Column('status', sa.String(length=64), server_default='RUNNING'),
        sa.Column('last_run_at', sa.DateTime(), nullable=False),
    )

    # 4. data_pipelines
    op.create_table(
        'data_pipelines',
        sa.Column('pipeline_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('source_datasets', sa.JSON(), nullable=True),
        sa.Column('target_dataset', sa.String(length=128), nullable=False),
        sa.Column('schedule_type', sa.String(length=64), server_default='SCHEDULED'),
        sa.Column('sla_minutes', sa.Integer(), server_default='60'),
        sa.Column('status', sa.String(length=64), server_default='ACTIVE'),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. data_lakehouse_datasets
    op.create_table(
        'data_lakehouse_datasets',
        sa.Column('dataset_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('domain_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('layer', sa.String(length=32), server_default='BRONZE'),
        sa.Column('format', sa.String(length=32), server_default='PARQUET'),
        sa.Column('storage_uri', sa.String(length=256), nullable=False),
        sa.Column('partition_keys', sa.JSON(), nullable=True),
        sa.Column('record_count', sa.Integer(), server_default='0'),
        sa.Column('size_mb', sa.Float(), server_default='0.0'),
        sa.Column('classification', sa.String(length=32), server_default='INTERNAL'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. data_schemas
    op.create_table(
        'data_schemas',
        sa.Column('schema_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_id', sa.String(length=64), nullable=False),
        sa.Column('version', sa.String(length=32), server_default='v1.0.0'),
        sa.Column('fields', sa.JSON(), nullable=True),
        sa.Column('compatibility_mode', sa.String(length=32), server_default='BACKWARD'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('registered_at', sa.DateTime(), nullable=False),
    )

    # 7. data_contracts
    op.create_table(
        'data_contracts',
        sa.Column('contract_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('producer_team', sa.String(length=128), nullable=False),
        sa.Column('consumer_team', sa.String(length=128), nullable=False),
        sa.Column('dataset_id', sa.String(length=64), nullable=False),
        sa.Column('schema_version', sa.String(length=32), server_default='v1.0.0'),
        sa.Column('freshness_sla_minutes', sa.Integer(), server_default='120'),
        sa.Column('quality_threshold_pct', sa.Float(), server_default='99.0'),
        sa.Column('status', sa.String(length=32), server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. data_products
    op.create_table(
        'data_products',
        sa.Column('product_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('domain_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('purpose', sa.Text(), nullable=False),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('underlying_datasets', sa.JSON(), nullable=True),
        sa.Column('consumers_count', sa.Integer(), server_default='0'),
        sa.Column('quality_score', sa.Float(), server_default='98.5'),
        sa.Column('health_status', sa.String(length=32), server_default='HEALTHY'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. data_catalog_assets
    op.create_table(
        'data_catalog_assets',
        sa.Column('asset_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('asset_name', sa.String(length=128), nullable=False),
        sa.Column('asset_type', sa.String(length=64), nullable=False),
        sa.Column('domain_name', sa.String(length=64), nullable=False),
        sa.Column('owner_email', sa.String(length=128), nullable=False),
        sa.Column('classification', sa.String(length=32), server_default='INTERNAL'),
        sa.Column('quality_score', sa.Float(), server_default='95.0'),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 10. business_glossary_terms
    op.create_table(
        'business_glossary_terms',
        sa.Column('term_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('term_name', sa.String(length=128), nullable=False),
        sa.Column('definition', sa.Text(), nullable=False),
        sa.Column('domain_name', sa.String(length=64), nullable=False),
        sa.Column('owner_email', sa.String(length=128), nullable=False),
        sa.Column('synonyms', sa.JSON(), nullable=True),
        sa.Column('related_metrics', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 11. semantic_metrics
    op.create_table(
        'semantic_metrics',
        sa.Column('metric_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('definition', sa.Text(), nullable=False),
        sa.Column('formula_sql', sa.Text(), nullable=False),
        sa.Column('dimensions', sa.JSON(), nullable=True),
        sa.Column('source_table', sa.String(length=128), nullable=False),
        sa.Column('owner_team', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 12. data_quality_rules
    op.create_table(
        'data_quality_rules',
        sa.Column('rule_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_id', sa.String(length=64), nullable=False),
        sa.Column('rule_type', sa.String(length=64), nullable=False),
        sa.Column('dimension', sa.String(length=64), server_default='COMPLETENESS'),
        sa.Column('severity', sa.String(length=32), server_default='HIGH'),
        sa.Column('pass_rate_pct', sa.Float(), server_default='100.0'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('last_evaluated_at', sa.DateTime(), nullable=False),
    )

    # 13. data_lineage_edges
    op.create_table(
        'data_lineage_edges',
        sa.Column('edge_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_asset_id', sa.String(length=64), nullable=False),
        sa.Column('target_asset_id', sa.String(length=64), nullable=False),
        sa.Column('relationship_type', sa.String(length=64), server_default='TRANSFORMS_INTO'),
        sa.Column('transformation_name', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 14. data_access_grants
    op.create_table(
        'data_access_grants',
        sa.Column('grant_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('principal_id', sa.String(length=64), nullable=False),
        sa.Column('dataset_id', sa.String(length=64), nullable=False),
        sa.Column('access_level', sa.String(length=32), server_default='READ'),
        sa.Column('row_filter_expression', sa.String(length=256), nullable=True),
        sa.Column('masked_columns', sa.JSON(), nullable=True),
        sa.Column('approved_by', sa.String(length=128), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. feature_store_items
    op.create_table(
        'feature_store_items',
        sa.Column('feature_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('entity_name', sa.String(length=64), nullable=False),
        sa.Column('data_type', sa.String(length=32), server_default='FLOAT'),
        sa.Column('source_dataset_id', sa.String(length=64), nullable=False),
        sa.Column('transformation_logic', sa.Text(), nullable=False),
        sa.Column('freshness_minutes', sa.Integer(), server_default='60'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 16. data_finops_costs
    op.create_table(
        'data_finops_costs',
        sa.Column('cost_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('domain_name', sa.String(length=64), nullable=False),
        sa.Column('cost_category', sa.String(length=64), nullable=False),
        sa.Column('monthly_spend_usd', sa.Float(), server_default='0.0'),
        sa.Column('waste_estimate_usd', sa.Float(), server_default='0.0'),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
    )

    # 17. data_incidents
    op.create_table(
        'data_incidents',
        sa.Column('incident_id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('severity', sa.String(length=32), server_default='SEV2'),
        sa.Column('incident_type', sa.String(length=64), nullable=False),
        sa.Column('affected_datasets', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), server_default='ACTIVE'),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('data_incidents')
    op.drop_table('data_finops_costs')
    op.drop_table('feature_store_items')
    op.drop_table('data_access_grants')
    op.drop_table('data_lineage_edges')
    op.drop_table('data_quality_rules')
    op.drop_table('semantic_metrics')
    op.drop_table('business_glossary_terms')
    op.drop_table('data_catalog_assets')
    op.drop_table('data_products')
    op.drop_table('data_contracts')
    op.drop_table('data_schemas')
    op.drop_table('data_lakehouse_datasets')
    op.drop_table('data_pipelines')
    op.drop_table('data_ingestion_jobs')
    op.drop_table('data_sources')
    op.drop_table('data_domains')
