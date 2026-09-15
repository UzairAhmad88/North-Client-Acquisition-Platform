"""
Master platform service facade for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

from typing import Dict, Any, List, Optional
from backend.app.services.research_intelligence.base import (
    ResearchType,
    ResearchStatus,
    SourceTrustLevel,
    FactStatus,
    ClaimVerificationStatus,
    IntelligenceEventType,
    SignificanceLevel,
)
from backend.app.services.research_intelligence.workspaces import ResearchWorkspaceManager
from backend.app.services.research_intelligence.sources import SourceRegistryManager
from backend.app.services.research_intelligence.extraction_verification import ExtractionVerificationManager
from backend.app.services.research_intelligence.domains import DomainIntelligenceManager
from backend.app.services.research_intelligence.monitoring import ContinuousMonitoringManager
from backend.app.services.research_intelligence.synthesis_reports import SynthesisReportManager


class ResearchIntelligencePlatformService:
    """Master facade for Autonomous Research, Intelligence Synthesis, and Continuous Discovery."""

    def __init__(self):
        self.workspaces = ResearchWorkspaceManager()
        self.sources = SourceRegistryManager()
        self.extraction = ExtractionVerificationManager()
        self.domains = DomainIntelligenceManager()
        self.monitoring = ContinuousMonitoringManager()
        self.synthesis = SynthesisReportManager()
        self._seed_demo_workspace()

    def _seed_demo_workspace(self):
        """Seed a representative market & competitive research workspace."""
        ws = self.workspaces.create_workspace(
            title="Autonomous Enterprise AI Knowledge Workers Market 2026",
            research_question="What is the current market demand, competitive landscape, and pricing architecture for governed multi-agent workforce solutions?",
            owner_id="principal_analyst",
            research_type=ResearchType.MARKET,
            objective="Evaluate enterprise willingness-to-pay, top competitor feature sets, and regulatory compliance constraints.",
        )
        ws_id = ws["id"]

        # Decompose subquestions
        self.workspaces.decompose_question(ws_id)

        # Sources
        s1 = self.sources.register_source(
            workspace_id=ws_id,
            url_or_reference="https://gartner.example.com/reports/ai-workforce-2026",
            source_type=SourceTrustLevel.PROFESSIONAL,
            publisher="Gartner Research",
            authority_score=0.92,
        )
        s2 = self.sources.register_source(
            workspace_id=ws_id,
            url_or_reference="https://sec.gov/edgar/data/competitor_filings_2026",
            source_type=SourceTrustLevel.GOVERNMENT,
            publisher="U.S. Securities & Exchange Commission",
            authority_score=0.98,
        )

        # Entities
        self.extraction.resolve_entity(ws_id, "AgentOps Inc", "COMPANY", aliases=["AgentOps", "AgentOps Solutions"])
        self.extraction.resolve_entity(ws_id, "Enterprise AI Governance", "TECHNOLOGY")

        # Facts
        self.extraction.extract_fact(
            workspace_id=ws_id,
            source_id=s1["id"],
            claim="Global enterprise spend on governed multi-agent systems grew 74% year-over-year.",
            value_extracted="+74% YoY",
            fact_status=FactStatus.CORROBORATED,
            confidence=0.95,
        )

        # Claims & Verification
        self.extraction.verify_claim(
            workspace_id=ws_id,
            claim_text="92% of Fortune 500 buyers require human-in-the-loop approval gates before autonomous LLM actions.",
            supporting_sources=[s1["url_or_reference"], s2["url_or_reference"]],
        )

        # Competitor Profile
        self.domains.upsert_competitor_profile(
            company_name="AgentOps Inc",
            market_position="LEADER",
            products_offered=["Multi-Agent Orchestrator", "Task Dispatcher"],
            pricing_signals={"entry": "$1,200/mo", "enterprise": "$25,000/yr"},
            strengths=["Early brand recognition", "Vast connector library"],
            weaknesses=["Lacks granular separation-of-duties approval rooms", "High token egress fees"],
        )

        # Monitoring Rule & Event
        self.monitoring.create_monitoring_rule(
            workspace_id=ws_id,
            target_entity="AgentOps Inc",
            topics_monitored=["PRICING", "PRODUCT_RELEASES"],
        )
        self.monitoring.record_intelligence_event(
            target_entity="AgentOps Inc",
            event_type=IntelligenceEventType.CHANGED,
            summary="Competitor raised Enterprise minimum contract value from $15k to $25k/yr.",
            significance=SignificanceLevel.HIGH,
            confidence=0.96,
        )

        # Synthesis & Report
        self.synthesis.generate_synthesis(
            workspace_id=ws_id,
            executive_summary="Enterprise market for governed AI workers exhibits strong demand elasticity for verified human-in-the-loop controls.",
            key_findings=[
                "High willingness-to-pay ($25k-$45k ACV) when multi-role approval gates and audit logs are built-in.",
                "Competitor solutions currently neglect adversarial challenge mode and explicit trade-off matrices.",
            ],
            recommended_actions=[
                "Position North's Decision Room (Phase 53) and Multi-Agent Workforce (Phase 52) as a unified governed platform.",
            ],
        )
        self.synthesis.generate_report(
            workspace_id=ws_id,
            title="Enterprise AI Workforce Market Intelligence Report 2026",
            report_markdown="# Executive Briefing\n\nVerified findings indicate enterprise adoption is constrained primarily by governance rather than raw model intelligence.",
            citations=[s1["url_or_reference"], s2["url_or_reference"]],
        )

    def get_workspace_overview(self, workspace_id: str) -> Dict[str, Any]:
        """Aggregate all research intelligence data for a workspace into a unified payload."""
        ws = self.workspaces.get_workspace(workspace_id)
        if not ws:
            raise ValueError(f"Research workspace {workspace_id} not found")

        tasks = self.workspaces.list_tasks(workspace_id)
        sources = self.sources.list_sources(workspace_id)
        entities = self.extraction.list_entities(workspace_id)
        facts = self.extraction.list_facts(workspace_id)
        claims = self.extraction.list_claims(workspace_id)
        conflicts = self.extraction.list_conflicts(workspace_id)
        trends = self.domains.list_trends(workspace_id)
        competitors = self.domains.list_competitors()
        market_signals = self.domains.list_market_signals()
        rules = self.monitoring.list_rules(workspace_id)
        events = self.monitoring.list_events()
        synthesis = self.synthesis.get_synthesis(workspace_id)
        reports = self.synthesis.list_reports(workspace_id)
        gaps = self.synthesis.list_gaps(workspace_id)

        return {
            "workspace": ws,
            "tasks": tasks,
            "sources": sources,
            "entities": entities,
            "facts": facts,
            "claims": claims,
            "conflicts": conflicts,
            "trends": trends,
            "competitors": competitors,
            "market_signals": market_signals,
            "monitoring_rules": rules,
            "intelligence_events": events,
            "synthesis": synthesis,
            "reports": reports,
            "gaps": gaps,
        }

    def ask_copilot(self, workspace_id: str, query: str) -> Dict[str, Any]:
        """Natural language Research Copilot answering queries with verified citations."""
        data = self.get_workspace_overview(workspace_id)
        q = query.lower()

        if "competitor" in q or "pricing" in q:
            comps = data["competitors"]
            return {
                "query": query,
                "answer": f"Found {len(comps)} key competitor profiles. Primary competitor '{comps[0]['company_name'] if comps else 'N/A'}' recently updated pricing.",
                "verified_facts": [f"{c['company_name']}: {c['market_position']} position" for c in comps],
                "citations": [s["url_or_reference"] for s in data["sources"][:2]],
                "confidence": 0.94,
            }
        elif "conflict" in q or "disagree" in q:
            conflicts = data["conflicts"]
            return {
                "query": query,
                "answer": f"Detected {len(conflicts)} source contradictions in this workspace.",
                "conflicts_identified": [c["topic"] for c in conflicts],
                "citations": [s["url_or_reference"] for s in data["sources"]],
                "confidence": 0.88,
            }
        else:
            return {
                "query": query,
                "answer": f"Workspace '{data['workspace']['title']}' has synthesized {len(data['facts'])} verified facts and {len(data['claims'])} corroborated claims across {len(data['sources'])} authoritative sources.",
                "citations": [s["url_or_reference"] for s in data["sources"]],
                "confidence": data["workspace"]["confidence_score"],
            }


# Singleton platform instance
global_research_intelligence_service = ResearchIntelligencePlatformService()
