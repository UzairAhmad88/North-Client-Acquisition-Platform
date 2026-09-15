"""
Phase 59: Lead Generation, 3-Component Lead Scoring, Qualification Stages, Nurture Programs, Funnel Analytics
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, LeadQualificationStage, generate_id


class LeadsNurtureFunnelService:
    """Manages marketing leads, 3-component scoring (Fit, Engagement, Intent), qualification stages, and funnel metrics."""

    def __init__(self):
        self._leads: Dict[str, AttrDict] = {}
        self._scores: Dict[str, AttrDict] = {}
        self._nurture_programs: Dict[str, AttrDict] = {}
        self._funnel_metrics: Dict[str, AttrDict] = {}

    def capture_lead(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company_name: Optional[str] = None,
        source_channel: str = "ORGANIC_SEARCH",
        first_touch_campaign: Optional[str] = None,
        consent_obtained: bool = True,
        is_suppressed: bool = False,
    ) -> AttrDict:
        lead_id = generate_id("led")
        lead = AttrDict({
            "id": lead_id,
            "email": email.strip().lower(),
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "source_channel": source_channel,
            "first_touch_campaign": first_touch_campaign,
            "last_touch_campaign": first_touch_campaign,
            "fit_score": 50.0,
            "engagement_score": 50.0,
            "intent_score": 50.0,
            "composite_lead_score": 50.0,
            "qualification_stage": LeadQualificationStage.NEW.value,
            "consent_obtained": consent_obtained,
            "is_suppressed": is_suppressed,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        })
        self._leads[lead_id] = lead
        return lead

    def calculate_lead_score(
        self,
        lead_id: str,
        company_size_tier: str = "MID_MARKET",
        industry_match: bool = True,
        budget_signal: bool = True,
        page_views: int = 5,
        content_downloads: int = 2,
        webinar_attended: bool = True,
        pricing_page_visits: int = 2,
        demo_requested: bool = False,
    ) -> AttrDict:
        lead = self._leads.get(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        # 1. Fit Score (Weight: 40%)
        fit = 30.0
        if industry_match:
            fit += 35.0
        if company_size_tier in ["MID_MARKET", "ENTERPRISE"]:
            fit += 20.0
        if budget_signal:
            fit += 15.0
        fit_score = min(100.0, max(0.0, fit))

        # 2. Engagement Score (Weight: 35%)
        eng = 20.0 + (page_views * 5.0) + (content_downloads * 15.0)
        if webinar_attended:
            eng += 25.0
        engagement_score = min(100.0, max(0.0, eng))

        # 3. Intent Score (Weight: 25%)
        intent = 10.0 + (pricing_page_visits * 25.0)
        if demo_requested:
            intent += 40.0
        intent_score = min(100.0, max(0.0, intent))

        # Composite Lead Score
        composite = (fit_score * 0.40) + (engagement_score * 0.35) + (intent_score * 0.25)
        composite_score = round(composite, 2)

        lead.fit_score = fit_score
        lead.engagement_score = engagement_score
        lead.intent_score = intent_score
        lead.composite_lead_score = composite_score
        lead.updated_at = datetime.utcnow().isoformat()

        # Update qualification stage automatically if threshold met
        if composite_score >= 80.0 and lead.qualification_stage == LeadQualificationStage.NEW.value:
            lead.qualification_stage = LeadQualificationStage.MQL.value
        elif composite_score >= 60.0 and lead.qualification_stage == LeadQualificationStage.NEW.value:
            lead.qualification_stage = LeadQualificationStage.ENGAGED.value

        score_record = AttrDict({
            "id": generate_id("lsc"),
            "lead_id": lead_id,
            "fit_score": fit_score,
            "engagement_score": engagement_score,
            "intent_score": intent_score,
            "composite_lead_score": composite_score,
            "fit_breakdown": {"industry_match": industry_match, "size_tier": company_size_tier, "budget_signal": budget_signal},
            "engagement_breakdown": {"page_views": page_views, "downloads": content_downloads, "webinar": webinar_attended},
            "intent_breakdown": {"pricing_views": pricing_page_visits, "demo_requested": demo_requested},
            "calculated_at": datetime.utcnow().isoformat(),
        })
        self._scores[lead_id] = score_record
        return score_record

    def advance_qualification_stage(
        self,
        lead_id: str,
        target_stage: str,
    ) -> AttrDict:
        lead = self._leads.get(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        lead.qualification_stage = target_stage
        lead.updated_at = datetime.utcnow().isoformat()
        return lead

    def get_lead(self, lead_id: str) -> Optional[AttrDict]:
        return self._leads.get(lead_id)

    def list_leads(self, qualification_stage: Optional[str] = None) -> List[AttrDict]:
        if qualification_stage:
            return [l for l in self._leads.values() if l.qualification_stage == qualification_stage]
        return list(self._leads.values())

    def create_nurture_program(
        self,
        name: str,
        goal: str,
        entry_conditions: Optional[Dict[str, Any]] = None,
        exit_conditions: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        nurture_id = generate_id("nur")
        nurture = AttrDict({
            "id": nurture_id,
            "name": name,
            "goal": goal,
            "entry_conditions": entry_conditions or {"stage": "ENGAGED", "min_score": 50},
            "exit_conditions": exit_conditions or {"stage": "MQL", "demo_requested": True},
            "active_leads_count": 0,
            "converted_leads_count": 0,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._nurture_programs[nurture_id] = nurture
        return nurture

    def list_nurture_programs(self) -> List[AttrDict]:
        return list(self._nurture_programs.values())

    def calculate_funnel_metrics(
        self,
        period: str = "2026-Q3",
        impressions: int = 150000,
        visitors: int = 24000,
        leads: int = 1200,
        mql: int = 420,
        sql: int = 180,
        opportunities: int = 95,
        deals_won: int = 38,
    ) -> AttrDict:
        lead_to_mql = round((mql / max(1, leads)) * 100.0, 2)
        mql_to_sql = round((sql / max(1, mql)) * 100.0, 2)
        sql_to_won = round((deals_won / max(1, sql)) * 100.0, 2)

        metric_id = generate_id("fnl")
        metrics = AttrDict({
            "id": metric_id,
            "period": period,
            "impressions": impressions,
            "visitors": visitors,
            "leads": leads,
            "mql": mql,
            "sql": sql,
            "opportunities": opportunities,
            "deals_won": deals_won,
            "conversion_rate_lead_to_mql_pct": lead_to_mql,
            "conversion_rate_mql_to_sql_pct": mql_to_sql,
            "conversion_rate_sql_to_won_pct": sql_to_won,
            "avg_funnel_velocity_days": 24.5,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._funnel_metrics[period] = metrics
        return metrics

    def get_funnel_metrics(self, period: str = "2026-Q3") -> Optional[AttrDict]:
        return self._funnel_metrics.get(period) or self.calculate_funnel_metrics(period=period)
