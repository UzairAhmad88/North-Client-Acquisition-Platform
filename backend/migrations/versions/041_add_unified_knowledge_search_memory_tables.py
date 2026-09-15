"""add_unified_knowledge_search_memory_tables

Revision ID: 041
Revises: 040
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "041"
down_revision = "040"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. knowledge_items
    op.create_table(
        "knowledge_items",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("organization_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("knowledge_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("item_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("domain", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=True),
        sa.Column("provenance", sa.String(length=50), nullable=False),
        sa.Column("authority", sa.String(length=50), nullable=False, index=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("freshness_status", sa.String(length=50), nullable=False, index=True, server_default="FRESH"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, index=True, server_default="ACTIVE"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. knowledge_item_versions
    op.create_table(
        "knowledge_item_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("knowledge_item_id", sa.Uuid(as_uuid=True), sa.ForeignKey("knowledge_items.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("change_reason", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. knowledge_facts
    op.create_table(
        "knowledge_facts",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("fact_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("predicate", sa.String(length=100), nullable=False),
        sa.Column("target_value", sa.Text(), nullable=False),
        sa.Column("authority", sa.String(length=50), nullable=False, server_default="OBSERVED"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("source_reference", sa.String(length=255), nullable=True),
        sa.Column("verified_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. knowledge_decisions
    op.create_table(
        "knowledge_decisions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("context_background", sa.Text(), nullable=False),
        sa.Column("options_considered", sa.JSON(), nullable=False),
        sa.Column("decision_outcome", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("approver_ids", sa.JSON(), nullable=False),
        sa.Column("evidence_references", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="APPROVED"),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. knowledge_lessons
    op.create_table(
        "knowledge_lessons",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("lesson_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("context_scope", sa.String(length=255), nullable=False),
        sa.Column("problem", sa.Text(), nullable=False),
        sa.Column("root_cause", sa.Text(), nullable=False),
        sa.Column("what_worked", sa.Text(), nullable=False),
        sa.Column("what_failed", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("applicability_domain", sa.String(length=100), nullable=False, server_default="TECHNICAL"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.9"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. knowledge_entities
    op.create_table(
        "knowledge_entities",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("entity_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("entity_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=100), nullable=False, server_default="BUSINESS"),
        sa.Column("canonical_uri", sa.String(length=500), nullable=True),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. knowledge_relationships
    op.create_table(
        "knowledge_relationships",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_entity_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("target_entity_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("relationship_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. knowledge_collections
    op.create_table(
        "knowledge_collections",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("collection_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. knowledge_collection_members
    op.create_table(
        "knowledge_collection_members",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("collection_id", sa.Uuid(as_uuid=True), sa.ForeignKey("knowledge_collections.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("knowledge_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("added_by", sa.String(length=100), nullable=False),
        sa.Column("added_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. knowledge_chunks
    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("chunk_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("document_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("section_heading", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("token_estimate", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("access_scope", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. knowledge_embeddings
    op.create_table(
        "knowledge_embeddings",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("chunk_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("model_name", sa.String(length=100), nullable=False, server_default="text-embedding-3-small"),
        sa.Column("model_version", sa.String(length=50), nullable=False, server_default="1.0"),
        sa.Column("dimensions", sa.Integer(), nullable=False, server_default="1536"),
        sa.Column("vector_data", sa.JSON(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. knowledge_conflicts
    op.create_table(
        "knowledge_conflicts",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("conflict_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("source_a_code", sa.String(length=100), nullable=False),
        sa.Column("source_b_code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_by", sa.String(length=100), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. knowledge_context_requests
    op.create_table(
        "knowledge_context_requests",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("request_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("agent_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("task_intent", sa.String(length=255), nullable=False),
        sa.Column("budget_tokens", sa.Integer(), nullable=False, server_default="4000"),
        sa.Column("consumed_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("item_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("context_bundle_summary", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. knowledge_evaluation_runs
    op.create_table(
        "knowledge_evaluation_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("run_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("dataset_name", sa.String(length=100), nullable=False),
        sa.Column("precision_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("recall_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("mrr_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("grounding_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("unauthorized_leakage_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. knowledge_search_feedback
    op.create_table(
        "knowledge_search_feedback",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("query_text", sa.String(length=500), nullable=False),
        sa.Column("result_knowledge_code", sa.String(length=100), nullable=False),
        sa.Column("rating", sa.String(length=50), nullable=False),
        sa.Column("feedback_notes", sa.Text(), nullable=True),
        sa.Column("submitted_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("knowledge_search_feedback")
    op.drop_table("knowledge_evaluation_runs")
    op.drop_table("knowledge_context_requests")
    op.drop_table("knowledge_conflicts")
    op.drop_table("knowledge_embeddings")
    op.drop_table("knowledge_chunks")
    op.drop_table("knowledge_collection_members")
    op.drop_table("knowledge_collections")
    op.drop_table("knowledge_relationships")
    op.drop_table("knowledge_entities")
    op.drop_table("knowledge_lessons")
    op.drop_table("knowledge_decisions")
    op.drop_table("knowledge_facts")
    op.drop_table("knowledge_item_versions")
    op.drop_table("knowledge_items")
