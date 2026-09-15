"""add_unified_governance_grc_privacy_tables

Revision ID: 040
Revises: 039
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "040"
down_revision = "039"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. governance_frameworks
    op.create_table(
        "governance_frameworks",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("framework_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False, server_default="1.0"),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("jurisdiction", sa.String(length=100), nullable=False, server_default="GLOBAL"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="compliance_officer"),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("effective_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. governance_requirements
    op.create_table(
        "governance_requirements",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("framework_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("requirement_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="IMPLEMENTED"),
        sa.Column("interpretation_notes", sa.Text(), nullable=True),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. governance_applicability_assessments
    op.create_table(
        "governance_applicability_assessments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("requirement_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("decision", sa.String(length=50), nullable=False),
        sa.Column("justification", sa.Text(), nullable=False),
        sa.Column("reviewer_id", sa.String(length=100), nullable=False),
        sa.Column("policy_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("evidence_references", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. governance_controls
    op.create_table(
        "governance_controls",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("domain", sa.String(length=100), nullable=False, index=True),
        sa.Column("control_type", sa.String(length=50), nullable=False, server_default="PREVENTIVE"),
        sa.Column("frequency", sa.String(length=50), nullable=False, server_default="CONTINUOUS"),
        sa.Column("automation_level", sa.String(length=50), nullable=False, server_default="AUTOMATED"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("operator_id", sa.String(length=100), nullable=False, server_default="system_automated"),
        sa.Column("health_status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("test_method", sa.String(length=100), nullable=False, server_default="AUTOMATED_PROBE"),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. governance_control_implementations
    op.create_table(
        "governance_control_implementations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("component_type", sa.String(length=100), nullable=False),
        sa.Column("component_reference", sa.String(length=300), nullable=False),
        sa.Column("verification_rule", sa.String(length=200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. governance_evidence
    op.create_table(
        "governance_evidence",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("evidence_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("source_subsystem", sa.String(length=100), nullable=False),
        sa.Column("source_record_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False, index=True),
        sa.Column("provenance_uri", sa.String(length=300), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("data_payload", sa.JSON(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("freshness_status", sa.String(length=50), nullable=False, server_default="FRESH"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. governance_evidence_links
    op.create_table(
        "governance_evidence_links",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("evidence_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. governance_control_tests
    op.create_table(
        "governance_control_tests",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("test_name", sa.String(length=200), nullable=False),
        sa.Column("test_type", sa.String(length=50), nullable=False, server_default="OPERATING_EFFECTIVENESS"),
        sa.Column("execution_frequency", sa.String(length=50), nullable=False, server_default="DAILY"),
        sa.Column("test_script_ref", sa.String(length=300), nullable=True),
        sa.Column("is_automated", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. governance_control_test_runs
    op.create_table(
        "governance_control_test_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("test_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("result", sa.String(length=50), nullable=False),
        sa.Column("details", sa.Text(), nullable=False),
        sa.Column("executed_by", sa.String(length=100), nullable=False, server_default="system_automated"),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. governance_risks
    op.create_table(
        "governance_risks",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("risk_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("threat", sa.Text(), nullable=False),
        sa.Column("vulnerability", sa.Text(), nullable=False),
        sa.Column("likelihood", sa.Float(), nullable=False),
        sa.Column("impact", sa.Float(), nullable=False),
        sa.Column("inherent_risk_score", sa.Float(), nullable=False),
        sa.Column("residual_risk_score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("treatment", sa.String(length=50), nullable=False, server_default="MITIGATE"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("mitigating_controls", sa.JSON(), nullable=False),
        sa.Column("accepted_by", sa.String(length=100), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. governance_exceptions
    op.create_table(
        "governance_exceptions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("exception_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("control_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("compensating_controls", sa.JSON(), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("requester_id", sa.String(length=100), nullable=False),
        sa.Column("approver_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="REQUESTED"),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. governance_findings
    op.create_table(
        "governance_findings",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("finding_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. governance_remediation_plans
    op.create_table(
        "governance_remediation_plans",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("finding_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("plan_title", sa.String(length=250), nullable=False),
        sa.Column("actions", sa.JSON(), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PLANNED"),
        sa.Column("verified_by", sa.String(length=100), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. governance_audits
    op.create_table(
        "governance_audits",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("audit_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("framework_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("lead_auditor", sa.String(length=100), nullable=False),
        sa.Column("audit_type", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PLANNING"),
        sa.Column("scope_controls", sa.JSON(), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. governance_audit_requests
    op.create_table(
        "governance_audit_requests",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("audit_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("request_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("control_code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("assigned_to", sa.String(length=100), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. governance_attestations
    op.create_table(
        "governance_attestations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("attestation_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("scope", sa.String(length=250), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("framework_code", sa.String(length=100), nullable=False),
        sa.Column("preparer_id", sa.String(length=100), nullable=False),
        sa.Column("approver_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("attested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 17. privacy_processing_activities
    op.create_table(
        "privacy_processing_activities",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("activity_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("data_categories", sa.JSON(), nullable=False),
        sa.Column("data_subject_categories", sa.JSON(), nullable=False),
        sa.Column("systems", sa.JSON(), nullable=False),
        sa.Column("retention_period_days", sa.Integer(), nullable=False, server_default="365"),
        sa.Column("security_controls", sa.JSON(), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 18. privacy_consent_records
    op.create_table(
        "privacy_consent_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("subject_id", sa.String(length=150), nullable=False, index=True),
        sa.Column("purpose", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False, server_default="EMAIL"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="GRANTED"),
        sa.Column("granted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("withdrawn_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 19. privacy_requests
    op.create_table(
        "privacy_requests",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("request_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("subject_id", sa.String(length=150), nullable=False, index=True),
        sa.Column("request_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="RECEIVED"),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assigned_to", sa.String(length=100), nullable=False, server_default="dpo_lead"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 20. vendor_profiles
    op.create_table(
        "vendor_profiles",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("vendor_code", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("service_provided", sa.String(length=200), nullable=False),
        sa.Column("criticality", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("data_access_level", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("security_risk", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("privacy_risk", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("dependent_services", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 21. vendor_risk_assessments
    op.create_table(
        "vendor_risk_assessments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("vendor_code", sa.String(length=100), nullable=False, index=True),
        sa.Column("assessor_id", sa.String(length=100), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="85.0"),
        sa.Column("findings", sa.JSON(), nullable=False),
        sa.Column("recommendation", sa.String(length=50), nullable=False, server_default="APPROVE"),
        sa.Column("assessed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("next_review_due", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 22. governance_posture_snapshots
    op.create_table(
        "governance_posture_snapshots",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("composite_compliance_score", sa.Float(), nullable=False),
        sa.Column("overall_health", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("total_requirements", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("implemented_requirements", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_controls", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("healthy_controls", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failing_controls", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("open_findings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("critical_findings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active_exceptions_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("stale_evidence_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("domain_scores", sa.JSON(), nullable=False),
        sa.Column("technical_debt_score", sa.Float(), nullable=False, server_default="10.0"),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("governance_posture_snapshots")
    op.drop_table("vendor_risk_assessments")
    op.drop_table("vendor_profiles")
    op.drop_table("privacy_requests")
    op.drop_table("privacy_consent_records")
    op.drop_table("privacy_processing_activities")
    op.drop_table("governance_attestations")
    op.drop_table("governance_audit_requests")
    op.drop_table("governance_audits")
    op.drop_table("governance_remediation_plans")
    op.drop_table("governance_findings")
    op.drop_table("governance_exceptions")
    op.drop_table("governance_risks")
    op.drop_table("governance_control_test_runs")
    op.drop_table("governance_control_tests")
    op.drop_table("governance_evidence_links")
    op.drop_table("governance_evidence")
    op.drop_table("governance_control_implementations")
    op.drop_table("governance_controls")
    op.drop_table("governance_applicability_assessments")
    op.drop_table("governance_requirements")
    op.drop_table("governance_frameworks")
