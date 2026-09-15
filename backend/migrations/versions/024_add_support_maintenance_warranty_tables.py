"""add_support_maintenance_warranty_tables

Revision ID: 024
Revises: 023
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "024"
down_revision = "023"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Support Requests
    op.create_table(
        "support_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("request_number", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("business_id", sa.String(length=36), nullable=True),
        sa.Column("client_account_id", sa.String(length=36), nullable=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("release_version_id", sa.String(length=36), nullable=True),
        sa.Column("requester", sa.String(length=255), nullable=False),
        sa.Column("requester_email", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="APPLICATION"),
        sa.Column("classification", sa.String(length=64), nullable=False, server_default="UNKNOWN"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="NEW"),
        sa.Column("warranty_status", sa.String(length=32), nullable=False, server_default="UNKNOWN"),
        sa.Column("maintenance_status", sa.String(length=32), nullable=False, server_default="NOT_APPLICABLE"),
        sa.Column("sla_status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("assigned_to", sa.String(length=255), nullable=True),
        sa.Column("resolution_summary", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["release_version_id"], ["release_versions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_number"),
    )
    op.create_index(op.f("ix_support_requests_request_number"), "support_requests", ["request_number"], unique=True)
    op.create_index(op.f("ix_support_requests_project_id"), "support_requests", ["project_id"], unique=False)
    op.create_index(op.f("ix_support_requests_status"), "support_requests", ["status"], unique=False)
    op.create_index(op.f("ix_support_requests_classification"), "support_requests", ["classification"], unique=False)

    # 2. Support Request Versions
    op.create_table(
        "support_request_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("support_request_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["support_request_id"], ["support_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_support_request_versions_support_request_id"), "support_request_versions", ["support_request_id"], unique=False)

    # 3. Support Request Events
    op.create_table(
        "support_request_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("support_request_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=255), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False, server_default="USER"),
        sa.Column("event_data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["support_request_id"], ["support_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_support_request_events_support_request_id"), "support_request_events", ["support_request_id"], unique=False)

    # 4. Support Request Evidence
    op.create_table(
        "support_request_evidence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("support_request_id", sa.String(length=36), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=512), nullable=False),
        sa.Column("file_type", sa.String(length=64), nullable=False, server_default="SCREENSHOT"),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("uploaded_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["support_request_id"], ["support_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_support_request_evidence_support_request_id"), "support_request_evidence", ["support_request_id"], unique=False)

    # 5. Incidents
    op.create_table(
        "incidents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("incident_number", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="SEV-2"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DETECTED"),
        sa.Column("affected_service", sa.String(length=128), nullable=False, server_default="CORE_APP"),
        sa.Column("impact_summary", sa.Text(), nullable=True),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("mitigation_steps", sa.Text(), nullable=True),
        sa.Column("postmortem", sa.Text(), nullable=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mitigated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("incident_number"),
    )
    op.create_index(op.f("ix_incidents_incident_number"), "incidents", ["incident_number"], unique=True)
    op.create_index(op.f("ix_incidents_project_id"), "incidents", ["project_id"], unique=False)
    op.create_index(op.f("ix_incidents_status"), "incidents", ["status"], unique=False)
    op.create_index(op.f("ix_incidents_severity"), "incidents", ["severity"], unique=False)

    # 6. Incident Timelines
    op.create_table(
        "incident_timelines",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("incident_id", sa.String(length=36), nullable=False),
        sa.Column("milestone", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("recorded_by", sa.String(length=255), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_incident_timelines_incident_id"), "incident_timelines", ["incident_id"], unique=False)

    # 7. Warranties
    op.create_table(
        "warranties",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False, server_default="Standard Deliverable Warranty"),
        sa.Column("terms", sa.Text(), nullable=True),
        sa.Column("exclusions", sa.Text(), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )
    op.create_index(op.f("ix_warranties_project_id"), "warranties", ["project_id"], unique=True)
    op.create_index(op.f("ix_warranties_status"), "warranties", ["status"], unique=False)

    # 8. Maintenance Plans
    op.create_table(
        "maintenance_plans",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("plan_type", sa.String(length=64), nullable=False, server_default="STANDARD"),
        sa.Column("scope_description", sa.Text(), nullable=False),
        sa.Column("frequency", sa.String(length=32), nullable=False, server_default="MONTHLY"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_maintenance_plans_project_id"), "maintenance_plans", ["project_id"], unique=False)
    op.create_index(op.f("ix_maintenance_plans_status"), "maintenance_plans", ["status"], unique=False)

    # 9. Maintenance Work Orders
    op.create_table(
        "maintenance_work_orders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("maintenance_plan_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("task_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="ROUTINE_BACKUP"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PLANNED"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("executed_by", sa.String(length=255), nullable=True),
        sa.Column("result_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["maintenance_plan_id"], ["maintenance_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_maintenance_work_orders_maintenance_plan_id"), "maintenance_work_orders", ["maintenance_plan_id"], unique=False)
    op.create_index(op.f("ix_maintenance_work_orders_status"), "maintenance_work_orders", ["status"], unique=False)

    # 10. SLA Policies
    op.create_table(
        "sla_policies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("response_target_hours", sa.Float(), nullable=False, server_default="4.0"),
        sa.Column("resolution_target_hours", sa.Float(), nullable=False, server_default="24.0"),
        sa.Column("business_hours_only", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )

    # 11. Knowledge Articles
    op.create_table(
        "knowledge_articles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("article_type", sa.String(length=64), nullable=False, server_default="USER_GUIDE"),
        sa.Column("visibility", sa.String(length=32), nullable=False, server_default="CLIENT_VISIBLE"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PUBLISHED"),
        sa.Column("author", sa.String(length=255), nullable=False, server_default="System"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_knowledge_articles_project_id"), "knowledge_articles", ["project_id"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_status"), "knowledge_articles", ["status"], unique=False)

    # 12. Monitoring Events
    op.create_table(
        "monitoring_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("signal_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="HEALTHY"),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_monitoring_events_project_id"), "monitoring_events", ["project_id"], unique=False)

    # 13. Client Health Snapshots
    op.create_table(
        "client_health_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("business_id", sa.String(length=36), nullable=True),
        sa.Column("health_score", sa.Float(), nullable=False, server_default="85.0"),
        sa.Column("health_status", sa.String(length=32), nullable=False, server_default="HEALTHY"),
        sa.Column("open_tickets_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("incident_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("satisfaction_score", sa.Float(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_health_snapshots_project_id"), "client_health_snapshots", ["project_id"], unique=False)

    # 14. Support Opportunities
    op.create_table(
        "support_opportunities",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("business_id", sa.String(length=36), nullable=True),
        sa.Column("support_request_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("opportunity_type", sa.String(length=64), nullable=False, server_default="NEW_FEATURE"),
        sa.Column("estimated_value", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.85"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="OPPORTUNITY_DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["support_request_id"], ["support_requests.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_support_opportunities_project_id"), "support_opportunities", ["project_id"], unique=False)
    op.create_index(op.f("ix_support_opportunities_status"), "support_opportunities", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("support_opportunities")
    op.drop_table("client_health_snapshots")
    op.drop_table("monitoring_events")
    op.drop_table("knowledge_articles")
    op.drop_table("sla_policies")
    op.drop_table("maintenance_work_orders")
    op.drop_table("maintenance_plans")
    op.drop_table("warranties")
    op.drop_table("incident_timelines")
    op.drop_table("incidents")
    op.drop_table("support_request_evidence")
    op.drop_table("support_request_events")
    op.drop_table("support_request_versions")
    op.drop_table("support_requests")
