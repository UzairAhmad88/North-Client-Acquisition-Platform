"""add_enterprise_knowledge_graph_tables

Revision ID: 070
Revises: 069
Create Date: 2026-09-14 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '070'
down_revision = '069'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'ekg_entities',
        'ekg_entity_aliases',
        'ekg_entity_attributes',
        'ekg_entity_sources',
        'ekg_entity_versions',
        'ekg_relationships',
        'ekg_relationship_versions',
        'ekg_relationship_sources',
        'ekg_claims',
        'ekg_claim_evidence',
        'ekg_claim_sources',
        'ekg_documents',
        'ekg_document_versions',
        'ekg_document_chunks',
        'ekg_document_entities',
        'ekg_sources',
        'ekg_source_reliability',
        'ekg_ontologies',
        'ekg_ontology_versions',
        'ekg_taxonomies',
        'ekg_taxonomy_versions',
        'ekg_glossary_terms',
        'ekg_glossary_relations',
        'ekg_metadata_assets',
        'ekg_metadata_fields',
        'ekg_data_lineage',
        'ekg_data_classifications',
        'ekg_access_policies',
        'ekg_embeddings',
        'ekg_embedding_versions',
        'ekg_search_indexes',
        'ekg_conflicts',
        'ekg_conflict_resolutions',
        'ekg_gaps',
        'ekg_quality_scores',
        'ekg_lessons',
        'ekg_lesson_sources',
        'ekg_change_events',
        'ekg_notifications',
        'ekg_search_queries',
        'ekg_search_results',
        'ekg_search_feedback',
        'ekg_stewards',
        'ekg_reviews',
        'ekg_retention_policies',
        'ekg_ingestion_jobs',
        'ekg_extraction_jobs',
        'ekg_indexing_jobs',
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
        'ekg_entities',
        'ekg_entity_aliases',
        'ekg_entity_attributes',
        'ekg_entity_sources',
        'ekg_entity_versions',
        'ekg_relationships',
        'ekg_relationship_versions',
        'ekg_relationship_sources',
        'ekg_claims',
        'ekg_claim_evidence',
        'ekg_claim_sources',
        'ekg_documents',
        'ekg_document_versions',
        'ekg_document_chunks',
        'ekg_document_entities',
        'ekg_sources',
        'ekg_source_reliability',
        'ekg_ontologies',
        'ekg_ontology_versions',
        'ekg_taxonomies',
        'ekg_taxonomy_versions',
        'ekg_glossary_terms',
        'ekg_glossary_relations',
        'ekg_metadata_assets',
        'ekg_metadata_fields',
        'ekg_data_lineage',
        'ekg_data_classifications',
        'ekg_access_policies',
        'ekg_embeddings',
        'ekg_embedding_versions',
        'ekg_search_indexes',
        'ekg_conflicts',
        'ekg_conflict_resolutions',
        'ekg_gaps',
        'ekg_quality_scores',
        'ekg_lessons',
        'ekg_lesson_sources',
        'ekg_change_events',
        'ekg_notifications',
        'ekg_search_queries',
        'ekg_search_results',
        'ekg_search_feedback',
        'ekg_stewards',
        'ekg_reviews',
        'ekg_retention_policies',
        'ekg_ingestion_jobs',
        'ekg_extraction_jobs',
        'ekg_indexing_jobs',
    ]

    for table in tables:
        op.drop_table(table)
