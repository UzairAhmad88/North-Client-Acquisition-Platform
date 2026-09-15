"""add autonomous data and knowledge os tables

Revision ID: 058
Revises: 057
Create Date: 2026-09-13 21:12:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '058'
down_revision = '057'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Sources & Connectors
    op.create_table(
        'adkos_sources',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('source_type', sa.String(length=64), nullable=False),
        sa.Column('provider', sa.String(length=64), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('team', sa.String(length=128), nullable=False),
        sa.Column('environment', sa.String(length=64), nullable=True),
        sa.Column('connection_config', sa.JSON(), nullable=True),
        sa.Column('auth_ref', sa.String(length=128), nullable=True),
        sa.Column('schema_definition', sa.JSON(), nullable=True),
        sa.Column('refresh_rate', sa.String(length=64), nullable=True),
        sa.Column('sensitivity', sa.String(length=64), nullable=True),
        sa.Column('classification', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('last_sync_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_connectors',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('connector_type', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('config_schema', sa.JSON(), nullable=True),
        sa.Column('capabilities', sa.JSON(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('health_status', sa.String(length=64), nullable=True),
        sa.Column('last_health_check', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_source_credentials',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('vault_key_ref', sa.String(length=256), nullable=False),
        sa.Column('auth_type', sa.String(length=64), nullable=False),
        sa.Column('rotated_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_ingestion_jobs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('connector_id', sa.String(length=64), nullable=False),
        sa.Column('job_type', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('records_ingested', sa.Integer(), nullable=True),
        sa.Column('bytes_processed', sa.Float(), nullable=True),
        sa.Column('duration_ms', sa.Float(), nullable=True),
        sa.Column('watermark', sa.String(length=128), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )

    # 2. Pipelines & Orchestration
    op.create_table(
        'adkos_pipelines',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('trigger_type', sa.String(length=64), nullable=True),
        sa.Column('schedule_cron', sa.String(length=64), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('sla_minutes', sa.Integer(), nullable=True),
        sa.Column('dependencies', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_pipeline_steps',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('pipeline_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('step_order', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('step_type', sa.String(length=64), nullable=False),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=True),
    )

    op.create_table(
        'adkos_pipeline_runs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('pipeline_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('run_status', sa.String(length=64), nullable=True),
        sa.Column('records_transformed', sa.Integer(), nullable=True),
        sa.Column('latency_seconds', sa.Float(), nullable=True),
        sa.Column('logs', sa.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_pipeline_dependencies',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('upstream_pipeline_id', sa.String(length=64), nullable=False),
        sa.Column('downstream_pipeline_id', sa.String(length=64), nullable=False),
        sa.Column('dependency_condition', sa.String(length=64), nullable=True),
    )

    # 3. Lakehouse, Warehouse & Marts
    op.create_table(
        'adkos_lake_assets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('layer', sa.String(length=32), nullable=True),
        sa.Column('format', sa.String(length=32), nullable=True),
        sa.Column('storage_path', sa.String(length=256), nullable=False),
        sa.Column('partition_columns', sa.JSON(), nullable=True),
        sa.Column('record_count', sa.Integer(), nullable=True),
        sa.Column('size_mb', sa.Float(), nullable=True),
        sa.Column('lineage_parent_id', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_warehouse_assets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('table_name', sa.String(length=128), nullable=False),
        sa.Column('model_type', sa.String(length=64), nullable=True),
        sa.Column('schema_fields', sa.JSON(), nullable=True),
        sa.Column('primary_keys', sa.JSON(), nullable=True),
        sa.Column('surrogate_key', sa.String(length=64), nullable=True),
        sa.Column('is_scd', sa.Boolean(), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_marts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('domain', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('underlying_tables', sa.JSON(), nullable=True),
        sa.Column('target_audiences', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 4. Products, Contracts, Schemas
    op.create_table(
        'adkos_products',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('source_datasets', sa.JSON(), nullable=True),
        sa.Column('contract_id', sa.String(length=64), nullable=True),
        sa.Column('schema_def', sa.JSON(), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('sla_freshness_minutes', sa.Integer(), nullable=True),
        sa.Column('security_classification', sa.String(length=64), nullable=True),
        sa.Column('monthly_cost_usd', sa.Float(), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_product_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('product_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('schema_snapshot', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_product_consumers',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('product_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('consumer_name', sa.String(length=128), nullable=False),
        sa.Column('consumer_type', sa.String(length=64), nullable=True),
        sa.Column('sla_tier', sa.String(length=64), nullable=True),
        sa.Column('registered_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_contracts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('schema_rules', sa.JSON(), nullable=True),
        sa.Column('constraints', sa.JSON(), nullable=True),
        sa.Column('freshness_sla_minutes', sa.Integer(), nullable=True),
        sa.Column('quality_threshold_pct', sa.Float(), nullable=True),
        sa.Column('compatibility_mode', sa.String(length=32), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_contract_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('contract_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('spec_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_schema_registry',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('subject', sa.String(length=128), nullable=False, index=True),
        sa.Column('schema_type', sa.String(length=32), nullable=True),
        sa.Column('current_version', sa.String(length=32), nullable=True),
        sa.Column('fields', sa.JSON(), nullable=True),
        sa.Column('compatibility', sa.String(length=32), nullable=True),
        sa.Column('producer', sa.String(length=128), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_schema_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('registry_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('fields', sa.JSON(), nullable=True),
        sa.Column('breaking_change', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 5. Quality, Observability & Incidents
    op.create_table(
        'adkos_quality_rules',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('dimension', sa.String(length=64), nullable=False),
        sa.Column('rule_type', sa.String(length=64), nullable=False),
        sa.Column('target_column', sa.String(length=128), nullable=True),
        sa.Column('expression', sa.String(length=256), nullable=False),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
    )

    op.create_table(
        'adkos_quality_runs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('completeness_score', sa.Float(), nullable=True),
        sa.Column('validity_score', sa.Float(), nullable=True),
        sa.Column('freshness_score', sa.Float(), nullable=True),
        sa.Column('accuracy_score', sa.Float(), nullable=True),
        sa.Column('rules_passed', sa.Integer(), nullable=True),
        sa.Column('rules_failed', sa.Integer(), nullable=True),
        sa.Column('executed_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_quality_results',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('run_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('rule_id', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('failed_records_count', sa.Integer(), nullable=True),
        sa.Column('failure_details', sa.JSON(), nullable=True),
    )

    op.create_table(
        'adkos_incidents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('pipeline_id', sa.String(length=64), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('impact_scope', sa.Text(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('root_cause', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_incident_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('incident_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('event_text', sa.Text(), nullable=False),
        sa.Column('actor', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_incident_postmortems',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('incident_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('preventative_actions', sa.JSON(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )

    # 6. Lineage
    op.create_table(
        'adkos_lineage',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_type', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=128), nullable=False),
        sa.Column('target_type', sa.String(length=64), nullable=False),
        sa.Column('target_id', sa.String(length=128), nullable=False),
        sa.Column('transformation_logic', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_column_lineage',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_table', sa.String(length=128), nullable=False),
        sa.Column('source_column', sa.String(length=128), nullable=False),
        sa.Column('target_table', sa.String(length=128), nullable=False),
        sa.Column('target_column', sa.String(length=128), nullable=False),
        sa.Column('transform_expression', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 7. Catalog & Glossary
    op.create_table(
        'adkos_catalog',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('asset_type', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('domain', sa.String(length=64), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('sensitivity', sa.String(length=32), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_metadata',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('asset_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('category', sa.String(length=64), nullable=True),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_glossary',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('term_name', sa.String(length=128), nullable=False),
        sa.Column('definition', sa.Text(), nullable=False),
        sa.Column('domain', sa.String(length=64), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('synonyms', sa.JSON(), nullable=True),
        sa.Column('related_metrics', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_business_term_relationships',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('term_id_a', sa.String(length=64), nullable=False),
        sa.Column('term_id_b', sa.String(length=64), nullable=False),
        sa.Column('relation', sa.String(length=64), nullable=True),
    )

    # 8. Semantic Layer & Metrics
    op.create_table(
        'adkos_semantic_models',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('entity_name', sa.String(length=128), nullable=False),
        sa.Column('underlying_source', sa.String(length=128), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('primary_key', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_semantic_relationships',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('entity_a', sa.String(length=128), nullable=False),
        sa.Column('entity_b', sa.String(length=128), nullable=False),
        sa.Column('join_type', sa.String(length=32), nullable=True),
        sa.Column('join_condition', sa.String(length=256), nullable=False),
    )

    op.create_table(
        'adkos_metrics',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('definition', sa.Text(), nullable=False),
        sa.Column('formula_sql', sa.Text(), nullable=False),
        sa.Column('source_table', sa.String(length=128), nullable=False),
        sa.Column('dimensions', sa.JSON(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('certification_status', sa.String(length=32), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_metric_dimensions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('metric_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dimension_name', sa.String(length=128), nullable=False),
        sa.Column('dimension_type', sa.String(length=32), nullable=True),
    )

    op.create_table(
        'adkos_metric_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('metric_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('formula_sql', sa.Text(), nullable=False),
        sa.Column('changed_by', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 9. Master Data & Entity Resolution
    op.create_table(
        'adkos_master_entities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('canonical_name', sa.String(length=128), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_entity_aliases',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('master_entity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('alias_name', sa.String(length=128), nullable=False),
        sa.Column('source_system', sa.String(length=64), nullable=False),
    )

    op.create_table(
        'adkos_entity_matches',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('master_entity_id', sa.String(length=64), nullable=False),
        sa.Column('matched_candidate_name', sa.String(length=128), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
    )

    op.create_table(
        'adkos_entity_merge_history',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('surviving_entity_id', sa.String(length=64), nullable=False),
        sa.Column('merged_entity_id', sa.String(length=64), nullable=False),
        sa.Column('merged_by', sa.String(length=128), nullable=False),
        sa.Column('merged_at', sa.DateTime(), nullable=True),
    )

    # 10. Knowledge Graph
    op.create_table(
        'adkos_knowledge_nodes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('label', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_knowledge_edges',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('from_node_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('to_node_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('relationship_type', sa.String(length=64), nullable=False),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_knowledge_sources',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('node_or_edge_id', sa.String(length=64), nullable=False),
        sa.Column('source_uri', sa.String(length=256), nullable=False),
        sa.Column('source_type', sa.String(length=64), nullable=True),
        sa.Column('extracted_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_knowledge_conflicts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('node_id', sa.String(length=64), nullable=False),
        sa.Column('property_name', sa.String(length=128), nullable=False),
        sa.Column('value_a', sa.Text(), nullable=False),
        sa.Column('source_a', sa.String(length=256), nullable=False),
        sa.Column('value_b', sa.Text(), nullable=False),
        sa.Column('source_b', sa.String(length=256), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 11. Documents & Search
    op.create_table(
        'adkos_documents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('file_type', sa.String(length=32), nullable=False),
        sa.Column('storage_uri', sa.String(length=256), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('extracted_topics', sa.JSON(), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_document_chunks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('document_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('chunk_index', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding_vector_id', sa.String(length=128), nullable=True),
        sa.Column('extracted_entities', sa.JSON(), nullable=True),
    )

    op.create_table(
        'adkos_search_indexes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('index_name', sa.String(length=128), nullable=False),
        sa.Column('doc_count', sa.Integer(), nullable=True),
        sa.Column('last_indexed_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_search_queries',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('query_text', sa.String(length=256), nullable=False),
        sa.Column('user_id', sa.String(length=128), nullable=False),
        sa.Column('results_count', sa.Integer(), nullable=True),
        sa.Column('latency_ms', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 12. AI Memory
    op.create_table(
        'adkos_memories',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('memory_type', sa.String(length=64), nullable=True),
        sa.Column('source', sa.String(length=128), nullable=False),
        sa.Column('entity_ref', sa.String(length=128), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('classification', sa.String(length=64), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('sensitivity', sa.String(length=32), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_memory_conflicts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('memory_id_a', sa.String(length=64), nullable=False),
        sa.Column('memory_id_b', sa.String(length=64), nullable=False),
        sa.Column('conflict_reason', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
    )

    # 13. Datasets & Features
    op.create_table(
        'adkos_datasets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('purpose', sa.String(length=64), nullable=True),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('pii_cleansed', sa.Boolean(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('storage_uri', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_features',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('entity_name', sa.String(length=64), nullable=False),
        sa.Column('data_type', sa.String(length=32), nullable=True),
        sa.Column('transformation_sql', sa.Text(), nullable=False),
        sa.Column('freshness_minutes', sa.Integer(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 14. Privacy, Access & Retention
    op.create_table(
        'adkos_classifications',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('column_name', sa.String(length=128), nullable=False),
        sa.Column('classification', sa.String(length=64), nullable=True),
        sa.Column('pii_type', sa.String(length=64), nullable=True),
        sa.Column('masking_strategy', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_pii_findings',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('column_name', sa.String(length=128), nullable=False),
        sa.Column('sample_masked_value', sa.String(length=128), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('reviewed', sa.Boolean(), nullable=True),
        sa.Column('discovered_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_access_policies',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('policy_name', sa.String(length=128), nullable=False),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('allowed_roles', sa.JSON(), nullable=True),
        sa.Column('row_filter_sql', sa.String(length=256), nullable=True),
        sa.Column('masked_columns', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
    )

    op.create_table(
        'adkos_access_requests',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('user_id', sa.String(length=128), nullable=False),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('justification', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('approver_id', sa.String(length=128), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_retention_policies',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('retention_days', sa.Integer(), nullable=True),
        sa.Column('archive_after_days', sa.Integer(), nullable=True),
        sa.Column('has_legal_hold', sa.Boolean(), nullable=True),
        sa.Column('auto_delete', sa.Boolean(), nullable=True),
    )

    op.create_table(
        'adkos_deletion_requests',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('target_entity', sa.String(length=128), nullable=False),
        sa.Column('target_id', sa.String(length=128), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
    )

    # 15. FinOps, Security & Reliability (SLOs)
    op.create_table(
        'adkos_costs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('cost_usd', sa.Float(), nullable=True),
        sa.Column('recorded_date', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_security_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('user_or_agent', sa.String(length=128), nullable=False),
        sa.Column('action', sa.String(length=64), nullable=False),
        sa.Column('dataset_name', sa.String(length=128), nullable=False),
        sa.Column('result', sa.String(length=32), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_slos',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('data_product_name', sa.String(length=128), nullable=False),
        sa.Column('freshness_target_pct', sa.Float(), nullable=True),
        sa.Column('availability_target_pct', sa.Float(), nullable=True),
        sa.Column('quality_target_pct', sa.Float(), nullable=True),
        sa.Column('current_health', sa.String(length=32), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'adkos_recommendations',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('category', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('potential_savings_usd', sa.Float(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    tables = [
        'adkos_recommendations', 'adkos_slos', 'adkos_security_events', 'adkos_costs',
        'adkos_deletion_requests', 'adkos_retention_policies', 'adkos_access_requests',
        'adkos_access_policies', 'adkos_pii_findings', 'adkos_classifications',
        'adkos_features', 'adkos_datasets', 'adkos_memory_conflicts', 'adkos_memories',
        'adkos_search_queries', 'adkos_search_indexes', 'adkos_document_chunks',
        'adkos_documents', 'adkos_knowledge_conflicts', 'adkos_knowledge_sources',
        'adkos_knowledge_edges', 'adkos_knowledge_nodes', 'adkos_entity_merge_history',
        'adkos_entity_matches', 'adkos_entity_aliases', 'adkos_master_entities',
        'adkos_metric_versions', 'adkos_metric_dimensions', 'adkos_metrics',
        'adkos_semantic_relationships', 'adkos_semantic_models',
        'adkos_business_term_relationships', 'adkos_glossary', 'adkos_metadata',
        'adkos_catalog', 'adkos_column_lineage', 'adkos_lineage',
        'adkos_incident_postmortems', 'adkos_incident_events', 'adkos_incidents',
        'adkos_quality_results', 'adkos_quality_runs', 'adkos_quality_rules',
        'adkos_schema_versions', 'adkos_schema_registry', 'adkos_contract_versions',
        'adkos_contracts', 'adkos_product_consumers', 'adkos_product_versions',
        'adkos_products', 'adkos_marts', 'adkos_warehouse_assets', 'adkos_lake_assets',
        'adkos_pipeline_dependencies', 'adkos_pipeline_runs', 'adkos_pipeline_steps',
        'adkos_pipelines', 'adkos_ingestion_jobs', 'adkos_source_credentials',
        'adkos_connectors', 'adkos_sources'
    ]
    for table in tables:
        op.drop_table(table)
