"""
Security Blast Radius Analysis Engine (Section 23).
Calculates downstream blast radius across 10 operational and business dimensions.
"""

from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone
import uuid

try:
    from app.security.base import BlastRadiusResult, SecurityIncident, SecurityEvent
except ImportError:
    from backend.app.security.base import BlastRadiusResult, SecurityIncident, SecurityEvent


class BlastRadiusEngine:
    """
    Quantifies the exact blast radius of a security detection or incident across:
    1. Users
    2. Clients
    3. Tenants
    4. Services
    5. Projects
    6. Documents
    7. Financial Records
    8. Integrations
    9. AI Agents
    10. Workflows
    """

    @classmethod
    def calculate_incident_blast_radius(
        cls,
        incident: SecurityIncident,
        related_events: Optional[List[SecurityEvent]] = None,
        context_topology: Optional[Dict[str, Any]] = None
    ) -> BlastRadiusResult:
        """
        Evaluates impacted entities and dependencies for the incident.
        """
        related_events = related_events or []
        context_topology = context_topology or {}

        affected_users: Set[str] = set(incident.affected_users)
        affected_tenants: Set[str] = set(incident.affected_tenants)
        affected_services: Set[str] = set(incident.affected_services)
        affected_resources: Set[str] = set(incident.affected_resources)
        affected_clients: Set[str] = set()
        affected_projects: Set[str] = set()
        affected_documents: Set[str] = set()
        affected_financial_records: Set[str] = set()
        affected_integrations: Set[str] = set()
        affected_agents: Set[str] = set()
        affected_workflows: Set[str] = set()

        if incident.tenant_id:
            affected_tenants.add(incident.tenant_id)

        # Scan related events
        for evt in related_events:
            if evt.user_id:
                affected_users.add(evt.user_id)
            if evt.principal_id:
                if evt.principal_type == "AGENT":
                    affected_agents.add(evt.principal_id)
                elif evt.principal_type == "USER":
                    affected_users.add(evt.principal_id)
                elif evt.principal_type == "SERVICE_ACCOUNT":
                    affected_services.add(evt.principal_id)

            if evt.agent_id:
                affected_agents.add(evt.agent_id)
            if evt.workflow_id:
                affected_workflows.add(evt.workflow_id)

            res_type = (evt.resource_type or "").lower()
            res_id = evt.resource_id or ""

            if "doc" in res_type or "file" in res_type:
                affected_documents.add(res_id or "unspecified_doc")
            elif "finan" in res_type or "pay" in res_type or "inv" in res_type:
                affected_financial_records.add(res_id or "unspecified_payment")
            elif "proj" in res_type:
                affected_projects.add(res_id or "unspecified_project")
            elif "client" in res_type:
                affected_clients.add(res_id or "unspecified_client")
            elif "integ" in res_type or evt.source.value == "integration":
                affected_integrations.add(res_id or "unspecified_integration")

        # Topologically inferred links
        if context_topology:
            for user in list(affected_users):
                if user in context_topology.get("user_projects", {}):
                    affected_projects.update(context_topology["user_projects"][user])
                if user in context_topology.get("user_clients", {}):
                    affected_clients.update(context_topology["user_clients"][user])

        # Compute impact score: Weighted sum of affected scopes
        # 1 user = 2 pts, 1 client = 10 pts, 1 tenant = 25 pts, 1 project = 5 pts, 1 fin record = 8 pts
        raw_score = (
            (len(affected_users) * 2.0) +
            (len(affected_clients) * 10.0) +
            (max(0, len(affected_tenants) - 1) * 35.0) +  # Penalty for multi-tenant breach
            (len(affected_services) * 5.0) +
            (len(affected_projects) * 4.0) +
            (len(affected_documents) * 1.5) +
            (len(affected_financial_records) * 8.0) +
            (len(affected_integrations) * 6.0) +
            (len(affected_agents) * 3.0) +
            (len(affected_workflows) * 4.0)
        )
        impact_score = round(min(100.0, max(5.0, raw_score)), 2)

        summary_parts = []
        if affected_tenants:
            summary_parts.append(f"{len(affected_tenants)} tenant(s)")
        if affected_users:
            summary_parts.append(f"{len(affected_users)} user(s)")
        if affected_clients:
            summary_parts.append(f"{len(affected_clients)} client(s)")
        if affected_agents:
            summary_parts.append(f"{len(affected_agents)} AI agent(s)")
        if affected_documents:
            summary_parts.append(f"{len(affected_documents)} document(s)")
        if affected_financial_records:
            summary_parts.append(f"{len(affected_financial_records)} financial record(s)")

        narrative = f"Incident blast radius spans {', '.join(summary_parts) if summary_parts else 'localized service resources'}."

        return BlastRadiusResult(
            radius_id=str(uuid.uuid4()),
            incident_id=incident.incident_id,
            tenant_id=incident.tenant_id,
            overall_impact_score=impact_score,
            affected_users=sorted(list(affected_users)),
            affected_clients=sorted(list(affected_clients)),
            affected_tenants=sorted(list(affected_tenants)),
            affected_services=sorted(list(affected_services)),
            affected_projects=sorted(list(affected_projects)),
            affected_documents=sorted(list(affected_documents)),
            affected_financial_records=sorted(list(affected_financial_records)),
            affected_integrations=sorted(list(affected_integrations)),
            affected_ai_agents=sorted(list(affected_agents)),
            affected_workflows=sorted(list(affected_workflows)),
            narrative_summary=narrative,
            calculated_at=datetime.now(timezone.utc)
        )
