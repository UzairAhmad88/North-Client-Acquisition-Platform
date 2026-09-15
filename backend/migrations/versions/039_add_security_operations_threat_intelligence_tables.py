"""add_security_operations_threat_intelligence_tables

Revision ID: 039
Revises: 038
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "039"
down_revision = "038"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. security_detections
    op.create_table(
        "security_detections",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("rule_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("rule_name", sa.String(length=200), nullable=False),
        sa.Column("anomaly_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("severity", sa.String(length=50), nullable=False, index=True),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("mitre_technique_id", sa.String(length=50), nullable=True),
        sa.Column("mitre_tactic", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_events", sa.JSON(), nullable=False),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. security_detection_rules
    op.create_table(
        "security_detection_rules",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("rule_type", sa.String(length=50), nullable=False, server_default="DETERMINISTIC"),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("anomaly_type", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3. security_alerts
    op.create_table(
        "security_alerts",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("detection_id", sa.String(length=100), nullable=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, index=True),
        sa.Column("status", sa.String(length=50), nullable=False, index=True),
        sa.Column("anomaly_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("mitre_technique_id", sa.String(length=50), nullable=True),
        sa.Column("mitre_tactic", sa.String(length=100), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("affected_actor_id", sa.String(length=150), nullable=True, index=True),
        sa.Column("affected_target_id", sa.String(length=150), nullable=True),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("assigned_to", sa.String(length=150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 4. security_alert_events
    op.create_table(
        "security_alert_events",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("alert_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_alerts.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("security_event_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 5. security_incidents
    op.create_table(
        "security_incidents",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, index=True),
        sa.Column("status", sa.String(length=50), nullable=False, index=True),
        sa.Column("category", sa.String(length=100), nullable=False, index=True),
        sa.Column("detection_source", sa.String(length=100), nullable=False),
        sa.Column("affected_tenants", sa.JSON(), nullable=False),
        sa.Column("affected_users", sa.JSON(), nullable=False),
        sa.Column("affected_services", sa.JSON(), nullable=False),
        sa.Column("affected_resources", sa.JSON(), nullable=False),
        sa.Column("timeline", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("containment_actions", sa.JSON(), nullable=False),
        sa.Column("remediation_actions", sa.JSON(), nullable=False),
        sa.Column("business_impact", sa.Text(), nullable=True),
        sa.Column("security_impact", sa.Text(), nullable=True),
        sa.Column("owner", sa.String(length=150), nullable=True),
        sa.Column("approvals", sa.JSON(), nullable=False),
        sa.Column("resolution", sa.Text(), nullable=True),
        sa.Column("postmortem", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 6. security_incident_events
    op.create_table(
        "security_incident_events",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("incident_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("security_event_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 7. security_investigations
    op.create_table(
        "security_investigations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("incident_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("lead_investigator", sa.String(length=150), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("hypotheses", sa.JSON(), nullable=False),
        sa.Column("investigation_steps", sa.JSON(), nullable=False),
        sa.Column("evidence_graph", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 8. security_attack_chains
    op.create_table(
        "security_attack_chains",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("incident_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_incidents.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("stages", sa.JSON(), nullable=False),
        sa.Column("affected_principal", sa.String(length=150), nullable=True, index=True),
        sa.Column("supporting_evidence", sa.JSON(), nullable=False),
        sa.Column("contradicting_evidence", sa.JSON(), nullable=False),
        sa.Column("recommended_investigation_steps", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 9. security_blast_radius
    op.create_table(
        "security_blast_radius",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("incident_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("overall_impact_score", sa.Float(), nullable=False),
        sa.Column("affected_users", sa.JSON(), nullable=False),
        sa.Column("affected_clients", sa.JSON(), nullable=False),
        sa.Column("affected_tenants", sa.JSON(), nullable=False),
        sa.Column("affected_services", sa.JSON(), nullable=False),
        sa.Column("affected_projects", sa.JSON(), nullable=False),
        sa.Column("affected_documents", sa.JSON(), nullable=False),
        sa.Column("affected_financial_records", sa.JSON(), nullable=False),
        sa.Column("affected_integrations", sa.JSON(), nullable=False),
        sa.Column("affected_ai_agents", sa.JSON(), nullable=False),
        sa.Column("affected_workflows", sa.JSON(), nullable=False),
        sa.Column("narrative_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 10. security_runbooks
    op.create_table(
        "security_runbooks",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False, server_default="INCIDENT_RESPONSE"),
        sa.Column("trigger_anomaly", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("requires_dual_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("rollback_steps", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 11. security_remediation_runs
    op.create_table(
        "security_remediation_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("incident_id", sa.Uuid(as_uuid=True), sa.ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("action_type", sa.String(length=100), nullable=False, index=True),
        sa.Column("target_type", sa.String(length=100), nullable=False),
        sa.Column("target_id", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending_approval", index=True),
        sa.Column("requested_by", sa.String(length=150), nullable=False),
        sa.Column("approved_by", sa.String(length=150), nullable=True),
        sa.Column("idempotency_key", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("execution_result", sa.JSON(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 12. security_threat_indicators
    op.create_table(
        "security_threat_indicators",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("indicator_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("indicator_value", sa.String(length=255), nullable=False, index=True),
        sa.Column("threat_category", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="medium"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.8"),
        sa.Column("source", sa.String(length=100), nullable=False, server_default="INTERNAL"),
        sa.Column("reputation", sa.Integer(), nullable=False, server_default="80"),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true"), index=True),
        sa.Column("metadata_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 13. security_behavior_baselines
    op.create_table(
        "security_behavior_baselines",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("entity_type", sa.String(length=50), nullable=False, index=True),
        sa.Column("entity_id", sa.String(length=150), nullable=False, index=True),
        sa.Column("metric_name", sa.String(length=100), nullable=False, index=True),
        sa.Column("baseline_mean", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("baseline_stddev", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("sample_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 14. security_posture_snapshots
    op.create_table(
        "security_posture_snapshots",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("posture_grade", sa.String(length=10), nullable=False, server_default="A"),
        sa.Column("composite_risk_score", sa.Float(), nullable=False, server_default="15.0"),
        sa.Column("overall_status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("open_critical_incidents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("high_risk_alerts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("domain_scores", sa.JSON(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 15. security_ai_runs
    op.create_table(
        "security_ai_runs",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("agent_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("run_type", sa.String(length=100), nullable=False, server_default="INVESTIGATION_SUMMARY"),
        sa.Column("query_or_prompt", sa.Text(), nullable=False),
        sa.Column("response_summary", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.85"),
        sa.Column("evidence_sources", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("prohibited_actions_checked", sa.JSON(), nullable=False),
        sa.Column("execution_time_ms", sa.Integer(), nullable=False, server_default="250"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 16. security_audit_records
    op.create_table(
        "security_audit_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, index=True),
        sa.Column("action", sa.String(length=150), nullable=False, index=True),
        sa.Column("actor_id", sa.String(length=150), nullable=False, index=True),
        sa.Column("actor_role", sa.String(length=100), nullable=False, server_default="SECURITY_OPERATOR"),
        sa.Column("target_resource", sa.String(length=200), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("ip_address", sa.String(length=100), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("security_audit_records")
    op.drop_table("security_ai_runs")
    op.drop_table("security_posture_snapshots")
    op.drop_table("security_behavior_baselines")
    op.drop_table("security_threat_indicators")
    op.drop_table("security_remediation_runs")
    op.drop_table("security_runbooks")
    op.drop_table("security_blast_radius")
    op.drop_table("security_attack_chains")
    op.drop_table("security_investigations")
    op.drop_table("security_incident_events")
    op.drop_table("security_incidents")
    op.drop_table("security_alert_events")
    op.drop_table("security_alerts")
    op.drop_table("security_detection_rules")
    op.drop_table("security_detections")
