"""add_unified_document_file_asset_tables

Revision ID: 033
Revises: 032
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "033"
down_revision = "032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. files
    op.create_table(
        "files",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("folder_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("extension", sa.String(length=50), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("storage_provider", sa.String(length=50), nullable=False, server_default="LOCAL"),
        sa.Column("storage_key", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="AVAILABLE"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="GENERAL"),
        sa.Column("sensitivity", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("visibility", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_files_tenant_id", "files", ["tenant_id"])
    op.create_index("ix_files_workspace_id", "files", ["workspace_id"])
    op.create_index("ix_files_checksum", "files", ["checksum"])
    op.create_index("ix_files_status", "files", ["status"])
    op.create_index("ix_files_classification", "files", ["classification"])
    op.create_index("ix_files_is_deleted", "files", ["is_deleted"])

    # 2. file_versions
    op.create_table(
        "file_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("storage_key", sa.String(length=500), nullable=False),
        sa.Column("change_summary", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="AVAILABLE"),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["file_id"], ["files.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_file_versions_file_id", "file_versions", ["file_id"])

    # 3. file_metadata
    op.create_table(
        "file_metadata",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags_json", sa.JSON(), nullable=True),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("dimensions_json", sa.JSON(), nullable=True),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("encoding", sa.String(length=50), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("custom_metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["file_id"], ["files.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_id"),
    )

    # 4. file_scans
    op.create_table(
        "file_scans",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=False),
        sa.Column("scanner_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("threat_name", sa.String(length=200), nullable=True),
        sa.Column("threat_category", sa.String(length=100), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("scan_duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("raw_output", sa.Text(), nullable=True),
        sa.Column("scanned_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["file_id"], ["files.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_file_scans_file_id", "file_scans", ["file_id"])

    # 5. file_access_logs
    op.create_table(
        "file_access_logs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("result", sa.String(length=50), nullable=False, server_default="ALLOW"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_file_access_logs_tenant_id", "file_access_logs", ["tenant_id"])
    op.create_index("ix_file_access_logs_file_id", "file_access_logs", ["file_id"])
    op.create_index("ix_file_access_logs_user_id", "file_access_logs", ["user_id"])

    # 6. folders
    op.create_table(
        "folders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("parent_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=1000), nullable=False),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_folders_tenant_id", "folders", ["tenant_id"])
    op.create_index("ix_folders_workspace_id", "folders", ["workspace_id"])

    # 7. managed_documents
    op.create_table(
        "managed_documents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("folder_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("current_version_id", sa.String(length=36), nullable=True),
        sa.Column("current_version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("classification", sa.String(length=50), nullable=False, server_default="GENERAL"),
        sa.Column("sensitivity", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("visibility", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("retention_status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("legal_hold", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_managed_documents_tenant_id", "managed_documents", ["tenant_id"])
    op.create_index("ix_managed_documents_workspace_id", "managed_documents", ["workspace_id"])
    op.create_index("ix_managed_documents_status", "managed_documents", ["status"])
    op.create_index("ix_managed_documents_classification", "managed_documents", ["classification"])

    # 8. managed_document_versions
    op.create_table(
        "managed_document_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=True),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("storage_key", sa.String(length=500), nullable=True),
        sa.Column("change_summary", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_managed_document_versions_document_id", "managed_document_versions", ["document_id"])

    # 9. document_extractions
    op.create_table(
        "document_extractions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("chunks_json", sa.JSON(), nullable=True),
        sa.Column("extraction_source", sa.String(length=50), nullable=False, server_default="NATIVE_TEXT"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("extracted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 10. document_reviews
    op.create_table(
        "document_reviews",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("requested_by", sa.String(length=36), nullable=False),
        sa.Column("reviewer_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUBMITTED_FOR_REVIEW"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 11. document_approvals
    op.create_table(
        "document_approvals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("approver_id", sa.String(length=36), nullable=False),
        sa.Column("approver_role", sa.String(length=50), nullable=False),
        sa.Column("decision", sa.String(length=50), nullable=False, server_default="APPROVED"),
        sa.Column("decision_notes", sa.Text(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 12. document_shares
    op.create_table(
        "document_shares",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("shared_by", sa.String(length=36), nullable=False),
        sa.Column("share_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", sa.String(length=36), nullable=False),
        sa.Column("permissions_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 13. document_share_links
    op.create_table(
        "document_share_links",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("permissions_json", sa.JSON(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("access_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("has_passcode", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("passcode_hash", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )

    # 14. document_comments
    op.create_table(
        "document_comments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=True),
        sa.Column("parent_id", sa.String(length=36), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("visibility", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 15. document_legal_holds
    op.create_table(
        "document_legal_holds",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("applied_by", sa.String(length=36), nullable=False),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("released_by", sa.String(length=36), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["document_id"], ["managed_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("document_legal_holds")
    op.drop_table("document_comments")
    op.drop_table("document_share_links")
    op.drop_table("document_shares")
    op.drop_table("document_approvals")
    op.drop_table("document_reviews")
    op.drop_table("document_extractions")
    op.drop_table("managed_document_versions")
    op.drop_table("managed_documents")
    op.drop_table("folders")
    op.drop_table("file_access_logs")
    op.drop_table("file_scans")
    op.drop_table("file_metadata")
    op.drop_table("file_versions")
    op.drop_table("files")
