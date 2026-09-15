"""add_data_governance_lineage_knowledge_tables

Revision ID: 030
Revises: 029
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "030"
down_revision = "029"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Data Sources & Catalog
    op.create_table(
        "data_sources",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default="PUBLIC_WEB"),
        sa.Column("trust_level", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_sources_tenant_id", "data_sources", ["tenant_id"])

    op.create_table(
        "data_catalog_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("domain", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("owner_role", sa.String(length=100), nullable=False, server_default="ADMIN"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("retention_days", sa.Integer(), nullable=False, server_default="365"),
        sa.Column("schema_definition", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_catalog_items_tenant_id", "data_catalog_items", ["tenant_id"])
    op.create_index("ix_data_catalog_items_domain", "data_catalog_items", ["domain"])

    op.create_table(
        "data_contracts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("producer_domain", sa.String(length=100), nullable=False),
        sa.Column("consumer_domain", sa.String(length=100), nullable=False),
        sa.Column("contract_name", sa.String(length=150), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False, server_default="1.0"),
        sa.Column("schema_spec", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_contracts_tenant_id", "data_contracts", ["tenant_id"])

    # 2. Quality Runs, Conflicts & Duplicates
    op.create_table(
        "data_quality_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("domain", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("records_evaluated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("composite_score", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("completeness_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("accuracy_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("consistency_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("freshness_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("validity_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("uniqueness_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("provenance_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("issues_found", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_quality_runs_tenant_id", "data_quality_runs", ["tenant_id"])

    op.create_table(
        "data_conflicts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("field_name", sa.String(length=100), nullable=False),
        sa.Column("source_a", sa.String(length=150), nullable=False),
        sa.Column("value_a", sa.Text(), nullable=False),
        sa.Column("source_b", sa.String(length=150), nullable=False),
        sa.Column("value_b", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="UNRESOLVED"),
        sa.Column("resolved_by", sa.String(length=100), nullable=True),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_conflicts_tenant_id", "data_conflicts", ["tenant_id"])
    op.create_index("ix_data_conflicts_entity", "data_conflicts", ["entity_type", "entity_id"])

    op.create_table(
        "data_duplicates",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("primary_id", sa.String(length=100), nullable=False),
        sa.Column("duplicate_id", sa.String(length=100), nullable=False),
        sa.Column("similarity_score", sa.Float(), nullable=False, server_default="0.9"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="CANDIDATE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_duplicates_tenant_id", "data_duplicates", ["tenant_id"])

    # 3. Provenance & Lineage
    op.create_table(
        "data_provenance_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default="OBSERVED"),
        sa.Column("source_reference", sa.String(length=255), nullable=True),
        sa.Column("authority", sa.String(length=50), nullable=False, server_default="OBSERVED"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("actor_id", sa.String(length=100), nullable=True),
        sa.Column("agent_id", sa.String(length=100), nullable=True),
        sa.Column("workflow_id", sa.String(length=100), nullable=True),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_provenance_tenant_id", "data_provenance_records", ["tenant_id"])
    op.create_index("ix_data_provenance_entity", "data_provenance_records", ["entity_type", "entity_id"])

    op.create_table(
        "data_lineage_edges",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("source_type", sa.String(length=100), nullable=False),
        sa.Column("source_id", sa.String(length=100), nullable=False),
        sa.Column("target_type", sa.String(length=100), nullable=False),
        sa.Column("target_id", sa.String(length=100), nullable=False),
        sa.Column("relationship", sa.String(length=50), nullable=False, server_default="DERIVED_FROM"),
        sa.Column("transformation", sa.String(length=255), nullable=True),
        sa.Column("actor_id", sa.String(length=100), nullable=True),
        sa.Column("agent_id", sa.String(length=100), nullable=True),
        sa.Column("workflow_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_lineage_tenant_id", "data_lineage_edges", ["tenant_id"])
    op.create_index("ix_data_lineage_source", "data_lineage_edges", ["source_type", "source_id"])
    op.create_index("ix_data_lineage_target", "data_lineage_edges", ["target_type", "target_id"])

    # 4. Documents & Integrity
    op.create_table(
        "document_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("project_id", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("doc_type", sa.String(length=50), nullable=False, server_default="REQUIREMENTS"),
        sa.Column("mime_type", sa.String(length=100), nullable=False, server_default="application/pdf"),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="AVAILABLE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_document_records_tenant_id", "document_records", ["tenant_id"])
    op.create_index("ix_document_records_checksum", "document_records", ["checksum"])

    op.create_table(
        "document_version_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("change_summary", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["document_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_document_versions_doc_id", "document_version_records", ["document_id"])

    # 5. Knowledge Base & Semantic Context
    op.create_table(
        "knowledge_item_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("project_id", sa.String(length=100), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, server_default="BUSINESS_FACT"),
        sa.Column("authority", sa.String(length=50), nullable=False, server_default="OBSERVED"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.9"),
        sa.Column("lifecycle", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("source_reference", sa.String(length=255), nullable=True),
        sa.Column("confirmed_by", sa.String(length=100), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_knowledge_items_tenant_id", "knowledge_item_records", ["tenant_id"])
    op.create_index("ix_knowledge_items_lifecycle", "knowledge_item_records", ["lifecycle"])

    op.create_table(
        "knowledge_relationship_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_knowledge_id", sa.String(length=36), nullable=False),
        sa.Column("target_knowledge_id", sa.String(length=36), nullable=False),
        sa.Column("relationship_type", sa.String(length=50), nullable=False, server_default="IMPLEMENTS"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["source_knowledge_id"], ["knowledge_item_records.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_knowledge_id"], ["knowledge_item_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 6. Retention & Legal Holds
    op.create_table(
        "data_retention_policy_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("domain", sa.String(length=100), nullable=False),
        sa.Column("retention_days", sa.Integer(), nullable=False, server_default="365"),
        sa.Column("archive_after_days", sa.Integer(), nullable=True, server_default="180"),
        sa.Column("auto_delete", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_retention_policies_tenant_id", "data_retention_policy_records", ["tenant_id"])
    op.create_index("ix_retention_policies_domain", "data_retention_policy_records", ["domain"])

    op.create_table(
        "legal_hold_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("applied_by", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("released_at", sa.DateTime(), nullable=True),
        sa.Column("released_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_legal_holds_tenant_id", "legal_hold_records", ["tenant_id"])
    op.create_index("ix_legal_holds_entity", "legal_hold_records", ["entity_type", "entity_id"])


def downgrade() -> None:
    op.drop_table("legal_hold_records")
    op.drop_table("data_retention_policy_records")
    op.drop_table("knowledge_relationship_records")
    op.drop_table("knowledge_item_records")
    op.drop_table("document_version_records")
    op.drop_table("document_records")
    op.drop_table("data_lineage_edges")
    op.drop_table("data_provenance_records")
    op.drop_table("data_duplicates")
    op.drop_table("data_conflicts")
    op.drop_table("data_quality_runs")
    op.drop_table("data_contracts")
    op.drop_table("data_catalog_items")
    op.drop_table("data_sources")
