"""add autonomous cybersecurity zero trust tables

Revision ID: 059
Revises: 058
Create Date: 2026-09-13 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '059'
down_revision = '058'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Assets
    op.create_table(
        'czt_assets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('asset_type', sa.String(length=64), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('environment', sa.String(length=32), nullable=True),
        sa.Column('criticality', sa.String(length=32), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('hostname', sa.String(length=256), nullable=True),
        sa.Column('location', sa.String(length=128), nullable=True),
        sa.Column('security_state', sa.String(length=32), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('metadata_context', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_asset_relationships',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_asset_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('target_asset_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('relationship_type', sa.String(length=64), nullable=False),
        sa.Column('protocol', sa.String(length=32), nullable=True),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 2. Identities
    op.create_table(
        'czt_identities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('principal_id', sa.String(length=128), nullable=False, index=True),
        sa.Column('identity_type', sa.String(length=64), nullable=False),
        sa.Column('email_or_handle', sa.String(length=256), nullable=True),
        sa.Column('display_name', sa.String(length=256), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('is_privileged', sa.Boolean(), nullable=True),
        sa.Column('mfa_enforced', sa.Boolean(), nullable=True),
        sa.Column('current_risk_level', sa.String(length=32), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('last_authenticated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_identity_roles',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('identity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('role_name', sa.String(length=128), nullable=False),
        sa.Column('scope', sa.String(length=128), nullable=True),
        sa.Column('granted_by', sa.String(length=128), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_identity_risk',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('identity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('anomaly_factor', sa.String(length=128), nullable=False),
        sa.Column('factor_score', sa.Float(), nullable=True),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
    )

    # 3. Devices & Machines
    op.create_table(
        'czt_devices',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('device_name', sa.String(length=256), nullable=False),
        sa.Column('owner_identity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('platform', sa.String(length=64), nullable=True),
        sa.Column('os_version', sa.String(length=128), nullable=True),
        sa.Column('is_managed', sa.Boolean(), nullable=True),
        sa.Column('is_encrypted', sa.Boolean(), nullable=True),
        sa.Column('edr_installed', sa.Boolean(), nullable=True),
        sa.Column('posture_status', sa.String(length=32), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_device_posture',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('device_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('firewall_enabled', sa.Boolean(), nullable=True),
        sa.Column('patches_up_to_date', sa.Boolean(), nullable=True),
        sa.Column('secure_boot_enabled', sa.Boolean(), nullable=True),
        sa.Column('compromise_indicators_detected', sa.Boolean(), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_service_identities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('service_name', sa.String(length=128), nullable=False, index=True),
        sa.Column('namespace', sa.String(length=128), nullable=True),
        sa.Column('allowed_endpoints', sa.JSON(), nullable=True),
        sa.Column('certificate_thumbprint', sa.String(length=128), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_agent_identities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('agent_id', sa.String(length=128), nullable=False, index=True),
        sa.Column('agent_name', sa.String(length=256), nullable=False),
        sa.Column('allowed_tools', sa.JSON(), nullable=True),
        sa.Column('data_access_scopes', sa.JSON(), nullable=True),
        sa.Column('max_risk_tolerance', sa.Float(), nullable=True),
        sa.Column('requires_human_approval', sa.Boolean(), nullable=True),
        sa.Column('is_sandboxed', sa.Boolean(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 4. Zero-Trust Policies
    op.create_table(
        'czt_policies',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('effect', sa.String(length=32), nullable=True),
        sa.Column('target_resource', sa.String(length=256), nullable=False),
        sa.Column('action_pattern', sa.String(length=128), nullable=True),
        sa.Column('conditions', sa.JSON(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_policy_decisions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('subject_id', sa.String(length=128), nullable=False),
        sa.Column('subject_type', sa.String(length=64), nullable=False),
        sa.Column('resource', sa.String(length=256), nullable=False),
        sa.Column('action', sa.String(length=128), nullable=False),
        sa.Column('decision', sa.String(length=32), nullable=False),
        sa.Column('eval_reasons', sa.JSON(), nullable=True),
        sa.Column('context_snapshot', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_privileged_access_requests',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('requester_id', sa.String(length=128), nullable=False),
        sa.Column('target_role', sa.String(length=128), nullable=False),
        sa.Column('justification', sa.Text(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('approved_by', sa.String(length=128), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    # 5. Sessions, Secrets, Certificates
    op.create_table(
        'czt_sessions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('identity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('device_id', sa.String(length=64), nullable=True),
        sa.Column('session_token_hash', sa.String(length=128), nullable=False, unique=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=512), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True),
        sa.Column('requires_step_up', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'czt_tokens',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('identity_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('token_name', sa.String(length=128), nullable=False),
        sa.Column('token_prefix', sa.String(length=16), nullable=False),
        sa.Column('hashed_secret', sa.String(length=128), nullable=False),
        sa.Column('scopes', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_secrets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('secret_name', sa.String(length=256), nullable=False, index=True),
        sa.Column('vault_reference_key', sa.String(length=256), nullable=False),
        sa.Column('secret_type', sa.String(length=64), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('rotation_period_days', sa.Integer(), nullable=True),
        sa.Column('last_rotated_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_certificates',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('domain_name', sa.String(length=256), nullable=False),
        sa.Column('issuer', sa.String(length=256), nullable=False),
        sa.Column('thumbprint_sha256', sa.String(length=128), nullable=False, unique=True),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_until', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('auto_renew', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 6. SIEM Events & Detections
    op.create_table(
        'czt_security_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source', sa.String(length=64), nullable=False),
        sa.Column('actor_id', sa.String(length=128), nullable=False, index=True),
        sa.Column('action', sa.String(length=128), nullable=False, index=True),
        sa.Column('target_resource', sa.String(length=256), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, index=True),
    )

    op.create_table(
        'czt_detection_rules',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('rule_type', sa.String(length=64), nullable=True),
        sa.Column('query_condition', sa.JSON(), nullable=True),
        sa.Column('window_seconds', sa.Integer(), nullable=True),
        sa.Column('threshold_count', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('mitre_attack_id', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_alerts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('rule_id', sa.String(length=64), nullable=True, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('actor_id', sa.String(length=128), nullable=False),
        sa.Column('affected_asset_id', sa.String(length=64), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('contributing_event_ids', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, index=True),
    )

    op.create_table(
        'czt_alert_correlations',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('correlation_pattern', sa.String(length=128), nullable=False),
        sa.Column('alert_ids', sa.JSON(), nullable=True),
        sa.Column('composite_risk_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 7. Threat Intelligence
    op.create_table(
        'czt_threat_indicators',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('indicator_type', sa.String(length=32), nullable=False),
        sa.Column('value', sa.String(length=512), nullable=False, index=True),
        sa.Column('threat_actor', sa.String(length=128), nullable=True),
        sa.Column('campaign', sa.String(length=128), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('source_feed', sa.String(length=128), nullable=True),
        sa.Column('first_seen', sa.DateTime(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
    )

    # 8. Vulnerabilities & SBOM
    op.create_table(
        'czt_vulnerabilities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('cve_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cvss_score', sa.Float(), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('affected_asset_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('package_name', sa.String(length=128), nullable=True),
        sa.Column('fixed_version', sa.String(length=64), nullable=True),
        sa.Column('exploitability', sa.String(length=32), nullable=True),
        sa.Column('remediation_status', sa.String(length=32), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_sbom_components',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('application_name', sa.String(length=128), nullable=False, index=True),
        sa.Column('component_name', sa.String(length=128), nullable=False),
        sa.Column('version', sa.String(length=64), nullable=False),
        sa.Column('license', sa.String(length=64), nullable=True),
        sa.Column('vulnerabilities_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # 9. Incidents & Forensics
    op.create_table(
        'czt_incidents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('assigned_analyst', sa.String(length=128), nullable=True),
        sa.Column('affected_assets', sa.JSON(), nullable=True),
        sa.Column('impact_summary', sa.Text(), nullable=True),
        sa.Column('root_cause', sa.Text(), nullable=True),
        sa.Column('containment_action', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, index=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_incident_timeline',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('incident_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('event_title', sa.String(length=256), nullable=False),
        sa.Column('event_type', sa.String(length=64), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source', sa.String(length=64), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_incident_evidence',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('incident_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('evidence_type', sa.String(length=64), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=False),
        sa.Column('sha256_hash', sa.String(length=64), nullable=False),
        sa.Column('storage_uri', sa.String(length=512), nullable=True),
        sa.Column('chain_of_custody', sa.JSON(), nullable=True),
        sa.Column('collected_at', sa.DateTime(), nullable=True),
    )

    # 10. Playbooks
    op.create_table(
        'czt_playbooks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('trigger_type', sa.String(length=64), nullable=True),
        sa.Column('steps', sa.JSON(), nullable=True),
        sa.Column('requires_human_signoff', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_playbook_runs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('playbook_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('incident_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('executed_steps', sa.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )

    # 11. AI Security
    op.create_table(
        'czt_ai_security_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('agent_id', sa.String(length=128), nullable=False, index=True),
        sa.Column('event_category', sa.String(length=64), nullable=False),
        sa.Column('detected_payload', sa.Text(), nullable=True),
        sa.Column('risk_level', sa.String(length=32), nullable=True),
        sa.Column('action_taken', sa.String(length=32), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )

    # 12. Security Graph
    op.create_table(
        'czt_graph_nodes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('entity_name', sa.String(length=256), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=True),
    )

    op.create_table(
        'czt_graph_edges',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('source_node_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('target_node_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('relationship_type', sa.String(length=64), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
    )

    # 13. Compliance & Audit
    op.create_table(
        'czt_compliance_controls',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('framework', sa.String(length=64), nullable=False),
        sa.Column('control_code', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('automated_check', sa.Boolean(), nullable=True),
        sa.Column('last_evaluated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'czt_audit_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('actor_id', sa.String(length=128), nullable=False),
        sa.Column('action', sa.String(length=128), nullable=False),
        sa.Column('resource', sa.String(length=256), nullable=False),
        sa.Column('decision', sa.String(length=32), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('metadata_context', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('czt_audit_events')
    op.drop_table('czt_compliance_controls')
    op.drop_table('czt_graph_edges')
    op.drop_table('czt_graph_nodes')
    op.drop_table('czt_ai_security_events')
    op.drop_table('czt_playbook_runs')
    op.drop_table('czt_playbooks')
    op.drop_table('czt_incident_evidence')
    op.drop_table('czt_incident_timeline')
    op.drop_table('czt_incidents')
    op.drop_table('czt_sbom_components')
    op.drop_table('czt_vulnerabilities')
    op.drop_table('czt_threat_indicators')
    op.drop_table('czt_alert_correlations')
    op.drop_table('czt_alerts')
    op.drop_table('czt_detection_rules')
    op.drop_table('czt_security_events')
    op.drop_table('czt_certificates')
    op.drop_table('czt_secrets')
    op.drop_table('czt_tokens')
    op.drop_table('czt_sessions')
    op.drop_table('czt_privileged_access_requests')
    op.drop_table('czt_policy_decisions')
    op.drop_table('czt_policies')
    op.drop_table('czt_agent_identities')
    op.drop_table('czt_service_identities')
    op.drop_table('czt_device_posture')
    op.drop_table('czt_devices')
    op.drop_table('czt_identity_risk')
    op.drop_table('czt_identity_roles')
    op.drop_table('czt_identities')
    op.drop_table('czt_asset_relationships')
    op.drop_table('czt_assets')
