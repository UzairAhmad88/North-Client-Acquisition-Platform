"""
Unit Tests for Phase 59: Unified Marketing Intelligence, Demand Generation, Content Strategy & Marketing Automation Platform
"""

import pytest
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
)
from backend.app.services.marketing.service import MarketingPlatformService
from backend.app.services.marketing.base import (
    CampaignStatus,
    ContentStatus,
    ClaimVerificationStatus,
    LeadQualificationStage,
    AttributionModelType,
)
from agents.marketing import (
    MarketingStrategyAgent,
    ContentStrategyAgent,
    ContentClaimsAgent,
    CampaignAgent,
    LeadScoringAgent,
    AttributionAgent,
    MarketingRoiAgent,
    MarketingCopilotAgent,
)


class TestAudiencesAndPositioning:
    def test_create_audience_and_segment(self):
        service = MarketingPlatformService()
        aud = service.audiences.create_audience(
            name="Healthcare Tech Enterprise",
            description="Enterprise health systems evaluating workflow modernization.",
            target_icp="500+ beds health networks",
            industry="Healthcare",
            company_size_tier="ENTERPRISE",
            buying_context="Operational cost reduction and compliance requirements.",
            primary_pain_points=["Manual intake workflows", "EHR integration bottlenecks"],
            channel_preferences=["LINKEDIN_ABM", "WEBINARS"],
            total_market_size=8000,
            reachable_market_size=1800,
        )
        assert aud.name == "Healthcare Tech Enterprise"
        assert aud.reachable_market_size == 1800

        seg = service.audiences.create_segment(
            audience_id=aud.id,
            name="CIOs & Health Informatics Leads",
            account_count=320,
            avg_revenue_potential_usd=150000.0,
        )
        assert seg.account_count == 320
        assert seg.avg_revenue_potential_usd == 150000.0

    def test_personas_positioning_and_message_house(self):
        service = MarketingPlatformService()
        aud = service.audiences.list_audiences()[0]

        persona = service.audiences.create_persona(
            audience_id=aud.id,
            title="Chief Information Officer",
            role_type="EXECUTIVE",
            core_responsibilities=["Digital Transformation", "Security Architecture"],
        )
        assert persona.title == "Chief Information Officer"

        pos = service.audiences.create_positioning(
            audience_id=aud.id,
            target_customer="Enterprise Healthcare Networks",
            problem_statement="Fragmented intake pipelines create operational delay.",
            alternative_solution="Custom internal scripting or unverified offshore dev.",
            our_solution="Uzaii Develop: Governed Autonomous Client Acquisition & Intake.",
            key_differentiators=["HIPAA compliant guardrails", "Closed-loop attribution"],
            value_statement="Cut intake cycle time by 60% with zero data exposure.",
            proof_points=["100% auditable logs", "Zero data breaches across 200+ deployments"],
        )
        assert pos.is_approved is False

        approved_pos = service.audiences.approve_positioning(pos.id, approver="VP Marketing")
        assert approved_pos.is_approved is True
        assert approved_pos.approved_by == "VP Marketing"

        mh = service.audiences.create_message_house(
            positioning_id=pos.id,
            core_message="Governed Healthcare Client Intake & Acquisition.",
            pillar_1={"title": "Security-First", "desc": "Air-gapped and auditable"},
            pillar_2={"title": "Fast Time to Value", "desc": "Deploy in 14 days"},
            pillar_3={"title": "Predictable ROI", "desc": "Closed-loop CAC tracking"},
            call_to_action="Request Compliance & Security Brief",
        )
        assert mh.core_message == "Governed Healthcare Client Intake & Acquisition."


class TestContentAndClaims:
    def test_content_asset_versioning_and_briefs(self):
        service = MarketingPlatformService()
        asset = service.content.create_content_asset(
            title="Enterprise Client Acquisition Blueprint",
            content_type="WHITEPAPER",
            journey_stage="CONSIDERATION",
            body_markdown="# Overview\n\nModern client acquisition relies on evidence...",
        )
        assert asset.current_version == 1
        assert asset.status == ContentStatus.DRAFT.value

        updated = service.content.update_content_asset(
            asset_id=asset.id,
            title="Enterprise Client Acquisition Blueprint (2026 Edition)",
            body_markdown="# Overview\n\nUpdated empirical benchmark research...",
            change_summary="Updated 2026 statistics",
        )
        assert updated.current_version == 2

        brief = service.content.create_content_brief(
            target_topic="Multi-Agent Commercial Orchestration",
            journey_stage="CONSIDERATION",
        )
        assert brief.target_topic == "Multi-Agent Commercial Orchestration"

    def test_claims_verification_approvals_and_gaps(self):
        service = MarketingPlatformService()
        asset = service.content.create_content_asset(title="ROI Whitepaper")

        claim = service.content.record_claim(
            asset_id=asset.id,
            claim_text="Firms achieve a 4.1x return on commercial automation investments.",
            source_reference="B2B Economic Growth Survey 2026, Table 1",
            confidence_pct=96.0,
            verification_status=ClaimVerificationStatus.VERIFIED.value,
        )
        assert claim.confidence_pct == 96.0
        assert claim.verification_status == ClaimVerificationStatus.VERIFIED.value

        approval = service.content.submit_for_approval(asset.id, approver="Head of Editorial", status="APPROVED")
        assert approval.status == "APPROVED"
        assert asset.status == ContentStatus.APPROVED.value

        gaps = service.content.list_content_gaps()
        assert len(gaps) >= 2

        # Brand consistency check
        check_clean = service.content.check_brand_consistency("Our evidence-backed, closed-loop platform optimizes CAC.")
        assert check_clean["is_compliant"] is True

        check_violation = service.content.check_brand_consistency("We offer a guaranteed 100% win rate magic bullet.")
        assert check_violation["is_compliant"] is False
        assert len(check_violation["violations"]) >= 1


class TestCampaignsChannelsAndEmail:
    def test_campaign_lifecycle_and_governance_gate(self):
        service = MarketingPlatformService()
        camp = service.campaigns.create_campaign(
            name="Q4 Enterprise Outreach Sprint",
            allocated_budget_usd=30000.0,
        )
        assert camp.status == CampaignStatus.DRAFT.value
        assert camp.is_governance_approved is False

        # Attempting activation without approval should raise ValueError
        with pytest.raises(ValueError):
            service.campaigns.advance_campaign_status(camp.id, target_status=CampaignStatus.ACTIVE.value)

        # Advance with explicit human approval
        approved_camp = service.campaigns.advance_campaign_status(
            camp.id,
            target_status=CampaignStatus.ACTIVE.value,
            approved_by="Executive Growth Board",
        )
        assert approved_camp.status == CampaignStatus.ACTIVE.value
        assert approved_camp.is_governance_approved is True

    def test_channels_suppression_and_sequences(self):
        service = MarketingPlatformService()
        ch = service.campaigns.create_channel(
            name="Webinar Co-Marketing",
            channel_type="EVENTS",
            total_spend_usd=15000.0,
            total_revenue_usd=95000.0,
            avg_cac_usd=850.0,
            avg_roas=6.33,
        )
        assert ch.total_revenue_usd == 95000.0

        # Suppressions
        service.campaigns.record_suppression(email="optout@client.com", reason="UNSUBSCRIBE")
        assert service.campaigns.is_suppressed("optout@client.com") is True
        assert service.campaigns.is_suppressed("valid@client.com") is False

        # Sequences
        seq = service.campaigns.create_email_sequence(name="3-Part Executive Nurture")
        assert len(seq.steps) == 3


class TestLeadsScoringAndFunnel:
    def test_lead_capture_3_component_scoring_and_qualification(self):
        service = MarketingPlatformService()
        lead = service.leads.capture_lead(
            email="marcus.vance@vancepartners.com",
            first_name="Marcus",
            last_name="Vance",
            company_name="Vance Partners Global",
            source_channel="LINKEDIN_ABM",
        )
        assert lead.composite_lead_score == 50.0
        assert lead.qualification_stage == LeadQualificationStage.NEW.value

        score = service.leads.calculate_lead_score(
            lead_id=lead.id,
            company_size_tier="ENTERPRISE",
            industry_match=True,
            budget_signal=True,
            page_views=8,
            content_downloads=3,
            webinar_attended=True,
            pricing_page_visits=2,
            demo_requested=True,
        )
        assert score.composite_lead_score > 75.0
        assert lead.qualification_stage == LeadQualificationStage.MQL.value

    def test_funnel_metrics_and_nurture(self):
        service = MarketingPlatformService()
        funnel = service.leads.calculate_funnel_metrics(
            period="2026-Q3",
            impressions=200000,
            visitors=30000,
            leads=1500,
            mql=525,
            sql=210,
            opportunities=105,
            deals_won=42,
        )
        assert funnel.conversion_rate_lead_to_mql_pct == 35.0
        assert funnel.conversion_rate_mql_to_sql_pct == 40.0
        assert funnel.conversion_rate_sql_to_won_pct == 20.0

        nurture = service.leads.create_nurture_program(name="High-Intent Mid-Market Sequence", goal="Convert MQL to SQL")
        assert nurture.is_active is True


class TestAttributionRoiAndBudgets:
    def test_multi_touch_attribution_models(self):
        service = MarketingPlatformService()
        touches = [
            {"touch_num": 1, "channel": "ORGANIC_SEARCH", "campaign_name": "Thought Leadership SEO"},
            {"touch_num": 2, "channel": "EMAIL", "campaign_name": "Executive Briefing Series"},
            {"touch_num": 3, "channel": "WEBINAR", "campaign_name": "Live Architecture Demo"},
        ]

        # W-Shaped (30% first, 40% mid, 30% last)
        rec = service.attribution.calculate_attribution(
            opportunity_id="opp_1001",
            deal_value_usd=100000.0,
            touches=touches,
            attribution_model=AttributionModelType.MULTI_TOUCH_W_SHAPED.value,
        )
        assert rec.campaign_credits["Thought Leadership SEO"] == 30000.0
        assert rec.campaign_credits["Executive Briefing Series"] == 40000.0
        assert rec.campaign_credits["Live Architecture Demo"] == 30000.0

    def test_roi_and_budget_simulation(self):
        service = MarketingPlatformService()
        roi = service.attribution.calculate_marketing_roi(
            period="2026-Q3",
            total_spend_usd=100000.0,
            total_attributed_revenue_usd=600000.0,
            leads_count=1000,
            mql_count=350,
            acquisitions_count=25,
        )
        assert roi.cost_per_lead_usd == 100.0
        assert roi.cost_per_acquisition_usd == 4000.0
        assert roi.roas == 6.0
        assert roi.roi_pct == 500.0

        sim = service.attribution.simulate_budget_optimization(
            current_budget_usd=100000.0,
            budget_shift_pct=25.0,
            target_focus_channel="ORGANIC_SEARCH",
        )
        assert sim["expected_additional_pipeline_usd"] > 0
        assert sim["expected_additional_revenue_usd"] > 0
        assert sim["confidence_pct"] == 86.5


class TestSeoEventsAndForecasting:
    def test_seo_landing_pages_and_calendar(self):
        service = MarketingPlatformService()
        kw = service.seo_events.track_keyword(keyword="b2b demand generation automation", monthly_search_volume=1800, current_ranking=2)
        assert kw.keyword == "b2b demand generation automation"

        lp = service.seo_events.create_landing_page(
            slug="enterprise-demand-gen",
            title="Enterprise Demand Generation Platform",
            visitors_count=1000,
            submissions_count=120,
        )
        assert lp.conversion_rate_pct == 12.0

        cal = service.seo_events.schedule_calendar_event(title="Q4 Product Launch Webinar", channel="WEBINAR")
        assert cal.title == "Q4 Product Launch Webinar"

    def test_probabilistic_forecasting_and_fatigue(self):
        service = MarketingPlatformService()
        fc = service.forecast_risks.generate_demand_forecast(
            period="2026-Q4",
            scenario="BASE",
            baseline_leads=2000,
        )
        assert fc.p10_leads < fc.p50_leads < fc.p90_leads
        assert fc.p50_pipeline_usd > 0

        # Fatigue check
        fat_normal = service.forecast_risks.monitor_audience_fatigue(channel="EMAIL", weekly_frequency=1.5, unsubscribe_rate_pct=0.15)
        assert fat_normal.fatigue_level == "NORMAL"

        fat_crit = service.forecast_risks.monitor_audience_fatigue(channel="EMAIL", weekly_frequency=5.0, unsubscribe_rate_pct=1.5)
        assert fat_crit.fatigue_level == "CRITICAL"


class TestFacadeAndCopilot:
    def test_overview_metrics(self):
        service = MarketingPlatformService()
        metrics = service.get_overview_metrics()
        assert metrics["total_campaigns_active"] >= 1
        assert metrics["total_leads_captured"] >= 1
        assert metrics["attributed_revenue_usd"] > 0
        assert metrics["status"] == "OPERATIONAL"

    def test_copilot_queries(self):
        service = MarketingPlatformService()

        # Query 1: Campaigns
        res1 = service.answer_copilot_query("What campaigns are performing best?")
        assert "Q3 Enterprise Advisory Modernization Initiative" in res1["answer"]
        assert len(res1["evidence"]) > 0

        # Query 2: Content gaps
        res2 = service.answer_copilot_query("Which content gaps matter most?")
        assert "gap" in res2["answer"].lower() or "framework" in res2["answer"].lower() or "governance" in res2["answer"].lower()

        # Query 3: Channels / Economics
        res3 = service.answer_copilot_query("Which channels have the best economics and CAC?")
        assert "Organic Search" in res3["answer"]

        # Query 4: Forecast
        res4 = service.answer_copilot_query("What is our expected revenue and demand forecast?")
        assert "P50" in res4["answer"]


class TestMarketingAgents:
    @pytest.mark.asyncio
    async def test_marketing_strategy_agent(self):
        agent = MarketingStrategyAgent()
        ctx = AgentContext(workflow_id="wf_01", task_id="t_01", agent_run_id="run_01", metadata={"audience_name": "Mid-Market Advisory"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["audience_name"] == "Mid-Market Advisory"

    @pytest.mark.asyncio
    async def test_content_strategy_agent(self):
        agent = ContentStrategyAgent()
        ctx = AgentContext(workflow_id="wf_02", task_id="t_02", agent_run_id="run_02", metadata={"topic": "B2B CAC Optimization"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["target_topic"] == "B2B CAC Optimization"

    @pytest.mark.asyncio
    async def test_content_claims_agent(self):
        agent = ContentClaimsAgent()
        ctx = AgentContext(workflow_id="wf_03", task_id="t_03", agent_run_id="run_03", metadata={"claim_text": "Verified 3.5x pipeline surge."})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["verification_status"] == "VERIFIED"

    @pytest.mark.asyncio
    async def test_campaign_agent(self):
        agent = CampaignAgent()
        ctx = AgentContext(workflow_id="wf_04", task_id="t_04", agent_run_id="run_04", metadata={"campaign_name": "Q4 Demand Sprint"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["campaign_name"] == "Q4 Demand Sprint"

    @pytest.mark.asyncio
    async def test_lead_scoring_agent(self):
        agent = LeadScoringAgent()
        ctx = AgentContext(workflow_id="wf_05", task_id="t_05", agent_run_id="run_05", metadata={"email": "growth@enterprise.com"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["composite_score"] > 50.0

    @pytest.mark.asyncio
    async def test_attribution_agent(self):
        agent = AttributionAgent()
        ctx = AgentContext(workflow_id="wf_06", task_id="t_06", agent_run_id="run_06", metadata={"opportunity_id": "opp_test", "deal_value_usd": 80000.0})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["attribution_id"] is not None

    @pytest.mark.asyncio
    async def test_marketing_roi_agent(self):
        agent = MarketingRoiAgent()
        ctx = AgentContext(workflow_id="wf_07", task_id="t_07", agent_run_id="run_07", metadata={"period": "2026-Q3"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["roas"] > 0

    @pytest.mark.asyncio
    async def test_marketing_copilot_agent(self):
        agent = MarketingCopilotAgent()
        ctx = AgentContext(workflow_id="wf_08", task_id="t_08", agent_run_id="run_08", metadata={"query": "Which channels perform best?"})
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert len(res["answer"]) > 0


class TestPermissionsAndProhibitions:
    def test_prohibited_permissions(self):
        prohibited = [
            "AUTONOMOUS_LAUNCH_CAMPAIGN",
            "AUTONOMOUS_SEND_MARKETING_EMAIL",
            "AUTONOMOUS_PUBLISH_CONTENT",
            "AUTONOMOUS_MODIFY_PRICING_CLAIM",
            "AUTONOMOUS_CHANGE_MARKETING_BUDGET",
            "FABRICATE_TESTIMONIALS",
            "FABRICATE_MARKET_SIGNALS",
            "IGNORE_CONSENT_OPT_OUT",
        ]
        for p in prohibited:
            with pytest.raises(AgentPermissionDeniedError):
                validate_agent_permissions({p})
