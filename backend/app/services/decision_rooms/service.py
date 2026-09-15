"""
Master platform service facade for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

from typing import Dict, Any, List, Optional
from backend.app.services.decision_rooms.base import (
    DecisionType,
    DecisionImportance,
    DecisionStatus,
    EvidenceType,
    StatementCategory,
    SpecialistRole,
    DisagreementCategory,
    ApprovalStatus,
)
from backend.app.services.decision_rooms.rooms import DecisionRoomManager
from backend.app.services.decision_rooms.context_evidence import ContextEvidenceManager
from backend.app.services.decision_rooms.assumptions_options import AssumptionOptionManager
from backend.app.services.decision_rooms.scenarios_risks import ScenarioRiskManager
from backend.app.services.decision_rooms.ai_workers_review import SpecialistReviewManager
from backend.app.services.decision_rooms.discussions_approvals import DiscussionApprovalManager
from backend.app.services.decision_rooms.outcomes_journal import OutcomeJournalManager


class DecisionRoomPlatformService:
    """Master facade for Decision Rooms, Augmented Intelligence, and Human-AI Collaboration."""

    def __init__(self):
        self.rooms = DecisionRoomManager()
        self.context_evidence = ContextEvidenceManager()
        self.assumptions_options = AssumptionOptionManager()
        self.scenarios_risks = ScenarioRiskManager()
        self.specialists = SpecialistReviewManager()
        self.discussions_approvals = DiscussionApprovalManager()
        self.outcomes_journal = OutcomeJournalManager()
        self._seed_demo_workspace()

    def _seed_demo_workspace(self):
        """Seed a representative high-impact decision room for demonstration."""
        room = self.rooms.create_room(
            title="Launch Dedicated Enterprise AI Agent Customization Service",
            question="Should North's launch a dedicated Enterprise AI Agent Customization service tier with bounded SLAs?",
            owner_id="executive_lead",
            decision_type=DecisionType.STRATEGIC,
            importance=DecisionImportance.HIGH,
            objective="Evaluate commercial demand, capacity impact, security liability, and profit margin expansion.",
        )
        r_id = room["id"]

        # Context
        self.context_evidence.set_context(
            room_id=r_id,
            background="High inbound demand from B2B clients requesting tailored AI worker squads and custom workflows.",
            current_state="Currently delivering standard fixed-scope digital presence & automation services.",
            constraints=["Zero direct outbound send without human approval", "Max 3 new senior engineer hires in Q3"],
            entities_involved=["Enterprise Clients", "Engineering Team", "Security & Governance Team"],
        )

        # Evidence
        self.context_evidence.add_evidence(
            room_id=r_id,
            evidence_type=EvidenceType.DATABASE,
            source="CRM Inbound Opportunities Q2",
            claim="Inbound enterprise requests for custom AI agents grew 145% quarter-over-quarter.",
            statement_category=StatementCategory.FACT,
            confidence=1.0,
        )
        self.context_evidence.add_evidence(
            room_id=r_id,
            evidence_type=EvidenceType.FINANCIAL_DATA,
            source="Financial Operating Model",
            claim="Estimated average contract value is $35,000 with 68% gross margin.",
            statement_category=StatementCategory.INFERENCE,
            confidence=0.85,
        )

        # Assumptions & Unknowns
        self.assumptions_options.add_assumption(
            room_id=r_id,
            statement="Client internal IT teams will accept standard API integrations within 30 days.",
            confidence=0.75,
            impact_if_false="HIGH",
        )
        self.assumptions_options.add_unknown(
            room_id=r_id,
            question="What is the exact client legal turnaround time on AI liability clauses?",
            impact="HIGH",
            resolution_path="Consult legal counsel on standard enterprise terms.",
        )

        # Options
        opt_a = self.assumptions_options.create_option(
            room_id=r_id,
            name="Full Enterprise Service Launch (Direct Sales)",
            description="Launch dedicated tier with bespoke multi-agent architecture and dedicated client success support.",
            benefits=["Highest ACV ($45k+)", "Strong competitive moat", "Recurring annual retainer model"],
            costs=65000.0,
            risks=["Longer sales cycle", "Higher technical support overhead"],
            uncertainty_level="MEDIUM",
            reversibility="PARTIALLY_REVERSIBLE",
        )
        opt_b = self.assumptions_options.create_option(
            room_id=r_id,
            name="Self-Service Template Catalog + Assisted Onboarding",
            description="Offer pre-configured AI worker templates with standardized implementation packages.",
            benefits=["Faster sales velocity", "Lower delivery burden", "Scalable self-serve adoption"],
            costs=25000.0,
            risks=["Lower deal size", "Requires robust documentation & UI tooling"],
            uncertainty_level="LOW",
            reversibility="REVERSIBLE",
        )

        # Criteria & Scores
        c1 = self.assumptions_options.add_criterion(room_id=r_id, name="Margin & Revenue Potential", weight=1.5)
        c2 = self.assumptions_options.add_criterion(room_id=r_id, name="Delivery Complexity", weight=1.2, criterion_type="COST")
        c3 = self.assumptions_options.add_criterion(room_id=r_id, name="Speed to Market", weight=1.0)

        self.assumptions_options.score_option(r_id, opt_a["id"], c1["id"], 92.0, "High contract values")
        self.assumptions_options.score_option(r_id, opt_a["id"], c2["id"], 45.0, "Substantial customization required")
        self.assumptions_options.score_option(r_id, opt_a["id"], c3["id"], 60.0, "Requires 6-8 weeks setup")

        self.assumptions_options.score_option(r_id, opt_b["id"], c1["id"], 70.0, "Moderate contract values")
        self.assumptions_options.score_option(r_id, opt_b["id"], c2["id"], 85.0, "Packaged delivery minimizes custom code")
        self.assumptions_options.score_option(r_id, opt_b["id"], c3["id"], 90.0, "Can launch within 2 weeks")

        # Trade-off
        self.assumptions_options.generate_tradeoff(r_id, opt_a["id"], opt_b["id"])

        # Specialists
        self.specialists.submit_specialist_analysis(
            room_id=r_id,
            specialist_role=SpecialistRole.FINANCE,
            summary="Option A provides $320k projected ARR within 6 months at 68% margin, while Option B delivers $160k at 82% margin.",
            recommendations=["Option A provides higher total profit dollars despite higher initial capital expenditure."],
            confidence=0.88,
        )
        self.specialists.submit_specialist_analysis(
            room_id=r_id,
            specialist_role=SpecialistRole.SECURITY,
            summary="Enterprise clients require ISO/SOC2 proof and default-deny data perimeter controls.",
            recommendations=["Mandate tenant isolation and zero client data retention for LLM training."],
            confidence=0.95,
        )

        # Adversarial Review
        self.specialists.submit_adversarial_review(
            room_id=r_id,
            critique_summary="Option A risks bottlenecking our principal architects on non-standard client integrations.",
            weak_assumptions=["Assumes clients have clean API access ready on Day 1."],
            hidden_costs=["Ongoing maintenance for bespoke external system connectors."],
        )

        # Approvals
        self.discussions_approvals.configure_approval_steps(
            room_id=r_id,
            steps=[
                {"step_name": "FINANCIAL_REVIEW", "required_role": "CFO"},
                {"step_name": "SECURITY_REVIEW", "required_role": "SECURITY_LEAD"},
                {"step_name": "EXECUTIVE_APPROVAL", "required_role": "CEO"},
            ]
        )

    def get_room_overview(self, room_id: str) -> Dict[str, Any]:
        """Aggregate all decision room workspace data into a single unified payload."""
        room = self.rooms.get_room(room_id)
        if not room:
            raise ValueError(f"Decision room {room_id} not found")

        context = self.context_evidence.get_context(room_id)
        evidence = self.context_evidence.list_evidence(room_id)
        assumptions = self.assumptions_options.list_assumptions(room_id)
        unknowns = self.assumptions_options.list_unknowns(room_id)
        options = self.assumptions_options.list_options(room_id)
        criteria = self.assumptions_options.list_criteria(room_id)
        tradeoffs = self.assumptions_options.list_tradeoffs(room_id)
        scenarios = self.scenarios_risks.list_scenarios(room_id)
        risks = self.scenarios_risks.list_risks(room_id)
        analyses = self.specialists.list_analyses(room_id)
        reviews = self.specialists.list_reviews(room_id)
        disagreements = self.specialists.list_disagreements(room_id)
        consensus = self.specialists.compute_consensus_metrics(room_id)
        discussions = self.discussions_approvals.list_comments(room_id)
        approvals = self.discussions_approvals.list_approvals(room_id)
        actions = self.discussions_approvals.list_actions(room_id)
        outcomes = self.outcomes_journal.list_outcomes(room_id)
        post_reviews = self.outcomes_journal.list_post_reviews(room_id)

        return {
            "room": room,
            "context": context,
            "evidence": evidence,
            "assumptions": assumptions,
            "unknowns": unknowns,
            "options": options,
            "criteria": criteria,
            "tradeoffs": tradeoffs,
            "scenarios": scenarios,
            "risks": risks,
            "analyses": analyses,
            "reviews": reviews,
            "disagreements": disagreements,
            "consensus": consensus,
            "discussions": discussions,
            "approvals": approvals,
            "actions": actions,
            "outcomes": outcomes,
            "post_reviews": post_reviews,
        }

    def ask_copilot(self, room_id: str, query: str) -> Dict[str, Any]:
        """Natural language Collaboration Copilot answering decision room queries with grounded context."""
        room_data = self.get_room_overview(room_id)
        q = query.lower()

        if "option" in q or "compare" in q:
            options = room_data["options"]
            tradeoffs = room_data["tradeoffs"]
            return {
                "query": query,
                "answer": f"There are {len(options)} candidate options evaluated in this room. Top option by composite score is '{options[0]['name'] if options else 'N/A'}' with score {options[0]['composite_score'] if options else 0.0}.",
                "key_findings": [f"Option: {o['name']} (Score: {o['composite_score']})" for o in options],
                "tradeoff_highlight": tradeoffs[0]["tradeoff_summary"] if tradeoffs else "No direct trade-off recorded yet.",
                "statement_category": StatementCategory.INFERENCE.value,
                "requires_human_decision": True,
            }
        elif "risk" in q or "wrong" in q or "critique" in q:
            reviews = room_data["reviews"]
            risks = room_data["risks"]
            return {
                "query": query,
                "answer": f"Adversarial review identified {len(reviews)} primary challenges and {len(risks)} risk items.",
                "weak_assumptions": reviews[0]["weak_assumptions"] if reviews else [],
                "hidden_costs": reviews[0]["hidden_costs"] if reviews else [],
                "statement_category": StatementCategory.INFERENCE.value,
                "requires_human_decision": True,
            }
        else:
            return {
                "query": query,
                "answer": f"Decision Room '{room_data['room']['title']}' is currently in state '{room_data['room']['status']}' with {len(room_data['evidence'])} evidence items and {room_data['consensus']['consensus_pct']}% specialist alignment.",
                "statement_category": StatementCategory.FACT.value,
                "requires_human_decision": True,
            }


# Singleton platform instance
global_decision_room_service = DecisionRoomPlatformService()
