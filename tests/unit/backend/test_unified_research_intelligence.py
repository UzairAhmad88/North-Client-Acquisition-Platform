"""
Unit test suite for Phase 54:
Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

import pytest
from backend.app.services.research_intelligence.service import ResearchIntelligencePlatformService
from backend.app.services.research_intelligence.base import (
    ResearchStatus,
    ResearchType,
    SourceTrustLevel,
    FactStatus,
    ClaimVerificationStatus,
    IntelligenceEventType,
    SignificanceLevel,
)
from agents.research_intelligence import (
    ResearchPlannerAgent,
    SourceDiscoveryAgent,
    FactCheckerAgent,
    SynthesisAgent,
    ResearchMonitorAgent,
)
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS


@pytest.fixture
def service():
    return ResearchIntelligencePlatformService()


def test_workspace_lifecycle_and_decomposition(service):
    # 1. Create Workspace
    ws = service.workspaces.create_workspace(
        title="Enterprise AI Support Systems",
        research_question="Should we build a multi-tenant autonomous customer support platform?",
        owner_id="lead_researcher",
        research_type=ResearchType.MARKET,
        objective="Analyze enterprise TAM, competitive pricing, and regulatory risk",
    )
    assert ws["id"].startswith("rws_")
    assert ws["status"] == ResearchStatus.PLANNED.value
    assert ws["version"] == 1

    # 2. Decompose Question
    subtasks = service.workspaces.decompose_question(
        workspace_id=ws["id"],
    )
    assert len(subtasks) >= 5
    assert any("competitor" in t["question"].lower() for t in subtasks)

    # 3. Create Research Tasks
    task = service.workspaces.create_task(
        workspace_id=ws["id"],
        question="What is the average ARR of enterprise AI support vendors?",
        task_type="COMPETITIVE_PRICING",
        priority=1,
    )
    assert task["id"].startswith("rtask_")
    assert task["status"] == "QUEUED"

    # 4. Transition Status
    updated = service.workspaces.transition_status(
        workspace_id=ws["id"],
        target_status=ResearchStatus.SYNTHESIZING,
    )
    assert updated["status"] == ResearchStatus.SYNTHESIZING.value
    assert updated["version"] == 2


def test_source_registry_and_ssrf_blocking(service):
    # Valid External Primary Source
    src = service.sources.register_source(
        workspace_id="rws_test_001",
        url_or_reference="https://sec.gov/edgar/data/sample_10k.htm",
        publisher="US SEC Edgar",
        source_type=SourceTrustLevel.GOVERNMENT,
        authority_score=0.98,
    )
    assert src["id"].startswith("src_")
    assert src["source_type"] == SourceTrustLevel.GOVERNMENT.value
    assert src["authority_score"] >= 0.95
    assert src["content_hash"] is not None

    # SSRF Attack Blocking (Localhost, Private IPs)
    with pytest.raises(ValueError, match=r"SSRF blocked"):
        service.sources.register_source(
            workspace_id="rws_test_001",
            url_or_reference="http://127.0.0.1:8000/internal_secrets",
        )

    with pytest.raises(ValueError, match=r"SSRF blocked"):
        service.sources.register_source(
            workspace_id="rws_test_001",
            url_or_reference="http://169.254.169.254/latest/meta-data/",
        )

    with pytest.raises(ValueError, match=r"Invalid source scheme"):
        service.sources.register_source(
            workspace_id="rws_test_001",
            url_or_reference="file:///etc/passwd",
        )


def test_fact_extraction_and_entity_resolution(service):
    ws_id = "rws_test_002"

    # Entity Resolution
    entity = service.extraction.resolve_entity(
        workspace_id=ws_id,
        name="Acme AI Inc",
        entity_type="COMPANY",
        aliases=["AcmeAI", "Acme Artificial Intelligence"],
    )
    assert entity["name"] == "Acme AI Inc"
    assert "AcmeAI" in entity["aliases"]

    # Fact Extraction
    fact = service.extraction.extract_fact(
        workspace_id=ws_id,
        claim="Acme AI Inc reached $12M ARR with 450 enterprise customers in Q4 2025.",
        source_id="src_acme_news",
        value_extracted="$12M ARR",
        confidence=0.94,
    )
    assert fact["id"].startswith("fact_")
    assert fact["confidence"] == 0.94
    assert fact["value_extracted"] == "$12M ARR"


def test_claim_verification_corroboration_and_conflicts(service):
    ws_id = "rws_verify"

    # Setup sources
    src1 = service.sources.register_source(
        workspace_id=ws_id,
        url_or_reference="https://industry-analytics.example.com/report1",
        source_type=SourceTrustLevel.PROFESSIONAL,
    )
    src2 = service.sources.register_source(
        workspace_id=ws_id,
        url_or_reference="https://tech-research.example.org/study2",
        source_type=SourceTrustLevel.ACADEMIC,
    )

    # Claim verification (Corroborated)
    claim = service.extraction.verify_claim(
        workspace_id=ws_id,
        claim_text="Enterprise agentic AI adoption is experiencing double-digit market growth.",
        supporting_sources=[src1["url_or_reference"], src2["url_or_reference"]],
    )
    assert claim["id"].startswith("clm_")
    assert claim["verification_status"] == ClaimVerificationStatus.SUPPORTED.value
    assert claim["independent_sources_count"] == 2
    assert len(claim["supporting_evidence"]) == 2

    # Surface Conflict
    conflict = service.extraction.surface_conflict(
        workspace_id=ws_id,
        topic="Average seat price for AI customer tier",
        source_a_id=src1["id"],
        claim_a="$49/seat/month",
        source_b_id=src2["id"],
        claim_b="$120/seat/month",
        possible_explanation="Report A evaluates SMB tier while Report B surveys Tier-1 Enterprise dedicated deployments.",
    )
    assert conflict["id"].startswith("conf_")
    assert conflict["resolution_status"] == "SURFACED"



def test_domain_intelligence_competitors_and_trends(service):
    # Competitor Profile
    comp = service.domains.upsert_competitor_profile(
        company_name="OmniSupport AI",
        market_position="LEADER",
        products_offered=["OmniAgent Chat", "OmniVoice VoiceBot"],
        pricing_signals={"entry_price": "$500/mo", "pricing_model": "per_resolved_ticket"},
        strengths=["Strong CRM integrations", "High brand awareness"],
        weaknesses=["High implementation cost", "Closed proprietary models"],
    )
    assert comp["id"] == "comp_omnisupport_ai"
    assert comp["company_name"] == "OmniSupport AI"

    # Market Demand Signal
    signal = service.domains.record_market_signal(
        market_segment="AI_CUSTOMER_SUPPORT",
        signal_type="DEMAND_GROWTH",
        description="Inbound enterprise RFP volume for autonomous customer support increased 240% YoY.",
        confidence=0.92,
        source_reference="Internal inbound pipeline + industry aggregator",
    )
    assert signal["id"].startswith("sig_")

    # Trend Observation
    trend = service.domains.record_trend(
        workspace_id="rws_trend_test",
        trend_name="Autonomous Voice AI in Tier-1 Support",
        trend_type="EMERGING",
        momentum_score=0.88,
        key_drivers=["10x drop in voice latency", "Major contact centers launching pilots"],
        impact_assessment="Accelerating adoption in enterprise customer support",
    )
    assert trend["id"].startswith("trd_")
    assert trend["momentum_score"] == 0.88


def test_continuous_monitoring_and_significance(service):
    # Create Monitoring Watch Rule
    rule = service.monitoring.create_monitoring_rule(
        workspace_id="rws_mon_test",
        target_entity="OmniSupport AI",
        watch_frequency="DAILY",
        topics_monitored=["PRICING", "PRODUCT_RELEASES"],
        alert_significance_threshold=SignificanceLevel.MEDIUM,
    )
    assert rule["id"].startswith("rule_")
    assert rule["active"] is True

    # Record Intelligence Event with Significance Rating
    event = service.monitoring.record_intelligence_event(
        target_entity="OmniSupport AI",
        event_type=IntelligenceEventType.CHANGED,
        summary="OmniSupport transitioned from seat model to outcome billing ($0.75/resolution).",
        significance=SignificanceLevel.HIGH,
        confidence=0.95,
        evidence_payload={"source": "Pricing page delta"},
    )
    assert event["id"].startswith("ievt_")
    assert event["significance"] == SignificanceLevel.HIGH.value


def test_synthesis_reporting_and_decision_room_handoff(service):
    # Setup Workspace with sources and claims
    ws = service.workspaces.create_workspace(
        title="Synthesis Test Workspace",
        research_question="What is the viable go-to-market strategy for autonomous support?",
        owner_id="strat_lead",
        research_type=ResearchType.STRATEGIC,
    )
    src = service.sources.register_source(
        workspace_id=ws["id"],
        url_or_reference="https://forrester.example.com/ai-support-report",
        source_type=SourceTrustLevel.PROFESSIONAL,
    )
    claim = service.extraction.verify_claim(
        workspace_id=ws["id"],
        claim_text="Outcome billing drives 3x faster client adoption in enterprise POCs.",
        supporting_sources=[src["url_or_reference"]],
    )

    # Synthesize
    synthesis = service.synthesis.generate_synthesis(
        workspace_id=ws["id"],
        executive_summary="Enterprise buyers prefer outcome-aligned pricing ($0.50-$1.00/resolution).",
        key_findings=[
            "Sub-500ms latency is mandatory for voice-enabled agents.",
            "Multi-tenant data isolation required for compliance.",
        ],
        strategic_implications=["Develop consumption meter", "Integrate WebRTC voice stack"],
        recommended_actions=["Launch Beta with 5 design partners on consumption billing."],
    )
    assert synthesis["id"].startswith("syn_")

    # Generate Formal Research Report
    report = service.synthesis.generate_report(
        workspace_id=ws["id"],
        title="Autonomous Support GTM & Architecture Intelligence Report",
        report_markdown="# Executive Briefing\nOutcome pricing delivers superior unit economics.",
        citations=[src["url_or_reference"]],
    )
    assert report["id"].startswith("rep_")
    assert len(report["citations"]) == 1

    # Record Research Gap
    gap = service.synthesis.record_research_gap(
        workspace_id=ws["id"],
        gap_description="What is the average agent failure rate during edge-case escalations?",
        importance="HIGH",
        recommended_investigation="Synthesize telemetry from Q1 beta pilots",
    )
    assert gap["id"].startswith("gap_")


@pytest.mark.asyncio
async def test_agent_permissions_and_execution(service):
    # Create workspace to attach agents
    ws = service.workspaces.create_workspace(
        title="Agent Execution Test Workspace",
        research_question="How is AI adoption evolving in fintech?",
        owner_id="research_architect",
    )

    # Context with metadata
    ctx = AgentContext(
        workflow_id="wf_54",
        task_id="task_54",
        agent_run_id="run_54",
        metadata={
            "workspace_id": ws["id"],
            "claim_text": "AI adoption in accounting grew 45% in 2025.",
            "supporting_sources": ["https://fintech-report.example.com/2025", "https://sec.gov/filing/sample"],
            "summary": "Fintech AI adoption exhibits high velocity.",
            "findings": ["Reconciliation speed +60%", "Adoption rate +45%"],
            "recommended_actions": ["Accelerate automated reconciliation pilot."],
        },
    )

    # 1. Research Planner Agent
    planner = ResearchPlannerAgent(service)
    assert AgentPermission.CREATE_RESEARCH_PLAN in planner.permissions
    plan_result = await planner.execute(ctx)
    assert plan_result["status"] == "SUCCESS"
    assert plan_result["tasks_created"] >= 4

    # 2. Fact Checker Agent
    fact_checker = FactCheckerAgent(service)
    assert AgentPermission.VERIFY_RESEARCH_CLAIMS in fact_checker.permissions
    check_result = await fact_checker.execute(ctx)
    assert check_result["status"] == "SUCCESS"
    assert check_result["claim_verification"]["verification_status"] == ClaimVerificationStatus.SUPPORTED.value

    # 3. Synthesis Agent
    synthesis_agent = SynthesisAgent(service)
    assert AgentPermission.SYNTHESIZE_RESEARCH_REPORT in synthesis_agent.permissions
    synth_result = await synthesis_agent.execute(ctx)
    assert synth_result["status"] == "SUCCESS"
    assert len(synth_result["synthesis"]["key_findings"]) >= 2

    # Verify Prohibitions
    for perm in PROHIBITED_PERMISSIONS:
        assert perm not in planner.permissions
        assert perm not in fact_checker.permissions
        assert perm not in synthesis_agent.permissions


def test_platform_overview_and_copilot_query(service):
    # Query Workspace Overview for Seeded Demo Workspace
    workspaces = service.workspaces.list_workspaces()
    assert len(workspaces) >= 1
    demo_ws_id = workspaces[0]["id"]

    overview = service.get_workspace_overview(demo_ws_id)
    assert "workspace" in overview
    assert "sources" in overview
    assert "facts" in overview
    assert "claims" in overview
    assert "conflicts" in overview
    assert "competitors" in overview
    assert "synthesis" in overview
    assert "reports" in overview

    # Query Copilot
    copilot_res = service.ask_copilot(
        workspace_id=demo_ws_id,
        query="What are the main competitors and pricing?",
    )
    assert "answer" in copilot_res
    assert copilot_res["confidence"] >= 0.8
    assert len(copilot_res["citations"]) >= 1
