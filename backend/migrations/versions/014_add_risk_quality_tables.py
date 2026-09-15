"""add_risk_quality_tables

Revision ID: 014
Revises: 013
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "014"
down_revision = "013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "risk_assessments",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("artifact_id", sa.String(length=255), nullable=False),
        sa.Column("artifact_type", sa.String(length=64), nullable=False, server_default="OUTREACH"),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("decision", sa.String(length=32), nullable=False, server_default="REVIEW"),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("quality_score", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("evidence_coverage", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("engine_version", sa.String(length=32), nullable=False, server_default="1.0.0"),
        sa.Column("policy_version", sa.String(length=32), nullable=False, server_default="v1"),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("artifact_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="COMPLETED"),
        sa.Column("human_override_decision", sa.String(length=32), nullable=True),
        sa.Column("human_override_reason", sa.Text(), nullable=True),
        sa.Column("human_override_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("human_override_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["human_override_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_risk_assessments_artifact_id"), "risk_assessments", ["artifact_id"], unique=False)
    op.create_index(op.f("ix_risk_assessments_artifact_type"), "risk_assessments", ["artifact_type"], unique=False)
    op.create_index(op.f("ix_risk_assessments_business_id"), "risk_assessments", ["business_id"], unique=False)
    op.create_index(op.f("ix_risk_assessments_lead_id"), "risk_assessments", ["lead_id"], unique=False)
    op.create_index(op.f("ix_risk_assessments_decision"), "risk_assessments", ["decision"], unique=False)
    op.create_index(op.f("ix_risk_assessments_risk_level"), "risk_assessments", ["risk_level"], unique=False)
    op.create_index(op.f("ix_risk_assessments_content_hash"), "risk_assessments", ["content_hash"], unique=False)

    op.create_table(
        "risk_findings",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("risk_assessment_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("rule_id", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("evidence_reference", sa.Text(), nullable=True),
        sa.Column("remediation", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["risk_assessment_id"], ["risk_assessments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_risk_findings_risk_assessment_id"), "risk_findings", ["risk_assessment_id"], unique=False)
    op.create_index(op.f("ix_risk_findings_rule_id"), "risk_findings", ["rule_id"], unique=False)
    op.create_index(op.f("ix_risk_findings_category"), "risk_findings", ["category"], unique=False)

    op.create_table(
        "quality_checks",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("risk_assessment_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("check_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["risk_assessment_id"], ["risk_assessments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quality_checks_risk_assessment_id"), "quality_checks", ["risk_assessment_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_quality_checks_risk_assessment_id"), table_name="quality_checks")
    op.drop_table("quality_checks")
    op.drop_index(op.f("ix_risk_findings_category"), table_name="risk_findings")
    op.drop_index(op.f("ix_risk_findings_rule_id"), table_name="risk_findings")
    op.drop_index(op.f("ix_risk_findings_risk_assessment_id"), table_name="risk_findings")
    op.drop_table("risk_findings")
    op.drop_index(op.f("ix_risk_assessments_content_hash"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_risk_level"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_decision"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_lead_id"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_business_id"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_artifact_type"), table_name="risk_assessments")
    op.drop_index(op.f("ix_risk_assessments_artifact_id"), table_name="risk_assessments")
    op.drop_table("risk_assessments")
